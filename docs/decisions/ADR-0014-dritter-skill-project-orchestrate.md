# ADR-0014: Ein dritter Skill `project-orchestrate` — eine Hauptsession steuert Worker-Sessions in Blöcken

## Status

Accepted — 2026-09-26

## Context

Nach `FOUNDATION READY` beginnt die Implementierung. Bei größeren Vorhaben — mehrere Repos,
mehrere unabhängige Arbeitspakete — läuft eine einzelne Session in zwei Grenzen: Ihr Kontext
wächst mit jedem Paket, bis frühe Entscheidungen verdrängt sind, und sie arbeitet streng
nacheinander. Gewünscht ist ein **Orchestrator**: eine Hauptsession, die andere Sessions steuert
und wenn möglich selbst startet, Aufgaben immer als **Blöcke** vergibt, am Ende jedes Blocks eine
**Übergabe** entgegennimmt, nach der die Unter-Session ihren Kontext leert.

Vor der Entscheidung wurde am 2026-09-26 geprüft, was Claude Code heute kann — in der
Dokumentation (code.claude.com/docs: `sub-agents`, `agent-teams`, `headless`, `agent-sdk/sessions`,
`worktrees`, `workflows`, `cross-session-messaging`, `claude-code-on-the-web`,
`plugins/components`) und durch Ausführen in einer Cloud-Session mit Claude Code 2.1.283. Die
Befunde stehen einzeln in `reference/mechanismen.md` des Skills; die tragenden sind:

