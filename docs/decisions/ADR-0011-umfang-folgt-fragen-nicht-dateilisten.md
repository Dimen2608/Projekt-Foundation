# ADR-0011: Der Foundation-Umfang folgt Fragen, nicht einer Dateiliste

## Status

Accepted — 2026-09-02

## Context

Das Toolkit verlangte von jedem Projekt denselben Satz: `README.md`, `STATUS.md`,
`CLAUDE.md`, `docs/PROJECT.md`, `docs/ARCHITECTURE.md`, `.project-foundation.yml`, das
Verzeichnis `docs/decisions/` und darin **mindestens ein ADR**. Das Manifest verlangte elf
Pflichtfelder, von denen der Validator vier benutzte.

Das widerspricht dem eigenen Leitsatz *the foundation must remain smaller than the system
it enables*. Konkret entstanden drei Fehler:

1. **Erzwungene ADRs.** `ADR count == 0 → BLOCKED` behandelt „es gab keine tragende
   Entscheidung" wie „die Entscheidung wurde verschwiegen". Der erste Fall ist bei
   kleinen Projekten der Normalfall. Die Regel produzierte dort Alibi-ADRs — genau die
   Sorte Dokument, vor der `anti-overengineering.md` warnt.
2. **Erzwungenes `STATUS.md`.** Sinnvoll, sobald mehrere Personen oder Sessions
   beteiligt sind. Für ein Ein-Personen-Projekt eine Datei, die veraltet und dann lügt.
3. **Aufgeblähtes Manifest.** `stack`, `architecture`, `infrastructure`, `quality_gates`,
   `project.type`, `project.maturity` standen doppelt: einmal in den Dokumenten, einmal
   maschinenlesbar. Gelesen wurde nichts davon. Damit war das Manifest auf dem Weg zur
   zweiten Wahrheitsquelle — dem Zustand, den ADR-0004 ausdrücklich verhindern soll.

## Decision

Ein Artefakt ist Pflicht, wenn ohne es eine notwendige Frage unbeantwortet bliebe — nicht,
weil es zum Standardsatz gehört. Der Denkweg ist `Frage → notwendiges Wissen → Artefakt`.

**Immer Pflicht**, weil ohne sie niemand ohne Raten arbeiten kann:

| Frage | Artefakt |
| --- | --- |
| Wie starte und benutze ich es? | `README.md` |
| Was bauen wir, was nicht? | `docs/PROJECT.md` |
| Wie ist es strukturiert? | `docs/ARCHITECTURE.md` |
| Woran erkennt ein Werkzeug die Foundation? | `.project-foundation.yml` |
| Was muss ein AI-Agent wissen? | `CLAUDE.md` **oder** `AGENTS.md` |

**Bedingt**, mit maschinell prüfbarer Bedingung:

- **ADRs.** `docs/ARCHITECTURE.md` beantwortet in der Bereichstabelle
  `Architecture Decisions` mit `REQUIRED` oder `NOT REQUIRED`. Bei `REQUIRED` blockieren
  ein fehlendes `docs/decisions/` und ein leeres Verzeichnis wie bisher. Bei
  `NOT REQUIRED` wird kein ADR verlangt. Fehlt die Aussage und gibt es kein ADR, ist das
  eine **Warnung** (`ADR-010`): unbeantwortet ist nicht dasselbe wie beantwortet, aber
  auch kein struktureller Fehler.
- **`STATUS.md`** ist optional (`STRUCT-002` entfällt). Existiert die Datei, wird sie
  unverändert geprüft — inklusive `STAT-002`, das eine selbst gemeldete `BLOCKED`-Domäne
  weiterhin zum Blocker macht.

**Manifest:** Pflicht sind nur noch `schema_version` und `foundation.status`. Alles andere
wird geprüft, wenn es da ist, und sonst nicht verlangt.

Verworfene Alternativen:

