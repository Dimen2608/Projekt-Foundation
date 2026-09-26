# ADR-0014: Ein dritter Skill `project-orchestrate` — eine Hauptsession steuert Worker-Sessions in Blöcken

## Status

Accepted — 2026-09-26

## Context

Nach `FOUNDATION READY` beginnt die Implementierung. Bei größeren Vorhaben — mehrere Repos,
mehrere unabhängige Arbeitspakete — läuft eine einzelne Session in zwei Grenzen: Ihr Kontext
wächst mit jedem Paket, bis frühe Entscheidungen verdrängt sind, und sie arbeitet streng
nacheinander. Gewünscht ist ein **Orchestrator**: eine Hauptsession, die andere Sessions steuert,
Aufgaben immer als **Blöcke** vergibt, am Ende jedes Blocks eine **Übergabe** entgegennimmt,
nach der die Unter-Session ihren Kontext leert. Die Unter-Sessions sind echte Sessions, auch in
anderen Repos und auf anderen Rechnern, per Remote Control erreichbar und per `SendMessage`
ansprechbar.

Vor der Entscheidung wurde am 2026-09-26 geprüft, was Claude Code heute kann — in der
Dokumentation (code.claude.com/docs: `sub-agents`, `agent-teams`, `headless`, `agent-sdk/sessions`,
`worktrees`, `workflows`, `remote-control`, `cross-session-messaging`, `plugins/components`) und
durch Ausführen in einer Cloud-Session mit Claude Code 2.1.283. Die Befunde stehen einzeln, mit
Quelle, in `reference/mechanismen.md` des Skills; die tragenden sind:

| Mechanismus | Befund |
| --- | --- |
| Remote Control + `SendMessage` | Doku: Sessions mit Remote Control sehen sich in `ListAgents` und reden in beide Richtungen, rechner- und repoübergreifend. Ohne Remote Control am Absender hat ein Empfänger auf einem anderen Rechner keine Antwortadresse. Befehle im Nachrichtentext laufen nie. Eine Fertig-Meldung (`notify_when_idle`) gibt es nur auf demselben Rechner. |
| Subagent (Agent-Tool, Plugin-Agents) | GA, frischer Kontext je Aufruf, Rückgabe ist die Schlussmeldung. Verschachtelung laut Doku bis Tiefe 3, in der geprüften Cloud-Umgebung auf 1 gesetzt. |
| Hintergrund `claude --bg` | Vorhanden. Außerhalb eines vertrauten Workspace verweigert; mit `bypassPermissions` vom Auto-Mode-Klassifikator abgelehnt. |
| Headless `claude -p --session-id` / `--resume` | Ausgeführt: feste ID, JSON-Rückgabe, Wiederaufnahme mit Kontext — aber blockierend, keine ansprechbare Session. |
| Cloud-Session per Remote-API | Ausgeführt: Start, Status, Archivierung. Die Antwort der Kind-Session ist vom Starter aus nicht lesbar. |
| Agent Teams | Experimentell, per Umgebungsvariable. |
| Kontext leeren | Ein Subagent-Kontext verfällt immer. `/clear` durch den Menschen immer. Auf Claude Desktop leert sich eine Session nach Angabe des Auftraggebers selbst — hier ungeprüft. In der Cloud kein Werkzeug dafür. |

Die Entscheidungen fielen in einem Interview mit dem Auftraggeber, Frage für Frage, je mit
Empfehlung; zwei davon nach einer Gegenlesung durch einen unabhängigen Gutachter.

## Decision

**1. Dritter Skill im selben Plugin**, unter `plugins/project-foundation/skills/project-orchestrate/`,
Phasen `SETUP → PLAN → DISPATCH → GATE → INTEGRATE`. Er setzt dort an, wo `project-foundation`
endet. ADR-0002 gilt: genau eine Kopie, unter `plugins/`.

**2. Der Worker ist eine eigenständige Session** — keine Subagent-Rolle. Er kann selbst
Subagents starten. Ein Worker lebt über mehrere Blöcke; **die eigentliche Blockarbeit läuft in
einem Subagent**, dessen Kontext mit seinem Ende verfällt. Das ist das Leeren, das überall
funktioniert. Wo die Umgebung einer Session erlaubt, sich selbst zu leeren, tut der Worker das
nach der Übergabe zusätzlich.

