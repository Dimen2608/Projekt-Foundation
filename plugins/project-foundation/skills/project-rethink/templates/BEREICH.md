# Bereich `<NN>` · `<Name>`

> Was dieses System **heute tut** — nicht, was es tun sollte. Der Wunsch steht im
> Abnahmekriterium und ist als solcher gekennzeichnet.

**Messstand:** `<Stand mit Datum>`
**Eigentümerschaft:** `<Modul/Router/Paket>` — dieser Bereich besitzt es, kein anderer.
**Kürzel:** `<Xx->` — eindeutig, nirgends sonst vergeben, wird nie umbenannt.
**Tor:** `<Datum>` · `<n>` Funde · `<n>` behoben · `<n>` offen · **Freigabe: ja / nein**
**Offene Lücken:** Verweis auf `LUECKEN.md`. **Dieser Abschnitt trägt keine eigene Zahl.**

**Einstieg** = jeder von außen aufrufbare Zugang: HTTP-Route, CLI-Kommando, Job,
Queue-Consumer, UI-Aktion, öffentliche Bibliotheksfunktion.

## Zielbild und Abnahmekriterium

**Zielbild (ein Satz):** `<Was dieser Bereich leisten soll.>`

**Abnahmekriterium:** `<Woran erkennt man, dass der Bereich fertig ist — prüfbar, nicht
gefühlt. Wörtlich aus der fachlichen Quelle zitiert, mit Stand der Abnahme; nicht
paraphrasiert.>`

Ein Bereich mit eigenen Einstiegen hat ein Kriterium. Ein Querschnitt hat keine eigenen
Einstiege und deshalb keins.

## Einstiegstabelle

Alle Einstiege, die dieser Bereich besitzt. Erhoben per Maske, nicht von Hand.

**Zähleinheit:** ein Paar (Methode, Pfad); Parameter normalisiert.
**Maske:** `<ausgeführter Befehl, stand-gebunden>`

| Einstieg | Was er tut | Schreibt | Absichernder Test |
| --- | --- | --- | --- |
| `<METHODE /pfad>` | `<ein Satz>` | `<Zustand oder "nichts">` | `<Datei::Funktion>` oder `Offen: L-NN` |

## Regeln

Je Regel: Kürzel, Zusage, Belegstelle, Ebene, Vorbehalt. **Eine Regel ohne Beleg und ohne
Lückeneintrag ist eine Meinung.**

### `<Xx-01>` — `<Zusage in einem Satz>`

- **Schnittstellenfassung:** `<Was sieht der Aufrufer, wenn die Regel greift — Statuscode,
  Antwort, Zustand danach. Nicht: was eine interne Funktion zurückgibt.>`
- **Belegstelle:** `<datei:zeile>` (Stand `<…>`) — `<wörtlicher Auszug oder Kern>`
- **Ebene:** `DB | Code | beides | entfällt` — „entfällt" nur für Regeln ohne Nebenwirkung,
  damit ein leeres Feld nie als „keine Nebenwirkung" gelesen wird.
- **Absicherung:** `<Datei::Funktion>` oder `Offen: L-NN`
- **Vorbehalt:** `<Was diese Regel nicht behauptet. Aussagen über Häufigkeit oder Betrieb
  gehören hierher, nicht in die Zusage.>`

> **Abwesenheitsaussage?** Dann statt einer Belegstelle eine **ausgeführte Maske über alle
> Kandidaten**, mit Zähleinheit, Messstand, Ausgabe und Positivkontrolle. Das gilt auch für
> Ausschließlichkeit („die einzige Stelle", „nirgendwo sonst") — ein positives Zitat belegt
> nur die genannte Stelle.

## Fremde Einstiege mit Rolle

Einstiege, die einem anderen Bereich oder einem Querschnitt gehören und hier vorkommen.
**Ohne Rolle steht hier keiner.**

Kriterium je Zeile: *Kann ein Test dieses Bereichs rot werden, weil sich das Verhalten
**dieses** Einstiegs ändert?* **Ja → Prüfgegenstand**, der Test gehört dem besitzenden
Bereich, hier steht nur der Verweis. **Nein → Werkzeug**, er bleibt hier und trägt seine
Rolle.

| Einstieg | Gehört zu | Rolle hier | Frage | Warum die Zeile trotzdem hier steht |
| --- | --- | --- | --- | --- |
| `<METHODE /pfad>` | `<Bereich NN oder Querschnitt>` | Vorbedingung / Zählpunkt / Beobachtungspunkt | Ja / Nein | `<Begründung, bei "Ja" zwingend>` |

Ist die Zusage einer Regel ein **Vergleich über Bereichsgrenzen**, ist die Frage für jede
Zeile mit Ja zu beantworten. Dann bleibt der vergleichende Test beim Aufrufer — mit einer
Begründung **je Zeile** —, und die Einzeltests gehören ihren Bereichen.

## Datenmodell aus Sicht dieses Bereichs

Was die Felder **für diesen Bereich** bedeuten — nicht das abgeschriebene Schema.

| Feld | Bedeutung hier | Wer schreibt es | Leerwert erlaubt |
| --- | --- | --- | --- |

## Nicht abgedeckt

Was dieser Bereich ausdrücklich **nicht** beschreibt, und wohin es gehört. Eine leere
Aufzählung ist eine Aussage und wird als solche begründet.

## Lücken

Verweis auf `LUECKEN.md`, gefiltert auf diesen Bereich, mit der **ausgeführten Maske**, die
den Filter erzeugt hat. Keine eigene Zählung, keine Kopie der Einträge.
