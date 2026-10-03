# Git-Ablauf, Definition of Done, Release-Prüfung

> Was kein Gate prüft, aber jeder Block braucht: der Weg vom Branch bis `main`, die feste Liste
> „fertig“ je PR, und die Liste vor dem ersten Prod-Deploy. Stand der Quelle: 03.10.2026
> (Teilblock 100-5, entschieden in ENT-214).

## Git-Ablauf

**Frage:** Welche Git-Regeln braucht die Bau-Session, wenn kein Mensch mehr je PR freigibt und der
Server nichts erzwingt?
**Antwort:** ein Weg, acht Schritte. Daneben gehen nur die Wege des Menschen: sein signierter Commit
an Sperrpfaden und sein eigener Merge. Jeder Schritt nennt, wer ihn prüft. Wo kein Gate prüft, steht
das als Grenze da, nicht als Regel ohne Wirkung. Was „grün“ heißt, steht in
[gruen-und-gate.md](gruen-und-gate.md); hier steht nur das Delta.

| # | Schritt | Regel | Geprüft durch |
| --- | --- | --- | --- |
| 1 | Lage | Vor dem Branch: `git fetch --prune`, `git worktree list`, offene PRs auf denselben Pfaden (`gh pr list --state open --json number,files`). Überschneidung → anderer Block oder warten | niemand; Grenze GA-1 |
| 2 | Branch | Von aktuellem `origin/main`, ein Branch je Block: `bau/<block>-<kurz>`, `nacharbeit/<pr>-<kurz>`, `werkstatt/<kurz>`; ASCII, klein, Bindestriche | niemand; den Werkstatt-PR erkennt das Merge-Skript an den Pfaden (G-7), nicht am Namen |
| 3 | Commit | Betreff mit Blocknummer, Rumpf mit dem Warum; vor `/simplify` committen; kein `--no-verify` | lokale Stufe; G-4 |
| 4 | Umfang | Nur Dateien des Blocks. Werkstatt-Dateien nie mit Produktcode (G-7), Sperrpfade nie (G-4) | G-4, G-7 |
| 5 | PR | Kein Draft. Geöffnet am Ende der Umsetzer-Kette, Text nach der PR-Vorlage GA-2 | Gate (G-8) liest Text und Diff |
| 6 | Aktualität | Liegt der Kopf hinter `origin/main`: `gh pr update-branch` (Merge von `main` in den Branch). **Kein Rebase** eines gepushten Branches | G-3 |
| 7 | Merge | Über das Merge-Skript mit Merge-Vermerk; bis es auf `main` liegt, per `gh pr merge` nach grüner CI | Merge-Skript, Merge-Vermerk auf `main` |
| 8 | Aufräumen | GA-3 | niemand; ein Rest fällt erst im Lage-Schritt des nächsten Blocks auf |

**Warum kein Rebase:** Ein Rebase in der Arbeitskopie ließe sich nur mit `git push --force` hochladen,
und das sperrt die Leitplanke LP-6; ein Rebase auf dem Server schreibt die Historie des Branches um.
Der Merge von `main` erfüllt G-3 ebenso (`git merge-base --is-ancestor` prüft nur, ob `origin/main`
enthalten ist). Folge: neue Kopf-SHA, neuer CI-Lauf, neues Gate-Urteil, derselbe Preis wie beim
Rebase.

**Nach dem zweiten Gate-„nein“** bleibt der PR offen und ungemergt, mit Label `gate-nein`. Die
Bau-Session schließt ihn nicht selbst, damit die Rückschau die Wiederholung sieht.

**GA-1 Lage vor dem Branch.** Verhindert, dass zwei Läufe dieselbe Datei bauen und dass gegen einen
veralteten Checkout gearbeitet wird. Ab dem zweiten gleichzeitig schreibenden Lauf trägt die
Worktree-Pflicht ([isolation.md](isolation.md)). Feuert-Nachweis keiner: Kein G-Punkt prüft
Doppelbau. **Grenze, benannt:** Danach fängt ihn G-3 (Konflikt) oder das Gate („global redundant“).