**3. Worker werden angebunden, nicht gespawnt.** Standard ist `attach`: Der Mensch öffnet im
Ziel-Repo eine Session mit Remote Control und fügt den Startprompt ein (`WORKER-START.md`); der
Worker meldet sich per `SendMessage` mit `WORKER BEREIT`. Nur wenn der Mensch es in `SETUP`
ausdrücklich will, startet der Orchestrator zusätzlich Worker auf seinem eigenen Rechner mit
`claude --bg` (`local_bg`). **Cloud-Sessions sind als Worker nicht vorgesehen** — sie werden
selten genutzt, ihre Antwort war nicht lesbar, und sie kosten einen Container je Worker. Nie
`bypassPermissions`; ein Worker hat höchstens die Rechte des Orchestrators.

**4. Der Orchestrator läuft auf dem Rechner des Menschen, mit Remote Control.** Ohne das können
Worker auf anderen Rechnern nicht antworten. `SETUP` prüft das und bricht sonst ab.

**5. Heimat-Repo plus fremde Repos.** Konfiguration, Blockplan und Blockdateien liegen unter
`orchestrate/` im Heimat-Repo und werden **committet**, auf einem eigenen `state_branch`, nie auf
einem Worker-Branch — der Stand überlebt jedes Leeren des Orchestrators, die Git-Historie ist
das Protokoll. Worker arbeiten im Heimat-Repo oder in fremden Repos, je Block auf dessen Branch.

**6. Übergabe: Die Nachricht ist Transport, die Blockdatei ist die Wahrheit.** Der Worker
schickt die vollständige Übergabe per `SendMessage`; der Orchestrator schreibt sie in die
Blockdatei. Worker brauchen so kein Schreibrecht auf das Heimat-Repo, und im Arbeitsrepo entsteht
keine Datei außerhalb des Auftrags. Weil es über Rechnergrenzen keine Fertig-Meldung gibt,
schickt der Worker die Übergabe selbst.

**7. Rollen.** Der Orchestrator **baut nicht** — kein Produktcode, kein Commit in einem
Arbeitsrepo; er schreibt nur unter `orchestrate/`. Einen PR auf „ready for review" stellen oder
mergen ist Zusammenführung, kein Bauen. Das ist *the head level does not build* aus ADR-0013,
übertragen. Jeder Block geht durch ein **Tor**, bevor er als erledigt gilt.

**8. Zwei neue Agents**, registriert als `project-foundation:orchestrate-blockarbeiter` und
`project-foundation:orchestrate-tor`. Frontmatter nur mit den Feldern, die ADR-0013 zulässt;
`background` und `maxTurns`, die die Doku kennt, bleiben außen vor.

| Rolle | Modell / Effort | Werkzeuge | Warum |
| --- | --- | --- | --- |
| Blockarbeiter | `sonnet` / `high` | Read, Write, Edit, Grep, Glob, Bash, Skill | Führt genau einen Bau-Block aus, in frischem Kontext; `Skill`, weil der Block den passenden Skill benennt. |
| Tor | `opus` / `high` | Read, Grep, Glob, Bash; `isolation: worktree` | Wie der Rethink-Gutachter die Rolle, die den Fehler findet, den niemand vermutet hat. Lesend; die Sperre ist begrenzt, nicht erzwungen, weil `Bash` bleibt. Holt den Block-Branch in seinen eigenen Worktree. |

Das Tor läuft **in der Worker-Session**, direkt nach dem Blockarbeiter: Dort liegt der Checkout
des Arbeitsrepos, und der Orchestrator-Kontext bleibt klein. Unabhängig ist es trotzdem — ein
frischer Subagent, der Auftrag und Diff bekommt, nicht die Begründung. Der Rethink-Gutachter
wird nicht wiederverwendet: Sein Maßstab (Messstand, Masken, Bereichsdateien) passt nicht auf
Bau-Blöcke.

**9. Vorbereitungsblock als einzige Ausnahme.** Ist `project-foundation` oder `project-rethink`
zuständig, läuft der Block **nicht** im Blockarbeiter, sondern in der Worker-Session selbst, und
seine Fragen gehen an den Menschen, der die Worker-Session vor sich hat. Grund (Fund der
Gegenlesung): Foundation fragt in `ASK` den Menschen, was ein Subagent nicht kann; ein ganzer
Foundation-Lauf passt nicht in einen Subagent-Kontext; Rethink startet eigene Agents, was bei
Verschachtelungstiefe 1 nicht ginge. Abnahme: `FOUNDATION VALID`, danach das Tor.

