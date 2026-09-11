# Ablauf — was kommt wann, wie und wo

> Der **eine Ort**, an dem steht, wo das Projekt steht und was als Nächstes dran ist.
> Jeder Auftrag nennt seine Phase und seinen Block. Jeder Block-Bericht schreibt „Jetzt"
> fort. Reihenfolge ist verbindlich, **Termine gibt es hier nicht** — Fortschritt wird am
> Ausgang je Phase gemessen, nicht am Kalender.

## Jetzt

| | |
| --- | --- |
| **Phase** | `<MEASURE \| MAP \| GAPS \| DECIDE \| GUARD \| HANDOFF>` |
| **Messstand** | `<Commit oder Stand mit Datum>` |
| **Läuft** | `<Block-Nummer, Gegenstand, wer>` |
| **Zuletzt fertig** | `<Block, Ergebnis, Beleg>` |
| **Wartet auf** | `<wer, worauf, seit wann>` |
| **Als Nächstes** | `<genau ein Block>` |

## Die Phasen

### MEASURE — Bestand messen

- **Eingang:** Leserecht auf den Bestand.
- **Ausgang:** Messstand benannt · Bereichsschnitt mit genau einem Eigentümer je Einstieg ·
  Liste der Abweichungen Dokument gegen Bestand.
- **Abbruch:** Der Bestand bewegt sich schneller, als er gemessen werden kann.

### MAP — Ist-Zustand als Spezifikation

- **Eingang:** MEASURE abgeschlossen.
- **Ausgang:** Je Bereich eine Datei nach `BEREICH.md`, jede durch das Tor freigegeben.
- **Abbruch:** Eine Regel ist an keiner Schnittstelle beobachtbar.

### GAPS — Register der offenen Punkte

- **Eingang:** Bereichsdateien liegen vor.
- **Ausgang:** `LUECKEN.md` vollständig, gegen den vorhandenen Aufgabenbestand abgeglichen.
- **Abbruch:** Das Register wächst schneller, als entschieden wird.

### DECIDE — Entscheidungen als Filter

- **Eingang:** Register abgeglichen.
- **Ausgang:** Jede Lücke entschieden oder gemessen · Entscheidungsvorrat je Frageklasse ·
  fremde Ressorts leergeräumt.
- **Abbruch:** Dieselbe Frageklasse zum dritten Mal — dann Regel statt Frage.

### GUARD — absichern

- **Eingang:** Bereich freigegeben, keine offene Lücke mit Sperrwirkung.
- **Ausgang:** Testauftrag abgearbeitet · Mutationsprobe je Regel belegt · Wächter laufen mit.
- **Abbruch:** Eine Mutationsprobe bleibt grün.

### HANDOFF — Übergabe

- **Eingang:** Alle Bereiche durch GUARD, Register ohne offene Lücke mit Sperrwirkung.
- **Ausgang:** Übergabe-Notiz; ab hier übernimmt der Foundation-Prozess.
- **Abbruch:** Eine tragende Entscheidung ist noch offen.

## Regeln für diesen Ablauf

Jede Regel nennt, welchen Schritt sie **ersetzt**. Eine Regel, die nur hinzukommt, wird
nicht aufgenommen.

1. **Jeder Auftrag nennt seine Phase und seinen Block.** Ein Auftrag ohne beides wird
   zurückgefragt.
2. **Jeder Block-Bericht endet mit dem neuen Stand von „Jetzt".** Wer den Block
   abschließt, schreibt die Tabelle oben fort.
3. **Eine Phase nimmt nur der Mensch ab.** „Fertig" sagt der Ausgang, nicht das Gefühl.
4. **Parallel ist nur, was hier so markiert ist.** Alles andere wartet.
5. **Was hier nicht steht, ist nicht dran.** Eine Idee ohne Phase wird notiert, nicht
   beauftragt.
6. **Kein Bau vor entschiedener Spezifikation.** Absichernde Tests und Dokumentarbeit sind
   jederzeit erlaubt.
7. **Abgleich-Lauf im festen Takt.** Ein Lauf misst, ob die Spezifikation noch zum Bestand
   passt (verschobene und inhaltlich geänderte Belegstellen, getrennt gezählt), ein zweiter,
   ob sie noch zum Aufgabenbestand passt. *Ersetzt:* das Nachmessen jeder Belegstelle bei
   jeder Berührung. Schwelle für „die Spezifikation altert schneller, als sie fortgeschrieben
   wird": `<Zahl>` inhaltlich geänderte Stellen zweimal in Folge.
8. **Bestände werden gemessen, nicht gepflegt.** Wo dieselbe Liste zweimal nachgeführt wird,
   tritt ein Wächter an ihre Stelle. *Ersetzt:* Handpflege und ihre Nachmessung im Tor.
9. **Nach dem Ja des Tores wird veröffentlicht, ohne weitere Rückfrage.** *Ersetzt:* die
   Einzelfreigabe nach dem Tor. Was eine **direkte** Freigabe des Menschen verlangt, bleibt
   bei ihm und läuft nie über ein Relais.
10. **Der Prüfauftrag nennt beide Seiten** — Schreibseite und Leseseite. *Ersetzt:* das
    Nachzählen beiläufiger Zahlen im Tor, weil jede Zahl Zähleinheit und Maske trägt.
11. **Eine Berichtigung greift über alle Fundstellen, im selben Commit; die Maske steht im
    Commit-Text.** Ab zwei Stellen ist die ausgeführte Maske Pflicht, eine Aufzählung zählt
    nicht. Die Maske läuft auch **innerhalb derselben Datei**. *Ersetzt:* das
    Runde-für-Runde-Finden derselben Abweichung in Nachbardateien.