**GA-2 PR-Vorlage.** Verhindert „Abwesenheit sieht aus wie Bestätigung“: einen PR ohne „wie
verifiziert“. Felder: (1) Block und Soll-Quelle. (2) Abnahmekriterium wörtlich. (3) Was und warum.
(4) Wie verifiziert: Befehl und Ergebnis, kein „Tests grün“. (5) Abweichungseintrag: ja/nein.
(6) `nacharbeit`: verursachender PR. (7) Mutationsproben je Wachposten. (8) Sicherheitsbericht und
Vermerke zum Baum-Hash. Bei einer Oberfläche mit Bildvergleich: geänderte Bilder je Ort und Zustand.
Die Felder stehen in der Regeldatei; als `.github/pull_request_template.md` ist die Vorlage
Werkstatt-Pfad (G-7). Feuert-Nachweis: Probe-PR mit leerem „Wie verifiziert“ → Gate „nein“;
vollständiger PR → „ja“.

**GA-3 Aufräumen nach dem Merge.** Den Fern-Branch löscht die Repo-Einstellung „Automatically delete
head branches“, nicht `--delete-branch`: Der löscht lokal zuerst und überspringt bei ausgechecktem
Worktree still die Fernlöschung. Danach `git fetch --prune`, `git worktree remove <pfad>`,
`git branch -d <branch>` (klein `-d`, verweigert ungemergte Branches; `-D` sperrt LP-6). Feuert-
Nachweis nach dem ersten Merge: `git ls-remote --heads origin <branch>` leer, `git worktree list` ohne
den Block.

**Repo-Einstellungen, setzt der Mensch beim Aufsetzen:** automatisch löschen an, Squash- und
Rebase-Merge aus. Der Merge-Vermerk verlangt Merge-Commits; so verweigert der Server den falschen
Weg, statt dass `main` ihn erst danach rot meldet. Messen mit `gh api repos/<owner>/<repo>` (GET):
`delete_branch_on_merge`, `allow_squash_merge`, `allow_rebase_merge`, `allow_merge_commit`.

## Definition of Done je PR

**Frage:** Wann ist eine Änderung fertig, wenn kein Mensch je PR freigibt?
**Antwort:** eine feste Liste neben dem Abnahmekriterium, je Punkt ein Nachweisweg. Fast jeder Punkt
ist schon ein Gate oder ein Schritt der Umsetzer-Kette; die Liste ordnet sie. Ein Punkt ohne
Nachweisweg ist Prosa und kommt nicht hinein.

| # | Punkt | Nachweisweg | Prüft |
| --- | --- | --- | --- |
| D-1 | Abnahmekriterium wörtlich im PR, Test vom Test-Autor, vor dem Bau rot | PR-Feld (2); Test gegen die Schnittstelle | Gate (G-8) |
| D-2 | Jeder Pflicht-Check `success` mit Lebenszeichen über null | Merge-Skript | G-1, G-5 |
| D-3 | Keine Lockerung ohne Abweichungseintrag, kein entschiedener Wert gelockert | Wächter aus `main` | G-4, G-7 |
| D-4 | Umsetzer-Kette vollständig zum Baum-Hash, Mutationsproben eingeschlossen | Stop-Hook, Gate Punkt 0 | Hook, Gate |
| D-5 | Diff-Coverage über der entschiedenen Schwelle, mit Zweigen | Pflicht-Check | G-1 |
| D-6 | Migration: ein Head, hoch und runter | Pflicht-Check, ab der ersten Migration | G-1 |
| D-7 | Nutzerdoku mitgeführt, wenn das Projekt eine solche Pflicht hat (etwa Hilfe je Seite) | Maske „jede Route hat einen Eintrag“ in den Tests; Inhalt prüft das Gate | Tests, Gate |
| D-8 | Oberfläche: Design-Gate bestanden, wenn das Projekt eines hat | Barrierefreiheit, Bildvergleich (unten) | G-1, Gate |
| D-9 | Keine Sperrpfade berührt; Werkstatt getrennt | G-4, G-7 | Merge-Skript |
| D-10 | `nacharbeit` gesetzt, wenn der PR einen gemergten Fehler behebt | Selbstauskunft der Bau-Session | Rückschau, Rework Rate |

D-7 und D-8 sind projektabhängig; fehlen sie, steht „entfällt, weil …“ in der Liste, nicht nichts.

### Design-Gate (optional, für Projekte mit Oberfläche)

