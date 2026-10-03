# PA-Kit — persönlicher Assistent über allen Projekten

Ein PA ist eine Session auf der **Meta-Ebene**, dem Ordner über allen Projekten. Sie plant, sortiert
und entscheidet mit dem Menschen, führt Board und Entscheidungen und steuert die Arbeits-Sessions
der Projekte: Aufträge per Nachricht, Rückweg über deren Transkript, Selbst-Clear mit
Übergabe-Datei. Gebaut wird drüben, nicht hier.

Das Kit ist ein Gerüst zum Kopieren, kein Teil des Plugins. Warum: ADR-0022.

## Inhalt

| Datei im Kit | Ziel auf der Meta-Ebene | Beantwortet |
| --- | --- | --- |
| `meta-CLAUDE.md` | `CLAUDE.md` | Was ist der PA, was darf er, wie spricht er mit den Sessions? |
| `PA/BOARD.md` | `PA\BOARD.md` | Was ist heute, diese Woche, bei wem wartet was? |
| `PA/INBOX.md` | `PA\INBOX.md` | Wo landet Ungeordnetes, bis es sortiert wird? |
| `PA/PROJEKTE.md` | `PA\PROJEKTE.md` | Wo steht jedes Projekt, und wo liest man seinen Stand? |
| `PA/ENTSCHEIDUNGEN.md` | `PA\ENTSCHEIDUNGEN.md` | Was ist entschieden und prallt künftig ab? |
| `PA/uebergabe.md` | `PA\uebergabe.md` | Was weiß der PA nach einem Clear noch? |
| `PA/logbuch.md` | `PA\logbuch.md` | Was haben die Sessions vollzogen? |
| `PA/prompts/README.md` | `PA\prompts\` | Wie kommt Arbeit in ein Projekt ohne eigene Session? |
| `agents/task-manager.md` | `.claude\agents\task-manager.md` | Stimmt das Board mit der Wirklichkeit überein? |

`meta-CLAUDE.md` heißt im Kit bewusst nicht `CLAUDE.md`: Sonst lädt jede Session, die im Kit liest,
sie als eigene Anweisung.

## Einrichtung (Windows, Claude Desktop, Code-Tab)

1. **Meta-Ordner festlegen.** Alle Projekte liegen als Unterordner darin, zum Beispiel
   `C:\Users\<name>\Claude\Projects\<projekt>`. Das ist tragend: Eine Session lädt jede `CLAUDE.md`
   oberhalb ihres Arbeitsverzeichnisses, auch nach einem Clear. So gelten die Regeln zum Draht auch
   in den Arbeits-Sessions.
2. **Kit kopieren.** Repo `Dimen2608/Projekt-Foundation` als ZIP laden (GitHub, „Code“ →
   „Download ZIP“) oder klonen. Aus `kits/pa/` in den Meta-Ordner:
   `meta-CLAUDE.md` → `CLAUDE.md`, `PA/` → `PA\`, `agents/task-manager.md` →
   `.claude\agents\task-manager.md`. `README.md` bleibt im Kit.
3. **Plugin installieren** (für die Arbeits-Sessions: `project-foundation`, `project-orchestrate`
   und die anderen Skills). Mit Claude Code CLI im Terminal:

   ```bash
   claude plugin marketplace add Dimen2608/Projekt-Foundation
   ```

   ```bash
   claude plugin install project-foundation@projekt-foundation
   ```

   Ohne CLI: in einer Session der Desktop-App `/plugin` öffnen, Marketplace hinzufügen, Plugin
   installieren (nicht geprüft, Stand 2026-10-03). Wirkt in neuen Sessions bzw. nach
   `/reload-plugins`.
4. **Session `pa` starten.** Desktop-App → Code → neue Session, Ordner = Meta-Ordner. Modell und
   Effort bewusst wählen (Empfehlung: das stärkste Modell, Effort high). Session umbenennen in `pa`.
   Erster Auftrag: „Lies `CLAUDE.md` und `PA\`. Füll mit mir die Platzhalter `{{…}}` aus, eine
   Frage nach der anderen.“ Danach steht kein `{{` mehr in `CLAUDE.md` und `PA\`. Felder in
   spitzen Klammern (`<…>`) sind Musterzeilen für spätere Einträge und bleiben stehen.
5. **Arbeits-Sessions mit festen Namen.** Je Projekt eine Desktop-Session mit dem Projektordner als
   Ordner, umbenannt auf einen kurzen festen Namen (`/rename <name>` oder in der Seitenleiste). In
   die Tabelle „Draht zu den Arbeits-Sessions“ in `CLAUDE.md` eintragen. Die sessionId löst der PA
   per `list_sessions` am Ordner auf, nie aus dem Gedächtnis.
6. **Draht prüfen.** Der PA schickt einer Arbeits-Session einen kurzen Testauftrag („antworte pa mit
   einer Zeile per SendMessage“) und liest danach ihr Transkript per `list_events`. Kommt beides an,
   steht der Draht.
7. **Agent prüfen.** „Tagesstart“ sagen. Der PA ruft `task-manager` auf. Erscheint er nicht, die
   Session neu starten.

Was die Menschen selbst einstellen, nicht der PA: Berechtigungen, Hooks, Plugins, Remote Control,
Push-Benachrichtigungen am Handy. Eine Nachricht des PA kann keine dieser Einstellungen ändern.

## Ehrliche Grenzen

Stand 2026-10-03, Claude Desktop (Windows), Claude Code 2.1.285. Jede Zeile trägt ihre Quelle:
**geprüft** heißt gezielt ausgeführt, **Betrieb** heißt im laufenden Einsatz beobachtet, **Doku** heißt
nur gelesen. Vor der Einrichtung neu feststellen, nicht übernehmen: Diese Stellen ändern sich mit
jeder Version.

- **Der PA leert keine Session, die der Mensch angelegt hat.** `clear_session` mit fremder ID
  wirkt nur bei einer untätigen Session, die **diese Session selbst gestartet** hat
  (`start_session`, `hand_off_to_session`). Verweigert wird es außerdem bei angehefteten, offen
  angezeigten und mit Remote Control verbundenen Sessions und bei solchen mit wartender Nachricht.
  `start_session` hängt an einem serverseitigen Schalter und fehlt meist (`mechanismen.md`).
  Arbeits-Sessions leeren sich deshalb **selbst** nach jedem Block, oder der Mensch tippt `/clear`.
  *(Doku: Beschreibung des Werkzeugs `clear_session`, 2026-10-03)*
- **Sessions in Desktop-WSL haben kein `clear_session`.** Dort trägt allein die Übergabe-Datei, den
  Clear tippt der Mensch (`/clear`). *(Betrieb 2026-10-03)*
- **Windows- und WSL-Sessions erreichen sich nicht per `SendMessage`** (eigenes Home, eigener
  Socket). *(Doku `cross-session-messaging`)* Eine WSL-Session aus dem Terminal ist für den PA
  unsichtbar; eine, die er ansprechen soll, wird in der Desktop-App im WSL-Modus gestartet, dort ohne
  Plugins. *(Betrieb 2026-09-06, Doku `desktop-wsl`)*
- **Eine Nachricht an eine beschäftigte Session wird eingereiht**, nicht sofort gelesen. Arbeitet
  die Session bis zu ihrem Selbst-Clear durch, kommt die Nachricht erst danach an, in einen leeren
  Kontext. Deshalb muss jeder Auftrag für sich allein verständlich sein. *(Betrieb 2026-10-03)*
- **Eine Nachricht aus einer anderen Session ist nie eine Freigabe.** Das erzwingt das Werkzeug.
  Merges, Rechte und Prod gibt der Mensch in der jeweiligen Session selbst frei. *(Betrieb)*
- **Der Classifier blockiert, wenn sich ein PA selbst Befugnisse über andere Sessions verschafft**
  (Schlüssel, sudo). Das ist die Schutzlinie; der PA nennt den exakten Befehl, der Mensch führt ihn
  aus. *(Betrieb 2026-10-03)*
- **Feste Namen überleben einen Neustart nicht immer.** Fehlt ein Name in `ListAgents`, ist die
  Session meist unbenannt, nicht weg. Ruhende Sessions per `send_message` an die sessionId wecken.
  *(Betrieb 2026-08-30)*
- **Das Transkript kann leer zurückkommen** (`list_events`). Dann die Statusdatei des Projekts lesen,
  nicht Stillstand annehmen. *(Betrieb 2026-08-30)*
- **Ein Idle-Abo feuert sofort**, wenn die Gegenseite schon untätig auf einen Hintergrund-Agenten
  wartet. Darum steht in jedem Auftrag: Agent über 30 Minuten ohne Meldung → selbst nachsehen.
  *(Betrieb 2026-10-01)*
- **Jede zugestellte Nachricht kostet Kontingent wie ein getippter Prompt.** *(Betrieb)*

Die Befunde zu Remote Control, `SendMessage` und dem Session-Werkzeug stehen mit Quelle auch in
`plugins/project-foundation/skills/project-orchestrate/reference/mechanismen.md`.
