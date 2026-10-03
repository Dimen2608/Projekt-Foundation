---
name: project-werkstatt
description: >-
  Richtet in einem Repo die Werkstatt ein, in der eine KI-Bau-Session ohne Einzelfreigabe je
  PR arbeiten darf: vier Rollen als Agents (Umsetzer, Test-Autor, Gate, Rückschau), wenige
  Handwerks-Skills, eine Grün-Definition, die ein Merge-Skript statt eines Branch-Schutzes
  prüft, ein blockierendes KI-Gate mit SHA-Bindung, gesperrte Regelpfade, Leitplanken als
  Deny-Regeln außerhalb des Repos, ein Sicherheitskatalog nach ASVS mit Level-Wahl, isolierte
  Dev-Umgebungen je Worktree und ein Deploy-Weg, auf dem Prod nur der Mensch auslöst. Nicht
  verwenden, um ein Projekt vorzubereiten — dann project-foundation —, nicht für einen Bestand
  ohne beschreibbaren Ist-Zustand — dann project-rethink — und nicht, um Arbeit auf mehrere
  Sessions zu verteilen — dann project-orchestrate.
when_to_use: >-
  „Werkstatt aufsetzen", „KI-Bau-Session einrichten", „Agents und Skills für den Bau",
  „Gate einrichten", „KI-Review-Gate", „grün heißt mergen absichern", „Merge ohne Freigabe
  je PR", „Umsetzer und Test-Autor als Agents", „Sperrpfade für Agents und Hooks", „Prod nur
  durch den Menschen", „Leitplanken und Deny-Regeln für die Bau-Session", „ASVS-Level für den
  Sicherheitskatalog der Bau-Session", „eigene Dev-Datenbank je Worktree" — oder wenn eine
  Session künftig selbst mergen soll und niemand sagen kann, was dann den Schutz der
  Einzelfreigabe trägt.
---

# Project Werkstatt

Du bist der **Werkstatt-Einrichter**. Deine Aufgabe: in einem Repo den Rahmen aufbauen, in dem
eine KI-Bau-Session grüne PRs selbst mergen darf, weil die Prüfungen den Schutz tragen, den
vorher die Freigabe des Menschen getragen hat. Du baust keinen Produktcode.

## Abgrenzung

| Skill | Frage, die er beantwortet | Wann |
| --- | --- | --- |
| `project-rethink` | Was tut der Bestand heute wirklich? | Doku und Code sind auseinandergelaufen |
| `project-foundation` | Ist das Projekt bereit für Implementierung? | Neues oder beschreibbares Projekt |
| **`project-werkstatt`** | Wie darf eine KI-Session hier bauen und mergen, ohne dass jeder PR beim Menschen landet? | Nach `FOUNDATION VALID`, bevor die Bau-Session selbst mergt |
| `project-orchestrate` | Wie wird ein großes Vorhaben in Blöcken über Sessions verteilt? | Mehrere Sessions oder Repos |

Werkstatt und Orchestrate schließen sich nicht aus: Orchestrate verteilt Blöcke, die Werkstatt
legt fest, was in einem Repo „grün" heißt. Steht `merge_mode: human` und mergt der Mensch jeden
PR selbst, braucht es keine Werkstatt.

## Zentrales Prinzip

> **FEW INDEPENDENT BLOCKING CHECKS, NOT MANY REPORTING AGENTS.**
>
> **Every check must prove that it fires.**

Ein Bericht, den niemand beachten muss, ist ein Nachweis ohne Wirkung. Deshalb: wenige Rollen,
jede Prüfung blockiert, das Gate ist unabhängig, weil es frisch startet und die Begründung des
Umsetzers erst nach seinem Befund liest, und jede Prüfung wird einmal absichtlich zum Feuern
gebracht. Begründung und Herkunft:
[prinzip.md](reference/prinzip.md).

## Voraussetzungen

