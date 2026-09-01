# ADR-0004: Serverseitige Sessions statt JWT

## Status

Accepted — 2026-09-01

## Context

Für die Anmeldung standen JSON Web Tokens im Cookie und serverseitige Sessions mit
Session-ID zur Wahl.

JWTs sind attraktiv, wenn mehrere Dienste ohne gemeinsamen Zustand validieren müssen.
TaskFlow ist ein einzelner Prozess mit einer Datenbank (ADR-0001) — dieser Vorteil greift
nicht. Der bekannte Nachteil greift dagegen sehr wohl: Ein ausgestelltes JWT lässt sich vor
Ablauf nicht zurückziehen, ohne genau die Zustandshaltung einzuführen, die man vermeiden wollte.

## Decision

Serverseitige Sessions. Die Session-ID liegt in einem Cookie mit `HttpOnly`, `Secure` und
`SameSite=Lax`. Der Session-Zustand liegt in PostgreSQL.

Passwörter werden mit Argon2id gehasht, Parameter nach OWASP-Empfehlung.

## Consequences

**Positiv**

- Abmelden und Sperren wirken sofort.
- Kein Token-Inhalt im Browser, der versehentlich Daten preisgibt.

**Negativ**

- Jede Anfrage kostet einen Datenbank-Lookup. Bei 20 Nutzern irrelevant.
- Sessions müssen aufgeräumt werden — ein Index auf dem Ablaufzeitpunkt und ein
  Löschlauf beim Start genügen.
