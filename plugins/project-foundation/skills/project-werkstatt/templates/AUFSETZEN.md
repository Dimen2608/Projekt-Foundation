# Werkstatt aufsetzen — {{PROJEKT}}

> Checkliste aus project-werkstatt. Kopieren nach `docs/werkstatt/AUFSETZEN.md`, abhaken, offene
> Punkte als offen stehen lassen. **[M]** = nur der Mensch. **[B]** = Bau-Session.
> Repo: `{{REPO_SLUG}}` · lokal: `{{REPO_PFAD}}` · Runner-Label: `{{RUNNER_LABEL}}` ·
> Stand: {{DATUM}}

## 1. Entscheidungen vorher

- [ ] [M] Die Bau-Session darf grüne PRs ohne Einzelfreigabe mergen — als ADR mit Filtersatz.
- [ ] [M] Werte, die nie lockerbar sind (z. B. Diff-Coverage-Schwelle, Prüfpunkte des Wächters),
      stehen in einer Entscheidung.
- [ ] [M] Was Geld kostet oder nach außen geht, bleibt beim Menschen — benannt.
- [ ] [M] Den ersten Stand **aller** Sperrpfade (Agents, Skills samt Manifest, Katalog und Evals,
      Hook-Skripte, `.claude/settings.json` ohne `permissions`, Wurzel-`CLAUDE.md`, Regeldatei)
      schreibt eine geprüfte Vorlage; die Bau-Session kopiert wörtlich, ein Dritter vergleicht den
      Hash.
- [ ] [M] Definition of Done D-1 bis D-10 abgenommen; D-7 (Nutzerdoku) und D-8 (Design-Gate)
      gelten oder „entfällt, weil …“ (`reference/git-und-dod.md`).
- [ ] [M] Ladewege gesperrt, Auto-Memory aus, übergeordnete `CLAUDE.md` ausgeschlossen
      (`reference/regeldateien.md`).
- [ ] [M] ASVS-Level der Anwendung und L3-Inseln, mit Begründung, als ADR mit Filtersatz
      (`reference/asvs-baseline.md`).
- [ ] [M] Laufumgebung der Bau-Session: mit Sandbox (unter Windows WSL2). Probe: Docker im
      Sandbox-Lauf, Ladeweg einer übergeordneten `CLAUDE.md`, `gh`-Login, Startweg. Scheitert sie:
      neu entscheiden.
- [ ] [M] Startweg mit `--settings {{SCHUTZ_DATEI}}` geklärt. Geht er nicht (etwa Desktop-Sitzung):
      Ersatz nach `reference/leitplanken.md`.
- [ ] [M] Worktree-Pflicht: Test-Autor und Rückschau immer; jeder zweite gleichzeitig schreibende
      Lauf; Umsetzer im Haupt-Checkout bis Probe F-8 (`reference/isolation.md`).
- [ ] [M] Nachbar-Repos, die die Bau-Session nur lesen darf (LP-4), benannt — oder keine.

## 2. Runner und Repo-Einstellungen

- [ ] [M] Eigener Runner-Benutzer, getrennt von anderen Runnern auf der Maschine.
- [ ] [M] workFolder unter `$HOME` des Runner-Benutzers.
- [ ] [M] Label `{{RUNNER_LABEL}}`; Grenzen (`MemoryMax`, `CPUQuota`, `NoNewPrivileges`,
      `PrivateTmp`) gesetzt.
- [ ] [M] Kein Runner dieses Repos auf dem Prod-Host.
- [ ] [M] Dependabot alerts und security updates eingeschaltet.
- [ ] [M] Environment `prod` mit dem Menschen als Required Reviewer.
- [ ] [M] Repo-Einstellungen: automatisch löschen gemergter Branches an, Squash- und Rebase-Merge
      aus (GA-3). Gemessen mit `gh api repos/{{REPO_SLUG}}` (GET).

## 2a. Leitplanken Stufe 1 — vor dem Aufsetz-Block

- [ ] [M] `{{SCHUTZ_DATEI}}` außerhalb des Repos nach `LEITPLANKEN.md`, Stufe 1: Push-Teil von
      LP-1, LP-4 bis LP-7, `"disableAllHooks": false`, Env-Scrub. Die Bau-Session startet damit.
- [ ] [M] Transkript-Frist bleibt beim Standard (30 Tage) oder ist bewusst geändert.

## 3. Rahmen im Repo

