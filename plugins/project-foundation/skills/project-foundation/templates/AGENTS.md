# AGENTS.md — <PROJEKTNAME>

> Gemeinsamer Kontext für alle Agent-Werkzeuge. Diese Datei nur anlegen, wenn tatsächlich
> mehrere Werkzeuge im Einsatz sind — sonst genügt `CLAUDE.md`.
>
> Werkzeugspezifisches gehört nicht hierher: Claude-Regeln in `CLAUDE.md`,
> Cursor-Regeln in `.cursor/rules/`.

## Projekt

<Ein bis zwei Sätze. Details: `docs/PROJECT.md`.>

## Aufbau

<Kurzer Verzeichnisüberblick mit einer Zeile Zweck je Bereich. Details:
`docs/ARCHITECTURE.md`.>

## Commands

```bash
<install>
<test>
<lint>
<build>
```

## Konventionen

- <Namensgebung, Verzeichnisstruktur, Commit-Format — nur das Nicht-Offensichtliche>

## Grenzen

- Keine tragende Architekturentscheidung ohne ADR in `docs/decisions/`.
- Keine Secrets im Repository.
- Bei Unklarheit: fragen, nicht raten.
