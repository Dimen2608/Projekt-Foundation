# Eingebaute Skills und Evals

> Gemessene Fakten, auf denen die Umsetzer-Kette steht, und wie Auslösen gemessen wird.
> **Stand: 01.10.2026**, Claude Code 2.1.285. Eine neue Fassung eines der Skills kann ihr
> Verhalten ändern — beim Aufsetzen den Skilltext erneut prüfen.

## `/security-review` und `/simplify`

Gemessen in einem Wegwerf-Repo (`git init`, eine gestagete Änderung mit eingebauter Command
Injection), aus der Hauptsession und aus einem Subagent.

| Befund | Folge für die Werkstatt |
| --- | --- |
| **`/security-review` liefert nur einen Bericht.** Der Skilltext verlangt, keine Datei zu schreiben; danach war keine Datei geändert. Er fand die eingebaute Lücke und meldete eine ältere im unveränderten Kontext bewusst nicht: Er bewertet **nur neu hinzugefügten Code**. | Der Bericht braucht einen Leser mit Wirkung — das Gate (Prüfpunkt 6). Ohne ihn wäre er ein Bericht ohne Wirkung. |
| **`/security-review` liest Status und Diff aus dem Arbeitsverzeichnis der Session**, nicht aus einem Pfad im Auftrag. In der Probe stammte der Git-Kontext aus dem falschen Repo. Ein Pfad als Argument genügt nicht; außerhalb eines Git-Repos bricht er ab. | **Alle Rollen laufen mit dem Projekt-Repo als Arbeitsverzeichnis.** Ein Agent aus einem anderen Verzeichnis prüft den falschen Diff und meldet grün. Er braucht ein `origin`, gegen dessen Default-Branch er vergleicht. |
| **`/simplify` ändert Dateien schon ohne Flag.** Ablauf: vier Review-Agents parallel, danach werden die Funde angewandt. Ein Berichtsmodus war im Skilltext nicht zu sehen. | **Vor jedem `/simplify` committen**, damit git den Rückweg hält. Danach die Tests erneut. |
| **`/simplify` startet vier Review-Agents.** | Einmal am Blockende, nicht nach jeder Teiländerung. Der Umsetzer braucht das Werkzeug `Agent`. Kosten je Aufruf sind nicht gemessen (`/usage`). |
| **Beide lassen sich aus einem Subagent aufrufen** (über das Skill-Werkzeug). `/simplify` wurde dort bis zum Start der Review-Agents geprüft, nicht bis zu den angewandten Änderungen. | Die Bindung an die Rollen trägt. `Skill` darf dem Umsetzer nicht per `tools` oder `disallowedTools` entzogen sein. |

**Nicht geprüft:** ob ein Subagent `/code-review` aufrufen kann; ob ein Projekt-Skill namens
`security-review` den eingebauten Befehl ersetzt (nicht dokumentiert) — deshalb heißt der eigene
Katalog `sicherheits-katalog`; ob `disable-model-invocation: true` das Vorladen per `skills:`
verhindert — deshalb nicht setzen. `/code-review` taugt als Zulieferer, nicht als Gate: Er liefert
kein maschinenlesbares Urteil und ist ohne ausdrückliche Effort-Stufe uneinheitlich.

## Skills: Budget und Verpackung

- Beschreibung und `when_to_use` zusammen höchstens 1.536 Zeichen je Skill; das Listing insgesamt
  1 % des Kontextfensters. Vorschlag der Quelle: höchstens 6 Skills, Beschreibung höchstens 700
  Zeichen.
- Die Skills liegen als Plugin im Repo (`.claude/skills/<plugin>/.claude-plugin/plugin.json`,
  Skills unter `skills/<name>/SKILL.md`, Evals unter `evals/`). Claude Code lädt solche
  `@skills-dir`-Plugins nur unter `<repo>/.claude/skills/`, nach Workspace-Trust, nicht aus
  Elternordnern. So sind sie mit `claude plugin validate --strict` prüfbar, kostenlos und
  deterministisch; `author` im Manifest, sonst warnt `--strict`. Die Agents nicht (Plugin-Agents
  ignorieren `hooks`).
- **Gemessen in der Quelle (2.1.285):** `validate --strict` endet an der Vorlage mit Exit 0 und mit
  einem Manifestpfad außerhalb des Plugins mit Exit 1. **Ein Skill mit kaputtem YAML-Frontmatter
  besteht `--strict` mit Exit 0.** Die Frontmatter prüft deshalb eine eigene Probe: mit PyYAML
  parsen, Name gleich Ordner, Beschreibung in Anführungszeichen und höchstens 700 Zeichen, höchstens
  500 Zeilen.
