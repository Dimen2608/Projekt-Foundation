# Die Grundsätze, ausführlich

Gezielt nachladen, nicht vorab lesen. `SKILL.md` nennt jeden Grundsatz in einem Satz mit
Filtersatz; hier steht, **warum er bricht, wenn man ihn weglässt**, mit einem generischen
Beispiel.

Ein Grundsatz ohne Filtersatz ist ein Vorsatz. Der Filtersatz ist der Einwand, der in der
Praxis kommt — und die Antwort darauf in einem Halbsatz. Ohne ihn wird jeder Grundsatz beim
nächsten Termindruck neu verhandelt.

---

## Messen und Belegen

### 1 · Eine Abwesenheitsaussage braucht eine ausgeführte Maske

**Warum es bricht.** „Hier passiert nichts" ist die einzige Aussage, die durch Nachsehen
nicht bestätigt werden kann: Wer nichts findet, hat entweder recht oder falsch gesucht. Die
beiden Fälle sehen identisch aus.

**Beispiel.** Eine Regel sagt: „Dieser Vorgang erzeugt keinen Beleg." Der absichernde Test
ruft den Einstieg auf und prüft, dass der Zähler unverändert ist. Dazu die
**Negativkontrolle**: derselbe Test gegen einen Vorgang, der einen Beleg erzeugt — er muss
den Unterschied sehen. Ohne sie ist der Test grün, weil er blind ist.

**Filtersatz.** „Da steht ja nichts im Code, was das tun könnte" — das ist eine Beobachtung,
kein Beleg.

### 2 · Ausschließlichkeit ist Abwesenheit

**Warum es bricht.** „Die einzige Stelle" behauptet über alle Stellen etwas, die man nicht
genannt hat. Ein Zitat der genannten Stelle belegt nur, dass sie existiert — nie, dass es
keine zweite gibt.

**Beispiel.** Eine Regel behauptet, ein bestimmter Zustandswechsel sei die einzige Stelle,
an der ein Folgevorgang automatisch entsteht. Belegt war sie mit einem Zitat der
Codestelle. Die Maske über **alle Aufrufer der auslösenden Funktion** zeigt drei weitere.
Die Regel fällt nicht — sie wird auf die gemessene Liste zurückgenommen.

**Achtung auf die Form ohne Signalwort.** „Der Weg zur Rechnung führt über …" trägt dieselbe
Aussage wie „der einzige Weg". Der Ausschließlichkeits-Grep sucht deshalb auch den
bestimmten Artikel in der Zusage.

**Filtersatz.** „Das steht so in der Belegstelle" — für eine „einzige Stelle" reicht das nicht.

### 3 · Jede Zahl trägt Zähleinheit und Maske

**Warum es bricht.** Zahlen ohne Herkunft irren fast immer in dieselbe Richtung: Der Befund
liest sich harmloser, als er ist. Wer sie nachzählt, zählt eine andere Größe.

**Beispiel.** „Sechs Leseeinstiege" gegen „20 Einstiege, gemessen per Registrierungsmarker
in `<datei>` am Stand `<x>`". Die erste Angabe kostet in jeder Prüfrunde eine Nachfrage; die
zweite lässt sich in zehn Sekunden widerlegen oder bestätigen. Wo eine Zahl klein ist, wird
sie durch die **Aufzählung** ersetzt, die sie zusammenfasst.

**Filtersatz.** „Die Zahl ist nur Illustration" — dann ersetze sie durch die Aufzählung.

### 4 · Eine Maske wird ausgeführt, nicht gelesen

**Warum es bricht.** Eine abgedruckte Maske ist eine Behauptung über den Suchraum. Ob sie
ihn trifft, weiß nur, wer sie laufen lässt.

**Beispiel.** Eine Maske schneidet auf ein Verzeichnis, in dem die Hälfte der Kandidaten
nicht liegt. Gelesen sieht sie vollständig aus; ausgeführt fehlen zwölf Dateien. Deshalb
liegt jede feste Maske als **Datei im Repository**, versioniert neben dem, was sie prüft.