**10. Eskalation und Runden.** Fragen eines Workers im Bau-Block gehen an den Orchestrator,
nicht an den Menschen. Der Orchestrator beantwortet sie, wenn Dokumentation oder ADR des
Zielprojekts es entscheiden, sonst fragt er den Menschen. Stop Conditions eines Zielprojekts
entscheidet er nie. **Die Runden zählt nur der Worker**, je Block über jeden Tor-Aufruf und jede
`NACHARBEIT` des Orchestrators hinweg; höchstens fünf. Danach übergibt er mit `exhausted`, der
Block wird `escalated`, und der Orchestrator legt dem Menschen „weiter oder nicht" mit Pro und
Contra vor — oder der Mensch entscheidet anders. (Der Rethink-Gutachter bleibt bei zwei Runden:
Spezifikationsdateien und Bau-Blöcke sind verschiedene Gegenstände.)

**11. Parallelität mit Regeln.** Der Blockplan führt je Block „hängt ab von" und „Repo/Branch".
Parallel laufen nur Blöcke, deren Abhängigkeiten erledigt sind; nie zwei Worker auf demselben
Branch.

**12. Ein Block hat sechs Pflichtfelder:** Ziel (ein Satz), Repo/Branch, Eingang (mit
Basis-Commit, gegen den das Tor den Diff bildet), Umfangsgrenze, Abnahmekriterium (prüfbar),
Zuständig (Skill oder Agent). Ohne Abnahmekriterium wird kein Block vergeben — das Tor hätte
nichts, woran es prüft. Ein Bau-Block muss in den Kontext eines Subagents passen, sonst wird er
geteilt.

**13. Zusammenführung konfigurierbar.** `merge_mode: human` (Standard): Nach dem Tor wird der
Draft-PR des Workers „ready for review", der Mensch mergt. `merge_mode: orchestrator`: Bei Tor-Ja
und grüner CI mergt der Orchestrator selbst.

**14. Installer als erste Phase `SETUP`**, ein geführtes Interview, wiederholbar. Es fragt
Heimat-Repo, weitere Repos (mit Rechner), Merge-Modus und Worker-Verfahren ab, prüft die
Erreichbarkeit des Orchestrators, prüft vorhandene Agents und Skills, ordnet sie Aufgabenarten
zu, sucht fehlende im Marketplace und **schlägt sie einzeln zur Installation vor** — installiert
wird nur, was der Mensch bestätigt. Ein Python-Installer ist verworfen: Skills und Plugins
suchen und installieren geht nur mit Werkzeugen einer Session. Ergebnis ist
`orchestrate/ORCHESTRATE.md` mit einem YAML-Block am Anfang und deutschem Fließtext.

**15. Voraussetzung je Repo: `FOUNDATION VALID`.** Ohne `VALID` ist der erste Block dieses Repos
ein Vorbereitungsblock (9). Das ist der Leitsatz *no feature work on an unresolved foundation*
aus ADR-0013, angewendet auf jedes Repo, in dem gebaut wird: Ein Worker mit frischem Kontext hat
nichts als die Foundation des Repos. Verlangt wird maschinell `VALID`, nicht `READY` —
`READY` ist ein Urteil aus Review und Entscheidungen des Menschen, das kein Programm feststellen
kann (ADR-0010); das Heimat-Repo steht ohnehin auf `READY`, bevor orchestriert wird.

**16. Keine Validator-Änderung.** `ORCHESTRATE.md`, `BLOCKPLAN.md` und die Blockdateien werden
keine Pflichtstellen: Die Fragen, die sie beantworten, stellt nur ein Projekt, das orchestriert.
Keine neue Finding-ID, `schema_version` bleibt `1`, `.project-foundation.yml` bleibt unberührt
(ADR-0004). Kein Test nach ADR-0009: Ein Skill ist Prompt-Material.

**17. Umfang nach ADR-0011.** Vier Vorlagen, jede gegen ihre Frage:

| Frage | Vorlage |
| --- | --- |
| Welche Repos, wer mergt, wie kommen Worker dazu, welcher Skill oder Agent für welche Aufgabenart? | `ORCHESTRATE.md` |
| Welche Blöcke gibt es, in welchem Zustand, wer arbeitet woran, was hängt wovon ab? | `BLOCKPLAN.md` |
| Was genau ist der Auftrag eines Blocks, was wurde übergeben, was sagt das Tor? | `BLOCK.md` |
| Wie wird eine Session zum Worker? | `WORKER-START.md` |

