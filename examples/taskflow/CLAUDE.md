# CLAUDE.md — TaskFlow

## Was ist das

Interner Aufgaben-Tracker für kleine Teams. Details: `docs/PROJECT.md`.

## Project Knowledge

| Frage | Datei |
| --- | --- |
| Was bauen wir? | `docs/PROJECT.md` |
| Wie ist es strukturiert? | `docs/ARCHITECTURE.md` |
| Warum wurde so entschieden? | `docs/decisions/` |
| Was gilt gerade? | `STATUS.md` |
| Wie starte ich es? | `README.md` |

## Commands

```bash
pnpm install      # install
pnpm dev          # dev
pnpm test         # test
pnpm lint         # lint
pnpm typecheck    # typecheck
pnpm build        # build
pnpm db:migrate   # Migrationen anwenden
```

## Regeln

- Jeder Datenbankzugriff läuft über die Repository-Schicht in `src/server/repositories/`.
  Kein SQL in Route-Handlern.
- Jede Route, die Aufgaben liest oder schreibt, prüft die Team-Zugehörigkeit. Es gibt
  keine Abfrage ohne `team_id`-Einschränkung (ADR-0003).
- Schema-Änderungen nur über Migrationen, nie von Hand an der Datenbank.
- Keine Secrets im Code. `SESSION_SECRET` kommt aus der Umgebung.
- Vor dem Commit: `pnpm lint && pnpm typecheck && pnpm test`.

## Constraints

- Node 22, pnpm 9, PostgreSQL 16.
- Kein SSO im MVP — bewusste Scope-Grenze (`docs/PROJECT.md`).

## Stop Conditions

Anhalten und fragen, wenn:

- Eine Änderung Team-Grenzen im Datenzugriff berührt.
- Eine Anforderung nicht in `docs/PROJECT.md` steht.
- Eine Migration bestehende Daten zerstören würde.
- Ein neuer externer Dienst eingebunden werden soll.
