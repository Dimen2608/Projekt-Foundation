# Status — Projekt-Foundation

> Source of Truth für **den aktuellen Zustand**. Keine Historie (`PROGRESS.md`),
> keine Pläne (`docs/PROJECT.md`), keine Architektur (`docs/ARCHITECTURE.md`).
>
> Stand: 2026-10-03

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
| Skill `project-werkstatt` | gebaut (0.10.0, ADR-0018 bis ADR-0021) mit dem Stand der Quelle vom 2026-10-03 (Werkstatt 100-5 und 100-6): Git-Ablauf und Definition of Done (`reference/git-und-dod.md`, Vorlage `LIVEGANG.md`), Ladewege und Regeldateien (`reference/regeldateien.md`, Vorlagen `wurzel-CLAUDE.md`, `rules/regeln.md`, `settings.json`), jeder Ladeweg Sperrpfad in Merge-Skript, CI und Deny-Regeln, ausformulierte Agent-Texte, fünf Hook-Skripte (`templates/hooks/`, 24 Proben ohne Modell, 0 Abweichungen), Gate-Marker v1, Skills als Plugin mit sieben Eval-Fällen, Mutationsprobe nach dem Bau; davor (0.9.0) Leitplanken, ASVS-Baseline, Isolation. **Offen**, markiert in `reference/prinzip.md`: Hooks mit echtem Payload, Sperr-Hooks der Leitplanken, Proben der Leitplanken und der Isolation, `maxTurns`, Übergabe der Testdateien aus dem Worktree, Fixture und Baseline der Evals, Stufe 2 der Katalogauswahl, Lizenzfrage der ASVS-CSV. Beschreibung seit 0.9.0 unverändert; Auslöse-Test zuletzt am 2026-10-02 mit geladenem Plugin 0.9.0 nach `/reload-plugins` (Sonnet-Subagent, reales Skill-Listing, 12 Sätze): 12 von 12 wie erwartet |
| Vorlagen (13 für Foundation, 7 für Rethink, 4 für Orchestrate, 25 Dateien und 7 Eval-Fälle für Werkstatt) | vollständig; Werkstatt mit offenen Stellen |
| Agents (`rethink-umsetzer`, `rethink-gutachter`, `rethink-zahlenpruefer`, `orchestrate-blockarbeiter`, `orchestrate-tor`) | vollständig; wirken nach `/reload-plugins` |
| Validator (`foundation_validate`) | vollständig, 45 mögliche Finding-IDs, Abdeckung erzwungen; seit 0.7.0 fremde ADR-Nummerierung und deutsche Gliederung gleichwertig (ADR-0017) |
| Plugin- und Marketplace-Manifest | vollständig |
| Beispielprojekt `examples/taskflow` | vollständig |
| PA-Kit `kits/pa/` (ADR-0022) | gebaut (9 Dateien: Meta-`CLAUDE.md`, 7 PA-Dateien, Agent `task-manager`; dazu Anleitung mit Grenzen, gemessen 2026-10-03). Kopiervorlage, nicht Teil des Plugins; ihre Befunde zu Clear und Nachrichten stehen seit 0.10.1 auch in `mechanismen.md`. **Offen:** Einrichtung an einem zweiten Rechner nicht geprobt; Weg der Plugin-Installation ohne CLI in der Desktop-App nicht geprüft |
| Foundation dieses Repos | vollständig |
