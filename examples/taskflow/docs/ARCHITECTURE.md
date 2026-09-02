# Architektur — TaskFlow

> Beispielprojekt. Zeigt eine ausgefüllte Bereichsbewertung.

## Bereichsbewertung

| Bereich | Bewertung | Begründung |
| --- | --- | --- |
| Application Architecture | RELEVANT | Modularer Monolith, siehe unten. |
| Frontend | RELEVANT | Serverseitig gerenderte Weboberfläche. |
| Backend | RELEVANT | Node/TypeScript, Route-Handler und Repository-Schicht. |
| Database | RELEVANT | PostgreSQL 16, siehe ADR-0002. |
| Data Model | RELEVANT | `users`, `teams`, `tasks`. |
| Authentication | RELEVANT | E-Mail und Passwort, serverseitige Session, siehe ADR-0004. |
| Authorization | RELEVANT | Team-Zugehörigkeit als einzige Zugriffsregel, siehe ADR-0003. |
| APIs | NOT REQUIRED | Keine öffentliche API im Scope. |
| External Services | NOT REQUIRED | Keine im MVP. E-Mail-Versand erst mit V1-Erinnerungen. |
| Deployment | RELEVANT | Ein Container auf der internen Plattform. |
| Security | RELEVANT | Argon2id, Session-Cookies, Team-Filter auf jeder Abfrage. |
| Configuration | RELEVANT | Environment-Variablen, `.env.example` als Referenz. |
| Secrets | RELEVANT | `SESSION_SECRET` und `DATABASE_URL` aus dem Secret Store der Plattform. |
| Background Jobs | FUTURE | Erst mit V1 nötig (Erinnerungen). |
| Multi-Tenancy | NOT REQUIRED | Eine Installation pro Team, siehe ADR-0003. |
| Observability | NOT REQUIRED | Container-Logs genügen bei dieser Nutzerzahl. |
| Caching | NOT REQUIRED | NFR-1 wird durch einen Index auf `(team_id, status)` erreicht. |
| Backup / Recovery | RELEVANT | Täglicher Datenbank-Dump durch die Plattform. |
| Architecture Decisions | REQUIRED | Persistenz, Mandantenmodell und Session-Verfahren sind schwer reversibel — ADR-0001 bis ADR-0004. |

## Aufbau

Modularer Monolith. Ein Prozess, klar getrennte Schichten:

```
src/
├── web/            Seiten und Formulare (serverseitig gerendert)
├── server/
│   ├── routes/         Route-Handler: Eingabevalidierung, Session, Antwort
│   ├── services/       Fachlogik
│   └── repositories/   Datenbankzugriff - der einzige Ort mit SQL
└── db/migrations/  Schema-Änderungen
```

**Abhängigkeitsrichtung:** `routes → services → repositories`. Niemals umgekehrt, und
niemals SQL außerhalb von `repositories/`. Diese Grenze ist der Grund, warum die
Team-Filterung an genau einer Stelle durchsetzbar ist.

**Warum Monolith:** Ein Team, ein Deployment, ein Datenmodell. Services würden hier nur
Netzwerkgrenzen einziehen, wo heute Funktionsaufrufe genügen (ADR-0001).

## Datenmodell

```
teams (id, name)
users (id, team_id → teams, email UNIQUE, password_hash, created_at)
tasks (id, team_id → teams, title, description, status, assignee_id → users, created_at)
```

Index auf `tasks(team_id, status)` — deckt die Listenansicht aus NFR-1 ab.

`tasks.status` ist auf `offen`, `in Arbeit`, `erledigt` per Check-Constraint eingeschränkt.

## Authentication und Authorization

**Authentication:** E-Mail und Passwort. Hash mit Argon2id. Serverseitige Session,
Cookie mit `HttpOnly`, `Secure`, `SameSite=Lax`. Kein JWT (ADR-0004).

**Authorization:** Eine einzige Regel — ein Nutzer sieht und ändert nur Datensätze mit
seiner `team_id`. Durchgesetzt in der Repository-Schicht: jede Abfrage auf `tasks` nimmt
`team_id` als Pflichtparameter. Ein Repository-Aufruf ohne `team_id` ist typseitig
unmöglich.

## Configuration

Ausschließlich Environment-Variablen. `.env.example` dokumentiert alle Variablen mit
Platzhaltern. Fehlt eine Pflichtvariable, bricht der Start mit einer klaren Fehlermeldung ab
— stiller Betrieb mit Standardwerten wäre gefährlicher als ein Startfehler.

## Secrets

`SESSION_SECRET` und `DATABASE_URL` kommen aus dem Secret Store der Container-Plattform und
werden zur Laufzeit als Umgebungsvariablen eingehängt. Kein Secret im Image, im Repository
oder in Logs.

## Deployment

Ein Container-Image, gebaut in CI, auf der internen Plattform ausgerollt. Migrationen laufen
als separater Schritt vor dem Start der neuen Version. Bei Fehlschlag: Rollback auf das
vorherige Image; Migrationen sind additiv, damit die alte Version weiterläuft.

## Security

- Argon2id für Passwörter, Parameter nach OWASP-Empfehlung.
- Session-Cookies `HttpOnly`, `Secure`, `SameSite=Lax`.
- Eingabevalidierung an der Systemgrenze in `routes/`, mit Schema-Prüfung.
- Ausschließlich parametrisierte Abfragen.
- Kein Zugriff über Team-Grenzen hinweg — durch die Repository-Signatur erzwungen.

## Quality Gates

| Gate | Wann | Bedingungen |
| --- | --- | --- |
| Foundation Gate | Vor der Implementierung | Alle Domänen PASS, Command-Chain geprüft |
| Change Gate | Vor jedem Commit | Lint, Typecheck, Tests, Build grün |
| Architecture Gate | Bei Schicht-/Schemaänderung | ADR aktualisiert, Abhängigkeitsrichtung eingehalten |
| Security Gate | Bei Auth-/Datenzugriffsänderung | Team-Filter geprüft, keine Secrets im Diff |

## Teststrategie

| Level | Status | Begründung |
| --- | --- | --- |
| Unit | aktiv | Statusübergänge und Berechtigungslogik. |
| Integration | aktiv | Repository gegen echte PostgreSQL-Instanz — dort liegt das Team-Filter-Risiko. |
| E2E | aktiv | Genau zwei Pfade: Anmeldung und Aufgabe anlegen bis zur Listenansicht. |
| Contract | NOT REQUIRED | Keine externen Schnittstellenpartner. |
| Performance | aktiv | Ein Test für NFR-1 mit 5.000 Datensätzen. |
| Mutation | NOT REQUIRED | Aufwand steht bei dieser Projektgröße in keinem Verhältnis. |

Bewusst nicht getestet: Rendering einzelner Formularfelder, ORM-Verhalten,
Framework-Routing. Das prüft Fremdcode ohne Schutzwirkung für dieses Projekt.
