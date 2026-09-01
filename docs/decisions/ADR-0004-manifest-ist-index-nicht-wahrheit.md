# ADR-0004: `.project-foundation.yml` ist ein Index, nicht die Source of Truth

## Status

Accepted — 2026-09-01

## Context

Das Manifest fasst Stack, Architektur, Teststrategie und Foundation-Status maschinenlesbar
zusammen. Damit steht dieselbe Information zwangsläufig zweimal im Repo: einmal in Prosa in
den Dokumenten, einmal strukturiert im Manifest.

Duplikation ohne Rangfolge ist die Hauptursache für Architecture Drift. Sobald zwei Quellen
sich widersprechen, muss entscheidbar sein, welche gilt — sonst raten Agent und Mensch.

## Decision

Die Dokumente gewinnen. Rangfolge:

| Frage | Quelle |
| --- | --- |
| Wie starte/benutze ich es? | `README.md` |
| Was bauen wir? | `docs/PROJECT.md` |
| Wie ist es strukturiert? | `docs/ARCHITECTURE.md` |
| Warum wurde so entschieden? | `docs/decisions/` |
| Was gilt gerade? | `STATUS.md` |
| Was ist passiert? | `PROGRESS.md` |

`.project-foundation.yml` ist ein abgeleiteter Index für Werkzeuge und für den schnellen
Überblick eines Agenten. Es steht nie über einem Dokument.

Der Validator setzt das durch: Ein Manifest mit `foundation.status: READY`, während
`STATUS.md` eine Domäne als `BLOCKED` oder `UNKNOWN` führt, ist ein Blocker (`CONS-001`).
Ebenso ein Manifest, das AI-Dateien behauptet, die es nicht gibt (`CONS-003`).

## Consequences

**Positiv**

- Widersprüche werden zu Fehlern statt zu stiller Verwirrung.
- Ein Agent kann das Manifest lesen, um sich zu orientieren, ohne ihm blind zu vertrauen.

**Negativ**

- Das Manifest muss bei jeder Statusänderung mitgepflegt werden, sonst schlägt die
  Konsistenzprüfung an. Das ist beabsichtigt: ein veraltetes Manifest soll auffallen.
