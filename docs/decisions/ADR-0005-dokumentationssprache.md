# ADR-0005: Deutscher Fließtext mit englischen Struktur-Keywords

## Status

Accepted — 2026-09-01

## Context

Die Vorlagen und der Skill müssen für den Betreiber dieses Repos gut lesbar sein
(deutschsprachig), gleichzeitig aber Statuswerte tragen, die maschinell geprüft und in
Reports ausgegeben werden.

Übersetzte Statuswerte (`BESTANDEN`, `BLOCKIERT`) hätten drei Nachteile: Der Validator
müsste beide Sprachen kennen, der geforderte Report-Wortlaut ist englisch, und die Begriffe
`ADR`, `Context/Decision/Consequences`, `Scope`, `MVP` sind als Fachbegriffe etabliert.

## Decision

- **Fließtext, Erklärungen, Begründungen:** Deutsch.
- **Struktur-Keywords:** Englisch und unübersetzt —
  `PASS` / `WARNING` / `BLOCKED` / `UNKNOWN`,
  `RELEVANT` / `NOT REQUIRED` / `FUTURE` / `UNKNOWN`,
  `Proposed` / `Accepted` / `Rejected` / `Superseded` / `Deprecated`,
  Abschnittsnamen wie `Purpose`, `Scope`, `MVP`, `Out of Scope`,
  `Context` / `Decision` / `Consequences`.
- **Code, Bezeichner, Docstrings:** Docstrings deutsch, Bezeichner englisch.
- **Audit-Report:** unverändert englisch, wie im Prozess festgelegt.

## Consequences

**Positiv**

- Der Validator braucht nur einen Satz Schlüsselwörter.
- Vorlagen bleiben für internationale Projekte brauchbar, weil die Struktur englisch ist.

**Negativ**

- Gemischte Sprache wirkt für Außenstehende zunächst inkonsistent. Die Trennlinie ist aber
  klar: alles, was der Validator liest, ist englisch; alles, was ein Mensch liest, ist deutsch.
- Bei einer späteren Umstellung auf durchgängig Englisch sind alle Vorlagen betroffen.
