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
- [ ] [M] **Offen bis entschieden:** Wer schreibt den ersten Stand der gesperrten Skills, der
      Hook-Skripte und der Hook-Verdrahtung in `.claude/settings*.json`? Für die Agent-Dateien
      gilt: geprüfte Vorlage, wörtliche Kopie, Hash-Vergleich. Empfehlung: dasselbe Muster für
      alle Sperrpfade, sonst legt der Geprüfte den Vertrauensanker an.

## 2. Runner und Repo-Einstellungen

- [ ] [M] Eigener Runner-Benutzer, getrennt von anderen Runnern auf der Maschine.
- [ ] [M] workFolder unter `$HOME` des Runner-Benutzers.
- [ ] [M] Label `{{RUNNER_LABEL}}`; Grenzen (`MemoryMax`, `CPUQuota`, `NoNewPrivileges`,
      `PrivateTmp`) gesetzt.
- [ ] [M] Kein Runner dieses Repos auf dem Prod-Host.
- [ ] [M] Dependabot alerts und security updates eingeschaltet.
- [ ] [M] Environment `prod` mit dem Menschen als Required Reviewer.

## 3. Rahmen im Repo

- [ ] [B] `.github/workflows/pr.yml` aus `ci-werkstatt.yml`, `defaults: run: shell: bash`.
      Den Job `merge-vermerk` noch **nicht** scharf schalten (auskommentiert oder ohne Datei);
      das geschieht als letzter Setup-Commit in Abschnitt 6.
- [ ] [B] Pflicht-Check-Liste, Skip-Erlaubnisliste, Abweichungsliste, Werkstatt-Pfadliste.
- [ ] [B] Merge-Skript unter `{{MERGE_SKRIPT_PFAD}}` aus `merge-gruen.py`; Gate-Marker-Format und
      Erlaubnisliste der Gate-Autoren festgelegt (offen bis hier).
- [ ] [B] Je Pflicht-Check eine Rauchprobe; CI grün auf dem leeren Repo mit Lebenszeichen > 0.
- [ ] [B] `.claude/run/` in `.gitignore`.

## 4. Rollen, Skills, Hooks, Evals — alles vor der Sperre

- [ ] [B oder Vorlage, siehe 1] Hook-Skripte unter `.claude/hooks/` (Umsetzer-Kette, Test-Autor,
      Gate). Alles, was sie ausführen, liegt selbst unter den Sperrpfaden; keine Symlinks dort.
- [ ] [M] Workspace-Trust für genau diesen Ordner.
- [ ] [B] Proben der Umsetzer-Kette mit echtem Payload: ohne `/simplify` → verweigert;
      Sicherheitsbericht vor den Tests → verweigert; Baum nach Bericht geändert → verweigert;
      vollständige Kette → erlaubt; ohne Workspace-Trust → Hook übersprungen.
- [ ] [B] Probe Test-Autor: Abgabe mit Produktdatei → verweigert; nur Tests → erlaubt.
- [ ] [B] Probe-PRs Gate: Doppelbau → BLOCKIEREND; toter Pfad → BLOCKIEREND; sauber → „ja" mit
      Prüfumfang; „behebe selbst" → Baum unverändert; Sicherheitsbefund ohne Vermerk →
      BLOCKIEREND.
- [ ] [B] Probe: Plugin-Skill-Name in `skills:` (mit oder ohne Namensraum).
- [ ] [B] Probe: Testdateien aus dem Worktree des Test-Autors auf den Feature-Branch.
- [ ] [B] Probe: begrenzt `maxTurns` ein Stopp-Veto?
- [ ] [B] Probe: Skilltext von `/simplify` und `/security-review` in der installierten Fassung
      noch wie dokumentiert (ändert / nur Bericht).
- [ ] [B] Alle Rollen starten mit `{{REPO_PFAD}}` als Arbeitsverzeichnis.
- [ ] [B] Eval-Fälle je Skill und Rolle: einer „löst aus", einer „bleibt still".
- [ ] [M] Eval-Baseline auf Zuruf (`--threshold 0`, `--ablation none`, `runs: 5`).
- [ ] [M] Kostendeckel `--max-cost-usd` nach der Baseline gesetzt.
- [ ] [B] Schärfungsrunden der Beschreibungen, bis jeder Fall 0,8 erreicht. Eine neue Fassung
      wird zur neuen geprüften Vorlage; der Hash-Vergleich läuft auf ihr.
