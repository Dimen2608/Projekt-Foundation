# ADR-0015: `project-orchestrate` übernimmt die Lehren aus dem Betrieb auf Claude Desktop

## Status

Accepted — 2026-09-26

## Context

ADR-0014 entstand in einer Cloud-Session. Zwei tragende Stellen blieben dort ungeprüft: der
Rückkanal und das Selbst-Leeren auf Claude Desktop. Zur selben Zeit lief auf dem Rechner des
Auftraggebers seit dem 2026-08-28 ein Lauf nach demselben Muster: eine Kopf-Session (plant,
schreibt nicht im Produktcode) und zwei Arbeits-Sessions (Spezifikation, Bau), verbunden über
`SendMessage` und das Session-Werkzeug von Claude Desktop. Ein Gegenlesen von ADR-0014 gegen
diesen Betrieb fand fünf Stellen, an denen der Skill hinter dem Betrieb zurückbleibt; eine davon
bricht den Ablauf.

1. **Der Worker vergisst nach dem Leeren seine Rolle.** `WORKER-START.md` lässt ihn nach der
   Übergabe leeren. Danach ist der Startprompt weg — Name des Orchestrators, Protokoll,
   Rundenregel. Der nächste Auftrag trifft eine Session, die nicht weiß, dass sie Worker ist.
   Im Betrieb trägt das eine lokale, nicht committete Übergabe-Datei und ein Weckauftrag, der
   für sich allein verständlich ist.
2. **Das Session-Werkzeug von Claude Desktop fehlt.** Der Skill kennt `SendMessage`,
   `ListAgents` und `notify_when_idle`. Im Betrieb tragend sind `list_sessions`, `send_message`
   an die Session-ID (weckt auch eine geleerte Session — `SendMessage` an den Namen tut das
   nicht sicher), `list_events` und `clear_session` mit `"self"`.
3. **Der Rückweg ist nur die Nachricht.** Im Betrieb war die Kopf-Session in einer Woche, in der
   der Mensch anwesend war, blind: 154 direkte Rückfragen in den Arbeits-Sessions gegen 6
   Nachrichten an den Kopf. Die Ursache ist grundsätzlich — eine Nachricht trägt nie den zweiten
   Kanal, das direkte Gespräch des Menschen mit dem Worker. Das Transkript trägt beide.
4. **Freigaben laufen über den Orchestrator.** Der Skill lässt jede Frage des Workers über den
   Orchestrator zum Menschen wandern. Eine Nachricht aus einer anderen Session kann aber keine
   Zustimmung sein — das erzwingt das Werkzeug —, und jede Relaisstation macht aus „braucht die
   Freigabe des Menschen" ein „hat der andere sicher geklärt".
5. **Gesperrte Befehle sind nicht geregelt.** Der Berechtigungs-Klassifikator hielt im Betrieb
   Befehle an Produktion mehrfach an. Bewährt hat sich: nicht umgehen, sondern dem Menschen den
   exakten Befehl nennen.

Dazu eine kleinere Lücke: Parallelität hat keine Bremse, wenn das Kontingent knapp wird. Im
Betrieb gilt dann „genau ein offener Auftrag über alle Arbeits-Sessions".

## Decision

1. **Gedächtnis des Workers als Datei.** Der Worker legt beim Start `.claude/worker.md` an und
   schreibt sie nach jeder Übergabe fort; sie wird nie committet (`.git/info/exclude`), damit
   das Arbeitsrepo unberührt bleibt; der Pfad kommt aus `git rev-parse --git-path
   info/exclude`, damit es auch im Worktree gilt. Sie hält den Startprompt wörtlich und für den
   laufenden Block Auftrag und Rundenzahl, damit auch eine `NACHARBEIT` einen geleerten Worker
   trägt. Jede Nachricht des Orchestrators an einen Worker (`AUFTRAG`, `ANTWORT`,
   `NACHARBEIT`) trägt als zweite Zeile den Worker-Kopf, der auf die Datei zeigt und selbst sagt, was bei fehlender Datei zu
   tun ist: `WORKER UNBEKANNT` an den Orchestrator, der den Startprompt erneut schickt —
   mitten im Block mit `Runden bisher: <n>`, damit die Grenze von fünf Runden nicht neu
   beginnt.
   **Selbst leeren nur, wenn der Orchestrator wieder wecken kann** — also auf demselben Rechner;
   `self_clear` je Repo in `ORCHESTRATE.md` und im Startprompt, abgeleitet in `SETUP`. An einen
   solchen Worker geht jede Nachricht über seine Session-ID.
2. **Session-Werkzeug von Claude Desktop in `mechanismen.md`**, je Befund mit Quelle (geprüft
   oder Betrieb). Wecken nach dem Leeren per Session-ID, aufgelöst am Arbeitsverzeichnis.
   Selbst-Leeren auf Desktop ist damit geprüft; die Prüfliste trägt die Teilbefunde.
