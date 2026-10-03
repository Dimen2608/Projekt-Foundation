# Mechanismen — was wo funktioniert

> Beantwortet: **Wie kommen Worker zum Orchestrator, und wie laufen Auftrag und Übergabe?**
> Diese Datei veraltet schneller als jede andere des Plugins. Jeder Befund trägt seine Quelle;
> in `SETUP` wird er **erneut festgestellt, nicht übernommen**.
>
> Stand: 2026-09-26, Claude Code 2.1.283. Quellen: code.claude.com/docs (`remote-control`,
> `cross-session-messaging`, `sub-agents`, `headless`, `agent-teams`), Ausführung in einer
> Cloud-Session (ADR-0014) und Betrieb auf Claude Desktop (Code-Tab, Windows) in einem Lauf mit
> einer Kopf- und zwei Arbeits-Sessions vom 2026-08-28 bis 2026-09-26 (ADR-0015). **Geprüft**
> heißt ausgeführt; **Betrieb** heißt über Wochen im Einsatz; **Doku** heißt nur gelesen.

## Grundform: Remote Control + `SendMessage`

Orchestrator und Worker sind gewöhnliche Sessions auf den Rechnern des Menschen, jede mit Remote
Control verbunden. Dann sehen sie sich gegenseitig in `ListAgents` und reden per `SendMessage` in
beide Richtungen — über Rechner- und Repo-Grenzen hinweg; die Nachrichten laufen über die Server
von Anthropic. *(Doku)*

**Remote Control einschalten** *(Doku)*:

| Wo | Wie |
| --- | --- |
| Neue CLI-Session | `claude --rc` (bzw. `--remote-control`) im Repo-Ordner |
| Als Server, wartet auf Verbindungen | `claude remote-control` im Repo-Ordner |
| Laufende Session | `/remote-control` (bzw. `/rc`) |
| Dauerhaft für alle Sessions | `/config` → Remote Control für alle Sessions, oder `remoteControlAtStartup: true` in den Einstellungen |
| Claude Desktop | Remote Control je Session einschaltbar; nach dem Wecken einer geleerten Session wieder verbunden *(Betrieb)* |

**Der Orchestrator muss selbst verbunden sein.** Schreibt eine Session ohne Remote Control an
eine Session auf einem anderen Rechner, hat der Empfänger keine Antwortadresse. *(Doku)*

## Was eine Nachricht kann und was nicht

- **Adresse ist der Name**, den `ListAgents` zeigt. Doppelte Namen unterscheidet ein `[ref]`.
  Die erste Zeile ist oft alles, was der Empfänger in der Vorschau sieht — deshalb das feste
  Nachrichtenformat in `SKILL.md`. *(Doku)*
- **Befehle laufen nicht.** Ein `/clear` oder `/compact` im Text kommt als Text an. Eine Session
  kann eine andere per Nachricht nicht leeren; per Werkzeug nur eingeschränkt, siehe Tabelle unten. *(Doku, Betrieb 2026-10-03)*
- **`@datei` hängt nichts an.** Inhalte als Text schicken. *(Doku)*
- **Keine Fertig-Meldung über Rechnergrenzen.** `notify_when_idle` gilt nur für Sessions auf
  demselben Rechner. Der Worker schickt die Übergabe deshalb selbst. *(Doku)*
- **Annahme beim Empfänger** (`crossSessionInbound`): Ohne Einstellung nimmt eine Session, die
  nach Rechten fragt, Nachrichten an — außer der Absender läuft mit `bypassPermissions`, dann
  hält sie sie zur Freigabe zurück. Eine Session mit `bypassPermissions` hält Nachrichten
  zurück, außer der Absender auch. `accept` / `hold` / `refuse` lassen sich fest einstellen —
  **das entscheidet der Mensch je Worker, nicht der Skill.** Stille ist kein Einverständnis:
  Eine zurückgehaltene Nachricht meldet sich beim Absender nicht. *(Doku)*

## Claude Desktop: Sessions auf demselben Rechner

Der Code-Tab von Claude Desktop bringt ein Werkzeug zur Session-Verwaltung mit
(`mcp__ccd_session_mgmt__*`, per `ToolSearch` zu laden). Es reicht nur auf Sessions **dieses**
Rechners — Remote-Control-Sessions anderer Rechner kennt es nicht. Für Orchestrator und Worker
auf einem Rechner ist es der tragende Weg:

