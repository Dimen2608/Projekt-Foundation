# Regeldateien und Ladewege

> Was in den Dateien steht, die jede Session der Bau-Session und jeder ihrer Subagents lädt, und wie
> ihre Wirkung beim Menschen bleibt. Stand der Quelle: 03.10.2026 (Teilblock 100-5, entschieden in
> ENT-214 P4 bis P6).

## Die Leitfrage

Was steht in den Dateien, die jede Session lädt, wenn die Bau-Session grüne PRs selbst mergt? **Wenig,
und nur, was kein Gate trägt.** Eine Regel, die ein Gate oder Hook durchsetzt, steht dort nur als
Verweis. Und der Schutz muss **jeden Ladeweg** abdecken, nicht nur die Wurzel-`CLAUDE.md`. Die Doku
von Claude Code nennt unter 200 Zeilen je `CLAUDE.md` und sagt, sie sei Kontext, keine erzwungene
Konfiguration.

## Ladewege

| Ladeweg | Wann | Im Repo? |
| --- | --- | --- |
| `./CLAUDE.md` und gleichwertig `./.claude/CLAUDE.md` | Start | ja |
| `CLAUDE.local.md` je Ordner | Start bzw. bei Bedarf | ja, meist ungetrackt |
| `.claude/rules/**/*.md` ohne `paths` | Start, Rang wie `.claude/CLAUDE.md` | ja |
| `.claude/rules/*.md` mit `paths`, `CLAUDE.md` in Unterordnern | bei Bedarf | ja |
| `AGENTS.md` | nur ohne `CLAUDE.md` | ja |
| `.claude/output-styles/*.md`, gewählt per `outputStyle` | jede Anfrage | ja |
| `.claude/agent-memory/<agent>/MEMORY.md` (Feld `memory` eines Agents) | System-Prompt des Agents | ja |
| `@`-Importe und Symlinks aus einer dieser Dateien | mit der importierenden Datei | ja |
| Auto-Memory `~/.claude/projects/<projekt>/memory/MEMORY.md` | Start, erste 200 Zeilen | **nein** |
| Übergeordnete `CLAUDE.md` in Elternordnern | Start, auch in Subagents | nein |
| `~/.claude/CLAUDE.md`, `~/.claude/rules/`, Managed | Start | nein |

Subagents aus `.claude/agents/` laden die ganze Hierarchie samt Projekt-Rules und `CLAUDE.local.md`,
außer mit `omitClaudeMd: true`. Ein Umsetzer liest also, was die Bau-Session an einem dieser Orte
ablegt.

**Befund der Quelle:** Ein Sperrpfad nur auf der Wurzel-`CLAUDE.md` lässt dieselbe Startwirkung über
`.claude/CLAUDE.md` oder `.claude/rules/` zu, ohne einen Sperrpfad zu berühren, und über das
Auto-Memory ganz ohne PR.

## Entschieden in der Quelle

1. **Alle Ladewege im Repo sind Sperrpfad:** `**/CLAUDE.md`, `**/CLAUDE.local.md`, `**/AGENTS.md`,
   `**/.claude/rules/**`, `.claude/output-styles/**`, `.claude/agent-memory*/**`, dazu die Prüfer
   unter `.claude/`. Der Merge-Skript-Wächter (`LOCKED_PATHS`), die CI (zweimal) und die Deny-Regeln
   der Stufe 2 tragen dieselbe Liste.
2. **Auto-Memory aus:** `autoMemoryEnabled: false` in `.claude/settings.json` (selbst Sperrpfad). Die
   CI sieht das Auto-Memory nie, also darf es nicht schreiben.
3. **Die Regeldatei heißt `.claude/rules/regeln.md`, ohne `paths`.** Sie lädt ohne Import beim Start;
   ein `@`-Import aus der `CLAUDE.md` lädt ebenso, braucht aber eine Zeile, die verloren gehen kann.
4. **Übergeordnete `CLAUDE.md` ausschließen:** per `claudeMdExcludes` in `.claude/settings.json`. Die
   Meta-Regeln, die die Bau-Session braucht (Kommunikation, Meldeweg, Übergabe, Grenzen Geld und
   außen, Freigabe des Blocks), stehen in ihrer eigenen `CLAUDE.md`. Sonst ändert jemand außerhalb
   des Repos ihre Anweisungen ohne Sperrpfad, und die 200-Zeilen-Grenze reißt allein die Elterndatei.

