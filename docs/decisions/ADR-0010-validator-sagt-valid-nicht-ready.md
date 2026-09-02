# ADR-0010: Der Validator sagt VALID, nicht READY

## Status

Accepted — 2026-09-02

## Context

Der Validator gab bisher `FOUNDATION READY` aus, denselben Wortlaut, mit dem der Skill
den vollständigen Foundation-Prozess abschließt. Damit behauptete ein Programm eine
Aussage, die es nicht treffen kann.

Was der Validator entscheiden kann: existiert die Datei, hat sie die Abschnitte, ist der
Statuswert erlaubt, widersprechen sich zwei Quellen. Was er nicht entscheiden kann: ob der
Scope sinnvoll ist, ob die Architektur trägt, ob die Tests schützen oder nur Coverage
erzeugen, ob ein Agent tatsächlich genug Kontext hat.

Der Unterschied war in `README.md` und `SKILL.md` als Warnsatz vermerkt („Ein grüner
Validator ist keine gute Foundation"). Ein Warnsatz neben einer Ausgabe, die das Gegenteil
suggeriert, verliert diesen Wettbewerb: In der Praxis steht am Ende `FOUNDATION READY` auf
dem Bildschirm, und genau das wird zitiert.

Verschärfend kamen zwei kleinere Unehrlichkeiten dazu:

- Der Domänenstatus im Report übernahm hilfsweise den in `STATUS.md` **erklärten** Wert.
  Der Validator gab damit eine fremde Selbstauskunft als eigenes Prüfergebnis aus.
- Für `Development Setup` und `CI/CD & Infrastructure` hat er überhaupt keine Regel,
  meldete aber `PASS`.

## Decision

Der Validator endet auf `FOUNDATION VALID` bzw. `FOUNDATION INVALID`. Der Kopf des Reports
heißt `PROJECT FOUNDATION VALIDATION`. `FOUNDATION READY` bleibt ausschließlich dem
vollständigen Prozess vorbehalten — Review durch einen Agenten (Ebene 2) und Entscheidung
durch den Menschen (Ebene 3).

Zusätzlich:

- Der Domänenstatus wird ausschließlich aus eigenen Befunden abgeleitet: `OK`, `WARNING`
  oder `BLOCKED`.
- Domänen ohne eigene Regel melden `NOT CHECKED` statt `OK`.
- `Result.ready` heißt `Result.valid`.

Verworfene Alternativen:

- **Wortlaut lassen, Warnsatz verstärken.** Sieben Monate Erfahrung mit demselben Warnsatz
  sprechen dagegen. Der Ausgabetext gewinnt gegen die Fußnote.
- **Prozentwert oder Score ausgeben.** Ein Zahlenwert täuscht eine Genauigkeit vor, die
  weder Ebene 1 noch Ebene 2 hat. Bleibt ausgeschlossen (`reference/audit.md`, §5).
- **Den Validator um qualitative Prüfungen erweitern**, damit `READY` wieder stimmt. Das
  hieße, ein Programm zu bauen, das Architekturqualität beurteilt. Nicht machbar, und der
  Versuch würde die Grenze zwischen den Ebenen endgültig verwischen.

## Consequences

**Positiv**

- Die Ausgabe deckt sich mit dem, was der Code beweisen kann.
- Der Unterschied zwischen „strukturell in Ordnung" und „inhaltlich tragfähig" ist an der
  Oberfläche sichtbar und muss nicht erklärt werden.
- Der Report kann keine Domäne mehr grün melden, die nie geprüft wurde.

**Negativ**

- Ein Bruch für alle, die auf den Ausgabetext geprüft haben. Die Exit-Codes bleiben
  gleich, der Wortlaut nicht.
- Der bis dahin festgelegte Report-Wortlaut in `CLAUDE.md` wurde damit doch geändert.
  Das war eine Stop Condition; die Entscheidung fiel bewusst und wird hier festgehalten
  statt beiläufig vollzogen.
- Zwei ähnliche Reports (Validierung und Audit) können verwechselt werden. Gegenmittel:
  unterschiedliche Kopfzeile, unterschiedliche Endzeile, ein Absatz dazu in
  `reference/audit.md`.

**Grenze**

Neu zu bewerten, falls der Validator je Prüfungen bekommt, die tatsächlich über
inhaltliche Eignung entscheiden. Nach heutigem Stand ist das kein absehbarer Fall.
