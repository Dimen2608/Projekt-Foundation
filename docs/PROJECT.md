# Projekt-Definition — Projekt-Foundation

> Source of Truth für **was** gebaut wird. Architektur steht in `docs/ARCHITECTURE.md`,
> der aktuelle Zustand in `STATUS.md`.

## Purpose

Ein wiederverwendbares Toolkit, das beliebige Software-Projekte in einen Zustand bringt,
in dem Menschen und AI-Agents ohne Rückfragen und ohne Raten arbeiten können — mit dem
kleinstmöglichen Satz an Dokumenten, der dafür ausreicht.

## Problem

Neue Projekte starten typischerweise mit einem von zwei Fehlern:

1. **Zu wenig Foundation** — kein definierter Scope, keine dokumentierte Architektur,
   keine festgehaltenen Entscheidungen. Agents und neue Teammitglieder erfinden
   Anforderungen, treffen implizit Architekturentscheidungen und produzieren Drift.
2. **Zu viel Foundation** — Kubernetes, Microservices und sechs Observability-Tools für
   eine App mit zwölf Nutzern; Dokumentation, die sich selbst widerspricht, weil dieselbe
   Information an vier Stellen steht.

Beides kostet mehr, als es einbringt. Es fehlt ein reproduzierbarer Prozess, der die
Foundation *ausreichend* und gleichzeitig *klein* macht — und der prüfbar ist statt
Meinungssache.

## Target Users

- **Primär:** Entwickler und Tech Leads, die ein neues Projekt aufsetzen oder ein
  bestehendes für AI-gestützte Entwicklung nachrüsten.
- **Sekundär:** AI-Agents (Claude Code, Cursor), die den Prozess selbst ausführen und
  dabei an Stop-Conditions gebunden sind.

## Core Value

Eine belastbare Ja/Nein-Aussage mit benannten Blockern statt einer Prozentzahl — kein
„92 % fertig". Auf zwei getrennten Ebenen, damit keine davon mehr behauptet, als sie
belegen kann: **FOUNDATION VALID** (maschinell, durch das CLI) und **FOUNDATION READY**
(inhaltlich, durch Review und Mensch). Siehe ADR-0010.

## Scope

### MVP

- Skill `project-foundation`, der den vollständigen Prozess
  DISCOVER → ASSESS → ASK → DECIDE → GENERATE → VALIDATE → AUDIT führt.
- Vorlagen für alle Foundation-Dateien (`PROJECT.md`, `ARCHITECTURE.md`, ADR, `STATUS.md`,
  `CLAUDE.md`, `AGENTS.md`, Cursor-Rule, `.env.example`, CI-Workflow, Manifest).
- CLI `foundation-validate`, das die maschinell prüfbaren Regeln durchsetzt und den
  Audit-Report im festgelegten Format erzeugt.
- Verteilung als Claude-Code-Plugin über einen Marketplace im selben Repo.
- Ein vollständig ausgefülltes Beispielprojekt unter `examples/`.

### V1

- Weitere Review-Skills (`architecture-review`, `security-review`), sobald sie sich in
  der Anwendung als wiederkehrend erweisen — nicht vorab.
- Manifest-Schemaversionierung mit Migrationspfad, sobald `schema_version` 2 nötig wird.

**FUTURE IDEA** (nicht umgesetzt, nicht eingeplant): den Pflichtumfang aus `project.type`
und `project.maturity` ableiten, statt ihn für alle Projekte gleich zu halten. Braucht
Erfahrungswerte aus mehreren Fremdprojekten — vorher wäre die Zuordnung erfunden
(ADR-0011).

### Out of Scope

- Code-Generierung für Zielprojekte. Die Foundation ermöglicht Implementierung, sie
  ersetzt sie nicht.
- Projektmanagement, Ticketing, Roadmaps, Zeitschätzung.
- Inhaltliche Bewertung von Architekturqualität durch den Validator. Er prüft Struktur
  und Widersprüche; die fachliche Bewertung bleibt beim Review.
- Sprach- oder Framework-spezifische Scaffolds (kein `create-react-app`-Ersatz).
- Secret Scanning. Der Validator prüft Secret-*Hygiene* (`.env` nicht committet, `.env`
  ignoriert) und behauptet nie, ein Projekt sei frei von Secrets. Wer das braucht, nutzt
  GitHub Secret Scanning oder `gitleaks`.
- Veröffentlichung des Validators auf PyPI (siehe ADR-0006).

## Functional Requirements

| ID | Anforderung |
| --- | --- |
| FR-1 | Der Skill führt den Foundation-Prozess in fester Phasenreihenfolge aus und beginnt keine **Feature-Implementierung** vor `FOUNDATION READY`. Foundation Work und Bugfixes mit bekanntem Scope sind davon ausgenommen. |
| FR-2 | Der Skill fragt nach, statt kritische Entscheidungen zu erfinden. |
| FR-3 | Für jede Foundation-Datei existiert genau eine Vorlage. |
| FR-4 | `foundation-validate <pfad>` prüft ein beliebiges Zielprojekt. |
| FR-5 | Der Validator erkennt Widersprüche zwischen Manifest und `STATUS.md`. |
| FR-6 | Sicherheitsrelevante `UNKNOWN`-Entscheidungen führen zu einem Blocker. |
| FR-7 | Der Validator gibt Exit-Code 0 bei `FOUNDATION VALID`, 1 bei Blockern, 2 bei ungültigem Pfad. |
| FR-10 | Der Validator behauptet nichts, was er nicht geprüft hat: kein `FOUNDATION READY`, kein `PASS` für ungeprüfte Domänen, keine Aussage über Secret-Freiheit. |
| FR-11 | Pflicht ist ein Artefakt nur, wenn ohne es eine notwendige Frage unbeantwortet bliebe. ADRs und `STATUS.md` sind bedingt, nicht pauschal. |
| FR-8 | Jeder Blocker nennt ID, Reason, Required Action und Affected Area. |
| FR-9 | Das Toolkit ist per `/plugin marketplace add` in fremden Projekten installierbar. |

## Non-Functional Requirements

| ID | Anforderung |
| --- | --- |
| NFR-1 | Der Validator läuft ohne Netzwerkzugriff und ohne Projekt-Kontext des Zielprojekts. |
| NFR-2 | Genau eine Laufzeit-Abhängigkeit (`PyYAML`). Jede weitere braucht eine Begründung. |
| NFR-3 | Die Foundation dieses Repos bleibt kleiner als das System, das sie ermöglicht. |
| NFR-4 | Der Validator schreibt nie in das geprüfte Projekt — reine Lesezugriffe. |
| NFR-5 | Der Validator läuft auf einer Windows-Standardkonsole (cp1252) ohne Absturz. |

## Constraints

- Python ≥ 3.11 (siehe ADR-0003).
- Dokumentation: Deutsch im Fließtext, englische Struktur-Keywords (siehe ADR-0005).
- Keine Secrets im Repository; der Validator erzwingt das für Zielprojekte.

## Open Decisions

Aktuell keine offenen Entscheidungen mit Blocking-Charakter.

| ID | Frage | Status |
| --- | --- | --- |
| OD-1 | Ob zusätzliche Review-Skills nötig sind | vertagt bis V1, entscheidet sich durch Anwendung |