| Mechanismus | Befund |
| --- | --- |
| Subagent (Agent-Tool, Plugin-Agents) | GA, frischer Kontext je Aufruf, Rückgabe ist die Schlussmeldung. Verschachtelung laut Doku bis Tiefe 3, in der geprüften Cloud-Umgebung auf 1 gesetzt (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`). |
| Headless `claude -p --session-id` / `--resume` | Ausgeführt: Start mit fester ID, JSON-Rückgabe, Wiederaufnahme mit erhaltenem Kontext. |
| Hintergrund `claude --bg`, `claude agents --json` | Vorhanden. Scheiterte im Scratchpad am fehlenden Workspace-Vertrauen; mit `bypassPermissions` vom Auto-Mode-Klassifikator abgelehnt. |
| Cloud-Session per Remote-API (`create_session`, `get_session`, `archive_session`) | Ausgeführt: Start, Status, Archivierung. Die Antwort der Kind-Session ist vom Starter aus **nicht lesbar**, nur Status und Kurzzusammenfassung. |
| `SendMessage` / `ListAgents` zwischen Sessions | Lokal und über Remote Control in beide Richtungen. Eine Cloud-Session empfängt, kann laut Doku aber noch nicht zurückschreiben. |
| Agent Teams | Experimentell, per Umgebungsvariable. |
| Kontext leeren | Kein Werkzeug, mit dem eine Session sich in der Cloud selbst leert. Auf Claude Desktop nach Angabe des Auftraggebers möglich — hier ungeprüft. Ein Subagent-Kontext verfällt beim Ende immer. |

Die Entscheidungen fielen in einem Interview mit dem Auftraggeber, Frage für Frage, je mit
Empfehlung.

## Decision

**1. Dritter Skill im selben Plugin**, unter `plugins/project-foundation/skills/project-orchestrate/`,
Phasen `SETUP → PLAN → DISPATCH → GATE → INTEGRATE`. Er setzt dort an, wo `project-foundation`
endet. ADR-0002 gilt: genau eine Kopie, unter `plugins/`.

**2. Die Unter-Session ist eine eigenständige Session**, genannt **Worker** — keine Subagent-Rolle.
Sie kann selbst Subagents starten. Ein Worker lebt über mehrere Blöcke; **die eigentliche
Blockarbeit läuft in einem Subagent**, dessen Kontext mit seinem Ende verfällt. Das ist das
Leeren, das überall funktioniert. Wo die Umgebung einer Session erlaubt, sich selbst zu leeren,
tut der Worker das nach der Übergabe zusätzlich; wo nicht, genügt `/compact` bei Bedarf.

**3. Worker-Start in fester Stufenfolge**, das erste verfügbare Verfahren gilt: Cloud-Spawn per
Remote-API → lokaler Hintergrundstart (`claude --bg`) → **Handstart**. Für den Handstart erzeugt
der Skill einen Startprompt (`WORKER-START.md`); der Worker meldet sich per `SendMessage` mit
Name, Repo und Branch. Nie `bypassPermissions`; ein Worker erbt höchstens die Rechte des
Orchestrators.

**4. Heimat-Repo plus fremde Repos.** Der Orchestrator lebt in einem Repo; dort liegen
Konfiguration, Blockplan und alle Blockdateien unter `orchestrate/` und werden **committet** — der
Stand überlebt jedes Leeren des Orchestrators, die Git-Historie ist das Protokoll. Worker arbeiten
im Heimat-Repo oder in fremden Repos, jeder auf einem eigenen Branch.

**5. Übergabe: Die Nachricht ist Transport, die Datei ist die Wahrheit.** Der Worker schickt die
vollständige Übergabe per `SendMessage`; der Orchestrator schreibt sie in die Blockdatei. Wo kein
Rückkanal besteht (Cloud-Worker), legt der Worker dieselbe Übergabe als Datei in seinem Branch ab,
und der Orchestrator holt sie dort. Worker brauchen so kein Schreibrecht auf das Heimat-Repo.

**6. Rollen.** Der Orchestrator **baut nicht** — kein Produktcode, keine Änderung in einem
Arbeitsrepo; er schreibt nur unter `orchestrate/`. Das ist `the head level does not build` aus
ADR-0013, übertragen. Jeder Block geht durch ein **Tor**, bevor er als erledigt gilt.

**7. Zwei neue Agents**, registriert als `project-foundation:orchestrate-blockarbeiter` und
`project-foundation:orchestrate-tor`. Frontmatter nur mit den Feldern, die ADR-0013 zulässt;
`background` und `maxTurns`, die die Doku kennt, bleiben außen vor.

| Rolle | Modell / Effort | Werkzeuge | Warum |
| --- | --- | --- | --- |
| Blockarbeiter | `sonnet` / `high` | Read, Write, Edit, Grep, Glob, Bash, Skill | Führt genau einen Block aus, in frischem Kontext; `Skill`, weil der Block den passenden Skill benennt. |
| Tor | `opus` / `high` | Read, Grep, Glob, Bash; `isolation: worktree` | Wie der Rethink-Gutachter die Rolle, die den Fehler findet, den niemand vermutet hat. Lesend; die Sperre ist begrenzt, nicht erzwungen, weil `Bash` bleibt. |

Das Tor läuft **in der Worker-Session**, direkt nach dem Blockarbeiter: Dort liegt der Checkout
jedes fremden Repos, und der Orchestrator-Kontext bleibt klein. Unabhängig ist es trotzdem — es
ist ein frischer Subagent, bekommt Auftrag und Diff, nicht die Begründung des Blockarbeiters. Der
Orchestrator nimmt nur eine Übergabe mit Tor-Urteil `Freigabe: ja` und ausgeführten
Abnahmebefehlen ab. Der Rethink-Gutachter wird nicht wiederverwendet: Sein Maßstab (Messstand,
Masken, Bereichsdateien) passt nicht auf Bau-Blöcke.

**8. Eskalation.** Fragen eines Workers gehen an den Orchestrator, nie direkt an den Menschen. Der
Orchestrator beantwortet sie, wenn Dokumentation oder ADR des Zielprojekts es entscheiden, sonst
fragt er den Menschen. Stop Conditions eines Zielprojekts entscheidet er nie. Das Tor hat
**höchstens fünf Runden** je Block; danach legt der Orchestrator dem Menschen „weiter oder nicht"
mit Pro und Contra vor, oder der Mensch entscheidet anders. (Der Rethink-Gutachter bleibt bei
zwei Runden — Spezifikationsdateien und Bau-Blöcke sind verschiedene Gegenstände.)

**9. Parallelität mit Regeln.** Der Blockplan führt je Block „hängt ab von" und „Repo/Branch".
Parallel laufen nur Blöcke, deren Abhängigkeiten erledigt sind; nie zwei Worker auf demselben
Branch.

**10. Ein Block hat sechs Pflichtfelder:** Ziel (ein Satz), Repo/Branch, Eingang, Umfangsgrenze,
Abnahmekriterium (prüfbar), zuständiger Skill oder Agent. Ohne Abnahmekriterium wird kein Block
vergeben — das Tor hätte nichts, woran es prüft. Ein Block muss in den Kontext eines Subagents
passen, sonst wird er geteilt.

**11. Zusammenführung konfigurierbar.** `merge_mode: human` (Standard): Nach dem Tor wird der
Draft-PR des Workers „ready for review", der Mensch mergt. `merge_mode: orchestrator`: Bei Tor-Ja
und grüner CI mergt der Orchestrator selbst.

**12. Installer als erste Phase `SETUP`**, ein geführtes Interview, wiederholbar. Es fragt
Heimat-Repo, weitere Repos, Merge-Modus und Worker-Verfahren ab, prüft vorhandene Agents und
Skills, ordnet sie Aufgabenarten zu, sucht fehlende im Marketplace und **schlägt sie einzeln zur
Installation vor** — installiert wird nur, was der Mensch bestätigt. Ein Python-Installer ist
verworfen: Skills und Plugins suchen und installieren geht nur mit Werkzeugen einer Session.
Ergebnis ist `orchestrate/ORCHESTRATE.md` mit einem YAML-Block am Anfang und deutschem Fließtext.

**13. Voraussetzung je Repo: `FOUNDATION VALID`.** `SETUP` führt `foundation-validate` in jedem
eingebundenen Repo aus. Ohne `VALID` ist der erste Block dieses Repos `project-foundation` —
oder `project-rethink`, wenn der Ist-Zustand nicht beschreibbar ist. Erst danach Bau-Blöcke. Das
ist FR-1 (`no feature work on an unresolved foundation`), angewendet auf jeden Worker, der mit
frischem Kontext nichts hat als die Foundation des Repos.

**14. Keine Validator-Änderung.** `ORCHESTRATE.md`, `BLOCKPLAN.md` und die Blockdateien werden
keine Pflichtstellen: Die Fragen, die sie beantworten, stellt nur ein Projekt, das orchestriert.
Keine neue Finding-ID, `schema_version` bleibt `1`, `.project-foundation.yml` bleibt unberührt
(ADR-0004). Kein Test nach ADR-0009: Ein Skill ist Prompt-Material.

**15. Umfang nach ADR-0011.** Vier Vorlagen, jede gegen ihre Frage:

| Frage | Vorlage |
| --- | --- |
| Welche Repos, wer mergt, wie starten Worker, welcher Skill oder Agent für welche Aufgabenart? | `ORCHESTRATE.md` |
| Welche Blöcke gibt es, in welchem Zustand, wer arbeitet woran, was hängt wovon ab? | `BLOCKPLAN.md` |
| Was genau ist der Auftrag eines Blocks, was wurde übergeben, was sagt das Tor? | `BLOCK.md` |
| Wie wird eine von Hand gestartete Session zum Worker? | `WORKER-START.md` |

Dazu `reference/mechanismen.md`: welcher Start- und Rückkanal wo funktioniert, mit Datum und
Version des Befunds, und die Prüfliste für die noch ungeprüften Stellen (Desktop). Auftrag,
Übergabe und Tor-Urteil stehen in **einer** Blockdatei statt in drei: Wer einen Block nachliest,
braucht alle drei.

**16. Abgrenzung zu `Out of Scope`.** `docs/PROJECT.md` schließt Projektmanagement, Ticketing,
Roadmaps, Zeitschätzung und Code-Generierung für Zielprojekte aus. Der Orchestrator schätzt keine
Termine, führt keine Roadmap und kein Ticketsystem, und er erzeugt selbst keinen Code — er steuert
die Ausführung durch Sessions, deren Code von den Skills des Zielprojekts kommt. Der Blockplan ist
ein Ausführungsvertrag wie `ABLAUF.md` in Rethink, keine Planung auf Zeit. Wird aus dem
Blockplan ein Backlog mit Prioritäten und Terminen, ist diese Grenze überschritten.

**17. Abgrenzung der Trigger** allein in der `description` von `project-orchestrate`: Sie zieht
bei „mehrere Sessions steuern", nicht bei „Projekt vorbereiten". Die Beschreibungen der beiden
anderen Skills bleiben unverändert, weil sich ihre Trigger nicht überschneiden — Foundation und
Rethink bereiten vor, Orchestrate führt aus. Der Auslöse-Test bekommt einen dritten Satz.

Verworfene Alternativen:

- **Agent Teams als Grundlage.** Passt vom Konzept, ist aber experimentell; ein Toolkit, das sich
  selbst prüft, baut nicht auf einer Umgebungsvariable mit ungewisser Zukunft.
- **Nur Subagents in einer Session.** Stabil und überall verfügbar, aber keine eigenständigen
  Sessions — und in der geprüften Cloud-Umgebung könnte ein Subagent keine weiteren starten.
- **Eine neue Session je Block.** Das sauberste Leeren, aber abhängig vom Spawnen; im Handstart
  müsste der Mensch je Block eine Session öffnen.
- **Übergabe nur im Chat.** Geht beim Leeren des Orchestrators verloren und fehlt in der Cloud ganz.
- **Konfiguration in `.project-foundation.yml`.** Schema-Änderung, Stop Condition, gegen ADR-0004.
- **Teil von `project-rethink`.** Beide arbeiten in Blöcken mit Tor, aber mit anderem Zweck;
  vermischt ergäbe das einen Skill mit zwei Eingängen.

## Consequences

**Positiv**

- Größere Vorhaben lassen sich nach der Foundation in Blöcken über mehrere Sessions und Repos
  ausführen, ohne dass der Kontext einer Session mitwächst.
- Jeder Block ist nachlesbar: Auftrag, Übergabe und Tor in einer committeten Datei.
- Validator, Finding-IDs und Manifest-Schema bleiben unberührt.

**Negativ**

- Der Skill hängt an Werkzeugen, die je Umgebung verschieden sind (Remote-API nur in der Cloud,
  `SendMessage`-Rückweg nicht aus der Cloud). Die Stufenfolge fängt das ab, aber `mechanismen.md`
  veraltet schneller als jede andere Datei des Plugins. Sie trägt deshalb Datum und Version.
- Das Selbst-Leeren auf Claude Desktop ist nicht von hier aus geprüft. Bis die Prüfliste
  abgearbeitet ist, gilt es als optional.
- Das Plugin trägt jetzt Prompt-Material für drei Prozesse und fünf Agents. Der Leitsatz *the
  foundation must remain smaller than the system it enables* gilt auch hier: Orchestrate lohnt
  sich erst ab mehreren Blöcken; für einen Block ist eine Session genug.

**Grenze**

Neu zu bewerten, wenn Agent Teams GA werden oder eine Cloud-Session zurückschreiben kann — dann
vereinfacht sich die Stufenfolge. Und wenn der Blockplan anfängt, Termine zu tragen: Dann ist
der Skill Projektmanagement geworden.
