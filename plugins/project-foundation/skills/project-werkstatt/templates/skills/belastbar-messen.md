---
name: belastbar-messen
description: "Belastbare Befunde und Vollzugsmeldungen in {{PROJEKT}}: Aufbau prüfen, Abwesenheit mit ausgeführter Maske und Positivkontrolle belegen, Zahlen mit Zähleinheit und Stand nennen, Ungemessenes als „nicht gemessen“ kennzeichnen. Verwende ihn immer, wenn eine Aussage über einen Zustand entstehen soll: „ist X schon drin?“, „läuft Y?“, „wie viele Z gibt es?“, „fehlt“, „gibt es nicht“, „hat der Fix gewirkt?“, in Befund, Prüfbericht, Vollzug und PR-Text sowie vor einem Auftrag, der Ort, Nummer oder Zahl nennt. Nicht bei reiner Code-Änderung ohne Aussage über einen Zustand (Umbenennen, Formatieren, Feature bauen)."
---

<!--
Vorlage aus project-werkstatt (auslösender Skill). Ziel:
.claude/skills/{{PLUGIN}}/skills/belastbar-messen/SKILL.md (Sperrpfad). Höchstens 500 Zeilen,
Beschreibung höchstens 700 Zeichen und in Anführungszeichen. Evals: e-1 (löst aus), e-2 (bleibt
still) unter templates/skills/eval-faelle/. Diesen Kommentar beim Kopieren entfernen.
-->

# Belastbar messen

Die häufigste Fehlerklasse ist nicht der falsche Code, sondern der falsche Befund: eine Messung, die
eine ehrliche Antwort auf die falsche Frage gibt. Zwei Gesichter davon:

- **Abwesenheit sieht aus wie Bestätigung.** Die Suche fand nichts, also „gibt es nicht“. Dabei konnte
  die Suche gar nichts finden.
- **Nachweis ohne Wirkung.** Etwas ist dokumentiert, gelaufen oder grün, aber es hat nichts geprüft.

Der Skill gilt für jede Rolle. Was `.claude/rules/regeln.md` verlangt (Objekt, Maske und Messzeitpunkt
nennen), steht dort; hier steht das Handwerk dazu.

## 1. Die Kernregeln

1. **Maske ausführen, nicht lesen.** Eine Zahl oder Aufzählung kommt aus einem Befehl, den du gefahren
   hast. Aus dem Gedächtnis, einem Kommentar oder einem Bericht übernommen ist sie „ungemessen“.
2. **Abwesenheit braucht zwei Kontrollen:** die ausgeführte Maske und eine Positivkontrolle (ein Fall,
   von dem du weißt, dass er treffen muss).
3. **Jede Zahl nennt ihre Zähleinheit** (Dateien, Zeilen, Datensätze, Aufrufstellen, Tests) und ihren
   Stand (SHA).
4. **Was du nicht gemessen hast, steht als „nicht gemessen“ im Bericht.** Raten ist kein dritter
   Zustand, und eine ehrliche Lücke ist mehr wert als eine unbelegte Zusicherung.
5. **Eine Bestätigung misst anders als der Fund, den sie prüft.** Dasselbe Suchmuster ein zweites Mal
   bestätigt das Muster, nicht die Aussage.

## 2. Der Auslöser gilt auch für Aufträge

Ein Auftrag, der einen Ort, eine Nummer oder eine Zahl nennt, trägt dieselbe Messpflicht wie ein
Befund. Ein falscher Fakt im Bericht wird widerlegt, einer im Auftrag vervielfältigt.

- **Nummern und Orte vor dem Auftrag nachschlagen,** nicht aus dem Gedächtnis einsetzen. Eine falsche
  Nummer, die existiert, besteht jede Plausibilitätsprüfung.
- **Eine Zeile als Beleg verankerst du an der Struktur** (Konstruktor, Typ, Aufrufort), nicht am
  Feldwert.
- **Die Prämisse steht als eigener Satz mit Quelle im Auftrag.** Gültig sind der Code, eine benannte
  Messung und die Spezifikation `{{SPEC_ORT}}`. Ein eigener Bericht ist keine Quelle.
- **Ein Lösungsvorschlag im Ticket ist eine zweite Prämisse,** getrennt von der Ursache. Beide werden
  gemessen.

## 3. Bevor du misst: steht der Aufbau noch?

Erst Aufbau, dann Gültigkeit, dann Messwert.

- **Existiert das Gemessene noch?** Ein anlegender Commit belegt die Existenz zum Zeitpunkt der
  Abfassung, nicht der Ausführung. `git ls-tree <ref> <pfad>` kostet Sekunden.
- **Läuft es, oder liegt es nur da?** Bei Wächtern, Timern und Gates weist du die Ausführung selbst
  nach und siehst einen echten Lauf.