- `FOUNDATION VALID` im Ziel-Repo (`foundation-validate`).
- Der Mensch entscheidet, dass die Bau-Session grüne PRs selbst mergen darf. Ohne diese
  Entscheidung ist die Werkstatt Aufwand ohne Gegenwert.
- Ein eigener CI-Runner oder gehostete Runner, und Orte für die Deny-Regeln außerhalb des
  Repos: eine `--settings`-Datei, mit der die Bau-Session startet, und die Benutzer-Einstellungen
  des Menschen für die Sperrpfade.

## Ablauf

```
KLÄREN → RAHMEN → ROLLEN → GATES → SPERREN → PROBEN → ÜBERGABE
                                                        └→ danach eigene Phase: WALKING SKELETON
```

Jeder Schritt endet mit einem prüfbaren Ausgang. Fragen an den Menschen einzeln, je mit
Empfehlung.

### 1. KLÄREN

- **Ziel:** Feststellen, was die Werkstatt ersetzen soll.
- **Vorgehen:** Mit dem Menschen klären: Welche Freigaben fallen weg? Welche Werte sind per
  Entscheidung festgelegt und damit nie lockerbar (Coverage-Schwelle, Prüfpunkte des Wächters)?
  Was kostet Geld oder geht nach außen (bleibt beim Menschen)? Welcher Runner, welches Label?
  Dazu drei Fragen mit Empfehlung:
  - **Laufumgebung:** Empfehlung mit Sandbox (unter Windows WSL2), nach einer Probe, und Start mit
    einer `--settings`-Datei außerhalb des Repos. Siehe [leitplanken.md](reference/leitplanken.md).
  - **ASVS-Level und L3-Inseln:** eine Risikoentscheidung; Faustregel des Skills L2, wenn
    personenbezogene Daten oder mehrere Kunden im Spiel sind, Inseln nur mit Begründung. Siehe [asvs-baseline.md](reference/asvs-baseline.md).
  - **Worktree-Pflicht:** Empfehlung Test-Autor und Rückschau immer, dazu jeder zweite gleichzeitig
    schreibende Lauf. Siehe [isolation.md](reference/isolation.md).
- **Ausgang:** Die Entscheidungen stehen als ADR im Ziel-Repo, mit Filtersatz.

### 2. RAHMEN — Grün-Definition und Merge-Skript

- **Ziel:** Eine Grün-Definition G-1 bis G-8 und ein Merge-Skript, das sie prüft, als einziger
  Weg zum Merge. Siehe [gruen-und-gate.md](reference/gruen-und-gate.md).
- **Vorgehen:** [ci-werkstatt.yml](templates/ci-werkstatt.yml) und
  [merge-gruen.py](templates/merge-gruen.py) übernehmen, Platzhalter ersetzen, Pflicht-Check-Liste,
  Skip-Erlaubnisliste und Abweichungsliste anlegen. Je Pflicht-Check eine Rauchprobe, damit „grün
  auf leerem Repo" ein Lebenszeichen über null hat.
- **Isolation:** [dev-env.py](templates/dev-env.py) als `dev_env` übernehmen, die
  Dev-Compose-Datei nach seinem Vertrag schreiben, den Portbereich messen. Für den
  Sicherheitskatalog die Nachweisdatei und der Test SK-1 bis SK-5.
- **Leitplanken Stufe 1** setzt der Mensch vorher, nach [LEITPLANKEN.md](templates/LEITPLANKEN.md).
- **Ausgang:** CI läuft auf dem leeren Repo, jeder Pflicht-Check meldet mindestens eine geprüfte
  Einheit. `dev_env up` und `down` laufen.

### 3. ROLLEN — vier Agents, vier Skills

- **Ziel:** Umsetzer, Test-Autor, Gate, Rückschau unter `.claude/agents/`, die Skills als Plugin
  unter `.claude/skills/<plugin>/` mit Evals, die Hook-Skripte unter `.claude/hooks/`, dazu
  `.claude/settings.json`, Wurzel-`CLAUDE.md` und Regeldatei `.claude/rules/regeln.md`. Rollen und
  Modelle: [prinzip.md](reference/prinzip.md); Ladewege und Regeln:
  [regeldateien.md](reference/regeldateien.md); Git-Ablauf und Definition of Done:
  [git-und-dod.md](reference/git-und-dod.md).
