# Architektur — Projekt-Foundation

> Source of Truth für **wie** das System strukturiert ist. Das *Warum* einzelner
> Entscheidungen steht in `docs/decisions/`.

## Bereichsbewertung

Jeder Bereich ist bewertet mit `RELEVANT`, `NOT REQUIRED`, `FUTURE` oder `UNKNOWN`.
`UNKNOWN` bei Authentication, Authorization oder Secrets ist ein Blocker.

| Bereich | Bewertung | Begründung |
| --- | --- | --- |
| Application Architecture | RELEVANT | Skill + Vorlagen + CLI-Validator, siehe unten. |
| Frontend | NOT REQUIRED | Kein UI. Bedienung über Agent und Terminal. |
| Backend | NOT REQUIRED | Kein Server, kein Dienst. |
| Database | NOT REQUIRED | Kein persistenter Zustand über den Lauf hinaus. |
| Data Model | NOT REQUIRED | Nur In-Memory-Datentypen (`Finding`, `Result`). |
| Authentication | NOT REQUIRED | Lokales CLI ohne Nutzerkonzept. |
| Authorization | NOT REQUIRED | Rechte sind die des ausführenden Betriebssystem-Nutzers. |
| APIs | NOT REQUIRED | Keine Netzwerk-API. Die öffentliche Schnittstelle ist das CLI. |
| External Services | NOT REQUIRED | Keine externen Aufrufe zur Laufzeit. |
| Deployment | RELEVANT | Verteilung als Claude-Code-Plugin, siehe ADR-0001. |
| Security | RELEVANT | Secret-Hygiene in fremden Projekten (`.env`), kein Secret Scanning — und der Validator schreibt dort nie. |
| Configuration | RELEVANT | `.project-foundation.yml` im Zielprojekt. |
| Secrets | NOT REQUIRED | Das Toolkit selbst braucht keine Secrets. |
| Architecture Decisions | REQUIRED | Verteilung, Sprache, Manifest-Rolle und Report-Wortlaut sind tragende Entscheidungen — ADR-0001 bis ADR-0011. |
| Storage | NOT REQUIRED | Nur Dateisystem-Lesezugriffe im Zielprojekt. |
| Background Jobs | NOT REQUIRED | Ein Lauf ist synchron und in Millisekunden fertig. |
| Messaging / Events | NOT REQUIRED | Kein verteiltes System. |
| Caching | NOT REQUIRED | Keine teuren Operationen. |
| Multi-Tenancy | NOT REQUIRED | Ein Lauf, ein Projekt. |
| Observability | NOT REQUIRED | Ausgabe und Exit-Code sind die vollständige Beobachtbarkeit. |
| Scalability | NOT REQUIRED | Repos in dieser Größenordnung sind kein Skalierungsproblem. |
| Backup / Recovery | NOT REQUIRED | Git ist das Backup. Kein eigener Zustand. |

## Aufbau

Das Repository enthält drei Artefakte mit klar getrennten Aufgaben:

```
Projekt-Foundation
├── plugins/project-foundation/     Prozesswissen (Skill + Vorlagen)  → Agent liest
├── src/foundation_validate/        Maschinelle Prüfung               → CI/Mensch führt aus
└── docs/, examples/                Anwendung des Prozesses auf sich selbst
```

**Warum getrennt:** Der Skill ist Prompt-Material und verändert sich mit dem Prozess.
Der Validator ist ausführbarer Code und verändert sich mit den prüfbaren Regeln. Beide
zusammen in eine Datei zu legen würde bedeuten, Prosa und Logik gemeinsam zu versionieren.

### Skill (`plugins/project-foundation/skills/project-foundation/`)

- `SKILL.md` — Einstiegspunkt, Phasenreihenfolge, absolute Regeln, Stop-Conditions.
- `reference/` — vertiefende Checklisten, die erst bei Bedarf gelesen werden.
- `templates/` — die Vorlagen, die im Zielprojekt landen.

Der Skill lädt bewusst nur `SKILL.md` vorab; `reference/` und `templates/` werden gezielt
nachgeladen. Das hält den Kontextverbrauch klein.

### Validator (`src/foundation_validate/`)

```
cli.py        Argumente, Exit-Codes
report.py     Rendering des Audit-Reports
validator.py  Regeln (Struktur, Manifest, ADRs, Status, Secrets, Konsistenz)
model.py      Finding, Severity, Domain und die erlaubten Statuswerte
```

Datenfluss ist linear und ohne Seiteneffekte:

```
Projektpfad → validate() → Result(findings, domain_status) → render() → stdout + Exit-Code
```

