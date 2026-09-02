# Phasen im Detail

## 1 — DISCOVER

**Regel: In dieser Phase wird keine Datei verändert.**

Bei bestehenden Projekten gilt: *Bestehendes Wissen zuerst verstehen, bevor du etwas
ersetzt.* Vorhandene Dokumentation ist ein Signal über Absicht und Historie — auch wenn
sie veraltet ist.

### Checkliste

| Bereich | Wonach suchen |
| --- | --- |
| Struktur | Verzeichnisbaum, Monorepo oder einzelnes Paket |
| Source Code | Sprachen, Frameworks, Einstiegspunkte |
| Tests | Vorhanden? Welche Level? Laufen sie? |
| Dokumentation | `README`, `docs/`, Wiki-Verweise |
| AI-Instruktionen | `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/`, `.github/copilot-instructions.md`, Skills |
| Build | Package Manager, Lockfiles, Build-Tool, Task-Runner |
| CI/CD | `.github/workflows/`, `.gitlab-ci.yml`, Jenkinsfile |
| Infrastruktur | Dockerfile, Compose, Terraform, Helm, Deployment-Konfiguration |
| Environment | `.env*`, Konfigurationsdateien, Secret-Handhabung |
| Datenbank | Migrationen, Schema, ORM-Modelle |
| Auth | Authentication- und Authorization-Mechanismen |
| Entscheidungen | `docs/decisions/`, `docs/adr/`, Design-Dokumente |
| Arbeitsstand | Issues, `TODO`, `FIXME`, offene Branches |

Zusätzlich erfassen:

- **Technische Schulden** — was ist erkennbar provisorisch?
- **Overengineering** — welche Komplexität hat keine erkennbare Anforderung hinter sich?
- **Widersprüche** — wo sagen zwei Quellen Unterschiedliches?

### Ergebnis: FOUNDATION DISCOVERY REPORT

Enthält: vorhandene relevante Dateien, erkannte Architektur, erkannter Stack, vorhandene
AI-Instruktionen, vorhandene Tests, vorhandene CI/CD, vorhandene Infrastruktur, gefundene
Widersprüche, fehlende Entscheidungen, mögliche Overengineering-Bereiche, vorgeschlagene
Foundation-Schritte.

---

## 2 — ASSESS

Jede der acht Domänen bekommt einen Status:

| Status | Bedeutung |
| --- | --- |
| `PASS` | Vorhanden, konsistent, nutzbar |
| `WARNING` | Verbesserungswürdig, blockiert aber nicht |
| `BLOCKED` | Verhindert Implementierung |
| `UNKNOWN` | Information fehlt, muss erfragt werden |

Domänen: Project Definition, Architecture, Development Setup, AI Foundation,
Documentation, Testing & Quality, CI/CD & Infrastructure, Security.

Gezielt suchen nach: fehlenden Entscheidungen, widersprüchlichen Informationen, unnötiger
Komplexität, doppelter Dokumentation, doppelten Rules, nutzlosen Tests, fehlenden Quality
Gates, nicht reproduzierbaren Setups, Sicherheitsrisiken.

---

## 3 — ASK

Alles, was `UNKNOWN` ist und die Foundation blockiert, wird gefragt.

**Wie gefragt wird:**

- Fragen bündeln. Nicht nacheinander nachhaken.
- Bei mehreren gangbaren Wegen: Optionen mit Trade-offs vorlegen, eine Empfehlung geben,
  aber die Entscheidung dem Menschen überlassen.
- Trennen zwischen „muss jetzt beantwortet werden" und „kann später".
- Nichts fragen, was im Repository steht. Erst lesen, dann fragen.

**Was niemals geraten wird:** Zweck, Zielgruppe, Scope-Grenzen, Persistenzbedarf,
Auth-Modell, Mandantenfähigkeit, Deployment-Ziel, regulatorische Auflagen.

---

## 4 — DECIDE

Entscheidungen festhalten. Für jede tragende Entscheidung ein ADR (Kriterien in `SKILL.md`).

Bei jeder Entscheidung die einfachste ausreichende Lösung bevorzugen und **die verworfenen
Alternativen im ADR benennen** — ein ADR ohne verworfene Optionen erklärt nichts.

