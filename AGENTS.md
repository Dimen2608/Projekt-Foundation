# AGENTS.md — Projekt-Foundation

> Gemeinsamer Kontext für alle Agent-Werkzeuge. Werkzeugspezifisches gehört nicht hierher:
> Claude-Regeln in `CLAUDE.md`, Cursor-Regeln in `.cursor/rules/`.

## Projekt

Ein Toolkit, das andere Projekte auf Implementierung vorbereitet — bestehend aus einem
Claude-Code-Skill mit Vorlagen und einem Python-CLI, das die Foundation maschinell prüft.
Details: `docs/PROJECT.md`.

## Aufbau

```
plugins/project-foundation/   Plugin: Skill (Prozesswissen), reference/, templates/
src/foundation_validate/      CLI-Validator (cli, report, validator, model)
tests/                        Ein Test je Blocking-Regel + CLI-Schnittstelle
docs/                         Foundation dieses Repos
examples/taskflow/            Vollständig ausgefülltes Beispielprojekt
```

Details: `docs/ARCHITECTURE.md`.

## Commands

```bash
pip install -e ".[dev]"
ruff format . && ruff check .
mypy
pytest
```

## Konventionen

- Deutscher Fließtext, englische Struktur-Keywords (`PASS`, `BLOCKED`, `RELEVANT`, …).
- Docstrings deutsch, Bezeichner englisch.
- Finding-IDs nach Muster `BEREICH-NNN` und stabil über Versionen hinweg.
- ADR-Dateien: `docs/decisions/ADR-NNNN-kleingeschriebener-titel.md`.

## Grenzen

- Keine tragende Entscheidung ohne ADR in `docs/decisions/`.
- Keine Secrets im Repository.
- Der Validator verändert geprüfte Projekte nicht.
- Bei Unklarheit: fragen, nicht raten.
