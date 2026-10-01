# ADR-0019: Die Agent-Vorlagen der Werkstatt dürfen `skills:` und `hooks` tragen

## Status

Accepted — 2026-10-01. Ergänzt ADR-0013.

## Context

ADR-0013 beschränkt das Frontmatter der Agents dieses Plugins auf `name`, `description`, `tools`,
`model`, `effort`, `isolation`; jedes weitere Feld ist eine Stop Condition in `CLAUDE.md`. Grund:
`hooks`, `mcpServers` und `permissionMode` sind für Plugin-Agents nicht zulässig, und ein Toolkit,
das sich selbst prüft, setzt keine Felder, die ignoriert werden.

Der Skill `project-werkstatt` (ADR-0018) liefert vier Agent-**Vorlagen**, die ins Zielprojekt nach
`.claude/agents/` kopiert werden — Projekt-Agents, keine Plugin-Agents. Das Muster beruht genau auf
zwei Feldern jenseits der Liste:

- **`skills:`** lädt den vollen Skill-Text beim Start des Subagents. Gate und Test-Autor brauchen
  ihr Handwerk immer; ein auslösender Skill streut.
- **`hooks`** im Frontmatter (`PostToolUse`, `Stop`, wobei `Stop` beim Subagent zu `SubagentStop`
  wird) erzwingen die Reihenfolge der Umsetzer-Kette und prüfen beim Gate, dass nichts geändert
  wurde. Ohne sie wäre die Kette ein Satz im Prompt.

Der Auftraggeber hat am 01.10.2026 entschieden, diese beiden Felder für die Vorlagen zuzulassen.

## Decision

1. **Für die Agent-Vorlagen unter `skills/project-werkstatt/templates/agents/` sind `skills:` und
   `hooks` erlaubt**, zusätzlich zu den Feldern aus ADR-0013. Sie stehen dort, weil die Quelle sie
   für die jeweilige Rolle belegt.
2. **Für die Agents des Plugins selbst (`plugins/project-foundation/agents/`) gilt ADR-0013
   unverändert.** Dort bleibt jedes weitere Feld eine Stop Condition.
3. **Weitere Felder in den Vorlagen** (`maxTurns`, `disallowedTools`, `permissionMode`, …) brauchen
   ein neues ADR. `maxTurns` steht in der Umsetzer-Vorlage nur als Kommentar mit „offen", weil sein
   Wert und seine Wirkung auf ein Stopp-Veto nicht gemessen sind.
4. Die Stop Condition in `CLAUDE.md` verweist auf dieses ADR.

Verworfene Alternativen:

- **Felder weglassen und die Kette im Prompt beschreiben.** Dann trägt kein Werkzeug die
  Reihenfolge — genau das Muster, gegen das die Werkstatt gebaut ist.
- **ADR-0013 allgemein lockern.** Für Plugin-Agents bleibt `hooks` unzulässig; eine allgemeine
  Lockerung würde Felder erlauben, die dort ignoriert werden.

## Consequences

**Positiv**

- Die Vorlagen tragen das Frontmatter, auf dem das Muster beruht; das Zielprojekt muss nichts
  ergänzen.

**Negativ**

- `claude plugin validate` prüft die Vorlagen nicht als Agents (sie liegen nicht unter `agents/`).
  Ob das Frontmatter im Zielprojekt greift, zeigen erst die Proben beim Aufsetzen
  (`templates/AUFSETZEN.md`).
- Frontmatter-Hooks laufen nur nach Workspace-Trust und nicht unter `claude -p`; die Vorlagen und
  `reference/prinzip.md` nennen das.

**Grenze**

Neu zu bewerten, wenn Plugin-Agents `hooks` unterstützen — dann könnten die Rollen ins Plugin
wandern — oder wenn eine weitere Vorlage ein Feld jenseits dieser Liste braucht.
