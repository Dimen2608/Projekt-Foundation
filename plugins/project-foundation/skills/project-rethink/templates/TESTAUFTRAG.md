# Testauftrag · Bereich `<NN>` · `<Name>`

> Der **Vertrag zwischen Spezifikation und Bau**. Diese Datei fügt keine neue Aussage über
> den Bestand hinzu: Jede Zeile stammt aus der Bereichsdatei und ist nur in Testreihenfolge
> gebracht. Was hier gemessen wurde und dort noch nicht steht, wird gekennzeichnet und
> **dorthin nachgetragen**.

**Bereich:** `<Pfad zur Bereichsdatei>`
**Messstand:** `<Stand mit Datum>` · Abgleich-Lauf: `<Ergebnis oder "leer">`
**Vorgabe:** `ABLAUF.md`, Phase GUARD. Sie wird hier **verwiesen, nicht abgeschrieben.**
**Freigabe:** Jede Zusammenführung geht direkt an den Menschen, nicht über eine Relaisstation.

## Vorbedingungen

Ohne die prüft dieser Auftrag etwas anderes, als er behauptet. Jede ist gegen den Messstand
gemessen, jede steht auch im Kopf der Bereichsdatei.

### 1. `<Aufbau-Vorbedingung>`

`<Was am Aufbau stimmen muss, und warum eine falsche Variante still grün wird. Mit
Belegstelle und dem Nachweis, dass der Bestandsaufbau es heute anders macht.>`

### 2. `<Zustands-Vorbedingung>`

`<Welcher Ausgangszustand nötig ist, damit die geprüfte Bedingung überhaupt erreicht wird.
Ein fehlender Zustand macht eine Negativkontrolle leer erfüllt — grün, weil sie den
falschen Zweig trifft.>`

### 3. Testbestand am eigenen Einstieg

| Maske | Ergebnis |
| --- | --- |
| `<stand-gebundene Maske>` | `<Treffer oder leer>` |
| dieselbe Maske gegen einen bekannten Treffer (**Positivkontrolle**) | `<Treffer — die Maske ist nicht kaputt>` |

## Fremde Einstiege mit Rolle

Verweis auf den gleichnamigen Abschnitt der Bereichsdatei. **Beide Hälften zählen:** Die
Bereichsdatei ist der Ort, an dem der Wächter nachsieht; dieser Auftrag ist der Ort, an dem
der Testbauer liest. Ein fremder Einstieg ohne Rolle ist ein Fund.

## Je Regel

### `<Xx-01>` — `<Zusage>`

| | |
| --- | --- |
| **Schnittstellenfassung** | `<Aufruf → erwartete Antwort → erwarteter Zustand danach. Beobachtbar von außen.>` |
| **Negativkontrolle** | `<Der Nachweis, dass der Test die Wirkung sehen würde, wenn sie einträte. Schreibt sie, bekommt sie eigene Daten — und hier steht das Kriterium, an dem die Trennung hängt, nicht die Absicht.>` |
| **Mutationserwartung** | `<Welche Stelle im Bestand verletzt wird — Datei:Zeile>` |
| **Form des Mutanten** | `entfernen` / `umkehren` — eine **Abschwächung zählt nicht als Probe** |
| **Erwartung** | Der Test wird rot. Bleibt er grün, ist nicht die Regel bestätigt, sondern der Test blind. |
| **Messstand der Probe** | `<Stand>` · Rückbau verifiziert: `<ja/nein>` |
| **Ergebnis** | `<Mutation · Testname · rot/grün>` — gehört in den Änderungstext, nicht nur hierher |

> **Wo eine Regel mehrere Türen hat**, bekommt jede Tür ihre eigene Fassung mit eigener
> Negativkontrolle. Eine Tür, die im Auftrag fehlt, ist im Test nicht vorhanden.

## Messstand für die Probe

- Die Probe läuft gegen einen **Wegwerf-Aufbau auf dem eigenen Arbeitspfad**, nie gegen
  einen geteilten.
- Sie verletzt **die Stelle, die die Regel trägt** — nicht eine Stelle in der Nähe.
- Nach jeder Probe wird der Rückbau gegen den Ausgangsstand verifiziert.
- Ein Test ohne belegte Probe zählt für den Wächter nicht als Test.

## Reihenfolge

`<Welche Regel zuerst, und warum. In der Regel: die, deren Aufbau die anderen mitbenutzen.>`

## Was dieser Auftrag ausdrücklich nicht baut

`<Kontrollen, die leer erfüllt wären, mit Begründung und Verweis auf die Entscheidung, die
das festgelegt hat. Eine leere Kontrolle ist schlimmer als keine — sie sieht aus wie eine.>`
