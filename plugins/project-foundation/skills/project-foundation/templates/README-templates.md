# Vorlagen

Ausgangspunkte für die GENERATE-Phase. Kopieren, dann **vollständig ausfüllen**.

Eine Vorlage mit stehengebliebenen `<Platzhaltern>` ist keine Foundation — sie sieht nur
so aus. Der Validator erkennt fehlende Abschnitte, aber nicht leere.

| Vorlage | Ziel im Projekt |
| --- | --- |
| `PROJECT.md` | `docs/PROJECT.md` |
| `ARCHITECTURE.md` | `docs/ARCHITECTURE.md` |
| `ADR.md` | `docs/decisions/ADR-NNNN-titel.md` |
| `STATUS.md` | `STATUS.md` |
| `PROGRESS.md` | `PROGRESS.md` (optional) |
| `CLAUDE.md` | `CLAUDE.md` |
| `AGENTS.md` | `AGENTS.md` (optional) |
| `cursor-rule.mdc` | `.cursor/rules/<name>.mdc` (optional) |
| `README.md` | `README.md` |
| `SECURITY.md` | `SECURITY.md` (optional) |
| `env.example` | `.env.example` (nur bei Environment-Variablen) |
| `project-foundation.yml` | `.project-foundation.yml` |
| `ci-github-actions.yml` | `.github/workflows/ci.yml` (optional) |

Optionale Vorlagen nur verwenden, wenn sie einen konkreten Zweck erfüllen.
Ein ausgefülltes Gesamtbeispiel steht unter `examples/` im Toolkit-Repository.
