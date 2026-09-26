# Mechanismen — was wo funktioniert

> Beantwortet: **Wie startet der Orchestrator in dieser Umgebung Worker, und wie kommt die
> Übergabe zurück?** Diese Datei veraltet schneller als jede andere des Plugins. Jeder Befund
> trägt Datum und Version; in `SETUP` wird er **erneut festgestellt, nicht übernommen**.
>
> Stand der Befunde: 2026-09-26, Claude Code 2.1.283, geprüft in einer Cloud-Session
> (Claude Code on the Web) und gegen code.claude.com/docs (ADR-0014).

## Stufenfolge für den Worker-Start

Die erste verfügbare Stufe gilt. „Verfügbar" heißt: Das Werkzeug ist in **dieser** Session
vorhanden **und** ein Probestart gelingt — nicht, dass die Doku es kennt.

| Stufe | Verfahren | Woran erkennbar | Rückkanal | Befund |
| --- | --- | --- | --- | --- |
| 1 | **Cloud-Spawn** über die Remote-API: `create_session` (Prompt = Startprompt, `source_url` = Repo, eigener Branch), `get_session` für den Status, `archive_session` zum Aufräumen | Werkzeuge `mcp__Claude_Code_Remote__*` vorhanden | Übergabe-Datei im Worker-Branch; der Worker kann nicht per Nachricht zurück | Start, Status, Archivierung ausgeführt. Die Antwort des Workers ist vom Orchestrator aus **nicht lesbar** (nur Status und Kurzzusammenfassung). Die Statuszusammenfassung deutete an, dass der Startprompt nicht als erster Turn verarbeitet wurde — vor produktivem Einsatz mit einem Probeblock prüfen. |
| 2 | **Lokaler Hintergrundstart:** `claude --bg "<Startprompt>"`, Übersicht mit `claude agents --json` | `claude --help` nennt `--bg`; Workspace vertraut | `SendMessage` in beide Richtungen (gleiche Maschine) | `--bg` und `--print` schließen sich aus. Scheiterte außerhalb des Repos am fehlenden Workspace-Vertrauen; mit `bypassPermissions` vom Auto-Mode-Klassifikator abgelehnt — richtig so, nie umgehen. In einem vertrauten Repo mit geerbten Rechten ungeprüft. |
| 3 | **Handstart:** Der Orchestrator gibt den Startprompt aus `WORKER-START.md` aus, der Mensch öffnet eine Session im Ziel-Repo und fügt ihn ein | immer | `SendMessage`, wenn beide Sessions sich per `ListAgents` sehen (gleiche Maschine oder Remote Control); sonst Übergabe-Datei | Grundweg. Auf Claude Desktop nach Angabe des Auftraggebers mit `SendMessage` in beide Richtungen. |

Nicht als Stufe geführt:

- **`claude -p --session-id <uuid>` / `--resume <uuid>`** (ausgeführt, funktioniert: feste
  Session-ID, JSON-Ergebnis mit `result`, `session_id`, `total_cost_usd`; Wiederaufnahme mit
  erhaltenem Kontext). Das ist ein blockierender Aufruf, kein selbstständiger Worker. Taugt, wenn
  ein Orchestrator per Skript Blöcke nacheinander in eigenen Sessions laufen lassen will — dann
  ist die JSON-Ausgabe die Übergabe und `--resume` die Nacharbeit.
- **Agent Teams** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`): experimentell, siehe ADR-0014.

## Subagents im Worker

- Blockarbeiter und Tor sind Subagents des Workers. Jeder Aufruf startet mit frischem Kontext;
  zurück kommt nur die Schlussmeldung.
- **Verschachtelungstiefe:** laut Doku bis 3, in der geprüften Cloud-Umgebung
  `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`. Deshalb startet der **Worker** beide Subagents
  nacheinander — der Blockarbeiter startet das Tor nicht selbst.
- Plugin-Agents wirken erst nach `/reload-plugins` oder Neustart der Session.

## Kontext leeren

| Umgebung | Selbst leeren | Befund |
| --- | --- | --- |
| Subagent | immer — sein Kontext verfällt mit dem Ende | Grundlage des Verfahrens |
| Cloud-Session | nein, kein Werkzeug dafür; `/compact` verfügbar | geprüft 2026-09-26 |
| Claude Desktop | laut Auftraggeber ja | **ungeprüft**, siehe Prüfliste |
| CLI interaktiv | nur der Mensch mit `/clear` | Doku |

Eine per `SendMessage` empfangene Nachricht kommt als eingewickelte Nachricht an, nicht als
Befehl. Ein `/clear` im Nachrichtentext leert also nichts — das wäre sonst ein Weg, eine fremde
Session zu steuern.

## Nachrichten

- `SendMessage` an den **Namen**, den `ListAgents` zeigt. Die erste Zeile ist oft alles, was der
  Empfänger in der Vorschau sieht — deshalb das feste Nachrichtenformat in `SKILL.md`.
- Eine Session in einem anderen Rechtemodus hält eingehende Nachrichten zur Freigabe durch ihren
  Menschen zurück. Stille ist kein Einverständnis.
- `@datei` in einer Nachricht hängt beim Empfänger nichts an. Inhalte als Text schicken.
- Eine Cloud-Session empfängt, kann aber (Stand oben) nicht zurückschreiben.

## Prüfliste — noch ungeprüfte Stellen

Auf Claude Desktop abarbeiten, Ergebnis mit Datum und Version oben eintragen:

1. **Rückkanal:** Zwei Sessions öffnen (Orchestrator, Worker). Im Worker `ListAgents` — ist
   der Orchestrator gelistet? `SendMessage` mit erster Zeile `WORKER BEREIT test repo branch`.
   Kommt sie beim Orchestrator an, und kann er antworten?
2. **Selbst leeren:** Im Worker nach einem kleinen Block die Übergabe schicken und sich dann
   selbst leeren lassen. Ist der Kontext danach leer (Frage nach einem Detail des Blocks)? Ist
   die Session unter demselben Namen weiter per `SendMessage` erreichbar?
3. **Fremder Befehl:** Vom Orchestrator eine Nachricht mit Inhalt `/clear` an den Worker schicken.
   Erwartet: **wird nicht** als Befehl ausgeführt.
4. **Plugin-Agents im Worker:** Ist `project-foundation:orchestrate-blockarbeiter` im Worker
   aufrufbar? Kann der Worker danach `project-foundation:orchestrate-tor` starten?
5. **Hintergrundstart:** In einem vertrauten Repo `claude --bg "<kurzer Auftrag>"` ohne
   Rechte-Erweiterung. Startet er, erscheint er in `claude agents --json`, und ist er per
   `SendMessage` erreichbar?
6. **Cloud-Spawn mit Probeblock:** Einen Worker per `create_session` mit `source_url` und
   eigenem Branch starten, einen Block ausführen lassen, der eine Übergabe-Datei pusht. Liegt
   sie im Branch? Wurde der Startprompt als erster Turn verarbeitet?
