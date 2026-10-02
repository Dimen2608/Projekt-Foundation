# Status — Projekt-Foundation

> Source of Truth für **den aktuellen Zustand**. Keine Historie (`PROGRESS.md`),
> keine Pläne (`docs/PROJECT.md`), keine Architektur (`docs/ARCHITECTURE.md`).
>
> Stand: 2026-10-02

## Foundation

**FOUNDATION READY** — Review durchgeführt, `foundation-validate .` meldet
`FOUNDATION VALID`.

| Domain | Status |
| --- | --- |
| Project Definition | PASS |
| Architecture | PASS |
| Development Setup | PASS |
| AI Foundation | PASS |
| Documentation | PASS |
| Testing & Quality | PASS |
| CI/CD & Infrastructure | PASS |
| Security | PASS |

Blockers: 0
Warnings: 0

## Blocker

Keine.

## Warnungen

Keine.

## Command-Chain

| Command | Zustand | Zuletzt geprüft |
| --- | --- | --- |
| install (`pip install -e ".[dev]"`) | ok | 2026-09-01 |
| format (`ruff format --check .`) | ok | 2026-10-02 |
| lint (`ruff check .`) | ok | 2026-10-02 |
| typecheck (`mypy`) | ok | 2026-10-02 |
| test (`pytest`) | ok — 58 Tests | 2026-10-02 |
| build | n/a — kein Artefakt (ADR-0006) | — |

## Foundation-Validierung

`foundation-validate .` und `foundation-validate examples/taskflow` laufen beide ohne
Blocker durch. Das Toolkit prüft sich selbst.

## Implementierungsstand

| Bestandteil | Zustand |
| --- | --- |
| Skill `project-foundation` | vollständig; seit 0.6.0 mit Werkzeug-Abdeckung im Review (ADR-0016) |
| Skill `project-rethink` | vollständig (0.4.0, ADR-0013); `claude plugin validate --strict` grün, Auslöse-Test beider Skills bestanden am 2026-09-11 |
| Skill `project-orchestrate` | vollständig (0.5.3, ADR-0014, ADR-0015; SETUP Schritt 6 nutzt seit 0.6.0 die Werkzeug-Abdeckung); `claude plugin validate --strict` grün, Auslöse-Test aller drei Skills bestanden am 2026-09-26. Selbst-Leeren und Start per Chip auf Claude Desktop geprüft (ADR-0015). **Offen:** Prüfliste in `reference/mechanismen.md` (Rückkanal Worker → Orchestrator über Rechnergrenzen, `/clear` als Nachrichtentext, Plugin-Agents im Worker, optional `claude --bg`). `start_session` hängt an einem serverseitigen Feature-Flag (mechanismen.md) |
| Skill `project-werkstatt` | gebaut (0.9.0, ADR-0018, ADR-0019, ADR-0020) mit dem Stand vom 2026-10-02: Leitplanken (`reference/leitplanken.md`, Vorlage `LEITPLANKEN.md`), ASVS-Baseline mit Level-Wahl und Inseln (`reference/asvs-baseline.md`, Skill `sicherheits-katalog` gefüllt, Vorlagen unter `sicherheit/`), Isolation je Worktree (`reference/isolation.md`, Skizze `dev-env.py`), Arbeitskopie-Abgleich im Merge-Skript. **Offen**, markiert in `reference/prinzip.md`: Definition of Done und Git-Ablauf, ausformulierte Agent-Texte, Hook-Skripte, Gate-Marker-Format, Proben der Leitplanken und der Isolation, Stufe 2 der Katalogauswahl, Lizenzfrage der ASVS-CSV. Auslöse-Test am 2026-10-02 bestanden (Sonnet-Subagent, vier Beschreibungen als Skill-Listing, 12 Sätze): Vorbereitung → `project-foundation`, Doku-Drift → `project-rethink`, Verteilen → `project-orchestrate`; Merge ohne Freigabe, blockierender zweiter Agent, Deny-Regeln außerhalb des Repos, ASVS-Level für die Bau-Session, Dev-DB je Worktree → `project-werkstatt`; Tippfehler, einfache CI, PR-Sicherheitsprüfung, Unit-Test → keiner. Wiederholt am 2026-10-02 mit geladenem Plugin 0.9.0 nach `/reload-plugins` (Sonnet-Subagent, reales Skill-Listing mit allen vier Skills, 12 Sätze je Kategorie neu formuliert): 12 von 12 wie erwartet; die PR-Sicherheitsprüfung geht dort an den eingebauten Skill `security-review`, an keinen Plugin-Skill |
| Vorlagen (13 für Foundation, 7 für Rethink, 4 für Orchestrate, 15 für Werkstatt) | vollständig; Werkstatt mit offenen Stellen |
| Agents (`rethink-umsetzer`, `rethink-gutachter`, `rethink-zahlenpruefer`, `orchestrate-blockarbeiter`, `orchestrate-tor`) | vollständig; wirken nach `/reload-plugins` |
| Validator (`foundation_validate`) | vollständig, 45 mögliche Finding-IDs, Abdeckung erzwungen; seit 0.7.0 fremde ADR-Nummerierung und deutsche Gliederung gleichwertig (ADR-0017) |
| Plugin- und Marketplace-Manifest | vollständig |
| Beispielprojekt `examples/taskflow` | vollständig |
| Foundation dieses Repos | vollständig |
