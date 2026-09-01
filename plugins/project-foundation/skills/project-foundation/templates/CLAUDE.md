# CLAUDE.md — <PROJEKTNAME>

> Diese Datei bleibt **kurz**. Sie enthält Regeln, Constraints, Commands und
> Stop-Conditions — keine Dokumentation. Alles Erklärende steht in `docs/` und wird von
> hier nur verwiesen.

## Was ist das

<Ein bis zwei Sätze. Details: `docs/PROJECT.md`.>

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
<install>
<dev>
<test>
<lint>
<typecheck>
<build>
```

<Nicht zutreffende Commands ausdrücklich als „n/a — <Grund>" markieren.>

## Regeln

- <Projektspezifische Regel, die nicht selbstverständlich ist>
- Keine neue Abhängigkeit ohne Begründung.
- Keine tragende Architekturentscheidung ohne ADR.
- Vor dem Commit: Lint, Typecheck und Tests laufen lassen.
- Keine Secrets im Code, in Logs oder in Fehlermeldungen.

## Constraints

- <Technische oder organisatorische Vorgaben, die nicht verhandelbar sind>

## Stop Conditions

Anhalten und fragen, wenn:

- Eine fachliche Anforderung unklar ist und erfunden werden müsste.
- Eine Architektur-, Persistenz- oder Deployment-Entscheidung offen ist.
- Authentication oder Authorization betroffen und nicht eindeutig geklärt ist.
- Zwei Quellen sich widersprechen.
- Eine Änderung schwer reversibel wäre.
- Ein Secret angelegt oder committet werden müsste.