**Filtersatz.** „Die Maske steht doch da" — eine Maske, die niemand ausführt, ist eine Meinung.

### 5 · Eine leere Maskenausgabe braucht eine Positivkontrolle

**Warum es bricht.** Leer ist das Bild eines gelungenen Abwesenheitsbeweises **und** das
Bild einer kaputten Maske.

**Beispiel.** Die Shell schreibt ein Argument um, das mit einem Trennzeichen beginnt; das
Suchmuster kommt nie als Suchmuster an. Ergebnis: null Treffer, Fehlercode — und eine
„Berichtigung", die eine richtige Zahl gegen eine falsche tauscht. Gegenmittel: dieselbe
Maske gegen einen bekannten Treffer laufen lassen.

**Filtersatz.** „Die Maske findet nichts" — zeig, dass sie überhaupt etwas finden kann.

### 6 · Eine Maskenausgabe ist ein Verdacht, kein Urteil

**Warum es bricht.** Eine Maske unterscheidet nicht, **warum** eine Stelle so aussieht.

**Beispiel.** Ein Testauftrag begründet ausdrücklich, dass er einen fremden Einstieg
**nicht** aufruft — und erzeugt damit einen Treffer in der Maske, die nicht deklarierte
Einstiege sucht. Von zehn Treffern waren vier solcher Sätze. Jede Zeile wird an ihrer
Fundstelle gelesen, bevor sie ein Befund wird.

**Filtersatz.** „Die Maske hat es gefunden" — die Maske weiß nicht, warum die Stelle so klingt.

### 7 · Eine Messung ist an einen benannten Stand gebunden

**Warum es bricht.** Ein Bestand bewegt sich. Eine Messung ohne Stand ist morgen nicht mehr
nachvollziehbar und lässt sich nicht wiederholen.

**Beispiel.** Eine Maske über den Arbeitsbaum misst, was zufällig ausgecheckt ist — bei
einem Verzeichnis, das nur gelesen wird, ein beliebiger Stand. Sie kann die Zahl, die neben
ihr steht, gar nicht erzeugt haben. Abgedruckt gehört die **stand-gebundene** Fassung.

**Filtersatz.** „Gemessen am aktuellen Stand" — welcher war das, in einer Woche?

### 8 · Zahlen aus einem Demo-Bestand belegen nichts über den Betrieb

**Warum es bricht.** Sie wirken wie Betriebswissen und sind es nicht — in **beide**
Richtungen.

