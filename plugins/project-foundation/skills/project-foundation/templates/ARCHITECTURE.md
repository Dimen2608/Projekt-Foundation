# Architektur — <PROJEKTNAME>

> Source of Truth für **wie** das System strukturiert ist. Das *Warum* einzelner
> Entscheidungen gehört in `docs/decisions/`.

## Bereichsbewertung

Jeder Bereich braucht eine Bewertung: `RELEVANT`, `NOT REQUIRED`, `FUTURE` oder `UNKNOWN`.
Ein nicht bewerteter Bereich ist eine offene Frage.

**`UNKNOWN` bei Authentication, Authorization oder Secrets ist BLOCKING.**

| Bereich | Bewertung | Begründung |
| --- | --- | --- |
| Application Architecture | <...> | <...> |
| Frontend | <...> | <...> |
| Backend | <...> | <...> |
| Database | <...> | <...> |
| Data Model | <...> | <...> |
| Authentication | <...> | <...> |
| Authorization | <...> | <...> |
| APIs | <...> | <...> |
| External Services | <...> | <...> |
| Deployment | <...> | <...> |
| Security | <...> | <...> |
| Configuration | <...> | <...> |
| Secrets | <...> | <...> |
| Architecture Decisions | <REQUIRED / NOT REQUIRED> | <...> |

`Architecture Decisions` beantwortet, ob dieses Projekt ADRs braucht:

- `REQUIRED` — es gibt mindestens eine tragende Entscheidung; sie liegt in
  `docs/decisions/` oder an dem Ort, den die dritte Spalte nennt (Verzeichnis oder
  Sammeldatei, z. B. `docs/adr/`). Kriterien in `SKILL.md`.
- `NOT REQUIRED` — keine Entscheidung dieses Projekts erfüllt die Kriterien. Gültiger
  Zustand, aber die Begründungsspalte ist dann Pflicht, kein Freitextrest.

Optionale Bereiche nur aufnehmen, wenn sie relevant sind: Storage, Background Jobs,
Messaging, Events, Caching, Search, Multi-Tenancy, Networking, Observability, Scalability,
Backup/Recovery.

## Aufbau

<Struktur des Systems. Ein Diagramm oder ein Verzeichnisbaum mit einer Zeile Zweck je
Komponente. Wichtig ist, warum die Grenzen dort liegen, wo sie liegen.>

## Datenmodell

<Nur wenn RELEVANT. Die Entitäten und ihre Beziehungen, nicht das vollständige Schema —
das gehört in Migrationen.>

## Authentication und Authorization

<Nur wenn RELEVANT. Wer darf was, und an welcher Stelle wird das geprüft. Bei SaaS
zusätzlich: Tenant-Isolation und wie Cross-Tenant-Zugriff verhindert wird.>

## Configuration

<Woher kommt Konfiguration, was ist umgebungsabhängig, wo ist der Ort der Wahrheit.>

## Secrets

<Wie werden Secrets verwaltet. Niemals echte Werte hier oder irgendwo im Repository.>

## Deployment

<Wohin, womit, in welchen Schritten. Auch: was passiert bei einem Fehlschlag.>

## Security

<Die konkreten Sicherheitsmaßnahmen dieses Projekts. Keine allgemeine Sicherheitslehre.>

## Quality Gates

| Gate | Wann | Bedingungen |
| --- | --- | --- |
| Foundation Gate | Vor der Implementierung | <...> |
| Change Gate | Vor jedem Commit | <...> |
| Architecture Gate | Bei Strukturänderungen | <...> |
| Security Gate | Bei sicherheitsrelevanten Änderungen | <...> |

## Teststrategie

Risikobasiert. Nur aktivieren, was Schutz bietet.

| Level | Status | Begründung |
| --- | --- | --- |
| Unit | <aktiv / NOT REQUIRED / FUTURE> | <...> |
| Integration | <...> | <...> |
| E2E | <...> | <...> |
| Contract | <...> | <...> |
| Performance | <...> | <...> |
| Mutation | <...> | <...> |

<Ausdrücklich nennen, was bewusst nicht getestet wird und warum.>