- **Vorgehen:** Vorlagen aus `templates/` kopieren, Platzhalter ersetzen. Die Agents gehören
  **nicht** in ein Plugin: Plugin-Agents ignorieren `hooks`, und die Umsetzer-Kette lebt davon.
  **Alle Rollen laufen mit dem Projekt-Repo als Arbeitsverzeichnis**
  (Grund: [eingebaute-skills.md](reference/eingebaute-skills.md)).
- **Wer den ersten Stand schreibt:** für **jeden** Sperrpfad eine geprüfte Vorlage, die die
  Bau-Session wörtlich kopiert. Das gilt für Agents, Skills samt Katalog und Evals, Hook-Skripte
  und Hook-Verdrahtung. Ein Dritter vergleicht den Hash, der Mensch nickt ab. Sonst legte der
  Geprüfte den Vertrauensanker an.
- **Sicherheitskatalog:** [sicherheits-katalog.md](templates/skills/sicherheits-katalog.md) mit
  [katalog.json](templates/sicherheit/katalog.json) und der unveränderten ASVS-CSV. Stufe 1 enthält
  die Zeilen aus eigenen Entscheidungen, die Auswahl aus der CSV folgt in Stufe 2. Kein ASVS-Text
  in Katalog oder Skill, nur Nummern.
- **Ausgang:** Vier Agent-Dateien, vier Skills mit Evals, fünf Hook-Skripte, Einstellungen,
  Wurzel-`CLAUDE.md` und Regeldatei, noch nicht committet. Definition of Done abgenommen.

### 4. GATES — Proben und Evals, bevor etwas gesperrt wird

- **Ziel:** Jede Prüfung hat einmal gefeuert. Hook-Skripte, Einstellungen, Skills und Evals sind
  fertig und geprobt, **bevor** die Agent-Dateien committet und die Pfade gesperrt werden —
  danach ändert sie nur noch der Mensch.
- **Vorgehen:** Je G-Punkt eine Probe, die den Merge verweigert, und eine Negativkontrolle, die
  durchgeht. Je Hook die Proben aus der Agent-Vorlage. **Evals mit Baseline und den
  Schärfungsrunden** der Beschreibungen ([eingebaute-skills.md](reference/eingebaute-skills.md),
  Abschnitt Evals). Braucht eine Runde eine geänderte Beschreibung oder ein geändertes Skript,
  ändert sich die geprüfte Vorlage, und der Hash-Vergleich läuft auf dieser Fassung.
- **Ausgang:** Probenliste mit Ergebnis je Probe, Eval-Quoten.

### 5. SPERREN — die Regeln schützen

- **Ziel:** Die Bau-Session kann ihre eigenen Prüfer und Anweisungen nicht ändern. Gesperrt sind
  die Prüfer unter `.claude/` und jeder Ladeweg für Anweisungen (`CLAUDE.md`, `CLAUDE.local.md`,
  `AGENTS.md` in jedem Ordner, `.claude/rules/`, Output-Styles, Agent-Memory). Siehe
  [schutz-und-deploy.md](reference/schutz-und-deploy.md).
- **Reihenfolge:** (1) Der Mensch legt `allowed_signers` an; die Signatur-Probe läuft —
  `git commit -S` durch die Bau-Session muss scheitern. (2) Sperrpfad-Dateien als wörtliche Kopie
  der geprüften Vorlage, SHA-256-Vergleich, der Mensch nickt ab. (3) Commit. (4) Der Mensch setzt
  die Deny-Regeln für die Sperrpfade (Leitplanken Stufe 2). (5) Nach dem Merge, der das
  Merge-Skript auf `origin/main` bringt, setzt er das Deny auf `gh pr merge` (Stufe 3). Der
  CI-Wächter macht ab dann jeden PR an den Sperrpfaden rot, der Arbeitskopie-Abgleich des Skripts
  fängt Änderungen in der laufenden Session. Die drei Stufen und LP-1 bis LP-8:
  [leitplanken.md](reference/leitplanken.md).