| Aufgabe | Werkzeug | Befund |
| --- | --- | --- |
| Session-ID eines Workers finden | `list_sessions`, am **Arbeitsverzeichnis** auflösen | *Betrieb.* Nie aus dem Gedächtnis — sie ist die Adresse zum Wecken. Arbeitet der Worker in einem Worktree, ist sein `cwd` der Worktree-Pfad unter dem Repo, nicht der Repo-Ordner: am Präfix auflösen. |
| Worker benennen | `set_session_title` | *Geprüft 2026-09-26:* Der Titel ist die Adresse für `SendMessage`; ein vom App vergebener Titel wird ohne Rückfrage ersetzt. |
| Ruhenden oder geleerten Worker wecken | `send_message` an die Session-ID | *Betrieb.* Weckt zuverlässig. `SendMessage` an den Namen ist nach dem Leeren **nicht sicher** zustellbar. |
| Wartenden Worker erreichen (`ANTWORT`, `NACHARBEIT`), wenn er sich geleert haben kann | `send_message` an die Session-ID | *Betrieb.* Ein wartender Worker ruht; der Weg ist derselbe wie beim Wecken. |
| Laufenden Worker mitten im Turn erreichen | `SendMessage` an den Namen | *Betrieb.* Die Nachricht wird eingereiht; arbeitet der Worker bis zu seinem Selbst-Leeren durch, kommt sie erst danach an (Betrieb 2026-10-03). Namen fest vergeben (`claude --name`, `/rename`); ohne das leitet sich der Name aus dem Ordner ab und wechselt bei jedem Neustart. Sitzungstitel taugen nicht als Adresse. |
| Ist-Stand des Workers lesen | `list_events`, bei Suche `search_session_transcripts` | *Betrieb.* Das Transkript enthält **beide** Kanäle — die Nachrichten und das, was der Mensch direkt mit dem Worker bespricht. Die Nachricht allein ist blind für den zweiten: In einer Woche mit anwesendem Menschen standen 154 direkte Rückfragen im Worker gegen 6 Nachrichten an den Kopf. |
| Selbst leeren | `clear_session` mit `session_id: "self"` | *Geprüft 2026-09-23:* läuft ohne Klick des Menschen; Session-ID, Titel, Modell und Effort bleiben; `list_events` liest weiter; Remote Control ist nach dem Wecken wieder da. |
| Fremde Session leeren | `clear_session` mit fremder ID | *Geprüft:* verweigert. *Betrieb 2026-10-03:* geht nur bei eigenen, untätigen, nicht angehefteten Sessions ohne Remote Control; sonst verweigert. In Desktop-WSL gibt es `clear_session` nicht. |

**Warum leeren:** Eine Session liest bei jeder Anfrage ihren ganzen Verlauf mit — gemessen
250–290k Token gegen 60–70k bei einer frischen. Leeren kostet nichts, `/compact` ist selbst eine
teure Anfrage. *(Betrieb)*

**Was ein Worktree nicht mitbringt:** Dateien, die das Repo ignoriert — installierte Addons,
Import-Caches, lokale Konfiguration. Im Test fehlte einem Worker im Worktree ein ignoriertes
Test-Addon, die Tests liefen dort nicht; im Haupt-Checkout lag es. *(Geprüft 2026-09-26)*
Deshalb prüft der Worker beim Start, ob die Befehle des Repos in seinem Checkout laufen.

**Was nach dem Leeren fehlt:** alles, was nur im Chat stand — auch der Startprompt. Was auf der
Platte steht, bleibt: `CLAUDE.md` oberhalb des Arbeitsverzeichnisses wird bei jedem Start
geladen, und `.claude/worker.md` trägt das Gedächtnis des Workers. *(Betrieb)*

## Kosten und Grenzen einer Nachricht

- **Jede zugestellte Nachricht kostet Kontingent wie ein getippter Prompt.** Deshalb liest der
  Orchestrator den Rückweg, statt sich berichten zu lassen. *(Betrieb)*
