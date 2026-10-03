# ADR-0021: `project-werkstatt` bekommt Definition of Done, Regeldateien und ausformulierte Vorlagen

## Status

Accepted — 2026-10-03

## Context

ADR-0020 hat `project-werkstatt` auf den Stand der Quelle vom 02.10.2026 gebracht und als offen
markiert: Definition of Done und Git-Ablauf, die ausformulierten Agent-Texte, die Hook-Skripte,
das Format der Gate-Marker, dazu `CLAUDE.md` und Regeldatei als Sperrpfad „nach der Definition of
Done“.

Die Quelle (Werkstatt-Plan Atemluft V2) hat diese Teile am 03.10.2026 geschlossen:

- Teilblock 100-5 mit ENT-214: Git-Ablauf in acht Schritten, Definition of Done D-1 bis D-10 mit
  Design-Gate und Bildvergleich in zwei Stufen, alle Ladewege für Anweisungen gesperrt,
  Auto-Memory aus, Regeldatei `.claude/rules/regeln.md`, übergeordnete `CLAUDE.md` ausgeschlossen,
  Repo-Einstellungen gegen Squash und Rebase.
- Teilblock 100-6 mit dem Nachtrag und dem Zweiten Nachtrag zu ENT-214 samt Berichtigung: die
  Vorlagen der Sperrpfade (vier Agents, fünf Hook-Skripte, Skills als Plugin mit sieben
  Auslöse-Evals, Einstellungen, Wurzel-`CLAUDE.md`, Regeldatei), Gate-Marker v1, Livegang-Liste,
  Mutationsprobe neuer Wachposten durch den Umsetzer nach dem Bau (M-T1), Längenrahmen je Vorlage
  (ein Skill höchstens 500 Zeilen; Plan und Vorlagen zusammen kürzer als die Spezifikation).

Der Auftraggeber hat am 03.10.2026 beauftragt, beides in einem Lauf nachzuziehen, verallgemeinert
für beliebige Projekte und ohne Fachinhalt der Quelle.

## Decision

1. **Nachziehen, nicht neu schneiden** (Grenze von ADR-0018, wie ADR-0020). Ablauf, Rollen und
   Grün-Definition bleiben; die Teile kommen in die bestehenden Schritte ROLLEN, SPERREN und
   PROBEN.
2. **Jeder Ladeweg ist Sperrpfad.** `**/CLAUDE.md`, `**/CLAUDE.local.md`, `**/AGENTS.md`,
   `**/.claude/rules/**`, `.claude/output-styles/**`, `.claude/agent-memory*/**` kommen zu den
   Prüfern unter `.claude/`. Die Liste steht an vier Stellen, die sich nur zusammen ändern:
   `LOCKED_PATHS` (samt Arbeitskopie-Abgleich) in `merge-gruen.py`, zweimal in `ci-werkstatt.yml`,
   die Deny-Zeilen der Stufe 2 in `LEITPLANKEN.md`. `LOCKED_FILES` bleibt für projekteigene
   Einzeldateien (etwa Token-Datei); `CLAUDE.md` und Regeldatei deckt das Muster schon ab, auch in
   Unterordnern und unabhängig von der Schreibweise. Auto-Memory ist aus, übergeordnete `CLAUDE.md`
   ausgeschlossen.
3. **Ausformulierte Vorlagen statt Gerüste.** Die vier Agent-Vorlagen tragen den vollen Prompt,
   die fünf Hook-Skripte liegen unter `templates/hooks/`, die vier Skills auf dem Stand der Quelle
   mit Plugin-Manifest und sieben Eval-Fällen. Die Eval-Vorlagen liegen unter
   `templates/skills/eval-faelle/`, nicht unter einem Ordner `evals/`, damit kein Werkzeug sie als
   Evals dieses Plugins aufgreift. Wurzel-`CLAUDE.md` und Regeldatei heißen in den Vorlagen anders
   als ihr Ziel und liegen nicht unter `.claude/`, damit eine Session, die den Skill-Ordner liest,
   sie nicht als eigene Anweisung lädt.
4. **Gate-Marker v1** `<!-- werkstatt-gate v1 sha=… urteil=… -->` mit `##`-Abschnitten, gleich
   in `gate.md`, `gate_stop.py` und `merge-gruen.py`. G-3 verlangt `gh pr update-branch` statt
   Rebase.
5. **Mutationsprobe nach dem Bau** (M-T1): Der Test-Autor führt die Liste
   `wachposten-offen.txt`, der Umsetzer probt nach dem Bau, `kette_protokoll.py` protokolliert,
   `umsetzer_stop.py` prüft, das Gate liest.
6. **Frontmatter innerhalb von ADR-0019.** Die Quelle setzt `maxTurns` (200 und 60) und beim Gate
   `disallowedTools`. `maxTurns` bleibt draußen, bis die Probe zeigt, dass es eine Stopp-Schleife
   beendet; der Ausweg ist die Abbruchdatei. `disallowedTools` ist beim Gate überflüssig, weil
   `tools` Edit, Write und Agent schon nicht nennt. Damit greift die Stop-Condition „Frontmatter-Feld
   jenseits der Liste“ nicht.
