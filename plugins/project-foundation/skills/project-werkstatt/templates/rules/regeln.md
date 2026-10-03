<!--
Vorlage aus project-werkstatt. Ziel: .claude/rules/regeln.md, ohne `paths` im Frontmatter, damit
sie beim Start jeder Session und jedes Subagents lädt (Sperrpfad). Höchstens 150 Zeilen. Diesen
Kommentar beim Kopieren entfernen. Herleitung: reference/regeldateien.md.
-->
# Bau-Regeln {{PROJEKT}}

Diese Datei lädt beim Start jeder Session und jedes Subagents. Sie ist Sperrpfad: Änderungen schlägt
die Bau-Session vor, {{MENSCH}} committet sie signiert. Hier steht nur, was ein Urteil verlangt. Was
ein Gate durchsetzt, steht als Verweis; die Gates gelten, auch wenn hier nichts steht.

## Die Regeln

**RV-1 Nur der Block.** Gebaut wird, was der Auftrag nennt. Was daneben auffällt, geht in die
Rückmeldung, nicht in den Diff. Werkstatt-Dateien nie im selben PR wie Produktcode (G-7).

**RV-2 Lage vor dem Branch.** Vor jedem Block `git fetch --prune`, `git worktree list` und die offenen
PRs auf denselben Pfaden (`gh pr list --state open --json number,files`). Überschneidung: anderer
Block oder warten.

**RV-3 Aussagen ans Objekt binden.** Eine Aussage über einen Zustand nennt das Objekt, an dem sie
gemessen ist (SHA, Datei:Zeile, Endpunkt, Datenbank), und die Maske, mit der gemessen wurde.
Handwerk: Skill `belastbar-messen`.

**RV-4 Ein Weg, nicht zwei.** Gibt es für eine Aufgabe schon einen Weg im Bestand, wird er benutzt
oder ersetzt, nie ein zweiter daneben gebaut. Das Gate blockiert Doppelbau.

**RV-5 Recherche nicht ins Hauptfenster.** Suchen über viele Dateien oder im Netz laufen in einem
Subagent; zurück kommt der Befund mit Belegen, nicht der Rohtext.

**RV-6 Zustandsaussagen mit Messdatum.** Wer „läuft“, „ist grün“, „fehlt“ schreibt, nennt, wann und
gegen welchen Stand gemessen wurde. Eine Abwesenheit braucht die ausgeführte Maske und eine
Positivkontrolle.

**RV-7 Eine abgelehnte destruktive Aktion ist ein Stopp.** Lehnt eine Regel oder {{MENSCH}} einen
Befehl ab, wird derselbe Zweck nicht auf anderem Weg erreicht. Melden, warten.

**RV-8 Die Spezifikation ist das Soll.** Das Abnahmekriterium steht wörtlich im Auftrag und im PR.
Fehlt eine Fachantwort: Sachfrage, nie selbst entscheiden.

**RV-9 Abweichung statt still.** Was vom Werkstatt-Plan oder der Spezifikation abweicht, steht als
Abweichungseintrag im Werkstatt-PR (G-7) oder als Sachfrage.

**RV-10 {{BESTAND_NUR_LESEN}}**

## Sperrpfade

Ein PR, der einen dieser Pfade berührt, ist rot (G-4); ändern darf sie nur {{MENSCH}} per signiertem
Commit: `.claude/agents/**`, `.claude/hooks/**`, `.claude/skills/**`, `.claude/settings*.json`,
`**/CLAUDE.md`, `**/CLAUDE.local.md`, `**/AGENTS.md`, `**/.claude/rules/**`,
`.claude/output-styles/**`, `.claude/agent-memory*/**`{{WEITERE_SPERRPFADE}}.

## Die Kette je Block

1. **Test-Autor** schreibt die Tests aus dem Abnahmekriterium, im eigenen Worktree; sie sind rot.
2. **Umsetzer** baut bis grün, committet, `/simplify`, Tests erneut, Mutationsprobe je Eintrag in
   `{{TESTVERZEICHNIS}}wachposten-offen.txt` (schreibt der Test-Autor), `/security-review` als
   Bericht, Wächter lokal, Push, PR. Sein Stop-Hook prüft die Reihenfolge.
