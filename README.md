# Projekt-Foundation

Ein Toolkit, das beliebige Software-Projekte in einen Zustand bringt, in dem Menschen und
AI-Agents ohne Raten daran arbeiten können — mit dem kleinstmöglichen Satz an Dokumenten,
der dafür ausreicht.

> **NO FEATURE WORK ON AN UNRESOLVED FOUNDATION.**
> **The foundation must remain smaller than the system it enables.**

<details>
<summary><b>In English</b> — what this is, and a heads-up about the language</summary>

**The documentation in this repository is written in German.** Only the structural keywords
are English (`PASS` / `BLOCKED`, `Context` / `Decision` / `Consequences`, section names such
as `Purpose`, `Scope`, `MVP`) — a deliberate split, recorded in
[ADR-0005](docs/decisions/ADR-0005-dokumentationssprache.md): everything the validator reads
is English, everything a human reads is German.

**What it does.** Projekt-Foundation prepares a codebase for implementation — by humans or
AI agents — using the smallest set of documents that makes guessing unnecessary. It is an
AI-assisted development foundation, currently optimized for **Claude Code** and **Cursor**;
`AGENTS.md` covers other tools as a shared context file. It ships as:

- a **Claude Code skill** that walks an agent through
  `DISCOVER → ASSESS → ASK → DECIDE → GENERATE → VALIDATE → AUDIT`, with templates for every
  foundation file;
- a **CLI** (`foundation-validate <path>`) that checks a project for structure, missing
  answers and contradictions. Exit code `0` means `FOUNDATION VALID`, `1` means at least
  one structural blocker.

The validator only checks what is machine-decidable: file existence, structure, permitted
status values, and contradictions between the source-of-truth documents. It therefore says
`FOUNDATION VALID`, never `FOUNDATION READY` — that verdict is the result of the full
process: machine validation, then a qualitative review, then the human decisions that
neither of those can make.

Which files a project needs follows from the questions it must answer, not from a fixed
list: an ADR is required only when a load-bearing decision exists, and `STATUS.md` only
when the current state is not otherwise visible.

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
| 0 | Keine strukturellen Blocker — `FOUNDATION VALID` |
| 1 | Mindestens ein struktureller Blocker — `FOUNDATION INVALID` |
| 2 | Ungültiger Pfad |

Beispielausgabe:

```
╔══════════════════════════════════════╗
║    PROJECT FOUNDATION VALIDATION     ║
╚══════════════════════════════════════╝

Project Definition       OK
Architecture             OK
Development Setup        NOT CHECKED
...

OK = no structural finding. NOT CHECKED = no machine-checkable rule here.

Blocking Issues: 0
Warnings: 0

========================================

FOUNDATION VALID
```

## Drei Ebenen

Der Validator ist Ebene 1: Existenz, Struktur, erlaubte Statuswerte, Widersprüche. Ebene 2
ist das inhaltliche Review durch den Skill, Ebene 3 der Mensch mit den Entscheidungen, die
keine Maschine treffen darf. `FOUNDATION READY` ist das Ergebnis aller drei — **nie die
Ausgabe eines Programms** (ADR-0010). Die Ebenen im Einzelnen definiert der Skill
(`plugins/project-foundation/skills/project-foundation/SKILL.md`).

Was der Validator ausdrücklich **nicht** kann:

- beurteilen, ob Architektur, Scope oder Teststrategie taugen;
- erkennen, ob ein Dokument inhaltlich stimmt oder nur ausgefüllt aussieht;
- zusichern, dass ein Projekt frei von Secrets ist. Er prüft Secret-*Hygiene*
  (`.env` nicht committet, `.env` in `.gitignore`). Wer die Zusicherung braucht, nutzt
  GitHub Secret Scanning oder `gitleaks`.

## Welche Dateien ein Projekt braucht

Nicht jedes Projekt braucht denselben Satz. Pflicht ist ein Artefakt, wenn ohne es eine
notwendige Frage unbeantwortet bliebe (ADR-0011):

| Frage | Artefakt | Wann |
| --- | --- | --- |
| Wie starte und benutze ich es? | `README.md` | immer |
| Was bauen wir, was nicht? | `docs/PROJECT.md` | immer |
| Wie ist es strukturiert? | `docs/ARCHITECTURE.md` | immer |
| Woran erkennt ein Werkzeug die Foundation? | `.project-foundation.yml` | immer |
| Was muss ein AI-Agent wissen? | `CLAUDE.md` oder `AGENTS.md` | immer |
| Warum wurde so entschieden? | `docs/decisions/` | nur bei tragender Entscheidung |
| Was gilt gerade? | `STATUS.md` | wenn der Zustand nicht ohnehin sichtbar ist |

Ob ADRs nötig sind, beantwortet das Projekt selbst — mit einer Zeile
`Architecture Decisions | REQUIRED` oder `NOT REQUIRED` in `docs/ARCHITECTURE.md`.

## Wann Implementierung blockiert ist

Nicht pauschal. **Foundation Work** (Dokumente, ADRs, Aufräumen) ist immer erlaubt,
**Bugfixes** sind erlaubt, sobald Scope und Kontext klar sind — nur **Feature-Arbeit**
wartet auf `FOUNDATION READY`. Die Regel richtet sich gegen Architekturentscheidungen,
die stillschweigend durch Code getroffen werden, nicht gegen einen Einzeiler-Fix.

## AI-Unterstützung

Ausgelegt auf **Claude Code** (Skill, `CLAUDE.md`) und **Cursor** (`.cursor/rules/`),
plus `AGENTS.md` als werkzeugübergreifende Datei. Kein universelles Agent-System — was
darüber hinaus geht, müsste ein anderes Projekt bauen.

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