- **`notify_when_idle` ist ein einmaliges Abo**, und ein neueres verdrängt ein älteres —
  höchstens eines gleichzeitig, an den letzten Auftrag einer Runde. Ohne `message` kostet es den
  Empfänger nichts. Bleibt die Meldung aus, zuerst das eigene Vorgehen verdächtigen. *(Geprüft
  2026-08-30)*
- **Eine Nachricht aus einer anderen Session kann keine Zustimmung sein** — das erzwingt das
  Werkzeug, nicht nur die Hausregel. Sie kann auch keine Konfiguration ändern. *(Betrieb)*
- **Berechtigungs-Klassifikator:** Er hält Befehle an, die Produktion oder Rechte berühren —
  im Betrieb dreimal an einem Vormittag. Das ist die Schutzlinie, keine Panne; sie wird nicht
  umgangen, sondern der Mensch bekommt den exakten Befehl. *(Betrieb)*

## Worker-Verfahren

| Verfahren | Wann | Befund |
| --- | --- | --- |
| **`attach`** (Standard) | Immer. Der Mensch öffnet im Ziel-Repo eine Session mit Remote Control und fügt den Startprompt ein; der Worker meldet sich mit `WORKER BEREIT`. | Grundform oben. |
| **`chip`** (Claude Desktop) | Der Orchestrator ruft `spawn_task` mit `cwd` = Ordner des Ziel-Repos und dem Startprompt als `prompt` auf. Der Mensch sieht einen Chip und startet die Session mit einem Klick, in einem neuen Worktree. | *Geprüft 2026-09-26 (Prüfliste 7):* Ein Klick startet die Session in einem neuen Worktree des Ziel-Repos (`<repo>/.claude/worktrees/<name>`, Branch `<präfix>/<name>`, Ort und Präfix aus den Desktop-Einstellungen), mit Remote Control. Der Prompt läuft als erster Turn, die Meldung per `SendMessage` kommt an. Ihr Name ist zunächst der Chip-Titel; der Orchestrator benennt sie mit `set_session_title` in den Worker-Namen um, `ListAgents` zeigt den neuen Namen sofort. Der Klick bleibt Handarbeit — siehe `start_session` unten. |
| **`local_bg`** (nur auf ausdrücklichen Wunsch) | Worker auf dem Rechner des Orchestrators: `claude --bg "<Startprompt>"`, Übersicht mit `claude agents --json`. | *Geprüft:* `--bg` und `--print` schließen sich aus; außerhalb eines vertrauten Workspace verweigert; mit `bypassPermissions` vom Auto-Mode-Klassifikator abgelehnt — richtig so, nie umgehen. In einem vertrauten Repo mit geerbten Rechten ungeprüft. |

**Nicht vorgesehen:**

- **Cloud-Sessions als Worker.** *Geprüft:* Start, Status und Archivierung per Remote-API gehen,
  aber die Antwort der Kind-Session war vom Starter aus nicht lesbar, und die Statuszusammenfassung
  deutete an, dass der Startprompt nicht als erster Turn verarbeitet wurde. Dazu ein Container je
  Worker. Entscheidung des Auftraggebers: nicht Teil des Verfahrens.
- **`claude -p --session-id <uuid>` / `--resume <uuid>`.** *Geprüft:* feste Session-ID,
  JSON-Ergebnis (`result`, `session_id`, `total_cost_usd`), Wiederaufnahme mit erhaltenem
  Kontext. Aber ein blockierender Aufruf, keine eigenständige Session, die man per `SendMessage`
  erreicht.
- **Agent Teams** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`): experimentell. *(Doku)*
- **`start_session` / `hand_off_to_session`** — eine Session startet eine andere ohne Klick,
  sichtbar in der Seitenleiste. *Geprüft 2026-09-26 an Claude Desktop 2.9939.2 (Windows):* Die
  Werkzeuge gibt es im Code der App, im Server `ccd_session` neben `spawn_task`. Sie hängen an
  einem **serverseitigen Feature-Flag** (`2371478310`): Ist es an, fällt `spawn_task` weg und
  `start_session`, `hand_off_to_session` und `list_start_targets` erscheinen. Ist es aus, gibt es
  nur den Chip. Keine Einstellung, kein Rechtemodus und keine Umgebungsvariable schaltet es. Der
  Wunsch, es freizugeben, steht als Issue anthropics/claude-code#94697, geschlossen als
  „not planned". Die Doku (code.claude.com/docs) nennt die Werkzeuge nicht. Das Flag lokal zu
  überschreiben hieße, die signierte App zu verändern — nicht Teil des Verfahrens.
  **Neu bewerten**, sobald `start_session` in einer Session erscheint oder dokumentiert wird.

## Subagents im Worker

- Blockarbeiter und Tor sind Subagents des Workers. Jeder Aufruf startet mit frischem Kontext;
  zurück kommt nur die Schlussmeldung. *(Doku, geprüft)*
- **Verschachtelungstiefe:** laut Doku bis 3, in der geprüften Cloud-Umgebung
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`. Deshalb startet der **Worker** beide Subagents
  nacheinander — der Blockarbeiter startet das Tor nicht selbst.