3. **Gate** urteilt zur Kopf-SHA, als PR-Kommentar mit Gate-Marker.
4. **Merge-Skript** mergt nur bei grün (G-1 bis G-8); danach Aufräumen und Übergabe.

**Testlauf für die Kette:** Jeder Testlauf, der für die Kette zählt, schreibt JUnit-XML mit genau der
Option `--junitxml=.claude/run/testbericht.xml`: `{{TEST_BEFEHL}}`. Wächter: `{{WAECHTER_BEFEHL}}`.

**Ablage:** `.claude/run/` ist gitignored. Dort liegen `kette.log`, `hook-audit.log`, Testberichte,
Mutationsberichte (`--junitxml=.claude/run/mutationsbericht.xml`), `sicherheitsbericht-<baum>.md`,
`sicherheitsvermerke-<baum>.md`, `gate-urteil.md`, `abbruch.md` (nach Gebrauch `abbruch-<zeit>.md`)
und `payload-<event>.json`.

## Definition of Done je PR

D-1 Abnahmekriterium wörtlich im PR, Test vom Test-Autor, vor dem Bau rot. D-2 jeder Pflicht-Check
`success` mit Lebenszeichen über null. D-3 keine Lockerung ohne Abweichungseintrag, kein
entschiedener Wert gelockert. D-4 Umsetzer-Kette vollständig zum Baum-Hash. D-5 Diff-Coverage
mindestens {{DIFF_COVERAGE}} % der geänderten Zeilen mit Zweigen. D-6 Migration: ein Head, hoch und
runter. D-7 {{DOKU_PFLICHT}}. D-8 Oberfläche: {{DESIGN_GATE}}. D-9 keine Sperrpfade berührt,
Werkstatt getrennt. D-10 `nacharbeit` gesetzt, wenn der PR einen gemergten Fehler behebt.

## Git

Branch je Block von aktuellem `origin/main`: `bau/<block>-<kurz>`, `nacharbeit/<pr>-<kurz>`,
`werkstatt/<kurz>`. Commits mit Blocknummer im Betreff und dem Warum im Rumpf. Kein Draft-PR.
Hinter `origin/main`: `gh pr update-branch`, kein Rebase eines gepushten Branches. Kein `--force`,
kein `--no-verify`, kein `git reset --hard`. Nach dem zweiten Gate-„nein“ bleibt der PR offen mit
Label `gate-nein`. Nach dem Merge: `git fetch --prune`, `git worktree remove`, `git branch -d`.

**PR-Text, Felder:** (1) Block und Soll-Quelle. (2) Abnahmekriterium wörtlich. (3) Was und warum.
(4) Wie verifiziert: Befehl und Ergebnis, kein „Tests grün“. (5) Abweichungseintrag: ja/nein.
(6) `nacharbeit`: verursachender PR. (7) Mutationsproben je Wachposten. (8) Sicherheitsbericht und
Vermerke zum Baum-Hash.

## Auftragsvorlage

Jeder Auftrag der Bau-Session an eine Rolle hat diese Felder. Ein leeres Feld fällt auf, ein
ungedachter Gedanke nicht.

1. **Ziel:** ein beobachtbarer Satz.
2. **Ist-Stand:** Branch und SHA, gegen die gearbeitet wird.
3. **Abnahmekriterium:** wörtlich aus der Spezifikation, mit Fundstelle.
4. **Kontext:** Dateien, Entscheidungen, Regeln namentlich.
5. **Prämissen:** was die Bau-Session annimmt, aber nicht geprüft hat.
6. **Auftrag:** was die Rolle tut.
7. **Nicht dazu:** die Umfangsgrenze, und was die Rolle nie tut (Sperrpfade, Merge, Fachentscheidung).
8. **Abbruch und Rückmeldung:** wann die Rolle abbricht (Grund nach `.claude/run/abbruch.md`) und was
   sie zurückmeldet.
9. **Beleg:** woran die Bau-Session das Ergebnis prüft.

Kein Warten auf CI im Auftrag: Die Rolle pusht, die Bau-Session wartet.
