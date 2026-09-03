# ADR-0012: Der Ort der Architekturentscheidungen ist deklarierbar

## Status

Accepted — 2026-09-03. Ergänzt ADR-0008 in genau einem Punkt.

## Context

ADR-0008 hält die Pfadkonvention strikt und nimmt als Preis in Kauf, dass Bestandsprojekte
„umbenennen müssen". Der dritte Fremdtest (Atemluft.Cloud, 03.09.2026) hat gezeigt, dass das
nicht immer möglich ist: Das Projekt führt 45 ADRs in **einer** Datei
(`docs/architektur/decisions.md`, 4424 Zeilen) und greift absichtlich nur über ein
Indexwerkzeug darauf zu. Bei ehrlichem `Architecture Decisions: REQUIRED` blieben drei Wege —
die Datei in 45 Dateien zerlegen und das eigene Werkzeug aufgeben, `NOT REQUIRED` behaupten,
oder ein Alibi-ADR unter `docs/decisions/` ablegen. Das Alibi-Dokument ist genau das, was
ADR-0011 verhindern will; die Lüge ist schlimmer; der Umbau steht in keinem Verhältnis zur
Frage, die der Validator stellt.

Dieselbe Runde hat auch gezeigt, wo die Strenge **trägt**: `docs/PROJECT.md` erzwingt einen
Abschnitt `Out of Scope`, und genau das fehlte dem Projekt nach Urteil aller drei Reviewer.
`docs/ARCHITECTURE.md` erzwingt die Tabelle mit Authentication, Authorization und Secrets. Diese
Pflichten beantworten Fragen. Die Pflicht auf `docs/decisions/` beantwortet keine — die Frage
„Wo stehen Entscheidungen?" ist mit einer Sammeldatei ebenso beantwortet wie mit einem
Verzeichnis.

Damit widersprachen sich ADR-0008 („kein Alias erfüllt die Konvention") und ADR-0011 („Pflicht
liegt auf der Aussage, nicht auf dem Artefakt") an dieser einen Stelle. Festgehalten als OD-2
in `docs/PROJECT.md`, zunächst mit Entscheidung A (Strenge behalten), am 03.09.2026 nach dem
dritten Fremdtest neu entschieden.

## Decision

Die Zeile `Architecture Decisions` in `docs/ARCHITECTURE.md` darf in der dritten Spalte den Ort
der Entscheidungen nennen:

```
| Architecture Decisions | REQUIRED | docs/architektur/decisions.md — 45 ADRs, Zugriff über doku_index.py |
| Architecture Decisions | REQUIRED | `docs/adr/` |
| Architecture Decisions | REQUIRED | ADR-0001 hält die Wahl der Persistenz fest. |
```

Der Validator nimmt das erste Token mit Schrägstrich oder `.md`-Endung als Ort, mit oder ohne
Backticks. Fehlt ein solches Token, gilt `docs/decisions/` wie bisher. Dann:

- **Verzeichnis:** wird geprüft wie `docs/decisions/` — mindestens eine ADR-Datei
  (`STRUCT-011` sonst), jede Datei auf Abschnitte, Status und Namensmuster.
- **Datei:** mindestens ein Eintrag mit einer Überschrift wie `## ADR-001: …` (`STRUCT-011`
  sonst). Abschnitte und Status werden **nicht** geprüft. Der Validator kennt das Format einer
  Sammeldatei nicht und behauptet deshalb auch keine Prüfung.
- **Ort existiert nicht:** `STRUCT-010`, mit dem genannten Ort und den Beinahe-Treffern.
- **Ort zeigt aus dem Projekt heraus** (`..`, absoluter Pfad): `STRUCT-010`.

Warum das kein Alias im Sinne von ADR-0008 ist: Es ist keine Konfiguration im Manifest (die
erst existiert, wenn das Projekt konform ist) und keine wachsende Liste im Validator (die
niemand mehr überblickt). Es ist die Aussage im Dokument, das die Frage beantwortet — dieselbe
Form, in der ADR-0011 die ADR-Pflicht selbst an eine Aussage gebunden hat. Die Konvention bleibt
für alles andere strikt: `README.md`, `docs/PROJECT.md`, `docs/ARCHITECTURE.md` und das Manifest
haben weiterhin genau einen Ort.

Verworfene Alternativen:

- **Strenge behalten, Bestandsprojekte laufen ohne Ebene 1** (Ausnahme in `audit.md`). Hält
  den Code unverändert, macht `FOUNDATION READY` für jedes gewachsene Projekt aber per
  Definition unerreichbar, und die Ausnahme würde bei jedem Bestandsprojekt gezogen — eine
  Regel, die immer ausgesetzt wird, ist keine.
- **Sammeldatei als Format anerkennen und prüfen.** Erfordert ein zweites ADR-Format im
  Validator. Es gibt kein verbreitetes Sammeldatei-Format, das man prüfen könnte; jede Prüfung
  wäre erfunden.
- **`docs/adr/` fest als Alias.** Der Fall aus ADR-0008: die Liste wächst, der Validator prüft
  Selbstkonsistenz statt Konvention.
- **ADR-0011 zurücknehmen** (ADR-Verzeichnis immer Pflicht). Trifft kleine Projekte, um ein
  Problem großer zu lösen.

## Consequences

**Positiv**

- Ein gewachsenes Projekt kann ehrlich `REQUIRED` sagen, ohne umzubauen oder ein
  Alibi-Artefakt anzulegen. Der Anreiz aus OD-2 steht damit richtig herum: Die ehrliche Antwort
  ist nicht mehr die teurere.
- Der Validator prüft weiter, was er prüfen kann, und sagt, was er nicht prüft.

**Negativ**

- `STRUCT-010` verschiebt sich für den Fall „Ort erklärt und vorhanden" von Blocker auf
  nichts. Das ist die bewusste Aufweichung von ADR-0008 — in diesem einen Punkt.
- Zwei Projekte mit grünem Validator haben nicht mehr zwingend dieselbe Ablage für ADRs. Sie
  haben dieselbe Zeile, die sagt, wo sie liegt. Das ist der neue Stand der Konvention.
- Das erste pfadartige Token in der Begründungsspalte zählt. Wer dort eine andere Datei erwähnt
  (`siehe docs/ARCHITECTURE.md`), erklärt versehentlich einen falschen Ort. Die Meldung nennt
  den erkannten Ort, damit der Fehler sichtbar ist.
- Bei einer Sammeldatei steht die Architektur-Domäne auf `OK`, obwohl das ADR-Format nicht
  geprüft wurde. `OK` heißt weiterhin nur „kein struktureller Befund", nicht „geprüft und gut"
  (ADR-0010).

**Grenze**

Neu zu bewerten, wenn Projekte anfangen, den Ort auf Dateien zu setzen, die keine
Entscheidungen enthalten, um `REQUIRED` billig zu erfüllen. Dann nicht durch ein zweites
Format im Validator, sondern durch die Prüfung im Review (Ebene 2), das jeden erklärten Ort
öffnet.