Dazu `reference/mechanismen.md`: wie Remote Control und `SendMessage` eingesetzt werden, jeder
Befund mit Quelle, und die Prüfliste für die noch ungeprüften Stellen. Auftrag, Übergabe und
Tor-Urteil stehen in **einer** Blockdatei statt in drei: Wer einen Block nachliest, braucht alle
drei.

**18. Abgrenzung zu `Out of Scope`.** `docs/PROJECT.md` schließt Projektmanagement, Ticketing,
Roadmaps, Zeitschätzung und Code-Generierung für Zielprojekte aus. Der Orchestrator schätzt keine
Termine, führt keine Roadmap und kein Ticketsystem, und er erzeugt selbst keinen Code — er steuert
die Ausführung durch Sessions, deren Code von den Skills des Zielprojekts kommt. Der Blockplan ist
ein Ausführungsvertrag wie `ABLAUF.md` in Rethink, keine Planung auf Zeit. Wird aus dem
Blockplan ein Backlog mit Prioritäten und Terminen, ist diese Grenze überschritten.

**19. Abgrenzung der Trigger** allein in der `description` von `project-orchestrate`: Sie zieht
bei „mehrere Sessions steuern", nicht bei „Projekt vorbereiten". Die Beschreibungen der beiden
anderen Skills bleiben unverändert, weil sich ihre Trigger nicht überschneiden — Foundation und
Rethink bereiten vor, Orchestrate führt aus. Der Auslöse-Test bekommt einen dritten Satz.

Verworfene Alternativen:

- **Cloud-Sessions als Worker (Spawn per Remote-API).** Technisch startbar, aber die Antwort war
  nicht lesbar, und ein Worker ohne Rückkanal braucht einen zweiten Übergabeweg über Dateien im
  Arbeitsrepo, der im PR landet. Entscheidung des Auftraggebers: nicht vorgesehen.
- **Spawnen als Standard.** Der Mensch soll bestimmen, auf welchem Rechner und in welchem Repo
  ein Worker läuft; Spawnen gibt es nur lokal und nur auf Wunsch.
- **Agent Teams als Grundlage.** Passt vom Konzept, ist aber experimentell; ein Toolkit, das sich
  selbst prüft, baut nicht auf einer Umgebungsvariable mit ungewisser Zukunft.
- **Nur Subagents in einer Session.** Stabil, aber keine eigenständigen Sessions, keine anderen
  Repos auf anderen Rechnern.
- **Eine neue Session je Block.** Das sauberste Leeren, aber der Mensch müsste je Block eine
  Session öffnen.
- **Übergabe nur im Chat.** Geht beim Leeren des Orchestrators verloren.
- **Konfiguration in `.project-foundation.yml`.** Schema-Änderung, Stop Condition, gegen ADR-0004.
- **Teil von `project-rethink`.** Beide arbeiten in Blöcken mit Tor, aber mit anderem Zweck;
  vermischt ergäbe das einen Skill mit zwei Eingängen.

## Consequences

**Positiv**

- Größere Vorhaben lassen sich nach der Foundation in Blöcken über mehrere Sessions, Repos und
  Rechner ausführen, ohne dass der Kontext einer Session mitwächst.
- Jeder Block ist nachlesbar: Auftrag, Übergabe und Tor in einer committeten Datei.
- Validator, Finding-IDs und Manifest-Schema bleiben unberührt.

**Negativ**

- Der Skill hängt an Remote Control und `SendMessage`. `mechanismen.md` veraltet schneller als
  jede andere Datei des Plugins; sie trägt deshalb Datum, Version und je Befund die Quelle.
- Rückkanal über Rechnergrenzen und Selbst-Leeren auf Claude Desktop sind aus der Cloud-Session,
  in der dieser Skill entstand, nicht prüfbar gewesen. Bis die Prüfliste abgearbeitet ist, gilt
  das Selbst-Leeren als optional.
- Der Mensch öffnet die Worker-Sessions selbst. Das ist gewollt (Kontrolle über Rechner und
  Kosten), aber Handarbeit je Worker — nicht je Block.
- Das Plugin trägt jetzt Prompt-Material für drei Prozesse und fünf Agents. Der Leitsatz *the
  foundation must remain smaller than the system it enables* gilt auch hier: Orchestrate lohnt
  sich erst ab mehreren Blöcken; für einen Block ist eine Session genug.

**Grenze**

Neu zu bewerten, wenn Agent Teams GA werden oder Cloud-Sessions verlässlich zurückschreiben —
dann kann das Spawnen wieder in Frage kommen. Und wenn der Blockplan anfängt, Termine zu tragen:
Dann ist der Skill Projektmanagement geworden.