Am Ende dieser Phase steht eine der beiden Aussagen in `docs/ARCHITECTURE.md`:

- `Architecture Decisions | REQUIRED` — mit den ADRs, die es dann auch gibt.
- `Architecture Decisions | NOT REQUIRED` — mit der Begründung, warum keine Entscheidung
  dieses Projekts die Kriterien erfüllt.

Beides ist ein gültiger Abschluss. Was nicht geht: die Frage offenlassen.

---

## 5 — GENERATE

Reihenfolge, weil spätere Dokumente auf früheren aufbauen:

```
docs/PROJECT.md → docs/ARCHITECTURE.md → [docs/decisions/] → README.md
→ CLAUDE.md oder AGENTS.md (+ .cursor/rules/) → [STATUS.md] → .project-foundation.yml
```

Die eckigen Klammern sind ernst gemeint: `docs/decisions/` entsteht nur, wenn es eine
tragende Entscheidung gibt; `STATUS.md` nur, wenn der Zustand nicht ohnehin sichtbar ist.
Die Tabelle in `SKILL.md` sagt, welche Frage welches Artefakt rechtfertigt.

Regeln:

- `CLAUDE.md` bleibt kurz: Regeln, Constraints, Commands, Stop-Conditions, Verweise.
  Keine Dokumentation hineinkopieren.
- Jede Information genau einmal. Bei Bedarf verweisen statt wiederholen.
- Optionale Dokumente nur mit konkretem Zweck.
- Das Manifest bekommt nur, was maschinell gebraucht wird — kein Abbild der Dokumente.
- `.env.example` anlegen, sobald Environment-Variablen existieren. Niemals echte Werte.

### Architektur-Bereiche

Jeder Bereich wird bewertet mit `RELEVANT`, `NOT REQUIRED`, `FUTURE` oder `UNKNOWN`.

**Immer bewerten:** Application Architecture, Frontend, Backend, Database, Data Model,
Authentication, Authorization, APIs, External Services, Deployment, Security,
Configuration, Secrets.

**Nur bei Bedarf:** Storage, Background Jobs, Messaging, Events, Caching, Search,
Multi-Tenancy, Networking, Observability, Scalability, Backup/Recovery.

`UNKNOWN` bei Authentication, Authorization oder Secrets ist **BLOCKING**.

Zusätzlich, in derselben Tabelle: `Architecture Decisions` mit `REQUIRED` oder
`NOT REQUIRED` (siehe `SKILL.md`).

### Development Setup

Festlegen und dokumentieren: Language, Runtime, Framework, Package Manager,
Versionsstrategie, Dependencies, Git-Konventionen, Formatter, Linter, Typecheck, Build,
Test-Framework, Environment-Konfiguration, Secrets.

Konkrete Commands definieren: `install`, `dev`, `test`, `lint`, `typecheck`, `build`.
Nicht zutreffende Commands ausdrücklich als `NOT REQUIRED` mit Begründung markieren —
weglassen ohne Begründung erzeugt eine offene Frage.

### AI Foundation

| Artefakt | Zweck |
| --- | --- |
| `CLAUDE.md` | Regeln, Constraints, Commands, Stop-Conditions für Claude Code |
| `AGENTS.md` | Gemeinsamer Kontext, wenn mehrere Agent-Werkzeuge im Einsatz sind |
| `.cursor/rules/*.mdc` | Kleine, fokussierte Regeln; `globs` für dateispezifische Regeln, `alwaysApply` nur bei echt globalen Regeln |
| Skills | Nur für wiederverwendbare Prozesse, nicht für einzelne Regeln |

---

## 6 — VALIDATE

Die dokumentierten Commands tatsächlich ausführen. Nicht behaupten, dass sie laufen.

```
install → lint → typecheck → test → build
```

Eine dokumentierte, aber kaputte Command-Chain ist **BLOCKED**.

Wenn `foundation-validate` verfügbar ist, zusätzlich ausführen. Er endet auf
`FOUNDATION VALID` oder `FOUNDATION INVALID` und ersetzt das inhaltliche Review nicht —
das ist Ebene 2 und kommt danach.

---

## 7 — AUDIT

Siehe `audit.md`.
