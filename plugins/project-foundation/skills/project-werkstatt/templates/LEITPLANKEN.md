# Leitplanken — {{PROJEKT}}

> Vorlage aus project-werkstatt. Kopieren nach `docs/werkstatt/LEITPLANKEN.md`, Platzhalter
> ersetzen. Die Einstellungsblöcke setzt **nur der Mensch**, in Dateien **außerhalb des Repos**.
> Die Bau-Session schreibt sie nie und schlägt Änderungen nur vor.
> Begründung, Proben und Grenzen: `reference/leitplanken.md` des Skills.
> Repo absolut, in Regelform: `//{{REPO_PFAD_POSIX}}` (Windows `C:\x` → `//c/x`, unter WSL der
> POSIX-Pfad) · `--settings`-Datei: `{{SCHUTZ_DATEI}}` · Stand: {{DATUM}}

Die Muster sind ein **Vorschlag**. Was sie wirklich sperren, zeigt erst die Probe der Zeile.
Jedes Bash-Muster gibt es auch als PowerShell-Muster, wenn die Bau-Session PowerShell benutzen
kann.

## Stufe 1 — vor dem Aufsetz-Block

Datei `{{SCHUTZ_DATEI}}`, außerhalb des Repos. Die Bau-Session startet mit
`claude --settings {{SCHUTZ_DATEI}}`.

```json
{
  "disableAllHooks": false,
  "env": {
    "CLAUDE_CODE_SUBPROCESS_ENV_SCRUB": "1"
  },
  "permissions": {
    "deny": [
      "Bash(git push * main)",
      "Bash(git push * HEAD:main)",
      "Bash(git push * *:main)",
      "PowerShell(git push * main)",
      "PowerShell(git push * HEAD:main)",
      "PowerShell(git push * *:main)",

      "Bash(ssh *)",
      "Bash(scp *)",
      "Bash(sftp *)",
      "Bash(gh workflow run *)",
      "PowerShell(ssh *)",
      "PowerShell(scp *)",
      "PowerShell(sftp *)",
      "PowerShell(gh workflow run *)",
      "Read(~/.ssh/**)",

      "Bash(git push --force*)",
      "Bash(git push -f*)",
      "Bash(git push --delete*)",
      "Bash(git push * --force*)",
      "Bash(git push * -f*)",
      "Bash(git push * --delete*)",
      "Bash(git reset --hard*)",
      "Bash(git clean -f*)",
      "Bash(git branch -D*)",
      "Bash(gh repo delete *)",
      "PowerShell(git push --force*)",
      "PowerShell(git push -f*)",
      "PowerShell(git push --delete*)",
      "PowerShell(git push * --force*)",
      "PowerShell(git push * -f*)",
      "PowerShell(git push * --delete*)",
      "PowerShell(git reset --hard*)",
      "PowerShell(git clean -f*)",
      "PowerShell(git branch -D*)",
      "PowerShell(gh repo delete *)",

      "Read(//**/.env)",

      "Edit(//{{NACHBAR_REPO_POSIX}}/**)",
      "Write(//{{NACHBAR_REPO_POSIX}}/**)"
    ]
  }
}
```

- Zeilen 1–6 (oben): LP-1, Push-Teil. Fragil, weil Argumentmuster. Ein Netz ist der E1-Hook.
- `ssh` bis `Read(~/.ssh/**)`: LP-5.
- `git push --force*` bis `PowerShell(gh repo delete *)`: LP-6. Im Auto-Modus zusätzlich `autoMode.hard_deny`,
  Format aus `claude auto-mode defaults`.
- `Read(//**/.env)` und Env-Scrub: LP-7. `"disableAllHooks": false`: LP-3, Lesart L, Probe P3b.
- Die letzten zwei Zeilen: LP-4. Sie entfallen, wenn die Bau-Session kein Nachbar-Repo liest.
- `.gitignore` des Repos deckt `*env.list`, `*env.txt`, `*env.dump` (LP-7 c), das schreibt die
  Bau-Session.
- **Sperr-Hooks** (LP-1 `sh -c`, LP-2 Shell, LP-4): Skripte offen, Konvention LP-8.

## Stufe 2 — nach dem Hash-Vergleich der Sperrpfad-Dateien

Benutzer-Einstellungen des Menschen (`~/.claude/settings.json`), pfadgebunden, mit absolutem Pfad:

```json
{
  "permissions": {
    "deny": [
      "Edit(//{{REPO_PFAD_POSIX}}/**/.claude/agents/**)",
      "Write(//{{REPO_PFAD_POSIX}}/**/.claude/agents/**)",
      "Edit(//{{REPO_PFAD_POSIX}}/**/.claude/skills/**)",
      "Write(//{{REPO_PFAD_POSIX}}/**/.claude/skills/**)",
      "Edit(//{{REPO_PFAD_POSIX}}/**/.claude/hooks/**)",
      "Write(//{{REPO_PFAD_POSIX}}/**/.claude/hooks/**)",
      "Edit(//{{REPO_PFAD_POSIX}}/**/.claude/settings*.json)",
      "Write(//{{REPO_PFAD_POSIX}}/**/.claude/settings*.json)"
    ]
  }
}
```

LP-2. Die Muster folgen der Sperrpfad-Liste aus G-4. Wird sie erweitert (etwa um `CLAUDE.md` und
die Regeldatei nach der Definition of Done), kommen die Zeilen hier mit. Hat diese Datei schon
einen `permissions`-Block, werden die Zeilen dort ergänzt, nicht ersetzt.

## Stufe 3 — nach dem Merge, der das Merge-Skript auf `origin/main` bringt

In `{{SCHUTZ_DATEI}}` ergänzen:

```json
"Bash(gh pr merge *)",
"PowerShell(gh pr merge *)"
```

Dazu der E1-Hook gegen `sh -c "gh pr merge …"`. Ein eventuelles Allow auf `gh pr merge` in einer
`settings.local.json` entfernt der Mensch.

## Proben

| LP | Probe | Ergebnis | Mutant | Ergebnis | Datum |
| --- | --- | --- | --- | --- | --- |
| LP-1 | P1a–P1d | | ohne Deny; mit Deny ohne Hook | | |
| LP-2 | P2a, P2b, P2c | | ohne Regeln | | |
| LP-3 | P3a, P3b | | ohne `disableAllHooks` | | |
| LP-4 | Edit, `commit --help`, `show` | | ohne Deny und Hook | | |
| LP-5 | `ssh -V`, `gh workflow run --help` | | ohne Deny | | |
| LP-6 | `git reset --hard HEAD` mit Marker | | ohne Deny | | |
| LP-7 | Canary mit Scrub | | ohne Scrub | | |
| LP-8 | Fixture verboten / erlaubt | | `exit 0` vorn | | |
| Umgebung | Sandbox-Probe: Docker, `CLAUDE.md`-Ladeweg, `gh`-Login, Startweg | | — | | |

Aufruf: `claude -p "<Aktion>" --permission-mode dontAsk --output-format stream-json --verbose`,
in einem Wegwerf-Klon von `origin/main`, mit einer Allow-Zeile für den Probeaufruf in der Kopie
der Datei. Kein Eintrag und kein Ergebnis heißt unentschieden.

## Offen

- {{OFFENE_PUNKTE}}
