# TaskFlow

> **Beispielprojekt.** Fiktiv, dient nur zur Demonstration einer vollständig ausgefüllten
> Foundation. Es existiert kein Code — die Dateien zeigen, wie „ausgefüllt" aussieht.

Ein interner Aufgaben-Tracker für kleine Teams: Aufgaben anlegen, zuweisen, Status ändern.

## Voraussetzungen

- Node.js 22
- pnpm 9
- PostgreSQL 16 (lokal via Docker Compose)

## Installation

```bash
pnpm install
cp .env.example .env
docker compose up -d db
pnpm db:migrate
```

## Nutzung

```bash
pnpm dev          # http://localhost:3000
```

## Entwicklung

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

## Dokumentation

| Frage | Datei |
| --- | --- |
| Was bauen wir? | `docs/PROJECT.md` |
| Wie ist es strukturiert? | `docs/ARCHITECTURE.md` |
| Warum wurde so entschieden? | `docs/decisions/` |
| Was gilt gerade? | `STATUS.md` |
