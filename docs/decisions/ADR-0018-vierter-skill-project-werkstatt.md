# ADR-0018: Ein vierter Skill `project-werkstatt` — die Werkstatt, in der eine KI-Session selbst mergt

## Status

Accepted — 2026-10-01

## Context

`project-foundation` macht ein Projekt baubar, `project-orchestrate` verteilt den Bau auf
Sessions. Offen bleibt die Frage dazwischen: **Was trägt den Schutz, wenn eine KI-Bau-Session
grüne PRs ohne Einzelfreigabe selbst mergt?** `merge_mode: orchestrator` (ADR-0014) setzt „Tor-Ja
und grüne CI" voraus, sagt aber nicht, was „grün" umfassen muss.

In einem Neubau (Atemluft V2) ist dafür ein Werkstatt-Plan entstanden und am 01.10.2026 in den
wesentlichen Teilen entschieden: vier Rollen statt 25, vier Skills statt 15, eine Grün-Definition
G-1 bis G-8, die ein Merge-Skript aus `origin/main` prüft, weil der Git-Host keinen Branch-Schutz
erzwingt; ein blockierendes KI-Gate mit SHA-Bindung und der Regel „zwei Nein"; gesperrte Regelpfade
mit signierten Commits des Menschen; Staging automatisch, Prod nur durch den Menschen; Evals mit
Quote, nie in der CI; danach ein Walking Skeleton als eigene Phase. Dazu gemessene Fakten zu `/simplify` und
`/security-review`. Noch offen sind Leitplanken mit ASVS-Level, Definition of Done und die
ausformulierten Agent-Texte.

Der Auftraggeber hat am 01.10.2026 entschieden, das Muster als eigenen, wiederverwendbaren Skill
mit Erklärung aufzunehmen — **jetzt mit dem entschiedenen Stand**, Offenes sichtbar markiert.

## Decision

1. **Vierter Skill im selben Plugin** unter `plugins/project-foundation/skills/project-werkstatt/`.
   ADR-0002 gilt: genau eine Kopie. Ablauf `KLÄREN → RAHMEN → ROLLEN → GATES → SPERREN → PROBEN →
   ÜBERGABE`; danach als eigene Phase der Walking Skeleton, dessen Eingang die grüne Werkstatt
   ist.
2. **Abgrenzung in der `description`**, wie bei Orchestrate (ADR-0014): Werkstatt zieht bei „Gate
   einrichten", „grün heißt mergen absichern", „KI-Bau-Session einrichten" und verweist für
   Vorbereitung auf Foundation, für Bestandsvermessung auf Rethink, für Verteilung auf Orchestrate.
   Die drei anderen Beschreibungen bleiben unverändert: Ihre Trigger überschneiden sich nicht.
3. **Prinzip:** wenige, unabhängige, blockierende Prüfungen statt vieler Berichts-Agents;
   Unabhängigkeit vor Masse (frischer Kontext, Begründung erst nach dem Befund), jede Prüfung mit
   Feuert-Nachweis. Dass das Gate in der Quelle Opus nutzt, ist dort über die Effort-Regel
   „Prüfen eine Stufe höher" begründet, nicht als Unabhängigkeit durch ein anderes Modell.
4. **Die vier Rollen sind Vorlagen, keine Plugin-Agents.** Sie werden ins Zielprojekt nach
   `.claude/agents/` kopiert, weil die Umsetzer-Kette von Frontmatter-Hooks lebt und
   Plugin-Agents `hooks` ignorieren. Das Plugin bekommt damit **keinen** neuen Agent. Dass die
   Vorlagen `skills:` und `hooks` tragen, regelt ADR-0019.
