# Auftrag an den Gutachter — Tor zu Block `<NN>`

> Dieser Auftrag geht an eine Rolle, die den Gegenstand **weder gemessen noch geschrieben
> hat**. Genau das ist ihr Wert. Wird die Trennung aufgegeben, bleibt vom Tor die Zeremonie.

## Gegenstand

- **Dateien:** `<vollständige Liste der im Block geänderten Dateien>`
- **Bereich:** `<Pfad zur Bereichsdatei>` · **Messstand:** `<Stand mit Datum>`
- **Was der Block getan hat:** `<drei Sätze, ohne Begründung. Die Begründung liest der
  Gutachter erst, nachdem sein Befund steht.>`

## Vorlauf, der schon gelaufen ist

- **Zahlenprüfung:** liegt bei, Tabelle
  *(Stelle · Angabe · Maske · gemessen · Abweichung)*. **Sie ist leer oder jede Zeile ist
  behoben** — sonst geht der Block nicht ins Tor.
- **Feste Masken:** `<Liste>`, ausgeführt, mit Ausgabe.
- **Ausschließlichkeits-Grep:** ausgeführt, Fundstellen einzeln gelesen.

**Der Gutachter prüft die Masken stichprobenweise, nicht jede Zahl einzeln.**

## Prüfauftrag — beide Seiten

Ausdrücklich beide, sonst braucht der Block drei Runden statt einer:

- **Schreibseite:** Einstiege, Schreibstellen, Auslöser, Zustandswechsel.
- **Leseseite:** Leseeinstiege, Auswertungen, abgeleitete Felder, Spiegel.

## Maßstab

1. **Beleg je Regel.** Jede Regel trägt Datei und Zeile. **Mindestens drei Belegstellen
   werden nachgelesen** — am Gegenstand, mit einem aufschlagenden Befehl, nur lesend. Steht
   dort nicht, was die Regel sagt: **BLOCKIEREND**.
2. **Absicherung oder Lücke.** Jede Regel nennt einen Test oder eine offene Lückennummer.
   Keins von beidem: **BLOCKIEREND**.
3. **Zwei Quellen.** Stützt sich eine Regel auf eine einzige Stelle ohne Test, Aufgabe,
   Migration oder zweite Stelle? **VORSCHLAG**, bei sicherheitsrelevanten Regeln
   **BLOCKIEREND**.
4. **Abwesenheit und Ausschließlichkeit.** Jede Aussage der Form „passiert nicht", „die
   einzige Stelle", „nirgendwo sonst" — auch ohne diese Wörter, allein durch den bestimmten
   Artikel — trägt eine **ausgeführte Maske über alle Kandidaten** mit Zähleinheit,
   Messstand und Positivkontrolle. Ohne Maske: **BLOCKIEREND**.
5. **Zahlen.** Jede Zahl trägt Zähleinheit und Maske oder ist durch die Aufzählung ersetzt.
   Eine beiläufige Zahl ohne beides ist ein Fund, kein Stilproblem.
6. **Doppelung zwischen Bereichen.** Steht dieselbe Regel schon in einem anderen Bereich?
   Dann gehört ein Verweis hin, keine Kopie. Eine **abweichende Fassung derselben Regel in
   zwei Bereichen** ist **BLOCKIEREND**.
7. **Zuschnitt.** Jeder Einstieg gehört genau einem Bereich; jeder fremde Einstieg trägt
   eine Rolle und die beantwortete Frage *Kann der Test rot werden, wenn sich dieser
   Einstieg ändert?* Ein leerer Eintrag ist ein Fund, keine Ausnahme.
8. **Abnahmekriterium** wörtlich aus der fachlichen Quelle zitiert, mit Stand — nicht
   paraphrasiert.
9. **Keine Zahl aus einem Demo- oder Testbestand als Beleg für Häufigkeit oder Schwere.**
   **BLOCKIEREND**.
10. **Gliederung und Kürzel** vollständig; Kürzel eindeutig und nicht umbenannt.

Arbeitsweise des Tores — nur BLOCKIEREND blockiert, höchstens sieben Funde, ab der dritten
Runde wird vorgelegt statt entschieden — und die Ausgabeform stehen in der Agent-Definition
`rethink-gutachter` und werden hier nicht wiederholt.

## Runden

| Runde | Datum | Funde | Behoben | Offen | Freigabe |
| --- | --- | --- | --- | --- | --- |

**Zwischen zwei Runden gilt:** Maske erneut ausführen; bei jeder berührten Zeilenangabe das
Ziel aufschlagen statt den Versatz zu rechnen; den gerügten Wortlaut über **alle** Dateien
suchen, **einschließlich des eigenen neuen Textes**.

## Nach dem Ja

Der Stand wird **ohne weitere Rückfrage** veröffentlicht — das Tor **ist** die Freigabe für
diesen Schritt. Gemeldet wird nur der Vollzug mit Kennung.

**Nicht gedeckt und nie über eine Relaisstation:** die Zusammenführung in den
Hauptzweig, jede Freigabe, die die Regeln ausdrücklich beim Menschen belassen, und jeder
Eingriff in ein laufendes System. Dafür entscheidet die Kopf-Ebene beziehungsweise der
Mensch — direkt.