- Plugin-Agents wirken erst nach `/reload-plugins` oder Neustart der Session. *(geprüft:
  alle fünf Agents des Plugins werden registriert)*

## Kontext leeren

| Wo | Selbst leeren | Quelle |
| --- | --- | --- |
| Subagent | immer — sein Kontext verfällt mit dem Ende | Grundlage des Verfahrens |
| Session, Mensch tippt `/clear` | ja; mit Remote Control sehen alle verbundenen Geräte das | Doku |
| Session leert sich auf eigene Veranlassung (Claude Desktop) | ja, `clear_session` mit `"self"` | geprüft 2026-09-23, siehe oben |
| Cloud-Session | kein Werkzeug dafür; `/compact` verfügbar | geprüft |
| Fremde Session per Nachricht | nein — Befehle in Nachrichten laufen nicht | Doku |

## Prüfliste — noch ungeprüfte Stellen

Auf dem Rechner des Menschen abarbeiten, Ergebnis mit Datum und Version oben eintragen:

1. **Orchestrator erreichbar** *(halb geprüft 2026-09-16: Remote-Control-Sessions eines zweiten
   Rechners stehen in `ListAgents` und sind per `SendMessage` erreichbar; ihr Transkript ist vom
   ersten Rechner aus **nicht** lesbar. Die Gegenrichtung ist offen)*: Orchestrator auf Claude Desktop oder mit `claude --rc` öffnen.
   Auf einem **zweiten Rechner** oder in einem anderen Repo einen Worker mit `claude --rc`. Zeigt
   `ListAgents` im Worker den Orchestrator, und umgekehrt?
2. **Rückkanal:** Worker schickt `WORKER BEREIT test <repo> <branch>`. Kommt sie an, kann der
   Orchestrator mit `BLOCK T1 AUFTRAG` antworten, kommt die Antwort an?
3. **Selbst leeren auf Desktop** *(geprüft 2026-09-23, siehe „Claude Desktop" oben; nach dem
   Leeren per Session-ID wecken, nicht per Name)*: Im Worker nach einem kleinen Block die Übergabe schicken und
   sich selbst leeren lassen. Ist der Kontext danach leer (Frage nach einem Detail)? Ist die
   Session unter demselben Namen weiter erreichbar?
4. **Fremder Befehl** *(Teilbefund: Leeren einer fremden Session per Werkzeug wird verweigert;
   `/clear` als Nachrichtentext noch nicht ausdrücklich geprüft)*: Vom Orchestrator `/clear` als Nachricht schicken. Erwartet: wird **nicht**
   ausgeführt.
5. **Plugin-Agents im Worker:** `project-foundation:orchestrate-blockarbeiter` und danach
   `project-foundation:orchestrate-tor` aus dem Worker aufrufbar?
6. **Annahme ohne Rückfrage:** Laufen Orchestrator und Worker im selben Rechtemodus, kommt ein
   Auftrag ohne Freigabedialog an?
7. **`chip`** (Claude Desktop) *(geprüft 2026-09-26, siehe Worker-Verfahren)*: Chip mit einem
   kurzen Startprompt vorlegen, anklicken lassen. Startet die Session im richtigen Repo, meldet
   sie sich, findet der Orchestrator sie per `list_sessions`?
8. **`local_bg`** (nur falls gewünscht): In einem vertrauten Repo `claude --bg "<kurzer
   Auftrag>"` ohne Rechte-Erweiterung. Startet er, erscheint er in `claude agents --json`, ist er
   per `SendMessage` erreichbar?