5. **Umfang nach ADR-0011**, je Vorlage die Frage:

   | Frage | Vorlage |
   | --- | --- |
   | Wer baut, wer prüft, mit welchem Modell und welchen Rechten? | `agents/umsetzer.md`, `test-autor.md`, `gate.md`, `rueckschau.md` |
   | Welches Handwerk laden die Rollen, welches löst aus? | `skills/belastbar-messen.md`, `code-gutachten.md`, `sicherheits-katalog.md`, `test-qualitaet.md` |
   | Was läuft in der CI, und wie wird ein Sperrpfad erkannt? | `ci-werkstatt.yml` |
   | Was heißt grün, und wer mergt? | `merge-gruen.py` |
   | Was muss der Mensch selbst tun, welche Probe beweist was? | `AUFSETZEN.md` |

   Dazu fünf Dateien unter `reference/`: Prinzip und Rollen, Grün-Definition und Gate, Schutz und
   Deploy, eingebaute Skills und Evals, Walking Skeleton.
6. **Kein Fachinhalt des Ursprungsprojekts.** Die Vorlagen sind entprojektiert, mit Platzhaltern
   (`{{PROJEKT}}`, `{{REPO_SLUG}}`, `{{REPO_PFAD}}`, `{{RUNNER_LABEL}}`). `reference/prinzip.md` nennt die Herkunft einmal;
   `reference/walking-skeleton.md` nennt den Faden des Ursprungsprojekts einmal als Beispiel.
7. **Offenes bleibt sichtbar offen.** Leitplanken und ASVS-Level, Definition of Done, ausformulierte
   Agent-Texte, Hook-Skripte, Gate-Marker-Format: als „offen" mit Herkunft markiert und
   nachzuziehen, wenn die Quelle sie entscheidet. Der Skill `sicherheits-katalog` ist bis dahin ein
   Gerüst.
8. **Keine Validator-Änderung.** Keine neue Pflichtstelle, keine Finding-ID, `schema_version`
   bleibt `1`. Die Fragen, die die Vorlagen beantworten, stellt nur ein Projekt, in dem eine
   KI-Session selbst mergt. Kein Test nach ADR-0009: Prompt-Material. `merge-gruen.py` ist eine
   Skizze im Vorlagenordner, kein Code des Validators; sie läuft durch `ruff`, nicht durch `mypy`
   und `pytest`.
9. **Version 0.8.0.**

Verworfene Alternativen:

- **Teil von `project-orchestrate`.** Orchestrate verteilt Blöcke über Sessions; die Werkstatt gilt
  auch für eine einzige Bau-Session. Vermischt ergäbe das einen Skill mit zwei Eingängen.
- **Teil von `project-foundation`** (etwa als Quality Gate). Foundation fragt „ist das Projekt
  baubar?"; die Werkstatt setzt die Entscheidung voraus, dass eine KI selbst mergt — eine Frage,
  die die meisten Projekte nie stellen.
- **Die vier Rollen als Plugin-Agents.** Plugin-Agents ignorieren `hooks`; die Reihenfolge der
  Umsetzer-Kette wäre wieder nur ein Satz im Prompt.
- **Warten, bis die Quelle vollständig entschieden ist.** Entscheidung des Auftraggebers: jetzt
  bauen, Offenes markieren.

## Consequences

**Positiv**

- Ein Projekt, in dem eine KI-Session selbst mergen soll, bekommt eine geprüfte Antwort auf „was
  heißt grün?" samt Vorlagen und Probenliste.
- Validator, Finding-IDs und Manifest-Schema bleiben unberührt.

**Negativ**

- Der Skill trägt offene Stellen. Bis sie nachgezogen sind, ist die Werkstatt ein Rahmen, kein
  fertiges Paket — der Sicherheitskatalog vor allem.
- Die gemessenen Fakten zu `/simplify` und `/security-review` veralten mit jeder neuen Fassung;
  `reference/eingebaute-skills.md` trägt deshalb Datum und Version.
- Das Plugin trägt Prompt-Material für vier Prozesse. Die Werkstatt lohnt sich nur, wo eine KI
  selbst mergt; wer jeden PR selbst freigibt, braucht sie nicht.

**Grenze**

Neu zu bewerten, wenn die Quelle die offenen Teile entscheidet (nachziehen, nicht neu schneiden),
oder wenn die Werkstatt in einem zweiten Projekt angewandt wird und sich Teile als
projektspezifisch zeigen — dann gehören sie aus dem Skill heraus.
