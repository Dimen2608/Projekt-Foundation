# Schutz der Regeln und Deploy-Weg

> Wie verhindert wird, dass die Bau-Session ihre eigenen Prüfer ändert — und warum Prod beim
> Menschen bleibt.

## Das Problem

Die Bau-Session mergt grüne PRs selbst und läuft unter dem Benutzer des Menschen. Was sie prüft,
liegt im selben Repo: Agent-Definitionen, Skills, Hooks, Einstellungen. Ohne Schutz kann ein PR
den Prüfer abschwächen, der ihn danach durchwinkt.

## Sperrpfade

```
.claude/agents/**            .claude/skills/**          .claude/hooks/**
.claude/settings*.json       .claude/output-styles/**   .claude/agent-memory*/**
**/CLAUDE.md                 **/CLAUDE.local.md         **/AGENTS.md
**/.claude/rules/**          dazu projekteigene Dateien (etwa Soll-Bilder, Token-Datei)
```

Nach dem Aufsetzen ändert diese Pfade **nur noch ein direkter, signierter Commit des Menschen**.
Ganz `.claude/skills/**` ist gesperrt, nicht nur der Skill des Gates: Das Gate lädt seinen Skill
per `skills:` vor, ein änderbarer Skill wäre eine zweite Tür zum Urteil. Eine Regel ist leichter zu
prüfen als eine Ausnahmeliste. Braucht der Bau einen neuen Skill, kommt er per signiertem Commit.

**Die Ladewege gehören dazu** (entschieden in der Quelle mit der Definition of Done): jede
`CLAUDE.md`, `CLAUDE.local.md` und `AGENTS.md` in jedem Ordner, die Regeldatei unter
`.claude/rules/`, Output-Styles und Agent-Memory. Sonst erreicht ein PR die Wirkung der gesperrten
Wurzel-`CLAUDE.md` über einen ungesperrten Ort. Das Auto-Memory liegt außerhalb des Repos und ist
deshalb aus (`autoMemoryEnabled: false`). Herleitung: [regeldateien.md](regeldateien.md). Dieselbe
Liste steht an vier Stellen und ändert sich nur zusammen: `LOCKED_PATHS` im Merge-Skript, zweimal
in `ci-werkstatt.yml` (Wächter und Merge-Vermerk), Deny-Regeln der Stufe 2 in `LEITPLANKEN.md`.

## Drei Schichten, eine trägt

1. **Einspielen per wörtlicher Kopie mit Hash-Vergleich.** Die Agent-Dateien entstehen aus einer
   geprüften Vorlage. Die Bau-Session darf sie im Aufsetz-Block anlegen, aber nur wörtlich. Vor dem
   Commit vergleicht ein Dritter die SHA-256-Werte von Vorlage und Ergebnis
   (`sha256sum vorlage.md .claude/agents/gate.md`), der Mensch nickt ab. Weichen sie ab, wird nicht
   committet.
2. **Deny-Regeln außerhalb des Repos, gesetzt vom Menschen.** Unmittelbar nach dem Hash-Vergleich
   setzt der Mensch Deny-Regeln für die Sperrpfade in seinen **Benutzer-Einstellungen**, mit
   absolutem Repo-Pfad (Stufe 2 der Leitplanken). Kein Commit der Bau-Session kann sie aufheben.
   Das Deny auf `gh pr merge` kommt in die `--settings`-Datei der Bau-Session, sobald das
   Merge-Skript auf `origin/main` liegt (Stufe 3). Ebenen, Wortlaut und Proben stehen in
   [leitplanken.md](leitplanken.md).
3. **Der CI-Wächter ist der eigentliche Schutz.** Deny-Regeln sperren Edit und Write, aber nicht
   zuverlässig jeden Shell-Befehl. Deshalb macht der Wächter (G-4) jeden PR rot, der einen
   Sperrpfad berührt — ohne Ausnahme, auch nicht über einen Abweichungseintrag. Er vergleicht mit
   `git diff --no-renames` (eine Umbenennung aus einem Sperrpfad heraus zählt am alten Pfad) und
   ohne Unterschied der Groß- und Kleinschreibung. **Grenze:** Er schützt den Commit-Weg, nicht
   die Arbeitskopie. Eine Änderung an Hook oder Einstellung wirkt in der laufenden Session sofort.
   Das prüft der Arbeitskopie-Abgleich des Merge-Skripts vor jedem Merge.

