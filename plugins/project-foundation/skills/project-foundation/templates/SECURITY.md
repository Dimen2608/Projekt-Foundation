# Security — <PROJEKTNAME>

> Nur anlegen, wenn das Projekt einen tatsächlichen Meldeweg oder besondere
> Sicherheitsanforderungen hat. Die architektonischen Sicherheitsentscheidungen stehen in
> `docs/ARCHITECTURE.md`, nicht hier.

## Unterstützte Versionen

| Version | Unterstützt |
| --- | --- |
| <...> | <ja / nein> |

## Schwachstellen melden

<Kontaktweg und erwartete Reaktionszeit. Keine öffentlichen Issues für Schwachstellen.>

## Umgang mit Secrets

- Secrets stehen niemals im Repository.
- `.env` ist in `.gitignore` eingetragen; `.env.example` enthält nur Platzhalter.
- <Wie Secrets in Produktion bereitgestellt werden>

## Sicherheitsrelevante Änderungen

Bei Änderungen an Authentication, Authorization, Secrets, Datenzugriff, Eingabeverarbeitung
oder Mandantentrennung gilt das Security Gate aus `docs/ARCHITECTURE.md`.