- [ ] [B] `.github/workflows/pr.yml` aus `ci-werkstatt.yml`, `defaults: run: shell: bash`.
      Den Job `merge-vermerk` noch **nicht** scharf schalten (auskommentiert oder ohne Datei);
      das geschieht als letzter Setup-Commit in Abschnitt 6.
- [ ] [B] Pflicht-Check-Liste, Skip-Erlaubnisliste, Abweichungsliste, Werkstatt-Pfadliste.
- [ ] [B] Merge-Skript unter `{{MERGE_SKRIPT_PFAD}}` aus `merge-gruen.py` (Gate-Marker v1);
      Erlaubnisliste der Gate-Autoren festgelegt.
- [ ] [B] PR-Vorlage mit den Feldern aus GA-2; `docs/werkstatt/LIVEGANG.md` aus `LIVEGANG.md`
      angelegt, Zeilen per Maske über das Entscheidungsprotokoll.
- [ ] [B] Je Pflicht-Check eine Rauchprobe; CI grün auf dem leeren Repo mit Lebenszeichen > 0.
- [ ] [B] `.claude/run/`, `.claude/worktrees/`, `.env.worktree`, `*env.list`, `*env.txt`,
      `*env.dump` in `.gitignore`;
      keine `.worktreeinclude`, die `.env*` nennt.
- [ ] [B] `dev_env` aus `dev-env.py` unter `{{DEV_ENV_PFAD}}`; Dev-Compose-Datei nach dem Vertrag im
      Docstring (nur Variablen aus `.env.worktree`, keine Vorgabewerte, Ports an `127.0.0.1`).
      Portbereich gemessen gewählt.
- [ ] [B] Nachweisdatei `{{NACHWEIS_PFAD}}` aus `sicherheit/nachweise.json` und der Test SK-1 bis
      SK-5 über Katalog, CSV und Nachweisdatei.

## 4. Rollen, Skills, Hooks, Evals — alles vor der Sperre

- [ ] [B, wörtlich aus der Vorlage] Hook-Skripte unter `.claude/hooks/` aus `templates/hooks/`
      (`werkstatt_hook.py`, `kette_protokoll.py`, `umsetzer_stop.py`, `test_autor_stop.py`,
      `gate_stop.py`), nach der Konvention LP-8. Alles, was sie ausführen, liegt selbst unter den
      Sperrpfaden; keine Symlinks dort. Voraussetzung: `python3`, git ab 2.31.
- [ ] [B, wörtlich aus der Vorlage] Skill-Plugin unter `.claude/skills/{{PLUGIN}}/`: Manifest,
      vier Skills, Evals; `sicherheits-katalog` mit `katalog.json` (Stufe 1: Zeilen aus eigenen
      Entscheidungen, Lebenszeichen > 0) und der unveränderten ASVS-CSV daneben, ihr SHA-256 im
      Kopf des Katalogs. `claude plugin validate .claude/skills/{{PLUGIN}} --strict` → Exit 0;
      Negativkontrolle Manifestpfad außerhalb → Exit ≠ 0. Frontmatter jedes Skills mit PyYAML
      parsen: `validate --strict` lässt kaputtes YAML durch (gemessen in der Quelle).
- [ ] [B, wörtlich aus der Vorlage] `.claude/settings.json` (Auto-Memory aus,
      `claudeMdExcludes`), Wurzel-`CLAUDE.md`, `.claude/rules/regeln.md`.
- [ ] [M] Workspace-Trust für genau diesen Ordner.
- [ ] [B] Hook-Proben ohne Modell (Fixture-Payload, Wegwerf-Repo, Liste im Kopf jedes Skripts),
      danach mit echtem Payload: ohne `/simplify` → verweigert; Sicherheitsbericht vor den Tests →
      verweigert; Baum nach Bericht geändert → verweigert; Mutationsprobe fehlt oder Mutant
      überlebt → verweigert; vollständige Kette → erlaubt; ohne Workspace-Trust → Hook
      übersprungen; mit `disableAllHooks: true` im Projekt → ?; unter `claude -p` → ?.
- [ ] [B] Probe: Übergibt das Skill-Werkzeug den Namen im Feld `skill`, mit oder ohne Namensraum?
      Ist `cwd` im Payload eines Worktree-Subagents der Worktree?
