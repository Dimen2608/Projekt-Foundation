# ADR-0003: Python 3.11 mit einer einzigen Laufzeit-Abhängigkeit für den Validator

## Status

Accepted — 2026-09-01

## Context

Der Validator muss ein beliebiges fremdes Projekt prüfen können — unabhängig davon, in
welcher Sprache dieses Projekt geschrieben ist. Er darf dem Zielprojekt also keine
Toolchain aufzwingen.

Kandidaten:

- **Bash.** Keine Installation nötig, aber YAML-Parsing und strukturierte Fehlerberichte
  in Shell sind fehleranfällig und schlecht testbar.
- **Node/TypeScript.** Sinnvoll, wenn alle Zielprojekte JS/TS wären. Sie sind es nicht,
  und `node_modules` in ein fremdes Repo zu bringen ist invasiver als ein Python-Skript.
- **Python.** Auf Linux und macOS praktisch immer vorhanden, starke Standardbibliothek,
  gute Testbarkeit.

Für YAML gibt es keine sinnvolle stdlib-Lösung. Einen eigenen YAML-Subset-Parser zu
schreiben wäre genau die Art von Komplexität, die wir anderswo ablehnen.

## Decision

Python ≥ 3.11. Genau eine Laufzeit-Abhängigkeit: `PyYAML`.

Entwicklungswerkzeuge: `ruff` (Format + Lint), `mypy --strict` (Typecheck), `pytest` (Tests).
Alle drei sind Dev-Dependencies und für die Nutzung des Validators nicht erforderlich.

`>= 3.11` wegen `StrEnum` und moderner Typsyntax ohne `typing`-Importe.

## Consequences

**Positiv**

- Der Validator läuft in fremden Projekten, ohne deren Stack zu berühren.
- `mypy --strict` fängt Fehler in der Regel-Logik, bevor sie im Report landen.
- Eine einzige Abhängigkeit heißt: kein Lockfile-Aufwand, kaum Angriffsfläche.

**Negativ**

- Auf Windows ohne Python-Installation zusätzlicher Aufwand.
- Zielprojekte, die kein Python nutzen, brauchen es trotzdem für die Prüfung. Der Alternative
  — Prüfung nur durch den Agenten, ohne ausführbares Gate — steht entgegen, dass ein Gate
  ohne Ausführung kein Gate ist.

**Grenze**

Jede weitere Laufzeit-Abhängigkeit braucht ein eigenes ADR.