**Neu aufzumachen**, wenn Claude Code einen weiteren Ladeweg für Anweisungen einführt. Dann wird er
mitgesperrt, per Nachtrag, nicht still.

## Aufteilung

| Datei | Inhalt | Länge |
| --- | --- | --- |
| Wurzel-`CLAUDE.md` | wer die Bau-Session ist; Produkt in fünf Sätzen; die Spezifikation als Soll (nur lesen); Kommunikation (Sachfragen, Freigaben); Meldeweg; Übergabe; wo Werkstatt und Regeldatei liegen | ≤ 80 Zeilen |
| `.claude/rules/regeln.md` | die Bau-Regeln RV-1 bis RV-10, Sperrpfade, Kette, Definition of Done, Git und PR-Felder, Auftragsvorlage | ≤ 150 Zeilen |
| Handwerk | Skills, nicht hier: Mehrschritt-Abläufe gehören in Skills | — |

Vorlagen: [wurzel-CLAUDE.md](../templates/wurzel-CLAUDE.md), [rules/regeln.md](../templates/rules/regeln.md),
[settings.json](../templates/settings.json). Die Vorlagen heißen anders als ihr Ziel und liegen nicht
unter `.claude/`, damit eine Session, die diesen Ordner liest, sie nicht als eigene Anweisung lädt.

## Die Bau-Regeln

Hinein kommt nur, was ein Urteil des Modells verlangt. Aus einem Vorgängerbestand mit 18 Regeln sind
in der Quelle 7 übernommen, 3 umgebaut, 7 entfallen (4 davon, weil ein Gate sie trägt) und 1 offen;
dazu 3 neue.

| Regel | Trägt |
| --- | --- |
| RV-1 Nur der Block | Umfangsgrenze; den Werkstatt-Teil trägt G-7 |
| RV-2 Lage vor dem Branch | GA-1 |
| RV-3 Aussagen ans Objekt binden | Skill `belastbar-messen` |
| RV-4 Ein Weg, nicht zwei | Gate (Doppelbau) |
| RV-5 Recherche nicht ins Hauptfenster | Subagent für Suchen |
| RV-6 Zustandsaussagen mit Messdatum | Maske und Positivkontrolle |
| RV-7 Eine abgelehnte destruktive Aktion ist ein Stopp | Deny und Maske (LP-6) |
| RV-8 Die Spezifikation ist das Soll | Sachfrage statt eigener Entscheidung |
| RV-9 Abweichung statt still | Abweichungseintrag (G-7) |
| RV-10 Bestand nur lesen (projektabhängig, etwa ein Vorgänger-Repo per `git -C`) | Sachfrage |

Entfallen als Text, weil ein Gate sie trägt: Freigabe kritischer Änderungen (G-1 bis G-8),
Migrations-Reihenfolge (Migrations-Check, G-3), Tests vor Commit (lokale Stufe), Deploy-Weg
(Deploy-Workflow), Agents freigabepflichtig (Sperrpfade G-4).

## Auftragsvorlage

Jeder Auftrag der Bau-Session an eine Rolle hat neun Felder: Ziel (ein beobachtbarer Satz),
Ist-Stand mit SHA, Abnahmekriterium wörtlich, Kontext namentlich, Prämissen ungeprüft, Auftrag,
Nicht dazu (Umfangsgrenze und was die Rolle nie tut), Abbruch und Rückmeldung, Beleg. Ein leeres
Feld fällt auf, ein ungedachter Gedanke nicht. Kein Warten auf CI im Auftrag: Die Rolle pusht, die
Bau-Session wartet.

## Feuert-Nachweis

Probe-PR an `.claude/CLAUDE.md`, an `.claude/rules/x.md` und an `src/CLAUDE.md` → rot; Negativkontrolle
PR an `README.md` → grün. Subagent-Probe: Der Umsetzer nennt auf Frage eine Regel aus
`.claude/rules/regeln.md` (belegt das Laden). Auto-Memory: Nach einem Lauf ist
`~/.claude/projects/<projekt>/memory/` leer. Offen: ob ein Muster in `claudeMdExcludes` die
Elterndatei auch unter WSL2 ausschließt (Probe).