- [ ] [B] Probe Test-Autor: Abgabe mit Produktdatei → verweigert; nur Tests → erlaubt.
- [ ] [B] Probe-PRs Gate: Doppelbau → „nein“; toter Pfad → „nein“; sauber → „ja“ mit Prüfumfang;
      „behebe selbst“ → Baum unverändert; Sicherheitsbefund ohne Vermerk → „nein“; leeres „Wie
      verifiziert“ → „nein“.
- [ ] [B] Probe: Plugin-Skill-Name in `skills:` (mit oder ohne Namensraum).
- [ ] [B] Probe: Testdateien aus dem Worktree des Test-Autors auf den Feature-Branch.
- [ ] [B] Probe: begrenzt `maxTurns` ein Stopp-Veto? Erst danach steht das Feld in den Vorlagen.
- [ ] [B] Probe Ladewege: Umsetzer nennt auf Frage eine Regel aus `.claude/rules/regeln.md`; nach
      einem Lauf ist das Auto-Memory-Verzeichnis leer; die übergeordnete `CLAUDE.md` lädt nicht.
- [ ] [B] Probe: Skilltext von `/simplify` und `/security-review` in der installierten Fassung
      noch wie dokumentiert (ändert / nur Bericht).
- [ ] [B] Alle Rollen starten mit `{{REPO_PFAD}}` als Arbeitsverzeichnis.
- [ ] [B] Eval-Fälle je Skill (`templates/skills/eval-faelle/`, mit Fixture je Fall) und je
      Rolle (Eigenbau, ein Eval-Lauf lädt laut Doku kein `.claude/`): einer „löst aus“, einer
      „bleibt still“.
- [ ] [M] Eval-Baseline auf Zuruf (`--threshold 0`, `--ablation none`, `runs: 5`).
- [ ] [M] Kostendeckel `--max-cost-usd` nach der Baseline gesetzt.
- [ ] [B] Schärfungsrunden der Beschreibungen, bis jeder Fall 0,8 erreicht. Eine neue Fassung
      wird zur neuen geprüften Vorlage; der Hash-Vergleich läuft auf ihr.
- [ ] [B] Feuert-Nachweis des Harness (verdorbener Skill fällt, zu breiter Skill fällt).
- [ ] Evals nie in der CI.
- [ ] [B] Isolation F-1 bis F-11 (`reference/isolation.md`), je mit Mutant.
- [ ] [B] Sicherheitskatalog F-1 (Prüfung der Dateien) und F-3 (Skill-Eval, Inhaltsprobe).

## 5. Merge-Skript feuert

- [ ] [B] Je G-Punkt eine Probe im Prüfmodus, die rot wird (G-1 bis G-8, einschließlich
      „zweimal nein, dann ja → rot", „zwei Marker zur selben SHA → rot", „Marker von einem Konto
      außerhalb der Erlaubnisliste → rot", „Umbenennung aus einem Sperrpfad heraus → rot").
- [ ] [B] Negativkontrolle: sauberer PR mit „ja" wird gemergt.
- [ ] [B] Merge am Skript vorbei auf einem Wegwerf-Repo → Lauf auf `main` rot; Merge-Vermerk mit
      einer SHA, die nicht der zweite Elternteil ist → rot.
- [ ] [B] Arbeitskopie-Abgleich: ungetrackter Hook, `disableAllHooks` in `settings.local.json`,
      geänderte getrackte `.claude/settings.json`, fremde `settings.extra.json` → je rot; sauberer
      Klon mit den Dauerdateien → grün.
- [ ] [M] **Stufe 3** nach dem Merge, der das Skript auf `origin/main` bringt: Deny
      `gh pr merge *` (Bash, PowerShell) samt E1-Hook in `{{SCHUTZ_DATEI}}`; ein Allow auf
      `gh pr merge` in einer `settings.local.json` entfernt. Bis dahin mergt die Bau-Session nach
      grüner CI per `gh pr merge` (Restgrenze, benannt).

## 6. Sperren — in dieser Reihenfolge

1. - [ ] [M] Eigener SSH-Signierschlüssel mit Passphrase, nicht im ssh-agent zwischengespeichert.
2. - [ ] [M] `allowed_signers` unter einem Sperrpfad angelegt — vom Menschen, nicht von der
         Bau-Session.
3. - [ ] [B] Signatur-Probe (1): `git commit -S` durch die Bau-Session **scheitert** schon beim
         Signieren. Gelingt er: Restgrenze (siehe unten), bis die Ursache behoben ist.
