# Status — <PROJEKTNAME>

> **Optional.** Diese Datei lohnt sich, sobald mehr als eine Person oder mehr als eine
> Session am Projekt arbeitet. Ein Ein-Personen-Projekt, dessen Zustand ohnehin sichtbar
> ist, braucht sie nicht — ein ungepflegtes STATUS.md ist schlechter als keins.
>
> Source of Truth für **den aktuellen Zustand**. Ausschließlich Gegenwart — keine Historie
> (die gehört in `PROGRESS.md`), keine Pläne (die gehören in `docs/PROJECT.md`), keine
> Architektur (die gehört in `docs/ARCHITECTURE.md`) und nichts, was ein Werkzeug ohnehin
> ausrechnet (Testanzahl, Coverage, letzter Commit).
>
> Stand: <YYYY-MM-DD>

## Foundation

**<FOUNDATION READY | FOUNDATION NOT READY>**

| Domain | Status |
| --- | --- |
| Project Definition | <PASS / WARNING / BLOCKED / UNKNOWN> |
| Architecture | <...> |
| Development Setup | <...> |
| AI Foundation | <...> |
| Documentation | <...> |
| Testing & Quality | <...> |
| CI/CD & Infrastructure | <...> |
| Security | <...> |

Blockers: <n>
Warnings: <n>

## Blocker

<Leer lassen, wenn keine. Jeder Blocker mit ID, Grund, erforderlicher Maßnahme und
betroffenem Bereich. Niemals einen Blocker weglassen.>

| ID | Bereich | Grund | Erforderliche Maßnahme |
| --- | --- | --- | --- |

## Warnungen

| ID | Bereich | Beschreibung |
| --- | --- | --- |

## Command-Chain

<Der zuletzt geprüfte Zustand der Commands. „Läuft" nur eintragen, wenn tatsächlich
ausgeführt.>

| Command | Zustand | Zuletzt geprüft |
| --- | --- | --- |
| install | <ok / kaputt / n/a> | <YYYY-MM-DD> |
| lint | <...> | <...> |
| typecheck | <...> | <...> |
| test | <...> | <...> |
| build | <...> | <...> |