- Ob Plugin-Skills in `skills:` mit Namensraum (`<plugin>:<skill>`) geschrieben werden müssen, ist
  **offen** — Probe beim Aufsetzen. Die Grader nehmen beide Schreibweisen an
  (`(?:[\w-]+:)?<skill>`).

## Evals

**Frage:** Löst ein Skill oder eine Rolle aus, wenn sie soll, und bleibt sie still, wenn nicht —
obwohl das Auslösen streut?

| Regel | Wert |
| --- | --- |
| Fälle | Je Objekt einer „löst aus", einer „bleibt still" |
| Läufe je Fall | **5** |
| Schwelle | **0,8** (4 von 5). Bei 3 Läufen verlangte 0,8 jeden Treffer; 5 Läufe lassen einen Ausreißer zu |
| Reihenfolge | **Baseline zuerst** mit `--threshold 0`, die nur misst. Danach setzt der Mensch den Kostendeckel (`--max-cost-usd`) |
| Ort | **Nie in der CI.** Nur auf Zuruf des Menschen |
| Kosten | Auf das Kontingent des Menschen. Die Bau-Session startet sie nicht selbst |
| Unter der Schwelle | Die Beschreibung schärfen, nicht die Schwelle senken |

**Werkzeug** `claude plugin eval`: Fälle unter `evals/`, Grader `tool_used` mit `tool: Skill` und
`input_match` auf den Namen; Stillbleiben mit `min: 0` und `max: 0`. **`--ablation none` ist
Pflicht:** Im Standard-Zwei-Arm-Lauf zählen Skill-Grader nicht zum Score, der Fall wäre grün,
ohne etwas zu messen. Nur freie Grader (`tool_used`, `regex`); ein `llm`-Grader kostet zusätzlich.

**Vorgeladene Skills** (Gate, Test-Autor) rufen das Skill-Werkzeug nicht auf; dort wird die Rolle
geprüft. `/simplify` und `/security-review` bekommen keinen Eval — ihre Reihenfolge prüft der Hook
kostenlos und deterministisch.

**Die sieben Skill-Fälle** liegen als Vorlage unter `templates/skills/eval-faelle/` (Ziel
`.claude/skills/<plugin>/evals/`): je Fall `prompt.md` mit `runs: 5`, `max_turns: 10`,
`allowed_tools: [Read, Glob, Grep, Skill]` und ein Grader `tool_used`; „bleibt still“ mit `min: 0`,
`max: 0`, `arm: both`. `belastbar-messen` löst aus und bleibt still, `code-gutachten` bleibt still
(sein Auslösen prüfen die Probe-PRs des Gates), `test-qualitaet` und `sicherheits-katalog` je beide.
**Lücke, benannt:** Die Fälle haben noch keine Fixture (ein Mini-Repo je Fall); zwei Prompts nennen
einen Test bzw. Endpunkt, den ein leerer Lauf nicht hat. Die Fixture entsteht mit der Baseline beim
Aufsetzen und wird Teil der geprüften Vorlage.

**Rollen über den Eigenbau:** Laut Doku (Abschnitt „How runs are isolated“, Probe beim Aufsetzen)
lädt ein Lauf von `claude plugin eval` keine Projekt-Konfiguration und kein `.claude/`, sieht also
keinen Projekt-Agent. Die Rollen-Fälle laufen deshalb als `claude -p "<prompt>" --output-format
json` in einem Klon von `origin/main`, mit Auswertung des Transkripts auf den Agent-Aufruf der
Rolle.
Ob unter `-p` Frontmatter- und Projekt-Hooks laufen, ist widersprüchlich belegt
([leitplanken.md](leitplanken.md), Offen 5); für die Auslöse-Frage spielt das keine Rolle. Evals
laufen in einem Klon von `origin/main`.

**Feuert-Nachweis des Harness** (Wegwerf-Kopie außerhalb des Repos):

1. Positivkontrolle: unveränderter Satz besteht.
2. Verdorbener Skill: Beschreibung durch etwas Fremdes ersetzt → „löst aus" fällt unter die
   Schwelle. Bleibt er darüber, ist der Eval blind.
3. Zu breiter Skill: „Verwende diesen Skill immer" → „bleibt still" fällt.
4. Grader-Falle: derselbe verdorbene Skill im Standard-Zwei-Arm-Lauf bleibt grün — Beleg, dass
   `--ablation none` nötig ist.
5. Kostendeckel: winziger Wert bei `--max-cost-usd` → Exit 2.

**Anlässe:** geänderte Beschreibung, `when_to_use`, `model` oder `effort` eines Objekts (nur dessen
Fälle); Wechsel von Modell oder Claude-Code-Version (alle Fälle); die Rückschau meldet eine
Divergenz.