**Beispiel.** „Betrifft nur neun von dreizehntausend Vorgängen" stuft einen Befund herunter;
„dreizehntausend Fälle" stuft ihn hoch. Beide Sätze ruhen auf erfundenen Daten. Ein
Demo-Bestand kann eine **Untergrenze für Machbarkeit** belegen („der Weg wurde mindestens
einmal durchlaufen"), nie eine Häufigkeit und nie eine Priorisierung.

**Filtersatz.** Wer auf Bestandszahlen argumentiert, schreibt dazu, woher sie stammen — oder
lässt die Aussage weg.

### 9 · Wer misst, prüft das Messgerät mit

**Warum es bricht.** Die häufigste Art, falsch zu liegen, ist nicht falsches Denken, sondern
richtiges Messen am falschen Aufbau. Das Ergebnis ist sauber begründet und trotzdem falsch.

**Beispiel.** Ein Testlauf meldet „alles grün" — er lief in einem Arbeitsbereich mit fremder,
halbfertiger Arbeit. Die Gegenmessung, die das aufdeckt, ist selbst falsch konfiguriert: Ein
Schalter fehlt, ohne den die geprüfte Schutzfunktion gar nicht greift. Beinahe wäre ein
Testfehlschlag als Sicherheitslücke gemeldet worden.

**Filtersatz.** „Der Lauf war grün" — gegen welchen Aufbau, und woran hättest du gemerkt,
dass er falsch steht?

### 10 · Eine Fundstelle aus einem Bericht ist keine Fundstelle

**Warum es bricht.** Ein Bericht ist eine Aussage über den Bestand, nicht der Bestand.
Zwischen beiden liegt mindestens eine Interpretation.

**Beispiel.** Ein Befund lautete „hier fehlt dieselbe Prüfung wie am Nachbarpfad". Am Code
nachgelesen: Der Nachbarpfad ist ein anderer Fall, die Prüfung fehlt dort mit Absicht. Kein
Fund — aber eine Aufgabe war schon angelegt.

**Filtersatz.** „Steht so im Bericht" — dann schlag es auf.

---

## Berichtigen

### 11 · Eine Berichtigung greift über alle Fundstellen

**Warum es bricht.** Wird nur die auffällige Stelle berichtigt, sind die anderen nicht nur
weiterhin falsch — sie **widersprechen** jetzt der berichtigten. Aus einem Fehler werden zwei.

**Beispiel.** Dieselbe Zeilenangabe stand in drei Dateien mit zwei Werten, entstanden beim
Beheben eines anderen Funds. **Ab zwei Fundstellen ist die ausgeführte Maske Pflicht**: der
Befehl und seine Ausgabe (Treffer vorher, Treffer nachher) gehören in den Änderungstext.
Eine Liste der Stellen aus dem Gedächtnis zählt nicht. Die Maske läuft auch **innerhalb
derselben Datei** — zwei Türen zur selben Messung in einer Datei sind der Regelfall.

**Filtersatz.** „Ich habe alle Stellen aufgezählt" — dann zeig die Maske.

### 12 · Nach jeder Behebung wird erneut gemessen

**Warum es bricht.** Eine Berichtigung verschiebt Angaben, die sie selbst nicht nennt — und
erzeugt neue Sätze, die denselben Fehler enthalten können.

**Beispiel.** Der Fund der achten Prüfrunde war ein Satz, den die Behebung der siebten
erzeugt hatte. Deshalb gehört der **eigene neue Text** in den Suchraum: Er wird mit
derselben Maske geprüft wie der gerügte.

**Filtersatz.** „Der Fund ist behoben, die Datei ist gelesen" — Maske gelaufen, Wortlaut über
alles gesucht, dann ist er behoben.

### 13 · Zeilenziel aufschlagen statt Versatz rechnen

**Warum es bricht.** Eine Verschiebung heilt keinen Verweis, der vorher schon falsch war —
sie verschiebt ihn zeichengenau mit.

**Beispiel.** Nach einer Einfügung von drei Zeilen werden alle Angaben darunter um drei
erhöht. Eine davon zeigte vorher auf die falsche Funktion; jetzt zeigt sie drei Zeilen
weiter auf die falsche Funktion. Aufschlagen kostet Sekunden und beantwortet beide Fragen.

**Filtersatz.** „Es sind drei Zeilen nach unten gerutscht" — schlag auf, was dort steht.

### 14 · Der Registerstand lebt an genau einer Stelle

**Warum es bricht.** Ein Stand an sieben Stellen bedeutet, dass jede Bewegung sieben
Änderungen braucht — und dass sechs davon vergessen werden.

**Beispiel.** Der Stand des Lückenregisters stand in vier Dateien plus Anhang. Jede
geschlossene Lücke kostete eine Prüfrunde. Nach der Umstellung trägt nur der Kopf des
Registers die Zahl; alle anderen verweisen. Dieselbe Regel gilt für Zeilen- und
Spannenangaben: Sie stehen in der Bereichsdatei, der Testauftrag verweist.

**Filtersatz.** „Die Zahl muss auch hier stehen, sonst versteht man den Abschnitt nicht" —
nein, ein Verweis genügt.

---

## Zuschnitt und Prüfgegenstand

### 15 · Ein Einstieg gehört genau einem Bereich

**Warum es bricht.** Gehört ein Einstieg allen, testet ihn niemand — oder alle, und der
Wächter fordert denselben Test siebenmal.

**Beispiel.** Ein zentraler Einstieg wurde von sieben Bereichen referenziert, keiner war
„der Eigentümer". Lösung: ein eigener Bereich für ihn; die sieben führen ihn als **fremd**
und verweisen. Für Infrastruktur ohne eigene Fachlogik gibt es den **Querschnitt** — er hat
keine eigenen Einstiege und deshalb kein Abnahmekriterium. Ein **leerer Eintrag** ist immer
ein Befund, nie eine Ausnahme.

**Filtersatz.** „Das gehört allen" heißt: niemand prüft es.

### 16 · Prüfgegenstand oder Werkzeug

**Warum es bricht.** „Testen" und „beobachten" unter einem Wort führt dazu, dass die Frage
„gehört dieser Aufruf hierher?" in jedem Tor neu gestellt wird.

**Das Kriterium.** *Kann dieser Test rot werden, weil sich das Verhalten **dieses**
Einstiegs ändert?*

- **Ja → Prüfgegenstand.** Der Test gehört dem besitzenden Bereich; der rufende verweist.
- **Nein → Werkzeug.** Er bleibt beim Aufrufer und trägt seine Rolle: Vorbedingung,
  Zählpunkt einer Negativkontrolle, Beobachtungspunkt der eigenen Wirkung.

**Sonderfall.** Ist die Zusage einer Regel ein **Vergleich über Bereichsgrenzen**, ist die
Frage für jede Zeile mit Ja zu beantworten. Dann ist nicht die Zuordnung falsch, sondern Ja
die Bauart: Die Einzeltests gehören ihren Bereichen, der vergleichende Test bleibt beim
Aufrufer — mit einer Begründung **je Zeile**.

**Filtersatz.** „Der Test ruft ihn nur auf" — dann beantworte die Frage; die Antwort ist die
Zuordnung.

### 17 · Jede Regel braucht eine Schnittstellenfassung

**Warum es bricht.** Eine Regel, die nur als Verhalten einer internen Funktion formuliert
ist, ist beim Neubau nicht prüfbar — die Funktion gibt es dann nicht mehr.

**Beispiel.** „Die Funktion liefert einen Leerwert, wenn kein Preis ermittelbar ist" wird zu
„Der Aufruf antwortet mit `<Status>`, der Körper trägt `<Feld>`, und in der Ablage steht
danach `<Zustand>`". Ein vorhandener Funktionstest darf bleiben, zählt aber nicht als
Absicherung der Regel.

**Filtersatz.** „Das ist nur über die Funktion testbar" — dann ist es noch nicht als
Verhalten beschrieben.

### 18 · Ein Bereich ohne Abnahmekriterium ist kein Bereich

**Warum es bricht.** Die Beschreibung sagt, was das System **tut**. Ohne Kriterium sagt
niemand, was es **soll** — und „fertig" wird zur Gefühlsfrage.

**Beispiel.** Zwei nachträglich geschnittene Bereiche hatten vollständige Regeln und keinen
Maßstab. Jeder bekam einen Satz: woran die ausführende Rolle selbst erkennt, dass der
Bereich fertig ist — Schnittstellenfassungen grün, Mutationsproben rot, Einstiegstabelle
vollständig, Wächter ohne Lücke.

**Filtersatz.** „Das ist Querschnitt, braucht kein Kriterium" — ein Bereich mit eigenen
Einstiegen hat eins.

---

## Absichern

### 19 · Ein Test ohne bestandene Mutationsprobe ist eine Behauptung

**Warum es bricht.** Ein grüner Test beweist, dass er grün ist. Ob er rot werden **kann**,
ist eine andere Frage — und die entscheidet, ob er etwas schützt.

**Beispiel.** Ein Test las einen Zähler, der ohnehin bei jedem Ausgeben stieg, und merkte
das Abschalten der geprüften Automatik nicht. Er war grün und blind; der Testauftrag wies
die Lücke als geschlossen aus. Ablauf der Probe: Stelle verletzen → Test wird rot → Rückbau
verifizieren → Ergebnis (Mutation, Testname, rot/grün) in den Änderungstext.

**Filtersatz.** „Der Test ist grün und hat einen Docstring" — ohne Probe ist das eine
Behauptung.

### 20 · Der Mutant entfernt oder kehrt um

**Warum es bricht.** Eine abgeschwächte Bedingung berührt genau den Teil nicht, der trägt.
Die Probe ist dann grün, ohne etwas geprüft zu haben.

**Beispiel.** Ein Filter auf einen bestimmten Wert wurde zu „ist nicht leer" abgeschwächt.
Grün — also galt der Filter als überflüssig. Tatsächlich schloss er genau die Leerfälle aus,
die der abgeschwächte Mutant weiterhin traf. Der **entfernte** Filter zeigte dann: kein Test
wird rot. Das heißt nicht „redundant", sondern **„der Test ist blind"**.

**Filtersatz.** „Der Mutant war grün, die Bedingung ist redundant" — oder der Test ist blind.

### 21 · Eine Deckungsaussage ist eine Abwesenheitsaussage andersherum

**Warum es bricht.** „Für X gibt es keinen Test" und „X passiert nicht" haben dieselbe
Beweislast: Beide behaupten etwas über alles, was man nicht gesehen hat.

**Beispiel.** Die Zählung der Tests eines Bereichs brauchte vier Anläufe, jedes Mal aus einer
anderen blinden Stelle — Filter auf den Namen des Testobjekts, nur einzeilige Aufrufe,
vollständige statt endender Pfade. Regel daraus: **parsen statt suchen, Endstück statt
vollem Pfad, kein Filter auf Namen.**

**Filtersatz.** „Ich habe gesucht, es gibt N Tests" stützt keine Tabelle.

### 22 · Ein Bestand wird gemessen, nicht gepflegt

**Warum es bricht.** Eine Liste, die zweimal geführt wird, ist nach der ersten Änderung eine
Liste und eine Lüge.

**Beispiel.** Statt der Handpflege einer Einstiegstabelle sammelt ein Wächter alle Aufrufe
der Testsuite per Strukturanalyse und vergleicht sie mit der Tabelle. Er schlägt **in beide
Richtungen** an: Einstieg ohne Test, und Tabelle nennt einen Einstieg, den es nicht gibt.
Er läuft bei jeder Änderung mit — ein Test, den niemand auslöst, ist kein Wächter. Und er
**ersetzt** den Pflichtschritt, den er ablöst: das Nachmessen der Tabelle im Tor.

**Filtersatz.** „Wir führen das sorgfältig nach" — Sorgfalt ist kein Wächter.

### 23 · Der absichernde Test schreibt den Ist-Zustand fest

**Warum es bricht.** Wer ändert, bevor der Ausgangszustand festgehalten ist, kann nicht mehr
zeigen, was er geändert hat.

**Beispiel.** Eine Aufgabe, die eine spezifizierte Regel ändert, bekommt als **erstes**
Abnahmekriterium: Der absichernde Test der Regel liegt im selben Änderungssatz **vor** dem
Fix — erst grün gegen das alte Verhalten, dann mit dem Fix umgeschrieben, **beide Fassungen
im Verlauf**. Das ist auch dann richtig, wenn der Test damit falsches Verhalten festschreibt
— genau dafür ist er da.

**Filtersatz.** „Der Fix ist klein, der Test kann nachkommen" — nein.

### 24 · Der Testauftrag ist der Vertrag

**Warum es bricht.** Was der Auftrag nicht sagt, erfindet der Testbauer — plausibel und falsch.

**Beispiel.** Eine Negativkontrolle sollte zeigen, dass ein Datensatz nach dem Ausmustern
sichtbar bleibt. Erste Fassung: Der Aufbau erzeugte nie einen Datensatz, sie verglich Leer
mit Leer. Zweite Fassung: Der eingebaute Schreibaufruf setzte ein Feld und nahm der
**Nachbarkontrolle** ihre Voraussetzung. **Beide Fassungen sahen richtig aus.** Regel daraus:
Wo eine Kontrolle schreibt, bekommt sie **eigene Daten**, und der Auftrag nennt das
**Kriterium**, an dem die Trennung hängt — nicht die Absicht.

**Filtersatz.** „Steht doch in der Bereichsdatei" — dann verweise darauf, statt es neu zu
erfinden.

---

## Entscheiden und Berichten

### 25 · Erst prüfen, ob die Frage schon beantwortet ist

**Warum es bricht.** Ein Register ohne Abgleich driftet nur in eine Richtung: Es hält Fragen
offen, die längst beantwortet sind.

**Beispiel.** Ein einziger Abgleich gegen den Aufgabenbestand fand an einem Tag drei Fragen,
deren Antwort seit Stunden, seit fünf Tagen und seit **drei Wochen** vorlag. Regel daraus:
Eine Frage an ein anderes Ressort gilt erst als offen, wenn der letzte Abgleich sie nicht
beantwortet gefunden hat — und ein Fragenpaket wird nur aus solchen Fragen geschnürt.

**Filtersatz.** „Das ist eine Frage an das Fach" — erst nachsehen, ob es sie schon
beantwortet hat.

### 26 · Eine Entscheidung braucht Filtersatz und Neuaufmachen

**Warum es bricht.** Ohne Filtersatz prallt nichts ab; ohne Bedingung zum Neuaufmachen ist
die Entscheidung entweder ewig oder beliebig.

**Beispiel.** „Wir nehmen hin, dass dieser Zustand nicht behoben wird." Filtersatz: „Aber das
ist doch ein Fehler" — ja, und er ist bewusst hingenommen; der Grund steht hier. Bedingung
zum Neuaufmachen: „Sobald ein echter Nutzer betroffen sein kann." Ohne beides taucht
derselbe Punkt in der nächsten Prüfrunde als neue Aufgabe auf — genau das Muster, gegen das
dieser Prozess antritt.

**Filtersatz.** Ein bewusst hingenommener Zustand ist ein Eintrag, kein Schweigen.

### 27 · Dreimal dieselbe Frageklasse ist eine Regel

**Warum es bricht.** Wiederkehrende Einzelfragen halten den Bau an jeder Stelle an, an der
niemand vorher entschieden hat.

**Beispiel.** An einem Tag waren rund zwanzig Entscheidungen nötig, fast alle Vertreter von
fünf Klassen: Zuschnitt, sperrend ja/nein, Aufgabe ja/nein, Modell und Effort, Vorgehen im
Tor. In derselben Nacht liefen drei Bereiche ohne Rückfrage durch, weil Testauftrag,
Sammelfreigabe und Probe vorher feststanden. Die Grenze lag nicht am Können, sondern an dem,
was vorher nicht entschieden war.

**Und jede neue Regel nennt den Schritt, den sie ersetzt.** Sonst wächst das Vorgehen, bis
niemand mehr alles ausführt — und die Regeln, die tragen, gehen in denen unter, die nur
dastehen.

**Filtersatz.** „Das entscheiden wir, wenn es so weit ist" — nein, sonst hält es den Bau an.

### 28 · Eine Entscheidung wirkt erst im Arbeitssystem

**Warum es bricht.** Ein Register liest nur, wer es kennt. Gearbeitet wird an der
Aufgabenliste.

**Beispiel.** Eine Entscheidung, die einen Zustand hinnimmt, stand im Register. Die
Aufgabenliste kannte sie nicht und erzeugte in der nächsten Prüfrunde eine Aufgabe dafür.
Bis eine Entscheidung dort angekommen ist, gehört „im System durchziehen" in den Aufgabenbestand.

**Filtersatz.** „Ist entschieden" — dann zeig den Eintrag dort, wo gearbeitet wird.

### 29 · Der Rückweg ist das Protokoll, nicht die Meldung

**Warum es bricht.** Eine Meldung zwischen zwei Sitzungen trägt nie den Verlauf der
Gegenseite. Wer nach Meldungen steuert, sieht genau den Kanal, der ihm gemeldet wird.

**Beispiel.** Eine steuernde Ebene arbeitete fehlerfrei, solange sie der einzige Kanal war.
Sobald der Mensch direkt mit der Arbeitsseite sprach, steuerte sie an der Wirklichkeit
vorbei — gemessen: über hundert Direktgespräche gegen eine Handvoll Meldungen. Die Ebene war
nicht kaputt, sondern blind. Gegenmittel: **vor** jedem Auftrag den Stand der Gegenseite
selbst lesen.

**Filtersatz.** „Es kam nichts zurück" — erst nachsehen, dann interpretieren.

### 30 · Meldeweg und Freigaben

**Warum es bricht.** Ohne festen Meldeweg wird jede Rückfrage zu einer Unterbrechung; mit
einer Relaisstation wird aus „das braucht eine Freigabe" ein „das hat der andere sicher
geklärt".

**Der Weg.** Vollzug nach jedem Block, mit Beleg. Sofort „warte auf", sobald eine
Entscheidung oder Freigabe nötig ist — nicht am Blockende gesammelt. Meldung bei Abbruch,
mit dem Stand, den der nächste Block vorfindet. **Sachfragen** gehen an die Kopf-Ebene,
**Freigaben** direkt an den Menschen.

**Filtersatz.** Im Zweifel direkt fragen, nicht weiterreichen.

---

## Das Tor

### 31 · Das Tor ist beidseitig

**Warum es bricht.** Die Schreibseite ist die naheliegende Hälfte. Die Leseseite — Berichte,
Auswertungen, Spiegel — wird übersehen, und dort liegen die stillsten Fehler.

**Beispiel.** Zwei Bereiche brauchten je drei Runden; beide Male sah Runde 1 nur die
Schreibseite. Der Fund lag beide Male auf der Leseseite: eine Auswertung filterte auf Werte,
die keine Schreibstelle je schreibt — ein Bericht, der immer leer ist und aussieht, als sei
nichts passiert.

**Filtersatz.** „Die Schreibseite ist sauber" — die Hälfte ist kein Ergebnis.

### 32 · Vor der ersten Torrunde läuft die Zahlenprüfung

**Warum es bricht.** Ein teures Tor, das Zahlen nachzählt, ist die teuerste Art, Zahlen
nachzuzählen.

**Beispiel.** Fünfzehn Torrunden an einem Tag, dreiunddreißig blockierende Funde, fast alle
derselben Klasse — eine Zahl, die ihre Aufzählung nicht deckt, und eine Berichtigung, die
nur ihren Absatz erreicht. Die Prüfung läuft **vor** dem Tor, mit einem kleinen Modell, über
die im Block geänderten Dateien. Sie **ersetzt** die Nachzählrunden, sie kommt nicht hinzu.

**Bedingung zum Neuaufmachen.** Findet sie drei Blöcke in Folge nichts, entfällt sie wieder;
die Grundsätze 3 und 11 tragen dann allein.

**Filtersatz.** „Das Tor findet es schon" — das Tor hat es viermal erst in Runde drei gefunden.

### 33 · Nach dem Ja wird veröffentlicht

**Warum es bricht.** Ein Gutachten, das danach noch eine zweite Freigabe braucht, hält jede
Runde doppelt an — und die zweite Freigabe prüft nichts, was die erste nicht geprüft hat.

**Die Grenze.** Das Tor ist die Freigabe **für den Schritt, den es prüft**, und für keinen
darüber hinaus. Zusammenführung in den Hauptzweig, Eingriffe in ein laufendes System und
alles, was die Regeln ausdrücklich beim Menschen belassen, bleiben dort — und laufen nie
über eine Relaisstation.

**Filtersatz.** Ohne das Ja wird nicht veröffentlicht; mit dem Ja wird nicht nachgefragt.

---

## Zuschnitt der Arbeit

### 34 · Zählen, nicht fühlen

**Warum es bricht.** „Umbau oder Neubau" wird sonst nach Geschmack entschieden, und
Geschmack lässt sich nicht widerlegen.

**Das Maß.** *Kann ich diesen Befund an einer Stelle beheben, ohne dass er an einer anderen
wieder entstehen kann?* Ist die Antwort für **alle** Befunde eines Moduls ja, ist es
Umbau-Kandidat. Ist sie für einen **tragenden** Befund nein, ist nicht die Stelle kaputt,
sondern der Bau erlaubt den Fehler — Neubau-Kandidat.

**Beispiel.** Sieben Schreibstellen eines Zustands, fünf davon vollständig. Die zwei lassen
sich flicken — die achte, kopierte Stelle hat den Aufruf wieder nicht. Behebbar nur, indem
es **einen** Schreibweg gibt. Das ist ein anderer Bau. Gegenbeispiel: eine strikte,
getestete Zustandsmaschine mit zwei Einzelbefunden — an einer Stelle behebbar, danach
nirgends wieder möglich.

**Zwei Zusätze.** Bei zwei Stellen ist Umbau billiger, bei sieben plus allen künftigen
Neubau. Und: **Ein Modul ohne Befund ist kein Neubau-Kandidat**, auch wenn es hässlich
aussieht. Hässlich ist keine Fehlerklasse.

**Filtersatz.** „Das sieht hässlich aus" — hässlich ist keine Fehlerklasse.

### 35 · Kein Bau ohne Entscheidungsvorrat

**Warum es bricht.** Ein Bauauftrag hält an jeder Stelle an, an der vorher nichts entschieden
wurde — und das sind fast nie neue Fragen.

**Die fünf Punkte des Vorrats.** (1) Für jede wiederkehrende Frageklasse eine Regel mit
Filtersatz. (2) Fremde Ressorts **vorher** leergeräumt; eine offene Frage dort sperrt ihren
Bereich. (3) Freigaben als Dauerregeln, an Tor und Probe gebunden, mit benannten Ausnahmen,
die beim Menschen bleiben. (4) Abnahme **vorher**: Jeder Bereich trägt sein Kriterium vor dem
Bau. (5) Eine Wirklichkeitsprüfung als vorbereitete Liste, die ein Mensch durchgeht — sie
ersetzt ihn nicht, sie macht seine Prüfung kurz.

**Filtersatz.** Eine Frage, die dreimal derselben Klasse angehört, wird zur Regel.

### 36 · Eine Lücke schließt durch Messung oder Entscheidung

**Warum es bricht.** Eine besser formulierte Lücke ist immer noch eine Lücke — sie fällt nur
nicht mehr auf. **Eine Lücke, die nicht auffällt, wird zur Behauptung.**

**Beispiel.** „Unklar, ob dieser Zustand gewollt ist" wird nicht dadurch geschlossen, dass
man schreibt „der Zustand ist dokumentiert". Geschlossen wird sie durch eine Messung (mit
Maske und Messstand, Ergebnis als Regel) oder durch eine Entscheidung (mit Filtersatz und
Bedingung zum Neuaufmachen). Geschlossene Einträge werden durchgestrichen, nicht gelöscht,
und Nummern nie neu vergeben.

**Filtersatz.** „Das haben wir jetzt klarer beschrieben" — was ist gemessen, was ist entschieden?