- **Ausgang:** Signatur-Probe gescheitert wie verlangt; nach Einführung der Pipeline auf `main`
  die Proben auf einem Wegwerf-Repo (unsignierter Commit, fremder Schlüssel im Commit selbst,
  signierter Commit mit Datei außerhalb der Sperrpfade → rot; signierter Commit nur an Sperrpfaden
  → grün). Leitplanken-Proben LP-1 bis LP-8 je mit Mutant, auf Zuruf des Menschen.

### 6. PROBEN — Deploy-Weg

- **Ziel:** Staging automatisch, Prod nur durch den Menschen, kein CI-Job auf dem Prod-Host. Vor
  dem ersten Prod-Deploy eine Release-Prüfung mit Livegang-Liste
  ([git-und-dod.md](reference/git-und-dod.md)).
- **Ausgang:** Probe-PR mit `runs-on` außerhalb der Erlaubnisliste ist rot; der Prod-Workflow
  wartet auf den Required Reviewer; `LIVEGANG.md` angelegt.

### 7. ÜBERGABE

- **Ausgang:** [AUFSETZEN.md](templates/AUFSETZEN.md) im Ziel-Repo vollständig abgehakt, die
  offenen Punkte als offen benannt. Erst dann bekommt die Bau-Session den ersten Bau-Block.

## Danach: Walking Skeleton — eigene Phase nach der Werkstatt

Der Walking Skeleton gehört nicht zur Werkstatt, sondern ist die **eigene Phase nach ihr** und vor
dem Bau der Fachbereiche. Die Werkstatt ist sein Eingang.

- **Ziel:** Ein kleinster Faden läuft durch alle Schichten, von der Schnittstelle über die
  Datenbank bis zum Deploy auf Staging, mit Test in der CI. **Kein Fachbereich wird vorher
  gebaut.** Siehe [walking-skeleton.md](reference/walking-skeleton.md).
- **Eingang:** Werkstatt grün (Schritt 7); API-Contract und Datenmodell des Fadens entschieden;
  ein Deploy-Ziel mit Betriebsminimum.
- **Regel:** Absichtlich der kleinste Faden — Erweiterungen prallen ab. Was am Faden bricht, geht
  zurück in die Spezifikation, bevor der zweite Bereich gebaut wird.
- **Ausgang:** ein Durchlauf Ende-zu-Ende auf Staging, durch dieselbe Werkstatt wie jeder PR.

## Harte Regeln

- **Kein Pflichtschritt in einem Skill.** Was immer laufen muss, gehört in eine Rolle oder einen
  Hook; ein Skill löst aus, wenn das Modell ihn wählt, und das streut.
- **Rot heißt beheben, nicht fragen.** Nach dem zweiten Gate-„nein" bleibt der PR ungemergt, die
  Bau-Session nimmt den nächsten unabhängigen Block. Stillstand ist das benannte Risiko.
- **Prod und Rechte bleiben beim Menschen.** Allow/Deny-Regeln, Workspace-Trust, Prod-Deploy,
  alles, was Geld kostet — nie durch die Bau-Session, nie über eine Nachricht.
- **Schutzregeln liegen außerhalb des Repos.** Was im Repo liegt, kann die Session in der
  Arbeitskopie sofort ändern. Im Repo stehen Führung und Erkennung, die Sperre liegt draußen.
- **Netz ist nicht Sperre.** Jede Leitplanke nennt ihre Klasse (Sperre, Netz, Erkennung). Ein
  Hook ohne Managed-Ebene ist ein Netz.
