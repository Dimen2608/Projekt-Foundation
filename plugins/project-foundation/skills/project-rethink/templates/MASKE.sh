#!/usr/bin/env bash
# <name>.sh — Maske zu <Regel oder Entscheidung>, aufgerufen von der Zahlenpruefung je Block.
#
# SHELL: bash. Unter Windows ist damit GIT-BASH gemeint, NICHT PowerShell. Die Datei
#   laeuft in PowerShell nicht, und die Werkzeugfallen unten (Pfad-Umschreibung durch
#   MSYS, MSYS_NO_PATHCONV) betreffen genau diese Git-Bash.
#
# Eine Maske, die niemand ausfuehrt, ist eine Meinung. Deshalb liegt sie als Datei im
# Repository, versioniert neben dem, was sie prueft — nicht als Satz in einer Vorgabe.
#
# FRAGE, DIE DIESE MASKE BEANTWORTET
#   <Eine Frage, keine Aufgabe. Sie muss mit ja/nein oder mit einer Liste beantwortbar
#    sein, und ein Dritter muss an der Ausgabe erkennen koennen, ob sie beantwortet ist.>
#
# ZAEHLEINHEIT
#   <Was genau eine Zeile der Ausgabe zaehlt. Ohne diese Angabe ist jede Zahl, die aus
#    dieser Maske stammt, wertlos — zwei Leser zaehlen sonst zwei Groessen.>
#
# NORMALISIERUNG
#   <Welche Schreibweisen zusammenfallen, damit dasselbe nicht zweimal zaehlt.>
#
# MESSSTAND
#   Diese Maske ist an einen benannten Stand gebunden, nicht an den Arbeitsbaum. Ein
#   Aufruf ohne Stand misst, was zufaellig ausgecheckt ist, und kann die Zahl, die neben
#   ihr steht, gar nicht erzeugt haben.
#
# AUSGABE IST EIN VERDACHT, KEIN URTEIL
#   Eine Maske weiss nicht, WARUM eine Stelle so aussieht. Sie trifft auch Saetze, die
#   ausdruecklich begruenden, dass etwas NICHT geschieht. Jede Ausgabezeile wird an ihrer
#   Fundstelle gelesen, bevor sie ein Befund wird.
#
# LEERE AUSGABE BRAUCHT EINE POSITIVKONTROLLE
#   Leer ist das Bild eines gelungenen Abwesenheitsbeweises und zugleich das Bild einer
#   kaputten Maske. Der Schalter --positivkontrolle laeuft dieselbe Maske gegen einen
#   bekannten Treffer. Liefert er nichts, ist die Maske defekt, nicht der Bestand leer.
#
# BEWUSSTE GRENZEN
#   1. <Was diese Maske strukturell nicht sehen kann.>
#   2. Zeilenweise: was ueber einen Zeilenumbruch laeuft, faellt durch.
#   3. Spaltenmasken ueber Tabellen zaehlen von RECHTS — ein maskiertes Trennzeichen in
#      einer Zelle verschiebt sonst jede Spalte.
#
# AUFRUF
#   <name>.sh <stand> <pfadmuster> [--positivkontrolle]

set -u

stand="${1:?Messstand fehlt — eine Maske ohne Stand misst den Arbeitsbaum}"
pfadmuster="${2:?Pfadmuster fehlt}"
modus="${3:-normal}"

# Git-Bash/MSYS schreibt unter Windows jedes Argument um, das mit / oder ./ beginnt: aus
# ^/etc/ wird ^C:/Program Files/Git/etc/ — ohne Fehlermeldung. Das Muster kommt nie als
# Muster an, und das Ergebnis ist null Treffer: genau das Bild eines gelungenen
# Abwesenheitsbeweises. Also fuehrenden Schraegstrich vermeiden ODER abschalten:
export MSYS_NO_PATHCONV=1

muster='<Suchmuster>'
gegenmuster='<Muster, das sicher trifft — fuer die Positivkontrolle>'

suchen() {
  git grep -n -F "$1" "$stand" -- "$pfadmuster"
}

normalisieren() {
  sed -E 's/<zusammenfallende Schreibweisen>//g' | sort -u
}

if [ "$modus" = "--positivkontrolle" ]; then
  echo "# Positivkontrolle: dieselbe Maske gegen einen bekannten Treffer"
  suchen "$gegenmuster" | normalisieren
  exit 0
fi

treffer=$(suchen "$muster" | normalisieren)

if [ -z "$treffer" ]; then
  echo "# Leere Ausgabe. Kein Befund — ERST nachdem --positivkontrolle getroffen hat." >&2
  exit 0
fi

printf '%s\n' "$treffer"