**Wer den ersten Stand schreibt** (entschieden in der Quelle): für **jeden** Sperrpfad,
den die Bau-Session im Aufsetz-Block füllt, dasselbe Muster wie bei den Agents. Das gilt für Skills
samt Evals und Plugin-Manifest, für die Hook-Skripte und für die Hook-Verdrahtung in
`.claude/settings*.json`, aber ohne `permissions`, die setzt nur der Mensch. Das Muster: geprüfte
Vorlage, wörtliche Kopie, Hash-Vergleich durch einen Dritten, Nicken des Menschen. Die Vorlagen
liefert dieser Skill unter `templates/` (Agents, Hook-Skripte, Skills mit Manifest und Evals,
`settings.json`, Wurzel-`CLAUDE.md`, Regeldatei); nach dem Ersetzen der Platzhalter ist die
ausgefüllte Fassung die geprüfte Vorlage des Ziel-Repos. Hash: SHA-256 über den Git-Blob, beidseitig
LF (`git show <sha>:<vorlage> | sha256sum` gegen `git show <sha>:<zielpfad> | sha256sum`). Schriebe die
Bau-Session sie selbst, legte der Geprüfte den Vertrauensanker an. Eine Regel für alle Sperrpfade
ist leichter zu prüfen als eine Ausnahme.

**Reihenfolge im Aufsetz-Block:**

1. Hook-Skripte, Einstellungen und ihre Proben fertig und geprobt.
2. Skills und Evals mit Baseline und Schärfungsrunden fertig — nach der Sperre ändert sie nur
   noch der Mensch. Braucht eine Runde eine neue Fassung, wird die geprüfte Vorlage neu
   geschrieben, und der Hash-Vergleich läuft auf ihr (übernähme die Vorlage die Fassung der
   Bau-Session, wäre der Vergleich zirkulär).
3. Der Mensch legt `allowed_signers` an; die Signatur-Probe (1) läuft.
4. Hash-Vergleich, Commit.
5. Deny-Regeln.

Sonst wird jede Nachbesserung an einem Hook oder Skill ein direkter Commit des Menschen.

**Bekannte Grenze: Verweise aus den Sperrpfaden heraus.** Ein Hook-Skript oder Skill, das eine
Datei außerhalb der Sperrpfade aufruft oder einliest (ein Hilfsskript unter `scripts/`, eine
Konfiguration), oder ein Symlink, der aus einem Sperrpfad auf eine solche Datei zeigt, macht diese
Datei zum ungesperrten Teil des Prüfers. Der Wächter sieht nur Pfade, nicht Aufrufe. Gegenmittel:
Hooks und Skills halten alles, was sie ausführen, selbst unter den Sperrpfaden, keine Symlinks
dort; die Rückschau prüft das.

## Signierte direkte Commits des Menschen

Die Pipeline auf `main` macht jeden Commit ohne Merge-Vermerk rot
([gruen-und-gate.md](gruen-und-gate.md)). Ein direkter Commit des Menschen an den Sperrpfaden
braucht deshalb eine Ausnahme, die die Bau-Session nicht nachahmen kann:

- Der Mensch bekommt einen **eigenen SSH-Schlüssel zum Signieren**, mit **Passphrase** und **ohne
  Zwischenspeicher im ssh-agent**. Ein Schlüssel ohne Passphrase oder im Agent-Cache wäre für die
  Bau-Session nutzbar, weil sie unter demselben Benutzer läuft.
- Die Pipeline lässt einen Commit ohne Merge-Vermerk nur zu, wenn er nur Sperrpfade ändert und
  `git verify-commit` ihn gegen die `allowed_signers`-Datei aus seinem **Eltern-Commit** bestätigt
  — nie aus dem geprüften Commit selbst.
- Die `allowed_signers`-Datei liegt **selbst unter einem Sperrpfad** (Vorschlag
  `.claude/hooks/allowed_signers`). Der Mensch legt sie an, bevor der Wächter wirkt, nicht die
  Bau-Session — sonst legte der Geprüfte den Vertrauensanker an.