3. **Erst lesen, dann schicken.** Vor jedem Auftrag und jeder Abnahme liest der Orchestrator den
   Ist-Stand des Workers selbst — auf demselben Rechner das Transkript, wo die Umgebung es kann.
   Über Rechnergrenzen bleibt nur die Nachricht; das steht in `ORCHESTRATE.md` unter
   „Erreichbarkeit".
4. **Eine Nachricht ist nie eine Freigabe.** `BLOCK <ID> FRAGE` ist eine Sachfrage. Freigaben
   holt der Worker beim Menschen in seiner eigenen Session und meldet dem Orchestrator nur
   `BLOCK <ID> WARTET freigabe`; nach der Entscheidung `BLOCK <ID> WEITER`. Der Blockarbeiter
   meldet `blocked` deshalb mit einer **Art** (`frage`, `freigabe`, `befehl`), nach der der
   Worker den Weg wählt. Der Orchestrator reicht keine Freigabe weiter und erteilt keine; das
   ist eine neue Stop Condition. Ergänzt ADR-0014, Entscheidung 10.
5. **Keine Sperre umgehen.** Bei einem gesperrten Befehl nennt der Worker bzw. der Blockarbeiter
   den exakten Befehl ohne Platzhalter und was aus welchem Ergebnis folgt; Meldung
   `BLOCK <ID> WARTET befehl`.
6. **`max_parallel_blocks`** in `ORCHESTRATE.md` deckelt die gleichzeitig vergebenen Blöcke über
   alle Worker. Sagt der Mensch ein nahes Kontingentlimit an, gilt `1`.

Statuswerte bleiben: `WARTET` setzt den Block auf `blocked`, wie eine offene `FRAGE`; `WEITER`
setzt ihn zurück auf `assigned`. Unter `max_parallel_blocks` zählen `assigned`, `blocked` und
`gate` mit — der Block liegt beim Worker, bis er abgenommen ist.

Keine Validator-Änderung, keine Finding-ID, `schema_version` bleibt `1`. Das Agent-Frontmatter
bleibt in den Feldern aus ADR-0013. Version 0.5.1.

Verworfene Alternativen:

- **Übergabe-Datei im Arbeitsrepo committen.** Eine Datei außerhalb der Umfangsgrenze in jedem
  PR — genau das hat ADR-0014 schon verworfen.
- **Startprompt in jeden Auftrag kopieren.** Verständlich, aber jede zugestellte Nachricht kostet
  Kontingent wie ein Prompt; der Worker-Kopf plus Datei plus `WORKER UNBEKANNT` als Rückfall ist
  billiger und genauso robust.
- **Jeder Desktop-Worker leert sich selbst.** Über Rechnergrenzen weckt ihn danach niemand
  sicher; das Leeren über den Subagent reicht dort.
- **Transkript-Lesen zur Pflicht machen.** Geht nur auf demselben Rechner und nur auf Claude
  Desktop. Als Regel „wo die Umgebung es kann", festgestellt in `SETUP`.

## Consequences

**Positiv**

- Ein Worker, der sich leert, bleibt Worker.
- Der Orchestrator sieht auf demselben Rechner, was der Mensch direkt mit dem Worker bespricht.
- Freigaben haben genau einen Weg, und der führt nicht über eine Nachricht.

**Negativ**

- `mechanismen.md` hängt jetzt zusätzlich am Session-Werkzeug von Claude Desktop, dessen Namen
  und Verhalten sich ändern können. Jeder Befund trägt deshalb Datum und Quelle.
- Der Worker schreibt eine Datei in seinen Checkout, wenn auch nicht ins Repo.

**Grenze**

Neu zu bewerten, wenn Transkripte auch über Rechnergrenzen lesbar werden oder `SendMessage` eine
geleerte Session zuverlässig weckt — dann entfällt die Sonderbehandlung für Claude Desktop.

## Nachtrag — 2026-09-26

Worker-Verfahren `chip` ergänzt. Auf Claude Desktop legt der Orchestrator den Startprompt als
Aufgaben-Chip (`spawn_task` mit `cwd` des Ziel-Repos) vor, der Mensch startet die Session mit
einem Klick. Der Klick bleibt, weil das Starten ohne Klick (`start_session`,
`hand_off_to_session`) im Code der App an einem serverseitigen Feature-Flag hängt, das der
Nutzer nicht schalten kann; die Freigabe ist als anthropics/claude-code#94697 „not planned"
geschlossen. Befund mit Quelle in `reference/mechanismen.md`. Neu zu bewerten, sobald
`start_session` in einer Session erscheint.