Jede Prüfung liefert `Finding`-Objekte mit stabiler ID. Der Domänenstatus wird abgeleitet:
ein `BLOCKING`-Finding macht die Domäne `BLOCKED`, ein `WARNING` macht sie `WARNING`,
sonst gilt der in `STATUS.md` erklärte Wert.

**Bewusste Grenze:** Der Validator prüft nur, was maschinell entscheidbar ist. Ob ein
`PROJECT.md` inhaltlich gut ist, kann er nicht beurteilen — er stellt nur sicher, dass die
Frage überhaupt beantwortet wurde. Deshalb endet er auf `FOUNDATION VALID`, nie auf
`FOUNDATION READY` (ADR-0010), meldet Domänen ohne eigene Regel als `NOT CHECKED` und
leitet den Domänenstatus ausschließlich aus eigenen Befunden ab.

Der Validator ist Ebene 1 von dreien (Validierung → Review → Mensch); die Ebenen sind in
`SKILL.md` definiert. Ebene 1 ist Voraussetzung für Ebene 2, nie Ersatz. Der Code kennt
Ebene 2 und 3 nicht.

## Configuration

`.project-foundation.yml` ist ein **Index**, keine Source of Truth. Es fasst maschinenlesbar
zusammen, was in den Dokumenten steht. Widersprüche zwischen Manifest und `STATUS.md` sind
Blocker — die Dokumente gewinnen. Siehe ADR-0004.

## Deployment

Kein Deployment im klassischen Sinn. Das Toolkit wird als Claude-Code-Plugin aus diesem
Repository installiert:

```
/plugin marketplace add Dimen2608/Projekt-Foundation
/plugin install project-foundation@projekt-foundation
```

Der Validator wird im Zielprojekt bei Bedarf per `pip install` aus dem geklonten Repo
eingebunden oder direkt mit `python -m foundation_validate <pfad>` ausgeführt.

## Security

Relevant sind zwei Punkte, beide betreffen fremde Projekte:

1. **Secret-Hygiene.** Eine vorhandene `.env` und ein `.gitignore` ohne `.env`-Eintrag
   sind Blocker (`SEC-001`, `SEC-002`). Das ist ausdrücklich **kein** Secret Scanning:
   Der Validator liest keine Dateiinhalte auf Geheimnisse hin und behauptet nie, ein
   Projekt sei frei von Secrets. Projekte, die diese Zusicherung brauchen, richten ein
   dafür gebautes Werkzeug ein (GitHub Secret Scanning, `gitleaks`).
2. **Nur-Lesen.** Der Validator schreibt nie in das geprüfte Projekt. Ein Prüfwerkzeug,
   das Dateien verändert, wäre in fremden Repos nicht vertretbar.

Ungeklärte sicherheitsrelevante Entscheidungen im Zielprojekt (`Authentication`,
`Authorization`, `Secrets` auf `UNKNOWN`) blockieren `FOUNDATION VALID` — und damit
alles, was darauf aufbaut.

## Quality Gates

| Gate | Wann | Bedingungen |
| --- | --- | --- |
| Foundation Gate | Vor Feature-Arbeit (nicht vor Bugfixes) | `foundation-validate` meldet `FOUNDATION VALID`, Review ohne Blocker |
| Change Gate | Vor jedem Commit | Format, Lint, Typecheck, Tests grün; keine bekannte Regression |
| Architecture Gate | Bei Struktur-/Schnittstellenänderung | ADR erstellt oder aktualisiert, `ARCHITECTURE.md` nachgezogen |
| Security Gate | Bei Änderungen an Secret-/Pfadlogik | Nur-Lesen-Eigenschaft geprüft, keine Secrets im Diff |

## Teststrategie

Risikobasiert. Getestet wird, was über `FOUNDATION VALID` entscheidet.

| Level | Status | Begründung |
| --- | --- | --- |
| Unit | aktiv | Jede Blocking-Regel hat genau einen Test, erzwungen durch `tests/test_regelabdeckung.py`. |
| Integration | aktiv | CLI-Tests prüfen Exit-Code und Reportstruktur — die Schnittstelle, auf die CI sich verlässt. |
| E2E | NOT REQUIRED | Es gibt keine Schicht jenseits des CLI. |
| Contract | NOT REQUIRED | Keine externen Schnittstellenpartner. |
| Performance | NOT REQUIRED | Laufzeit im Millisekundenbereich. |
| Mutation | NOT REQUIRED | Die Frage dahinter — hat jede Regel einen Test? — beantwortet der Abdeckungstest direkt (ADR-0009). |

Nicht getestet werden bewusst: Getter, Dataclass-Konstruktion, YAML-Parsing von PyYAML,
`argparse`-Verhalten. Das wäre Test von Framework-Verhalten ohne Schutzwirkung.
