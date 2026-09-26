# Mechanismen — was wo funktioniert

> Beantwortet: **Wie kommen Worker zum Orchestrator, und wie laufen Auftrag und Übergabe?**
> Diese Datei veraltet schneller als jede andere des Plugins. Jeder Befund trägt seine Quelle;
> in `SETUP` wird er **erneut festgestellt, nicht übernommen**.
>
> Stand: 2026-09-26, Claude Code 2.1.283. Quellen: code.claude.com/docs (`remote-control`,
> `cross-session-messaging`, `sub-agents`, `headless`, `agent-teams`) und Ausführung in einer
> Cloud-Session (ADR-0014). **Geprüft** heißt ausgeführt; **Doku** heißt nur gelesen.

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
| Claude Desktop | laut Auftraggeber per `SendMessage` erreichbar — **ungeprüft**, siehe Prüfliste |

**Der Orchestrator muss selbst verbunden sein.** Schreibt eine Session ohne Remote Control an
eine Session auf einem anderen Rechner, hat der Empfänger keine Antwortadresse. *(Doku)*

## Was eine Nachricht kann und was nicht

- **Adresse ist der Name**, den `ListAgents` zeigt. Doppelte Namen unterscheidet ein `[ref]`.
  Die erste Zeile ist oft alles, was der Empfänger in der Vorschau sieht — deshalb das feste
  Nachrichtenformat in `SKILL.md`. *(Doku)*
- **Befehle laufen nicht.** Ein `/clear` oder `/compact` im Text kommt als Text an. Eine Session
  kann eine andere nicht leeren. *(Doku)*
- **`@datei` hängt nichts an.** Inhalte als Text schicken. *(Doku)*
- **Keine Fertig-Meldung über Rechnergrenzen.** `notify_when_idle` gilt nur für Sessions auf
  demselben Rechner. Der Worker schickt die Übergabe deshalb selbst. *(Doku)*
- **Annahme beim Empfänger** (`crossSessionInbound`): Ohne Einstellung nimmt eine Session, die
  nach Rechten fragt, Nachrichten an — außer der Absender läuft mit `bypassPermissions`, dann
  hält sie sie zur Freigabe zurück. Eine Session mit `bypassPermissions` hält Nachrichten
  zurück, außer der Absender auch. `accept` / `hold` / `refuse` lassen sich fest einstellen —
  **das entscheidet der Mensch je Worker, nicht der Skill.** Stille ist kein Einverständnis:
  Eine zurückgehaltene Nachricht meldet sich beim Absender nicht. *(Doku)*

## Worker-Verfahren

| Verfahren | Wann | Befund |
| --- | --- | --- |
| **`attach`** (Standard) | Immer. Der Mensch öffnet im Ziel-Repo eine Session mit Remote Control und fügt den Startprompt ein; der Worker meldet sich mit `WORKER BEREIT`. | Grundform oben. |
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
| Session leert sich auf eigene Veranlassung (Claude Desktop) | laut Auftraggeber ja | **ungeprüft**, siehe Prüfliste |
| Cloud-Session | kein Werkzeug dafür; `/compact` verfügbar | geprüft |
| Fremde Session per Nachricht | nein — Befehle in Nachrichten laufen nicht | Doku |

## Prüfliste — noch ungeprüfte Stellen

Auf dem Rechner des Menschen abarbeiten, Ergebnis mit Datum und Version oben eintragen:

1. **Orchestrator erreichbar:** Orchestrator auf Claude Desktop oder mit `claude --rc` öffnen.
   Auf einem **zweiten Rechner** oder in einem anderen Repo einen Worker mit `claude --rc`. Zeigt
   `ListAgents` im Worker den Orchestrator, und umgekehrt?
2. **Rückkanal:** Worker schickt `WORKER BEREIT test <repo> <branch>`. Kommt sie an, kann der
   Orchestrator mit `BLOCK T1 AUFTRAG` antworten, kommt die Antwort an?
3. **Selbst leeren auf Desktop:** Im Worker nach einem kleinen Block die Übergabe schicken und
   sich selbst leeren lassen. Ist der Kontext danach leer (Frage nach einem Detail)? Ist die
   Session unter demselben Namen weiter erreichbar?
4. **Fremder Befehl:** Vom Orchestrator `/clear` als Nachricht schicken. Erwartet: wird **nicht**
   ausgeführt.
5. **Plugin-Agents im Worker:** `project-foundation:orchestrate-blockarbeiter` und danach
   `project-foundation:orchestrate-tor` aus dem Worker aufrufbar?
6. **Annahme ohne Rückfrage:** Laufen Orchestrator und Worker im selben Rechtemodus, kommt ein
   Auftrag ohne Freigabedialog an?
7. **`local_bg`** (nur falls gewünscht): In einem vertrauten Repo `claude --bg "<kurzer
   Auftrag>"` ohne Rechte-Erweiterung. Startet er, erscheint er in `claude agents --json`, ist er
   per `SendMessage` erreichbar?