- **Eine dokumentierte Regel ist keine wirksame Regel.** Frag, wodurch sie wirkt: ein Feld, das
  gelesen wird, ein Hook, der feuert, ein Gate, das blockiert. Ohne Mechanismus hast du eine
  Absichtserklärung gemessen.
- **Das Auswertungskriterium steht vor der Messung, und eine Sonde variiert genau einen Faktor.**
- **Die Messumgebung bildet die des Ziels nach.** „Bei mir grün“ ohne Umgebungsangabe ist keine Aussage.

## 4. Das Messmittel ist zuerst verdächtig

Sagt jede Probe dasselbe oder meldet eine Prüfung plötzlich viele Funde, ist zuerst die Probe
verdächtig, nicht die Wirklichkeit.

- **Sechsmal null** ist eher ein Formatfehler im Muster als sechs fehlende Einträge. **Auffällig viele
  Funde:** zwei Soll/Ist-Paare von Hand vergleichen, bevor du dem Ergebnis glaubst.
- **Zwei eigene Suchen derselben Quelle widersprechen sich:** Findet das breitere Muster weniger als
  das engere, ist es fehlerhaft.
- **Kandidatenlisten nie aus Ausgabe für Menschen ableiten.** Gekürzte Pfade lassen Dateien still aus
  der Prüfung fallen. Nimm das Maschinenformat (`--name-only`, JSON).
- **Die Eigenschaft am Objekt messen, nicht an der Umgebung.** Fremder Verkehr auf einem geteilten
  Zähler misst nicht, was du behaupten willst.
- **Werkzeuge verschieben Werte still:** Zeitzonen, Pfadumschreibung der Shell, Vorgabe-Limits.
- **Eine Zählung zählt Erwähnungen, nicht Datensätze.** Verankere die Extraktion an der Struktur
  (Spalte, JSON-Schlüssel, Zeilenanfang).
- **Eine gekappte Liste sieht aus wie ein vollständiges Ergebnis.** `--limit`, `head -n` und
  Seiten-APIs schneiden ab, ohne es zu zeigen. Frag je Objekt gezielt ab, oder nenne die Reichweite:
  „bis #N geprüft, kein PR“, nicht „kein PR gefunden“.

### Die Wegwerf-Auswertung ist ein Messmittel

- **Werte fail-closed aus.** Grün ist, was ein positives Erfolgsmerkmal trägt (Exit-Code 0, „N
  passed“). Ein `case … *) grün` verbucht eine leere Ausgabe als Erfolg.
- **Füttere die Auswertung einmal mit dem Fall, den sie melden soll, und einmal mit leerer oder
  abgebrochener Eingabe.** Meldet sie beide Male dasselbe, misst sie nichts.
- **Exit-Codes nie durch eine Pipe erfassen:** `cmd | tee log` liefert den Code des letzten Glieds;
  sonst `set -o pipefail`.

## 5. Negativbefunde brauchen zwei Kontrollen

- **Kontrolle über die Adresse, bevor über den Inhalt.** Ein leeres Ergebnis heißt zuerst „hier ist
  nichts“, erst dann „das gibt es nicht“. Belege vorher, dass Pfad, Tabelle und Spalte existieren.
- **Eine Operation auf einem Objekt misst du über Typ, Klasse oder Aufrufort, nie über den
  Variablennamen.** Ein Bezeichner-Muster greift nicht, wo Variablen generisch heißen.
- **Kontrolle über die Suchbegriffe.** Wer „kommt nicht vor“ berichtet, prüft vorher an einer Stelle,
  die treffen muss. Der Text sagt vielleicht „zurücksetzen“, du suchtest „wiederherstellen“.
- **Null Fehlschläge sind kein Wirksamkeitsbeweis.** Lies bei jedem Guard das Prädikat gegen den
  Schadensfall und löse ihn einmal absichtlich aus.
- **Negativprobe vor der Erfolgsmeldung.** Änderung testweise zurücknehmen und prüfen, dass der neue
  Test rot wird.

**Auch ein Positivbefund braucht einen Kontrollarm.** Benennt eine Messung eine Ursache (Version,
Schalter, Commit), ist sie ein Vergleich. Miss die Gegenprobe mit der alten Fassung; läuft die auch
durch, ist die Ursache offen.

**Eine Kontrolle, die den Zustand verändert, ist keine Kontrolle.** Prüfe vor jedem wiederholten
Kontrollaufruf, ob die Lage, die du selbst hergestellt hast, ihn scharf gemacht hat. Wird die
Gegenprobe blockiert, suche nicht den Umweg; benenne die Eigenschaft und miss sie eingriffsfrei.

## 6. Ein Signal, ein Objekt

- **Nie „der neueste Lauf“, immer die ID.** Fremd-fertig mit eigen-fertig zu verwechseln sieht aus
  wie Erfolg.