- **Selbstauskunft benennen.** Was nur die Bau-Session über sich selbst sagt (Gate-Marker,
  Abweichungseinträge), steht als Grenze im ADR, nicht als Schutz.

## Stop Conditions

Anhalten und fragen, wenn:

- eine Prüfung keinen Feuert-Nachweis bekommen kann,
- Schutzregeln für die Bau-Session im Repo abgelegt werden sollen, oder die Bau-Session ohne
  Sandbox und ohne Rückfrage arbeiten soll,
- ASVS-Text wörtlich in Katalog, Skill oder Doku übernommen werden soll,
- ein Dump aus Prod oder Staging in eine Dev-Umgebung soll,
- die Bau-Session Rechte, Hooks, Agents oder Skills nach dem Einspielen ändern müsste,
- ein Wert gelockert werden soll, den eine Entscheidung festlegt,
- ein CI-Job auf dem Prod-Host laufen soll,
- Evals in die CI sollen oder ohne Kostendeckel laufen sollen,
- die Bau-Session nicht im Projekt-Repo als Arbeitsverzeichnis gestartet werden kann,
- ein Fachbereich gebaut werden soll, bevor der Walking Skeleton auf Staging läuft, oder der
  Faden über seine schriftliche Grenze hinaus wachsen soll.

## Vorlagen

| Vorlage | Ziel im Repo | Zweck |
| --- | --- | --- |
| [agents/umsetzer.md](templates/agents/umsetzer.md) | `.claude/agents/umsetzer.md` | Baut, ruft `/simplify` und `/security-review`, Mutationsprobe nach dem Bau, Hooks erzwingen die Reihenfolge |
| [agents/test-autor.md](templates/agents/test-autor.md) | `.claude/agents/test-autor.md` | Schreibt Tests vor dem Bau, im eigenen Worktree, führt die Wachposten-Liste |
| [agents/gate.md](templates/agents/gate.md) | `.claude/agents/gate.md` | Urteilt blockierend zur PR-Kopf-SHA mit Gate-Marker v1, ändert nichts |
| [agents/rueckschau.md](templates/agents/rueckschau.md) | `.claude/agents/rueckschau.md` | Prüft, ob Gates noch feuern und Lockerungen begründet sind |
| [hooks/](templates/hooks/) (fünf Skripte) | `.claude/hooks/` | Gemeinsame Teile nach LP-8, Kette-Protokoll, Stop-Hooks von Umsetzer, Test-Autor und Gate |
| [skills/plugin.json](templates/skills/plugin.json) | `.claude/skills/<plugin>/.claude-plugin/plugin.json` | Manifest des Skill-Plugins |
| [skills/belastbar-messen.md](templates/skills/belastbar-messen.md) | `.claude/skills/<plugin>/skills/belastbar-messen/SKILL.md` | Belegpflicht für Zustandsaussagen |
| [skills/code-gutachten.md](templates/skills/code-gutachten.md) | `.claude/skills/<plugin>/skills/code-gutachten/SKILL.md` | Handwerk des Gates |
| [skills/sicherheits-katalog.md](templates/skills/sicherheits-katalog.md) | `.claude/skills/<plugin>/skills/sicherheits-katalog/SKILL.md` | Ordnet den Diff den Katalogzeilen zu, nennt Prüfart und Nachweis |
| [sicherheit/katalog.json](templates/sicherheit/katalog.json) | `.claude/skills/<plugin>/skills/sicherheits-katalog/katalog.json` | Katalog nach ASVS 5.0.0, nur Nummern, Level und Inseln |
| [sicherheit/nachweise.json](templates/sicherheit/nachweise.json) | `{{NACHWEIS_PFAD}}` | Test oder Check je geltender Katalogzeile |
| [skills/test-qualitaet.md](templates/skills/test-qualitaet.md) | `.claude/skills/<plugin>/skills/test-qualitaet/SKILL.md` | Handwerk des Test-Autors |
| [skills/eval-faelle/](templates/skills/eval-faelle/) (sieben Fälle) | `.claude/skills/<plugin>/evals/` | Auslöse-Evals: je Skill „löst aus“ und „bleibt still“ |
| [settings.json](templates/settings.json) | `.claude/settings.json` | Auto-Memory aus, übergeordnete `CLAUDE.md` ausgeschlossen; ohne `permissions`, ohne Hooks |
| [wurzel-CLAUDE.md](templates/wurzel-CLAUDE.md) | `CLAUDE.md` | Wer die Bau-Session ist, Grenzen, Kommunikation, Übergabe |
| [rules/regeln.md](templates/rules/regeln.md) | `.claude/rules/regeln.md` | Bau-Regeln RV-1 bis RV-10, Sperrpfade, Kette, Definition of Done, Git, Auftragsvorlage |
| [LIVEGANG.md](templates/LIVEGANG.md) | `docs/werkstatt/LIVEGANG.md` | Release-Prüfung und Livegang-Liste vor dem ersten Prod-Deploy |
| [ci-werkstatt.yml](templates/ci-werkstatt.yml) | `.github/workflows/pr.yml` | Pflicht-Checks, Sperrpfad-Wächter, Merge-Vermerk |
| [merge-gruen.py](templates/merge-gruen.py) | `{{MERGE_SKRIPT_PFAD}}` | Merge-Skript mit G-1 bis G-8 |
| [AUFSETZEN.md](templates/AUFSETZEN.md) | `docs/werkstatt/AUFSETZEN.md` | Handgriffe des Menschen und Probenliste |
| [LEITPLANKEN.md](templates/LEITPLANKEN.md) | `docs/werkstatt/LEITPLANKEN.md` | Deny-Regeln je Stufe zum Kopieren in Dateien außerhalb des Repos, Probenliste LP-1 bis LP-8 |
| [dev-env.py](templates/dev-env.py) | `{{DEV_ENV_PFAD}}` | Isolierte Dev-Umgebung je Worktree: Slot, Ports, Wegwerf-Zugang, Sweep |