- **Alles optional machen.** Macht die Foundation beliebig und den Validator wertlos. Die
  fünf „immer"-Artefakte bleiben ohne Ausnahme.
- **Pflichtumfang aus `project.type`/`maturity` ableiten** (`library` braucht weniger als
  `service`). Klingt sauber, ist aber erfunden: Es gibt keine Erfahrung, die diese
  Zuordnung stützt, und sie wäre schwer zu widerlegen. Später möglich, wenn genug Projekte
  durch das Werkzeug gelaufen sind. Bis dahin: `FUTURE IDEA`.
- **ADR-Pflicht an die Zahl der `RELEVANT`-Bereiche knüpfen.** Ein automatisch abgeleiteter
  Schwellenwert, den niemand begründen kann — dieselbe Willkür wie vorher, nur besser
  versteckt.
- **Die Aussage ins Manifest legen** statt nach `docs/ARCHITECTURE.md`. Widerspricht
  ADR-0004: Die inhaltliche Aussage gehört ins Dokument, das Manifest indiziert nur.

## Consequences

**Positiv**

- Ein kleines Projekt kann `FOUNDATION VALID` erreichen, ohne ein ADR zu erfinden oder ein
  `STATUS.md` zu pflegen, das niemand liest.
- Das Manifest hat keinen Anlass mehr, zur zweiten Dokumentation zu werden.
- Die Pflicht liegt auf der **Aussage**, nicht auf dem Artefakt. Das ist die Form, in der
  sich der Validator nicht überschätzt: Er prüft, dass die Frage beantwortet wurde, nicht
  ob die Antwort stimmt.

**Negativ**

- Ein Projekt kann sich mit `Architecture Decisions: NOT REQUIRED` an einem nötigen ADR
  vorbeischreiben. Maschinell nicht zu verhindern; deshalb prüft das Review (Ebene 2)
  jedes `NOT REQUIRED` gegen den Code, und `reference/audit.md` nennt „fehlendes ADR"
  ausdrücklich als Blocker auch dann, wenn die Zeile das Gegenteil behauptet.
- `docs/ARCHITECTURE.md` bekommt eine Zeile mehr — der Preis dafür, dass an anderer Stelle
  ganze Dateien entfallen.
- `STRUCT-002` ist zurückgezogen. Die ID wird nicht neu vergeben (Repo-Regel: IDs werden
  nicht umgewidmet).
- Bestehende Manifeste bleiben gültig: Es entfallen nur Anforderungen, es kommen keine
  hinzu. `schema_version` bleibt deshalb bei `1`.

**Grenze**

Neu zu bewerten, wenn sich zeigt, dass `NOT REQUIRED` in der Praxis als Schlupfloch
benutzt wird — dann nicht durch eine härtere Maschinenregel, sondern durch eine schärfere
Prüfung im Review.

## Nachtrag — 2026-09-02

Der erste Lauf gegen ein Fremdprojekt nach dieser Entscheidung hat eine Wechselwirkung mit
ADR-0008 gezeigt, die beim Entwurf nicht bedacht war:

Ein Projekt mit 14 ADRs in `docs/adr/` bekommt bei ehrlichem `REQUIRED` den Blocker
`STRUCT-010` — bleibt die Zeile weg, nur eine Warnung. **Die ehrlichere Antwort ist die
teurere.** Zusätzlich behauptete die Warnung wörtlich, es gebe kein ADR, obwohl der
Validator die 14 Dateien kannte und im alten Blockertext sogar genannt hatte.

Behoben wurde der falsche Text: `ADR-010` nennt jetzt das gefundene Verzeichnis samt Anzahl
und warnt vor dem Blocker, den `REQUIRED` auslösen würde. Die Schieflage selbst bleibt
bestehen und ist als `OD-2` in `docs/PROJECT.md` festgehalten — die Strenge aus ADR-0008
wird nicht auf Verdacht aufgeweicht.