**Barrierefreiheit:** Pflicht-Check je Ort und Zustand, in jeder Farbbelegung (etwa Playwright
`colorScheme` hell und dunkel) mit `@axe-core/playwright`; Lebenszeichen ist die Zahl geprüfter
Seiten. axe-core hat `color-contrast` (AA) an und `color-contrast-enhanced` (AAA) aus; wer AAA
verlangt, schaltet es ausdrücklich ein (Probe). Feuert-Nachweis: Seite unter AA → rot; Seite nur in
einer Belegung kontrastschwach → rot in diesem Lauf, grün im anderen (belegt, dass beide laufen);
Seite mit Token-Farben → grün.

**Bildvergleich in zwei Stufen.** Ein Pixelvergleich gegen eine Designprobe, die eine andere Seite
ist als das Produkt, ist kein taugliches Rot-Kriterium. Messbar sind:
1. **Token-Gleichheit:** Die Token-Datei ist byte-gleich mit der abgenommenen Fassung (Hash), und
   außerhalb von ihr steht kein Farbliteral. Pflicht-Check `tokens`.
2. **Erst-Abnahme durch den Menschen:** Die CI rendert je Ort, Zustand, Belegung und Dichte das
   Produktbild und, wo vorhanden, das Probebild nebeneinander (Artefakt). Der Mensch nimmt jedes
   Bild ab, ohne Probe auch ohne Vorlage.
3. **Regression automatisch:** Das abgenommene Bild ist das Soll. Pflicht-Check `bildvergleich`
   (etwa Playwright `toHaveScreenshot`), Schwelle zu Beginn streng; eine Lockerung ist nach G-7 rot,
   sobald die Schwelle entschieden ist. Lebenszeichen: Zahl verglichener Bilder.

Soll und Ist nur im gepinnten Image auf dem Runner, nie auf einem Entwicklerrechner; feste Uhr,
Seed-Daten, selbst gehostete Schrift mit `document.fonts.ready`. **Soll-Bilder und Token-Datei sind
Sperrpfad:** Ein neues Soll legt die Bau-Session in einen eigenen PR, den das Merge-Skript nie mergt;
der Mensch übernimmt die Bilder mit signiertem Commit. Preis, benannt: Jede gewollte
Oberflächenänderung wartet auf den Menschen. Ein „ist gewollt“ der Bau-Session macht den Vergleich
nicht grün, nur das neue Soll. Fehlalarm (rot, auf derselben SHA ohne Änderung grün) zählt ein
Wochenzähler.

Feuert-Nachweis: Farbwert im Code statt in der Token-Datei → rot; wertgleiches Farbliteral im Code →
`tokens` rot; Knopf um 4 px verschoben → `bildvergleich` rot; Soll-Bild ausgetauscht → rot nach G-4;
PR ohne Oberflächenänderung → grün; derselbe Lauf zweimal auf derselben SHA → gleiches Ergebnis.

## Release-Prüfung und Livegang-Liste

Den Prod-Deploy löst nur der Mensch aus. Die Release-Prüfung ist deshalb **eine Liste vor dem ersten
Prod-Deploy**, nicht je PR, gegliedert nach der Production Readiness Review (Google SRE Book,
Kap. 32): Architektur und Abhängigkeiten, Monitoring und Notfallreaktion, Kapazität und Performance,
Änderungsmanagement; dazu die Livegang-Pflichten des Projekts. Je Achse steht der Träger im Plan.

Die **Livegang-Liste** führt jede Pflicht vor dem Start mit Wer, Nachweis und Quelle; eine Zeile ohne
Quelle kommt nicht hinein. Gefunden werden die Zeilen mit einer ausgeführten Maske über das
Entscheidungsprotokoll, mit Positivkontrolle. Abgehakt wird mit Datum und Beleg. Vorlage:
[LIVEGANG.md](../templates/LIVEGANG.md).

## Filtersatz

Vorschläge, gepushte Branches zu rebasen, einen Draft-PR früh zu öffnen, den Bildvergleich direkt
gegen eine Designprobe zu fahren oder Soll-Bilder durch die Bau-Session setzen zu lassen, prallen ab.
**Neu aufzumachen**, wenn der Server einen Merge-Weg erzwingen kann, der den Merge-Vermerk ersetzt,
oder wenn der Bildvergleich mehr als einen Fehlalarm je Woche zeigt.