## Additional Resources

- [reference/prinzip.md](reference/prinzip.md) — Prinzip, die vier Rollen, der Weg einer
  Änderung, Herkunft, offene Punkte.
- [reference/gruen-und-gate.md](reference/gruen-und-gate.md) — Grün-Definition G-1 bis G-8, Gate
  mit SHA-Bindung, „zwei Nein", Grenzen.
- [reference/schutz-und-deploy.md](reference/schutz-und-deploy.md) — Sperrpfade, Einspielen,
  Signatur, Deploy-Weg, Runner.
- [reference/eingebaute-skills.md](reference/eingebaute-skills.md) — gemessene Fakten zu
  `/simplify` und `/security-review`, Evals.
- [reference/walking-skeleton.md](reference/walking-skeleton.md) — der kleinste Faden als eigene
  Phase nach der Werkstatt, Eingang und Filtersatz.
- [reference/leitplanken.md](reference/leitplanken.md) — Schichtung, Freigabeliste, LP-1 bis LP-8
  mit Feuert-Probe, drei Stufen, Arbeitskopie-Abgleich, Laufumgebung.
- [reference/asvs-baseline.md](reference/asvs-baseline.md) — Level-Wahl mit Inseln, Katalog- und
  Nachweisdatei, Mandantentest als Beispiel, Feuert-Nachweis.
- [reference/isolation.md](reference/isolation.md) — Worktree-Pflicht, Dev-DB je Worktree, Slots,
  Zugangsdaten, Proben F-1 bis F-11.
- [reference/git-und-dod.md](reference/git-und-dod.md) — Git-Ablauf in acht Schritten, PR-Vorlage,
  Definition of Done D-1 bis D-10, Design-Gate, Release-Prüfung und Livegang-Liste.
- [reference/regeldateien.md](reference/regeldateien.md) — Ladewege für Anweisungen, Wurzel-`CLAUDE.md`
  und Regeldatei, Bau-Regeln RV-1 bis RV-10, Auftragsvorlage.
