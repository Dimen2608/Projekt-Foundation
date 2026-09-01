# ADR-0007: Ausgabetexte des Validators bleiben ASCII

## Status

Accepted — 2026-09-01

## Context

`foundation-validate` brach unter Windows beim ersten Aufruf mit einem `UnicodeEncodeError`
ab, bevor eine einzige Zeile Report sichtbar wurde. Ursache waren die Rahmenzeichen der
Kopfzeile (`╔ ═ ╗`): Die Standardkonsole arbeitet dort mit Codepage 1252, und `print()`
schreibt auf einen `sys.stdout`, dessen Encoding die Konsole vorgibt.

Beim Aufräumen fiel auf: Der Rahmen war die **einzige** Nicht-ASCII-Stelle im gesamten
`src/`. Sämtliche Meldungstexte sind konsequent ASCII — „pruefen", „fehlt", „unzulaessig",
„enthaelt". Das ist zu systematisch für Zufall, war aber nirgends festgehalten. Eine
ungeschriebene Regel, die nur zufällig eingehalten wird, ist keine Regel: Der Rahmen war
genau die Stelle, an der sie gebrochen wurde, und sie hat das Werkzeug für jeden
Windows-Nutzer unbrauchbar gemacht.

ADR-0005 regelt die *Sprache* (deutscher Fließtext, englische Keywords), sagt aber nichts
über den *Zeichenvorrat*.

## Decision

**Alles, was der Validator auf stdout oder stderr schreibt, ist reines ASCII.**

Das betrifft `reason`, `required_action`, alle Report-Bestandteile und Fehlermeldungen der
CLI. Konkret: keine Umlaute (`ue` statt `ü`), keine typografischen Anführungszeichen, kein
Gedankenstrich `—`, kein `…`, keine Box-Zeichen.

Nicht betroffen sind Docstrings, Kommentare, Tests und die Dokumentation unter `docs/` —
diese werden gelesen, nicht auf eine Konsole geschrieben, und dürfen deutsche Rechtschreibung
verwenden.

Wo eine Rahmengrafik gewünscht ist, prüft `stream_supports_box()` vorab die Encoding-Fähigkeit
des Zielstreams und weicht auf einen ASCII-Rahmen aus. Das ist die einzige zulässige Form,
Nicht-ASCII auszugeben: als Zugabe, die bei Bedarf entfällt — niemals als einzige Variante.

Bewusst **nicht** gewählt: `sys.stdout.reconfigure(encoding="utf-8")`. Das verhindert zwar
den Absturz, schickt aber Bytes an eine Konsole, die sie nicht darstellen kann. `errors=
"replace"` erzeugt Buchstabensalat statt eines Rahmens.

## Consequences

**Positiv**

- Der Validator läuft auf jeder Konsole, ohne dass der Aufrufer `PYTHONIOENCODING` kennen muss.
- Die Regel ist mechanisch prüfbar: Ein Test mit erzwungener cp1252-Codepage fängt jeden
  Rückfall, unabhängig davon, auf welcher Plattform die CI läuft.

**Negativ**

- Deutsche Meldungstexte lesen sich mit „ue"/„ae"/„oe" holprig. Das ist der Preis dafür,
  dass sie überhaupt erscheinen.
- Wer neue Meldungen schreibt, muss die Regel kennen. Sie steht deshalb hier und nicht nur
  im Code.
