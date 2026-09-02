# CLAUDE.md — Projekt-Foundation

> Kurz gehalten: Regeln, Constraints, Commands, Stop-Conditions. Alles Erklärende steht in
> `docs/` und wird von hier nur verwiesen.

## Was ist das

Ein Toolkit (Claude-Code-Plugin + Python-CLI), das andere Projekte auf Implementierung
vorbereitet. Details: `docs/PROJECT.md`.

## Project Knowledge

| Frage | Datei |
| --- | --- |
| Was bauen wir? | `docs/PROJECT.md` |
| Wie ist es strukturiert? | `docs/ARCHITECTURE.md` |
| Warum wurde so entschieden? | `docs/decisions/` |
| Was gilt gerade? | `STATUS.md` |
| Wie starte ich es? | `README.md` |

## Commands

```bash
pip install -e ".[dev]"     # install
ruff format .               # format
ruff check .                # lint
mypy                        # typecheck
pytest                      # test
# build: n/a - kein Artefakt, siehe ADR-0006
```

Vor jedem Commit müssen `ruff format --check .`, `ruff check .`, `mypy` und `pytest`
grün sein.

## Regeln

- **Das Toolkit gilt für sich selbst.** Änderungen an diesem Repo folgen demselben
  Prozess, den der Skill vorschreibt.
- Genau eine Laufzeit-Abhängigkeit (`PyYAML`). Jede weitere braucht ein ADR (ADR-0003).
- Der Skill existiert nur unter `plugins/project-foundation/` — keine zweite Kopie
  unter `.claude/skills/` (ADR-0002).
- Der Validator **schreibt nie** in ein geprüftes Projekt. Reine Lesezugriffe.
- Der Validator behauptet nur, was er geprüft hat: `FOUNDATION VALID`, nie
  `FOUNDATION READY`; `NOT CHECKED` statt `OK` für Domänen ohne Regel; Secret-*Hygiene*
  statt Secret Scanning (ADR-0010).
- Pflicht ist ein Artefakt nur, wenn ohne es eine notwendige Frage unbeantwortet bliebe
  (ADR-0011). Keine neue Pflichtdatei ohne die Frage, die sie beantwortet.
- Neue Blocking-Regel im Validator = neuer Test, der genau diese Regel schützt. Keine
  Tests, die nur Coverage erzeugen. Erzwungen durch `tests/test_regelabdeckung.py` (ADR-0009).
- Finding-IDs sind stabil. Eine bestehende ID wird nicht umgewidmet. Jede neue ID gehört
  ins Register `FINDING_IDS`.
- `.project-foundation.yml` ist ein Index, nie die Source of Truth (ADR-0004).
- Deutscher Fließtext, englische Struktur-Keywords (ADR-0005).

## Constraints

- Python ≥ 3.11.
- Der Validator läuft ohne Netzwerkzugriff.
- Der Audit-Report-Wortlaut (Ebene 2, `reference/audit.md`) und der Validierungs-Report
  (Ebene 1, `report.py`) sind festgelegt und werden nicht umformuliert. Sie werden auch
  nicht gegeneinander ausgetauscht: kein Programm gibt `FOUNDATION READY` aus.

## Stop Conditions

Anhalten und fragen, wenn:

- Eine neue Prüfregel den Unterschied zwischen `BLOCKING` und `WARNING` verschieben würde.
- Ein Artefakt zur Pflicht würde, ohne dass eine Frage benannt ist, die es beantwortet.
- Eine Änderung das Manifest-Schema bricht (`schema_version`).
- Eine weitere Laufzeit-Abhängigkeit nötig erscheint.
- Die Plugin-Verzeichnisstruktur geändert werden müsste (ADR-0001).
- Eine Änderung dazu führen würde, dass der Validator schreibt statt nur liest.
