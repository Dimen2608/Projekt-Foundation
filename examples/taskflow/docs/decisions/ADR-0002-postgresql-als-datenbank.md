# ADR-0002: PostgreSQL 16 als Datenbank

## Status

Accepted — 2026-09-01

## Context

TaskFlow braucht relationale Daten mit Fremdschlüsseln (`teams`, `users`, `tasks`) und
Constraints auf Statuswerten. Geprüft wurden SQLite, PostgreSQL und eine Dokumentendatenbank.

- **SQLite** wäre für die Datenmenge ausreichend, erschwert aber den Betrieb mehrerer
  Instanzen und rollierende Deployments.
- **Dokumentendatenbank** passt schlecht zu einem Datenmodell, das im Kern aus Beziehungen
  besteht, und macht die Team-Filterung zu Anwendungslogik statt zu einer Constraint.
- **PostgreSQL** ist im Team bereits im Betrieb und auf der Plattform verfügbar.

## Decision

PostgreSQL 16. Schema-Änderungen ausschließlich über versionierte Migrationen unter
`src/db/migrations/`, additiv, damit ein Rollback auf die vorherige Anwendungsversion
möglich bleibt.

## Consequences

**Positiv**

- Fremdschlüssel und Check-Constraints sichern Invarianten in der Datenbank ab, nicht nur
  im Anwendungscode.
- Vorhandene Betriebserfahrung inklusive Backup-Verfahren.

**Negativ**

- Lokale Entwicklung braucht einen laufenden Container. Über Docker Compose abgedeckt.