4. - [ ] [B] Agent-Dateien, Skills samt Katalog, Hook-Skripte, `.claude/settings.json`,
         Wurzel-`CLAUDE.md` und Regeldatei als wörtliche Kopie der geprüften Vorlage angelegt.
5. - [ ] [M] SHA-256 von Vorlage und Ergebnis verglichen und abgenickt. Abweichung → kein Commit.
6. - [ ] [B] Commit der Sperrpfad-Dateien.
   - [ ] [B] **Letzter Setup-Commit:** Job `merge-vermerk` scharf schalten, `{{C2_STARTPUNKT}}`
         = Vorgänger dieses Commits (oder per Folge-Commit gesetzt). Ein nicht ersetzter
         Platzhalter lässt den Job mit klarer Meldung rot werden.
7. - [ ] [M] **Stufe 2:** Deny-Regeln für alle Sperrpfade samt Ladewegen in den
         Benutzer-Einstellungen, mit absolutem Repo-Pfad (`LEITPLANKEN.md`, Stufe 2).
8. - [ ] [B] Probe-PR an einem Sperrpfad, auch mit Abweichungseintrag, auch als Umbenennung,
         auch als `.Claude/…`, an `.claude/CLAUDE.md`, `.claude/rules/x.md` und `src/CLAUDE.md`
         → rot; Negativkontrolle PR an `README.md` → grün.
9. - [ ] [B] Signatur-Proben auf einem Wegwerf-Repo mit derselben Pipeline:
         (2) direkter Commit nur an Sperrpfaden ohne Signatur → rot;
         (3) Commit trägt einen fremden Schlüssel selbst in `allowed_signers` ein und ist mit ihm
         signiert → rot;
         (4) signierter Commit des Menschen, der auch eine Datei außerhalb der Sperrpfade ändert →
         rot;
         (5) Negativkontrolle: signierter Commit des Menschen nur an Sperrpfaden → grün.

10. - [ ] [M] Leitplanken-Proben LP-1 bis LP-8 auf Zuruf, in einem Wegwerf-Klon von `origin/main`,
          Ergebnisse in `LEITPLANKEN.md`. Kein Eintrag und kein Ergebnis heißt unentschieden.
11. - [ ] [M] Projekteigene Sperrdateien (etwa Soll-Bilder eines Bildvergleichs, Token-Datei) in
          `LOCKED_FILES` des Merge-Skripts, in beiden Listen der CI und als Deny-Zeilen — oder
          keine.

**Restgrenze, solange Probe (1) gelingt:** Die Signatur-Ausnahme ist ausgesetzt. Der Mensch nimmt
seinen Schlüssel mit einem letzten signierten Commit aus `allowed_signers` und mergt Änderungen an
Sperrpfaden selbst als PR mit Merge-Vermerk (Selbstauskunft, benannt).

## 7. Deploy-Weg

- [ ] [B] Staging-Deploy aus `main` automatisch.
- [ ] [B] Probe-PR mit `runs-on` außerhalb der Erlaubnisliste (auch `[self-hosted]` allein) → rot.
- [ ] [M] Prod-Workflow wartet auf den Required Reviewer; Deploy holt den Stand von außen.
- [ ] [M] Vor dem ersten Prod-Deploy: Livegang-Liste abgehakt, je Zeile Datum und Beleg.

## 8. Werkstatt grün

- [ ] Abschnitte 1 bis 7 abgehakt, offene Punkte als offen benannt. Erst dann bekommt die
      Bau-Session einen Block.

## Danach: Walking Skeleton (eigene Phase, nicht Teil der Werkstatt)

Eingang:

- [ ] Werkstatt grün (Abschnitt 8).
- [ ] [M] API-Contract des Fadens entschieden.
- [ ] [M] Datenmodell des Fadens entschieden, Identität und Rechte, soweit berührt.
- [ ] [M] Deploy-Ziel mit Betriebsminimum (Staging) steht.
- [ ] [M] Grenze des Fadens schriftlich: welcher **eine** Weg, wo er endet.

Ausgang:

- [ ] [B] Ein Durchlauf Ende-zu-Ende auf Staging — Schnittstelle, Datenbank, Deploy —, mit Test
      in der CI, durch dieselbe Werkstatt wie jeder PR.
- [ ] Was am Faden gebrochen ist, steht zurück in der Spezifikation.
- [ ] Erst danach der erste Fachbereich. „Der Skeleton sollte auch noch …" — nein.

## Offen

- {{OFFENE_PUNKTE}}