7. **Projektabhängiges bleibt Platzhalter oder Option.** Hilfe je Seite (D-7) und Design-Gate (D-8)
   sind projektabhängig und stehen sonst als „entfällt, weil …“; die Livegang-Liste ist eine
   Vorlage mit typischen Zeilen, je nur mit eigener Quelle. Nicht übernommen: Fachentscheidungen
   der Quelle (Statuscodes einzelner Endpunkte, Testaufträge), die Zahlen ihrer Probe-Bilder, ihre
   Session-Namen.
8. **Hook-Skripte geprobt ohne Modell.** 24 Proben mit Fixture-Payload im Wegwerf-Repo, darunter
   ein Mutant des Hooks, 0 Abweichungen. Mit echtem Payload sind sie offen. Die Skripte laufen wie
   die übrigen Skizzen durch `ruff`, nicht durch `mypy` und `pytest`.
9. **Umfang nach ADR-0011**, je neue Vorlage die Frage:

   | Frage | Vorlage |
   | --- | --- |
   | Wer erzwingt die Reihenfolge der Kette und das Urteil des Gates? | `hooks/` (fünf Skripte) |
   | Was lädt jede Session als Anweisung, und was steht darin? | `wurzel-CLAUDE.md`, `rules/regeln.md`, `settings.json` |
   | Löst ein Skill aus, wenn er soll, und bleibt er still, wenn nicht? | `skills/plugin.json`, `skills/eval-faelle/` |
   | Was muss vor dem ersten Prod-Deploy erledigt sein, und wer belegt es? | `LIVEGANG.md` |

   Dazu zwei Dateien unter `reference/`: `git-und-dod.md`, `regeldateien.md`.
10. **Offen bleibt und ist markiert:** Hooks mit echtem Payload (Workspace-Trust, `claude -p`,
    `disableAllHooks`, Feld `skill`, `cwd` im Worktree), die Sperr-Hooks der Leitplanken, die
    Proben der Leitplanken und der Isolation, `maxTurns`, die Übergabe der Testdateien aus dem
    Worktree, Fixture und Baseline der Evals, Stufe 2 des Sicherheitskatalogs und die Lizenzfrage
    der ASVS-CSV.
11. **Keine Validator-Änderung.** Keine neue Pflichtstelle, keine Finding-ID, `schema_version`
    bleibt `1`. Die Beschreibung des Skills bleibt unverändert; ein neuer Auslöse-Test ist nicht
    nötig.
12. **Version 0.10.0.**

Verworfene Alternativen:

- **Nur Wurzel-`CLAUDE.md` und Regeldatei als `LOCKED_FILES`.** So stand es in ADR-0020. Dieselbe
  Startwirkung erreicht ein PR über `.claude/CLAUDE.md`, `.claude/rules/` oder eine `CLAUDE.md` in
  einem Unterordner, ohne einen Sperrpfad zu berühren. Die Quelle hat das als Befund gemessen und
  alle Ladewege gesperrt.
- **Die Quell-Vorlagen wörtlich übernehmen.** Sie tragen Session-Namen, Spezifikationsorte und
  Fachregeln eines Projekts. Verallgemeinert bleiben Struktur, Proben und Grenzen.
- **Vorlagen unter `templates/.claude/`.** Dann läse eine Session in diesem Repo sie als eigene
  Anweisungen.

## Consequences

**Positiv**

- Ein Zielprojekt bekommt einen vollständigen ersten Stand aller Sperrpfade, den die Bau-Session
  nur noch wörtlich kopiert: Der Geprüfte legt den Vertrauensanker nicht selbst an.
- Hook, Stop-Hook und Merge-Skript lesen dasselbe Marker-Format; ein Bruch dazwischen fällt in den
  Proben auf.
- Die Mutationsprobe neuer Wachposten fällt nicht mehr still weg, bis ein nächtlicher Lauf kommt.

**Negativ**

- Der Skill wird deutlich länger: zwei Reference-Dateien, fünf Hook-Skripte, drei Vorlagen für
  Ladewege, ein Manifest, sieben Eval-Fälle und die Livegang-Vorlage mehr.
- Die Hook-Skripte sind nur ohne Modell geprobt. Was Claude Code im echten Payload liefert, kann
  sie noch brechen; das zeigt erst das Aufsetzen.
- Jede gewollte Änderung an `CLAUDE.md` oder Regeldatei wartet auf einen signierten Commit des
  Menschen.

**Grenze**

Neu zu bewerten, wenn eine Probe mit echtem Payload ein Hook-Skript widerlegt (neue Vorlage), wenn
`maxTurns` als wirksam belegt ist (Feld aufnehmen, ADR-0019 erweitern), wenn Claude Code einen
weiteren Ladeweg einführt (mitsperren) oder wenn die Lizenzfrage erlaubt, ASVS-Text abzulegen.
