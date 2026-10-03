# ADR-0022: PA-Kit als Kopiervorlage unter `kits/pa/`, nicht im Plugin

## Status

Accepted — 2026-10-03

## Context

Der Auftraggeber betreibt seit August 2026 eine Meta-Session über allen Projekten, den PA: Sie
plant und entscheidet mit dem Menschen, führt Board und Entscheidungen und steuert Arbeits-Sessions
(Aufträge per Nachricht, Rückweg über das Transkript, Selbst-Clear mit Übergabe-Datei). Am
2026-10-04 soll ein zweiter Mensch einen eigenen PA bekommen. Das Plugin hat dafür keine Vorlage:
`project-orchestrate` steuert Worker innerhalb **eines** Vorhabens und schließt Projektmanagement
ausdrücklich aus („keine Termine, keine Roadmap, keine Prioritätenliste“). Der PA ist genau das,
über alle Projekte.

Zu entscheiden: wohin, in welcher Form, und wie viel.

## Decision

1. **Ort `kits/pa/` im Repo, nicht im Plugin.** Das Kit wird einmal von Hand kopiert und danach vom
   Menschen gelebt; ein Skill, der bei jeder Session-Liste mitlädt, brächte dafür nur Kontextkosten
   und eine weitere `description` mit Auslöse-Test. In `project-orchestrate` passt es nicht wegen
   dessen Abgrenzung (siehe oben). Die Plugin-Verzeichnisstruktur (ADR-0001) bleibt unberührt.
2. **Keine aktive Anweisung im Kit.** Die Meta-Vorlage heißt `meta-CLAUDE.md`, der Agent liegt unter
   `kits/pa/agents/`, nicht unter `.claude/agents/`. Sonst lädt eine Session in diesem Repo sie als
   eigene Anweisung bzw. eigenen Agent (gleiche Begründung wie ADR-0021, Punkt 3, und ADR-0002).
3. **Umfang nach ADR-0011:** neun Dateien, je eine Frage, aufgeführt in `kits/pa/README.md`. Dazu
   die Einrichtung in sieben Schritten und die gemessenen Grenzen mit Datum und Version.
4. **Agent-Vorlage `task-manager`** mit `name`, `description`, `tools`, `model: sonnet`,
   `effort: medium`. Innerhalb der erlaubten Felder; nur lesend per Werkzeugliste und Prompt-Regel
   (`Bash` bleibt, die Sperre ist begrenzt, wie bei den lesenden Rethink-Rollen).
5. **Nichts aus der Quelle außer der Form.** Keine Nummern, Personen, Kunden, Hashes, Pfade oder
   Fachentscheidungen des Betriebs, aus dem das Kit stammt. Namen, Team, Ressorts, Projekte und
   Sessions sind Platzhalter `{{…}}`.
6. **Befunde vom 2026-10-03 auch in `mechanismen.md`**, mit Quelle „Betrieb“: fremde Session
   leeren nur eingeschränkt, eingereihte Nachricht an eine beschäftigte Session. Kit und Plugin sagen
   damit dasselbe. Weil das Plugin-Inhalt ist, Version 0.10.1.
7. **Keine Validator-Änderung**, keine Finding-ID, `schema_version` bleibt `1`. Das Kit ist keine
   Pflichtstelle eines Projekts.

## Consequences

- Das Kit kommt nicht mit der Plugin-Installation, sondern aus dem Repo (ZIP oder Klon). Das ist
  ein Handgriff mehr bei der Einrichtung, dafür kostet es im Alltag nichts.
- Die Grenzen in `kits/pa/README.md` veralten wie `mechanismen.md`; sie tragen Datum und Version und
  werden bei der Einrichtung neu festgestellt.
- Es gibt keinen Test für das Kit: Es ist Prompt-Material (ADR-0009). Geprüft wird, dass keine
  Platzhalter nach der Einrichtung übrig sind (Schritt 4 der Anleitung).
- Neu prüfen, wenn das Kit pro Einrichtung angepasst werden muss oder ein dritter PA entsteht:
  dann als Skill mit Interview, der die Platzhalter erfragt.