- **Proben:**
  1. Die Bau-Session versucht `git commit -S` und **muss schon beim Signieren scheitern** (im
     Projekt-Repo, vor dem Hash-Vergleich).
  2. Direkter Commit nur an Sperrpfaden ohne Signatur → rot.
  3. Ein Commit trägt einen **fremden Schlüssel selbst** in `allowed_signers` ein und ist mit ihm
     signiert → rot. Diese Probe fängt eine Umsetzung, die die Datei aus dem Commit selbst liest.
  4. Signierter Commit des Menschen, der auch eine Datei außerhalb der Sperrpfade ändert → rot.
  5. Negativkontrolle: signierter Commit des Menschen nur an Sperrpfaden → grün.

  (2) bis (5) laufen auf einem Wegwerf-Repo mit derselben Pipeline, nachdem sie eingeführt ist.
- **Restgrenze:** Gelingt Probe (1), ist der Weg nicht dicht. Bis die Ursache behoben ist, mergt
  der Mensch Änderungen an Sperrpfaden selbst als PR mit Merge-Vermerk (das Skript mergt sie nie),
  und den Vermerk könnte die Bau-Session genauso schreiben — Selbstauskunft. **Die
  Signatur-Ausnahme ist in dieser Zeit ausgesetzt** (Vorschlag der Quelle): Der Mensch nimmt seinen
  Schlüssel mit einem letzten signierten Commit aus `allowed_signers`, sonst bliebe neben dem
  PR-Weg ein grüner direkter Commit der Bau-Session ohne PR-Spur.
- Die Commits des Aufsetz-Blocks auf leerem `main` liegen vor dem ersten Lauf dieser Prüfung. Der
  Aufsetz-Block schaltet sie als **letzten Setup-Commit** scharf; Startpunkt ist dessen Vorgänger
  (oder per Folge-Commit gesetzt). Ist der Platzhalter nicht ersetzt, scheitert die Prüfung mit
  klarer Meldung.

Ein Hardware-Schlüssel mit Berührung (`sk-ssh-ed25519`) erfüllt dieselbe Bedingung.

## Workspace-Trust und Rechte

Allow- und Deny-Regeln, Classifier und Workspace-Trust setzt nur der Mensch. Eine Nachricht aus
einer anderen Session ist nie eine Freigabe.

## Deploy-Weg

| Ziel | Wer löst aus | Wie |
| --- | --- | --- |
| Staging | automatisch | Jeder grüne Merge auf `main` geht nach Staging. Staging hat nur Test-Zugänge. Bei Änderungen an Compose, Deploy oder Env laufen zusätzlich Secret-Scan und eine Infra-Prüfung (Compose gültig, kein Prod-Geheimnis). |
| Prod | **nur der Mensch** | Workflow mit GitHub-Environment `prod`, der Mensch als **Required Reviewer**. Prod ist nicht Teil von „grün heißt mergen": Was nach außen geht, bleibt beim Menschen. |

**Kein CI-Job auf dem Prod-Host.** Der Deploy holt den fertigen Stand von außen (gebautes Image per
Pull oder über SSH). Auf Prod führt kein Runner Code aus einem PR aus. Der Wächter prüft `runs-on:`
gegen eine **Erlaubnisliste** auf Mengengleichheit: `runs-on` muss genau
`[self-hosted, {{RUNNER_LABEL}}]` sein; jeder andere Wert ist rot, auch `[self-hosted]` allein.

**Neu aufzumachen**, wenn der Klick des Menschen zum Engpass wird — dann käme ein automatischer
Prod-Deploy mit Canary und Rollback in Frage, nicht vorher.

## Eigener Runner

- **Eigener Benutzer** je Repo, getrennt von anderen Runnern auf derselben Maschine.
- **workFolder unter `$HOME`** dieses Benutzers. Lehre aus der Quelle: Liegt er außerhalb, scheitert
  der Artefakt-Upload von gitleaks.
- **Eigenes Label** (`{{RUNNER_LABEL}}`), das genau die Erlaubnisliste bildet.
- **Grenzen** per systemd, in der Quelle: `MemoryMax=4G`, `CPUQuota=200%`, `NoNewPrivileges=yes`,
  `PrivateTmp=yes`.
- Jeder Workflow setzt `defaults: run: shell: bash`. Nur so läuft GitHub die Schritte mit
  `bash --noprofile --norc -eo pipefail {0}`; ohne die Angabe fehlt `pipefail`, und eine Pipe
  verschluckt den Exit-Code.
- **Dependabot:** Versions-Updates gebündelt, Security-Updates sofort als eigener PR; beide durch
  dieselbe CI. Die Repo-Schalter „Dependabot alerts" und „Dependabot security updates" setzt der
  Mensch.
