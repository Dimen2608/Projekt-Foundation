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

| Name (wie `ListAgents` ihn zeigt) | Repo | Rechner | Angebunden über | Seit | Aktueller Block |
| --- | --- | --- | --- | --- | --- |
| `<w1>` | `<owner/repo>` | `<Rechner>` | `<attach / local_bg / chip>` | `<Datum>` | `<ID oder —>` |

## Blöcke

| ID | Ziel (ein Satz) | Repo/Branch | Hängt ab von | Zuständig | Worker | Status | Tor-Runden | PR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `B01` | `<…>` | `<…>` | `—` | `<Skill/Agent>` | `<w1>` | `open` | `0` | `—` |

**Status:** `open` (vergebbar, wenn Abhängigkeiten `done`) · `assigned` (beim Worker, auch nach
`NACHARBEIT`) · `gate` (Übergabe liegt vor, wird abgenommen) · `done` · `blocked` (`FRAGE` offen oder `WARTET` auf Freigabe/Befehl beim Menschen bis `WEITER`, Block bleibt beim Worker)
· `escalated` (Übergabe `exhausted`: fünf Runden ohne Freigabe oder `NACHARBEIT` nach der
fünften, liegt beim Menschen).
**Tor-Runden** trägt der Orchestrator aus der Übergabe ein; gezählt werden sie nur vom Worker.

## Regeln

- Ein Block ohne Blockdatei unter `bloecke/` mit allen sechs Pflichtfeldern ist nicht `open`.
- Parallel nur, was keine offene Abhängigkeit hat; nie zwei Blöcke auf demselben Branch.
- Ein `done` ohne Tor-Ja in der Blockdatei ist ein Fehler im Blockplan, kein Fortschritt.

## Abschluss

`<Wenn alle Blöcke done sind: was ist erreicht, welche PRs, was bleibt bewusst offen.>`