- **Ein Signal, das zwei Zustände bedeutet, ist blind für den schlimmeren.** Warten braucht eine
  Deadline und drei unterscheidbare Zustände: nicht erzeugt, wartet, läuft.
- **Trägt ein Folge-Lauf nie den SHA des Auslösers,** lies den Stand am Ziel (`git rev-parse HEAD`
  dort, `git merge-base --is-ancestor`).
- **Ein grüner Teil-Check ist kein Beweis.** Teste die exakte reale Invocation, nicht ihr Bruchstück.

## 7. Die Quelle, nicht die Wiederholung

- **Zwei Zählungen aus derselben Quelle sind keine Bestätigung.** Bei widersprüchlichen Zahlen
  vergleichst du zuerst die Quelle, dann die Methode.
- **Eine Messung an einem Aufrufer belegt nichts über andere** (Hauptsitzung, Subagent, CI).
- **Ein wahrer Nebenbefund ist kein Kausalbeleg.** Stützt er eine Hypothese, die du schon hast, suche
  die Gegenbelege.

## 8. Gegen welchen Stand misst du?

- **Für „den aktuellen Stand“ liest du nach `git fetch` aus der Referenz** (`git show
  origin/main:<pfad>`, `gh api`). Im geteilten Arbeitsbaum liest `grep` einen unbekannten Stand.
- **Ein Widerspruch zwischen zwei eigenen Befunden ist erst dann ein Messfehler, wenn beide denselben
  Zeitpunkt meinen.** Bei mehreren Sessions ist die häufigste Erklärung die veränderte Welt.
- **„Unter Störung gemessen“ ist ein eigener Befundzustand,** weder sauber noch ungültig. Schreibe die
  Einschränkung auf.
- **Betrifft der Befund deine eigene Änderung, miss gegen den Stand vor ihr,** mit genau einer
  Variable. „Mit der Änderung passiert X“ trägt erst, wenn „ohne sie passiert X nicht“ mitgemessen
  wurde.
- **Testreihenfolge erzeugt Zustand.** Nenne, ob einzeln oder in der Suite gemessen wurde. Rot nur in
  der Suite: das Paar `<unbeteiligte_datei> <test>` gegen `<neue_datei> <test>` entscheidet, wer
  verschmutzt.

## 9. Vom Teil aufs Ganze

- **Wird eine Aussage über ein Ganzes aus einem Teil abgeleitet, gehört die Herkunft in den Befund:**
  „gelesen in X“ statt „ist so“.
- **Wer einen Handler nur bis zur ersten Fehlerprüfung liest, hat die Hälfte gelesen.** Prüfe am
  Zustandsübergang, und ob es neben dem Lesepfad einen Schreibpfad gibt.
- **„Ist es ersetzt?“ beantwortest du je Einstiegspunkt, nicht je Datei.**

## 10. Wenn Messungen sich widersprechen

- **Drei sorgfältige Messungen, drei Zahlen:** Die Definition ist unscharf, nicht die Ausführung.
  Vergleiche zuerst die Methode; hängt die Aussage nicht an der genauen Zahl, schreibe eine Spanne.
- **Bei roter Baseline ist nur das Delta belastbar.** „Identische Zahlen vor und nach der Änderung“,
  nicht „grün“.

## 11. Wie ein Befund berichtet wird

- **Eine PR-Beschreibung ist ein Bericht.** Jede Pfad-, Zahl- und Statusangabe darin braucht Beleg.
- **„Nicht verifizierbar“ aus einem Subagent ist eine Hypothese.** Rechne die Schlussfolgerung selbst
  nach, gerade wo sie bequem ist.
- **Ein Proxy-Signal ist kein Befund, und ein Zitat wird durch Weitergabe nicht zur Messung.**
- **Jede Zahl, die du hinterlässt, trägt Datum, Messort und Messenden,** oder sie ist als ungeprüfte
  Übernahme gekennzeichnet: „am TT.MM.JJJJ in `<umgebung>` gemessen: `<wert>`“.

## 12. Wenn du eine Messung beauftragst

Drei Sätze gehören in jeden Messauftrag:

1. **Was genau gemessen wird** (das Prädikat, nicht die Absicht).
2. **Unter welcher Bedingung der Messwert ungültig ist.**
3. **Keine Ursachendeutung.** Messwert berichten, den Schluss zieht der Auftraggeber.

Prämissen im Auftrag sind Behauptungen, auch Pläne aus dem eigenen Repo: Prüfe pro Eintrag, nicht
pro Dokument. Deine eigene Diagnose ist eine der zu prüfenden Hypothesen.

## 13. Der Abgleich am Anfang

Vor einer Untersuchung prüfst du, ob die Antwort schon in der Spezifikation oder den Entscheidungen
steht. Eine dokumentierte Lehre verhindert den Fehler aber nicht: Wo es zählt, gehört die Absicherung
in die Maschine (Hook, Gate, Test).