- [ ] [B] Feuert-Nachweis des Harness (verdorbener Skill fällt, zu breiter Skill fällt).
- [ ] Evals nie in der CI.

## 5. Merge-Skript feuert

- [ ] [B] Je G-Punkt eine Probe im Prüfmodus, die rot wird (G-1 bis G-8, einschließlich
      „zweimal nein, dann ja → rot", „zwei Marker zur selben SHA → rot", „Marker von einem Konto
      außerhalb der Erlaubnisliste → rot", „Umbenennung aus einem Sperrpfad heraus → rot").
- [ ] [B] Negativkontrolle: sauberer PR mit „ja" wird gemergt.
- [ ] [B] Merge am Skript vorbei auf einem Wegwerf-Repo → Lauf auf `main` rot; Merge-Vermerk mit
      einer SHA, die nicht der zweite Elternteil ist → rot.
- [ ] [M] **Vorschlag:** Deny-Regel für `gh pr merge` außerhalb des Repos (Ort und Wortlaut offen).

## 6. Sperren — in dieser Reihenfolge

1. - [ ] [M] Eigener SSH-Signierschlüssel mit Passphrase, nicht im ssh-agent zwischengespeichert.
2. - [ ] [M] `allowed_signers` unter einem Sperrpfad angelegt — vom Menschen, nicht von der
         Bau-Session.
3. - [ ] [B] Signatur-Probe (1): `git commit -S` durch die Bau-Session **scheitert** schon beim
         Signieren. Gelingt er: Restgrenze (siehe unten), bis die Ursache behoben ist.
4. - [ ] [B] Agent-Dateien (und nach Entscheidung 1 die Skills und Hooks) als wörtliche Kopie der
         geprüften Vorlage angelegt.
5. - [ ] [M] SHA-256 von Vorlage und Ergebnis verglichen und abgenickt. Abweichung → kein Commit.
6. - [ ] [B] Commit der Agent-Dateien.
   - [ ] [B] **Letzter Setup-Commit:** Job `merge-vermerk` scharf schalten, `{{C2_STARTPUNKT}}`
         = Vorgänger dieses Commits (oder per Folge-Commit gesetzt). Ein nicht ersetzter
         Platzhalter lässt den Job mit klarer Meldung rot werden.
7. - [ ] [M] Deny-Regeln für `.claude/agents/**`, `.claude/skills/**`, `.claude/hooks/**`,
         `.claude/settings*.json` in den Benutzer-Einstellungen, außerhalb des Repos.
8. - [ ] [B] Probe-PR an einem Sperrpfad, auch mit Abweichungseintrag, auch als Umbenennung,
         auch als `.Claude/…` → rot.
9. - [ ] [B] Signatur-Proben auf einem Wegwerf-Repo mit derselben Pipeline:
         (2) direkter Commit nur an Sperrpfaden ohne Signatur → rot;
         (3) Commit trägt einen fremden Schlüssel selbst in `allowed_signers` ein und ist mit ihm
         signiert → rot;
         (4) signierter Commit des Menschen, der auch eine Datei außerhalb der Sperrpfade ändert →
         rot;
         (5) Negativkontrolle: signierter Commit des Menschen nur an Sperrpfaden → grün.

**Restgrenze, solange Probe (1) gelingt:** Die Signatur-Ausnahme ist ausgesetzt. Der Mensch nimmt
seinen Schlüssel mit einem letzten signierten Commit aus `allowed_signers` und mergt Änderungen an
Sperrpfaden selbst als PR mit Merge-Vermerk (Selbstauskunft, benannt).

## 7. Deploy-Weg

- [ ] [B] Staging-Deploy aus `main` automatisch.
- [ ] [B] Probe-PR mit `runs-on` außerhalb der Erlaubnisliste (auch `[self-hosted]` allein) → rot.
- [ ] [M] Prod-Workflow wartet auf den Required Reviewer; Deploy holt den Stand von außen.

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
