# Blockplan

> Der **eine Ort** für den Stand aller Blöcke. Beantwortet: **Welche Blöcke gibt es, in welchem
> Zustand, wer arbeitet woran, was hängt wovon ab?** Nur der Orchestrator schreibt hier; nach
> jeder Statusänderung wird committet. **Termine gibt es hier nicht** — Fortschritt ist der
> Status, nicht der Kalender.

## Jetzt

| | |
| --- | --- |
| **Vorhaben** | `<ein Satz, mit Verweis auf die Quelle im Zielprojekt>` |
| **Läuft** | `<Block-IDs mit Worker>` |
| **Wartet auf** | `<wen, worauf, seit wann>` |
| **Als Nächstes** | `<Block-IDs, deren Abhängigkeiten erfüllt sind>` |

## Worker

| Name | Repo | Branch | Gestartet über | Seit | Aktueller Block |
| --- | --- | --- | --- | --- | --- |
| `<w1>` | `<owner/repo>` | `<branch>` | `<cloud_spawn / local_bg / manual>` | `<Datum>` | `<ID oder —>` |

## Blöcke

| ID | Ziel (ein Satz) | Repo/Branch | Hängt ab von | Zuständig | Worker | Status | Tor-Runden | PR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `B01` | `<…>` | `<…>` | `—` | `<Skill/Agent>` | `<w1>` | `open` | `0` | `—` |

**Status:** `open` (vergebbar, wenn Abhängigkeiten `done`) · `assigned` · `gate` (Übergabe
liegt vor, wird abgenommen) · `done` · `blocked` (wartet auf Antwort) · `escalated` (nach fünf
Tor-Runden beim Menschen).

## Regeln

- Ein Block ohne Blockdatei unter `bloecke/` mit allen sechs Pflichtfeldern ist nicht `open`.
- Parallel nur, was keine offene Abhängigkeit hat; nie zwei Blöcke auf demselben Branch.
- Ein `done` ohne Tor-Ja in der Blockdatei ist ein Fehler im Blockplan, kein Fortschritt.

## Abschluss

`<Wenn alle Blöcke done sind: was ist erreicht, welche PRs, was bleibt bewusst offen.>`
