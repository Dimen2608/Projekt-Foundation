# Walking Skeleton — die eigene Phase nach der Werkstatt

> Der Walking Skeleton ist **eine eigene Phase nach der Werkstatt** und vor dem Bau der
> Fachbereiche, nicht ihr letzter Schritt. Die grüne Werkstatt ist sein Eingang. In der Quelle war
> er zuerst als Ausgang der Werkstatt gedacht und wurde zur eigenen Phase, weil er Ergebnisse
> braucht, die die Werkstatt nicht liefert (Datenmodell, API-Contract, Deploy-Ziel). Eine
> Werkstatt, die nur auf einem leeren Repo grün ist, hat noch nichts Echtes geprüft — der Faden
> ist der erste echte Durchlauf.

## Die Regel

**Kein Fachbereich wird gebaut, bevor ein kleinster Faden durch alle Schichten läuft** — von der
Schnittstelle über die Datenbank bis zum Deploy auf Staging, mit Test in der CI. Erst danach kommt
der zweite Fachbereich.

Der Grund: Ein Plan, der vollständig vor dem Bau entsteht, trägt das Risiko, an der ersten echten
Codezeile zu brechen (Big Design Up Front). Der Faden prüft den Plan früh gegen Code statt spät.
**Jede Planannahme, die am Faden bricht, geht zurück in die Spezifikation** (Regel, ADR,
Entscheidung), bevor weitergebaut wird.

## Eingang

Der Faden beginnt erst, wenn alles hier vorliegt:

- **Die Werkstatt ist grün:** jede Prüfung hat gefeuert, CI grün auf dem leeren Repo mit
  Lebenszeichen je Pflicht-Check ([AUFSETZEN.md](../templates/AUFSETZEN.md)).
- **Der API-Contract des Fadens ist entschieden.** Der Faden läuft über die Schnittstelle, nicht
  an ihr vorbei.
- **Das Datenmodell des Fadens ist entschieden**, ebenso Identität und Rechte, soweit er sie
  berührt.
- **Ein Deploy-Ziel mit Betriebsminimum** (Staging) existiert. Das Betriebsminimum wird dafür
  vorgezogen, wenn es sonst später käme.
- Der Fachbereich des Fadens hat keine offene Frage und ein geschriebenes Abnahmekriterium.

## Ausgang

Ein Durchlauf Ende-zu-Ende auf Staging, mit Test in der CI. Der Faden ist durch dieselbe Werkstatt
gegangen wie jeder spätere PR: Test-Autor, Umsetzer-Kette, Gate, Merge-Skript, Staging-Deploy.

## Absichtlich der kleinste Faden

Der Faden nimmt **einen** Weg durch das System, nicht alle. Weitere Wege, Übersichten und
Folgebereiche kommen danach als eigene Blöcke. Die Grenze steht vor dem Bau schriftlich fest und
endet an einer benannten Stelle (zum Beispiel an einem Entwurf statt am endgültigen,
gesperrten Dokument).

**Filtersatz:** „Der Skeleton sollte auch noch …" — nein, er ist absichtlich der kleinste Faden.
Ebenso: „Wir wissen doch, wie es geht, lass uns den großen Bereich zuerst bauen" — nein.
**Neu aufzumachen**, wenn das entschiedene Datenmodell einen Punkt des Fadens unmöglich macht.

## Beispiel aus der Quelle

Im Ursprungsprojekt (Atemluft V2) ist der Faden die **Füllung**: ein Kundenweg über einen
einzigen Endpunkt, Gerät, Preis-Snapshot beim Anlegen, Kostenwert in eigener Spalte, Zeitzone an
der Basis — und er endet am **Rechnungsentwurf**, nicht an der Rechnung mit Sperre. Andere Wege
(Walk-in, Übersicht) und die Auswertung, die liest, was der Faden schreibt, sind eigene, spätere
Bereiche.
