# Projekt-Foundation

Ein Toolkit, das beliebige Software-Projekte in einen Zustand bringt, in dem Menschen und
AI-Agents ohne Raten daran arbeiten können — mit dem kleinstmöglichen Satz an Dokumenten,
der dafür ausreicht.

> **NO CODING BEFORE FOUNDATION READY.**
> **The foundation must remain smaller than the system it enables.**

<details>
<summary><b>In English</b> — what this is, and a heads-up about the language</summary>

**The documentation in this repository is written in German.** Only the structural keywords
are English (`PASS` / `BLOCKED`, `Context` / `Decision` / `Consequences`, section names such
as `Purpose`, `Scope`, `MVP`) — a deliberate split, recorded in
[ADR-0005](docs/decisions/ADR-0005-dokumentationssprache.md): everything the validator reads
is English, everything a human reads is German.

**What it does.** Projekt-Foundation prepares a codebase for implementation — by humans or
AI agents — using the smallest set of documents that makes guessing unnecessary. It ships as:

- a **Claude Code skill** that walks an agent through
  `DISCOVER → ASSESS → ASK → DECIDE → GENERATE → VALIDATE → AUDIT`, with templates for every
  foundation file;
- a **CLI** (`foundation-validate <path>`) that checks a project for structure, missing
  decisions and contradictions, then prints an audit report. Exit code `0` means
  `FOUNDATION READY`, `1` means at least one blocker.

The validator only checks what is machine-decidable: file existence, structure, permitted
status values, and contradictions between the source-of-truth documents. **A green validator
is not a good foundation** — it only means no structural errors are left in the way.

The path convention is strict on purpose: a missing `docs/decisions/` is not satisfied by an
existing `docs/adr/`. The validator names the near miss in its message, but the finding stays
blocking — see [ADR-0008](docs/decisions/ADR-0008-strikte-pfade-mit-beinahe-treffern.md) for
the reasoning. Two projects with a green validator have the same structure; that is the point
of the tool.

Everything is read-only: the validator never writes into a project it inspects.

</details>

Es besteht aus zwei Teilen:

- **Skill `project-foundation`** — führt einen Agenten durch
  `DISCOVER → ASSESS → ASK → DECIDE → GENERATE → VALIDATE → AUDIT`, inklusive Vorlagen
  für alle Foundation-Dateien.
- **CLI `foundation-validate`** — prüft ein Projekt maschinell auf Struktur, fehlende
  Entscheidungen und Widersprüche und erzeugt den Audit-Report.

## Voraussetzungen

- Python ≥ 3.11 (nur für das CLI)
- Claude Code (nur für den Skill)

## Installation

### Skill in einem anderen Projekt

```bash
/plugin marketplace add Dimen2608/Projekt-Foundation
/plugin install project-foundation@projekt-foundation
```

Danach greift der Skill automatisch bei Anfragen wie „setz das Projekt auf",
„bau die Foundation" oder „ist das Repo bereit für Implementierung".

### CLI

```bash
git clone https://github.com/Dimen2608/Projekt-Foundation.git
cd Projekt-Foundation
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Nutzung

```bash
foundation-validate /pfad/zum/projekt
```

Ohne Installation:

```bash
python -m foundation_validate /pfad/zum/projekt
```

Exit-Codes:

| Code | Bedeutung |
| --- | --- |
| 0 | Keine Blocker — `FOUNDATION READY` |
| 1 | Mindestens ein Blocker — `FOUNDATION NOT READY` |
| 2 | Ungültiger Pfad |

Beispielausgabe:

```
╔══════════════════════════════════════╗
║       PROJECT FOUNDATION AUDIT       ║
╚══════════════════════════════════════╝

Project Definition       PASS
Architecture             PASS
...

Blocking Issues: 0
Warnings: 0

========================================

FOUNDATION READY

Implementation may begin.
```

Der Validator prüft ausschließlich, was maschinell entscheidbar ist: Existenz, Struktur,
erlaubte Statuswerte und Widersprüche zwischen den Source-of-Truth-Dateien. **Ein grüner
Validator ist keine gute Foundation** — er bedeutet nur, dass keine strukturellen Fehler
mehr im Weg stehen.

## Entwicklung

```bash
pip install -e ".[dev]"     # install
ruff format .               # format
ruff check .                # lint
mypy                        # typecheck
pytest                      # test
```

Es gibt keinen Build-Schritt — das Projekt erzeugt kein Artefakt (siehe ADR-0006).

## Aufbau

```
plugins/project-foundation/   Das Plugin: Skill, Reference, Vorlagen
src/foundation_validate/      Der Validator
examples/taskflow/            Ein vollständig ausgefülltes Beispielprojekt
docs/                         Foundation dieses Repos (Dogfooding)
```

## Dokumentation

| Frage | Datei |
| --- | --- |
| Was bauen wir? | `docs/PROJECT.md` |
| Wie ist es strukturiert? | `docs/ARCHITECTURE.md` |
| Warum wurde so entschieden? | `docs/decisions/` |
| Was gilt gerade? | `STATUS.md` |
| Was ist passiert? | `PROGRESS.md` |

## Lizenz

MIT
