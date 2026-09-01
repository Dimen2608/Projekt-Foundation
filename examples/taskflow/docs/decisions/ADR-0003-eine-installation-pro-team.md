# ADR-0003: Eine Installation pro Team statt Multi-Tenancy

## Status

Accepted — 2026-09-01

## Context

`tasks` und `users` tragen bereits eine `team_id`. Damit läge nahe, mehrere Organisationen
in einer Installation zu betreiben. Multi-Tenancy bedeutet aber, dass jeder Fehler in der
Filterung Daten fremder Organisationen offenlegt — die teuerste Fehlerklasse in dieser
Anwendung.

Der reale Bedarf ist heute genau ein Team. `docs/PROJECT.md` führt mehrere Organisationen
ausdrücklich als Out of Scope.

## Decision

Eine Installation pro Team. Die `team_id` bleibt im Schema, weil sie das Datenmodell
korrekt beschreibt und die Filterung von Anfang an erzwingt — sie wird aber nicht als
Mandantengrenze im Sinne getrennter Kunden behandelt.

Durchsetzung: Jede Repository-Funktion auf `tasks` nimmt `team_id` als Pflichtparameter.
Ein Aufruf ohne `team_id` ist typseitig nicht möglich.

## Consequences

**Positiv**

- Keine Cross-Tenant-Fehlerklasse. Die schwerwiegendste Sicherheitsfrage entfällt.
- Der Team-Filter ist trotzdem von Beginn an vorhanden, falls sich der Bedarf ändert.

**Negativ**

- Mehrere Teams bedeuten mehrere Installationen und mehrere Datenbanken.
- Eine spätere Umstellung auf echte Mandantenfähigkeit erfordert ein neues ADR und eine
  Sicherheitsprüfung jedes Zugriffspfads.
