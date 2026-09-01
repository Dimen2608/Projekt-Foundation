# ADR-0002: Der Skill liegt ausschließlich unter `plugins/`, nicht zusätzlich unter `.claude/skills/`

## Status

Accepted — 2026-09-01

## Context

Damit dieses Repository seinen eigenen Skill beim Arbeiten daran nutzen kann, läge es nahe,
ihn zusätzlich nach `.claude/skills/project-foundation/` zu legen. Dann wäre er lokal ohne
Plugin-Installation aktiv.

Das erzeugt aber zwei Kopien desselben Inhalts. Genau das verbietet die Regel
*DO NOT DUPLICATE SOURCE-OF-TRUTH INFORMATION* — und der wahrscheinlichste Fehlerfall ist,
dass jemand die lokale Kopie bearbeitet und die ausgelieferte Version davon abweicht.

Ein Symlink wäre ein Kompromiss, verhält sich aber je nach Betriebssystem und Git-Konfiguration
unterschiedlich und ist damit nicht reproduzierbar.

## Decision

Der Skill existiert genau einmal, unter
`plugins/project-foundation/skills/project-foundation/`.

Wer in diesem Repository mit dem Skill arbeiten will, installiert das eigene Plugin lokal:

```
/plugin marketplace add .
/plugin install project-foundation@projekt-foundation
```

## Consequences

**Positiv**

- Es gibt keine zwei Wahrheiten. Was ausgeliefert wird, ist das, was hier steht.
- Kein Symlink-Verhalten, das je nach Plattform abweicht.

**Negativ**

- Ein zusätzlicher Installationsschritt für Mitwirkende an diesem Repo. Akzeptiert:
  einmaliger Aufwand gegen dauerhaftes Drift-Risiko.