12. **Vor der ersten Torrunde läuft die Zahlenprüfung** über die im Block geänderten
    Dateien: jede Zahl, jede Aufzählung, jede Zeilenangabe gegen ihre ausgeführte Maske und
    gegen dieselbe Angabe in allen übrigen Dateien. Feste Masken: `<Liste>`, dazu der
    Ausschließlichkeits-Grep (*einzige, nirgendwo, nur hier, kein anderer, ausschließlich* —
    und der bestimmte Artikel in der Zusage). Ergebnis ist eine Tabelle
    *(Stelle · Angabe · Maske · gemessen · Abweichung)*; der Block geht erst ins Tor, wenn
    sie leer ist. *Ersetzt:* die Torrunden, die nur Zahlen nachzählen.
13. **Nach jeder Torbehebung wird erneut gemessen, bevor die nächste Torrunde läuft:**
    (a) die abgedruckte Maske noch einmal **ausführen**, und bei jeder berührten
    Zeilenangabe das Ziel **aufschlagen** statt den Versatz zu rechnen; (b) den gerügten
    Wortlaut über **alle** Dateien suchen, **einschließlich des eigenen neuen Textes**.
    *Ersetzt:* keinen neuen Schritt — sie gibt Regel 11 und 12 den Zeitpunkt.

## Werkzeugfallen

Jede hat einmal eine Runde gekostet. Sie sind keine neuen Pflichtschritte, sondern schärfen
die Maske eines bestehenden.

| Falle | Shell/Werkzeug | Folge | Ausweg |
| --- | --- | --- | --- |
| Maske misst den Arbeitsbaum statt eines Standes | jede | Die Maske kann die Zahl daneben gar nicht erzeugt haben | Maske stand-gebunden abdrucken |
| Pfad-Umschreibung: Git-Bash/MSYS unter Windows schreibt jedes Argument um, das mit `/` oder `./` beginnt — aus `^/etc/` wurde `^C:/Program Files/Git/etc/`, **ohne Fehlermeldung** | Git-Bash / MSYS (Windows) | Null Treffer — das Bild eines gelungenen Abwesenheitsbeweises | `MSYS_NO_PATHCONV=1` setzen; zusätzlich immer Positivkontrolle |
| Zeilenweise Maske über einen Zeilenumbruch | jede | Der Treffer bleibt stehen und gilt als behoben | mehrzeilig suchen oder mit Folgezeile |
| Spaltenmaske über eine Tabelle zählt von links | `awk`, `cut` | Falsche Spalte, sobald eine Zeile ein maskiertes Trennzeichen trägt | von rechts zählen oder Feldzahl vorher prüfen |

## Fehlerklassen

Der Katalog, gegen den gelesen wird. Jede Klasse einmal benannt, damit ein Fund einen Namen
hat statt einer Erzählung. Ergänzen, nicht umschreiben.

| # | Klasse | Kurzform |
| --- | --- | --- |
| 1 | Zwei Türen, eine bucht nicht | Derselbe Vorgang über zwei Wege, nur einer vollständig |
| 2 | Spiegel nur an einigen Schreibstellen | Ein abgeleitetes Feld wird nicht überall nachgezogen |
| 3 | Abwesenheit sieht aus wie Bestätigung | Nichts gefunden heißt nicht, dass nichts da ist |
| 4 | Regel nur an einer Ebene | Im Anwendungscode, aber nicht dort, wo die Verletzung weh tut |
| 5 | Nachweis ohne Wirkung | Protokolliert, aber nichts hängt daran |
| 6 | Beschreibung altert schneller als der Bestand | Das Zielbild wurde nie nachgezogen |
| 7 | Leerwert vergleicht sich mit Leerwert | Eine Bedingung, die nie greift |
| 8 | Irreversibler Schaden | Kein Rücknahmepfad zu einer Zeile mit Nebenwirkung |
| 9 | Riegel hält unter Gleichzeitigkeit nicht | Lesen und Schreiben ohne Sperre |
| 10 | Zustand, den die Beobachtung erzeugt | Der Testaufbau schafft, was er misst |
| 11 | Ergebnis hängt von Späterem ab | Ein Wert wird zu spät eingefroren |
| 12 | Regel kippt im Nachbarfall | Sie gilt, aber einen Pfad weiter nicht |
| 13 | Bedeutung nur im Kommentar | Nirgends erzwungen |
| 14 | Richtige Wirkung, falsche Bezeichnung | Der Name führt den nächsten Leser in die Irre |
| 15 | Wächter mit bekanntem totem Winkel | Er läuft und sieht den Fall nicht |
| 16 | Zwei Quellen schreiben voneinander ab | Eine Korrektur erreicht nur eine davon |
| 17 | Beleg zeigt auf die falsche Quelle | Die Herkunft stimmt nicht mehr |
| 18 | Fehler nur unter Randbedingungen | Zeitzone, Reihenfolge, Last |
| 19 | Konstante doppelt definiert | Zwei Werte, ein Begriff |
| 20 | Zwei Quellen, eine Herkunft | Dieselbe Messung zweimal geführt |
| 21 | Der Name sagt nicht, was der Test tut | Jede Suchmaske ist eine Annahme über den Bestand |
| 22 | Die Frage war schon beantwortet | Ohne Abgleich driftet ein Register nur in eine Richtung |
| 23 | Zahl ohne Herkunft | Keine Zähleinheit, keine Maske |
| 24 | Grün und blind | Der Test kann nicht rot werden |
| 25 | Basiszahl nachgeführt, Ableitung stehen gelassen | Die Berichtigung erreichte nur ihren Absatz |
