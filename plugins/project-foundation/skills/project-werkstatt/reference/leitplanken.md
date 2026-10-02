# Leitplanken — was die Bau-Session darf, was gesperrt ist, und wie die Sperre feuert

> Wer die Werkstatt aufsetzt, liest diese Datei vor Schritt 5 (SPERREN). Die Einstellungsblöcke
> zum Kopieren stehen in [templates/LEITPLANKEN.md](../templates/LEITPLANKEN.md).

## Herkunft

Werkstatt-Plan Atemluft V2, Teilblock 100-4 (A-05), entschieden mit ENT-206 Punkt 1 bis 5 am
02.10.2026. Die Aussagen über Claude Code stammen aus einer Doku-Recherche der Quelle vom selben
Tag. Was dort nicht belegt war, steht hier als **Probe** oder unter „Offen", nicht als Tatsache.
Doku und Verhalten ändern sich mit jeder Claude-Code-Version, darum entscheidet die Probe.

## Die Leitfrage

Was darf die Bau-Session, was ist verboten, was braucht den Menschen, und **wie wird gezeigt,
dass eine Sperre greift, statt bloß konfiguriert zu sein?**

**Antwort:** Was nicht fallen darf, liegt als Deny-Regel **außerhalb des Repos**. Ein Deny auf
einer Ebene kann keine andere Ebene freigeben. Hooks im Repo führen die Kette, sind aber keine
Sperre: Eine Änderung an Hook oder Einstellung wirkt in der laufenden Session sofort, ohne Commit
und ohne Review, und ein Projekt-`disableAllHooks: true` schaltet nach der Herleitung der Quelle auch
Benutzer-Hooks ab (abgeleitet, P3a misst es). CI und Merge-Skript erkennen, was committet wird, die Arbeitskopie sehen sie
nicht. Dafür gibt es den Arbeitskopie-Abgleich (unten).

## Drei Schutzklassen

Jede Leitplanke trägt ihre Klasse, damit niemand ein Netz für eine Sperre hält.

| Klasse | Wirkt | Beispiel |
| --- | --- | --- |
| **Sperre** | verhindert vor der Aktion | Deny-Regel außerhalb des Repos |
| **Netz** | fängt, was die Sperre nicht sieht, ist abschaltbar | `PreToolUse`-Hook auf den rohen Befehlstext |
| **Erkennung** | merkt es nachher | CI-Wächter, Merge-Vermerk, Rückschau, Transkript-Maske |

## Die Schichtung

| Ebene | Ort, Schreiber | Trägt | Grenze |
| --- | --- | --- | --- |
| **E0 Managed** | Managed-Einstellungen, der Mensch | `allowManagedHooksOnly`, Sperr-Hooks, die ein Projekt-`disableAllHooks` nicht abschaltet | Ort und Schreibrecht hängen am Betriebssystem; fehlt das Schreibrecht, entfällt E0 |
| **E1 außerhalb des Repos** | `--settings`-Datei oder Benutzer-Einstellungen, der Mensch | Deny-Regeln (Bash, PowerShell, Edit, Write, Read), Sperr-Hooks, Env-Variablen | Deny trifft den Befehlstext: `sh -c`, absoluter Pfad, Variablen und Wrapper umgehen es. Ohne Sandbox läuft die Shell ungebremst |
| **E2 Projekt** | Repo, die Bau-Session im Aufsetz-Block, danach Sperrpfad | Kette (Frontmatter-Hooks, Skripte), `.gitignore`, Regeln | Führung, kein Schutz: Arbeitskopie-Änderungen wirken sofort |
| **E3 CI, Merge-Skript** | Git-Host, Fassung von `origin/main` | G-4 Sperrpfade, Merge-Vermerk, Signatur, `runs-on`-Liste | Arbeitskopie unsichtbar; Marker und Vermerk sind Selbstauskunft |
| **E4 Beobachtung** | Rückschau, Planungs-Session | Transkript-Maske, Audit-Log der Hooks | Transkripte nur so lange, wie Claude Code sie aufbewahrt (Standard 30 Tage) |

**Welche Regel in welche Datei.** Regeln, die nur für die Bau-Session gelten sollen, kommen in
eine **`--settings`-Datei außerhalb des Repos**, mit der die Bau-Session gestartet wird. Grund: Die
Benutzer-Ebene gilt für jedes Projekt des Benutzers. Ein Benutzer-Deny auf `gh pr merge`,
`~/.ssh` oder `.env` träfe auch die anderen Sessions des Menschen. In die **Benutzer-Einstellungen**
gehört allein, was an einen Pfad gebunden ist, die Sperrpfade dieses Repos mit absolutem Pfad. Das
greift dann auch, wenn die Session ohne Startflag läuft.

**Kann die Bau-Session nicht mit `--settings` starten** (etwa eine Desktop-Sitzung, das ist nicht
belegt), bleiben die Benutzer-Einstellungen. Dann werden Read-Regeln auf den Repo-Pfad begrenzt,
die Bash-Sperren entfallen als Sperre, und ein Benutzer-Hook, der über `CLAUDE_PROJECT_DIR` auf das
Repo begrenzt ist, bleibt als Netz.

**Pfadform der Edit-, Write- und Read-Regeln** (Doku-Lage der Quelle, durch Probe LP-2 zu
bestätigen):

| Muster | In Benutzer-Einstellungen | In Projekt-, Local- und `--settings`-Datei |
| --- | --- | --- |
| `//abs/pfad/**` | absolut | absolut |
| `~/pfad` | Home-Verzeichnis | Home-Verzeichnis |
| `/pfad` | verankert an `~/.claude/`, trifft **kein** Projekt | verankert am Arbeitsverzeichnis, in einer Worktree-Session am Worktree |
| `pfad` | relativ zum aktuellen Verzeichnis, trifft **jedes** Projekt | relativ zum aktuellen Verzeichnis |

**Empfehlung:** absolut und auf das Repo begrenzt, `//<absoluter Repo-Pfad>/**/<muster>`. Unter
Windows wird `C:\` zu `//c/`, unter WSL gilt der POSIX-Pfad der Umgebung. Das `**/` soll die
Worktrees unter `.claude/worktrees/<name>/` mitnehmen. Das ist abgeleitet, nicht dokumentiert, und
genau das prüft P2b.

## Die Freigabeliste

| | Was |
| --- | --- |
| **Frei, ohne Rückfrage** | Branch, Commit, Push auf einen Feature-Branch, PR anlegen, CI lesen, Tests und Dev-Stack, Merge über das Merge-Skript |
| **Braucht den Menschen** | Prod-Deploy; Allow-Regeln und Workspace-Trust; Änderungen an Sperrpfaden (signierter Commit); Läufe, die Kontingent kosten (Evals); was Geld kostet oder nach außen geht |
| **Verboten** | LP-1, LP-2, LP-4 bis LP-6 unten |

## Die Leitplanken

| LP | Leitplanke, Klasse | Ebene, Mechanismus | Feuert-Probe | Negativkontrolle (Mutant) |
| --- | --- | --- | --- | --- |
| LP-1 | **Merge und Push auf `main` nur über das Merge-Skript.** Sperre, Netz, Erkennung | E1: Deny `gh pr merge *` und Push-auf-`main`-Muster, je für Bash und PowerShell. E1-Hook (`PreToolUse`, Teilstring auf den rohen Befehlstext) fängt `sh -c` und absolute Pfade. E3: Merge-Vermerk. Das Skript läuft als `git show origin/main:<pfad> \| python -`. Ein Allow auf `python -` hängt nicht an der Herkunft des Skripts, die Sperre trägt das Deny auf den Merge-Befehl | P1a `gh pr merge --help` in Bash → abgelehnt. P1b `sh -c "gh pr merge --help"` mit Hook → kein Hilfetext, Audit-Zeile „block". P1c wie P1a in PowerShell. P1d `git push --dry-run origin HEAD:main` gegen ein lokales Bare-Repo → abgelehnt | Kopie ohne Deny: P1a, P1c, P1d laufen durch. Kopie mit Deny ohne Hook: P1b liefert den Hilfetext. Das belegt die Lücke, die der Hook schließt |
| LP-2 | **Sperrpfade: Edit und Write auf die Muster aus G-4.** Sperre für Edit und Write, Netz für die Shell, Erkennung über G-4 | E1 (Benutzer-Einstellungen, absoluter Pfad): Deny `Edit(…)` und `Write(…)` je Muster. E1-Hook auf Bash und PowerShell: Befehl nennt einen Sperrpfad und ein Schreibwort → Exit 2. E3: G-4, Arbeitskopie-Abgleich | P2a Session im Haupt-Checkout schreibt je Muster einen neuen Pfad → abgelehnt. P2b dieselbe Session schreibt unter `.claude/worktrees/<name>/` (nicht dokumentiert, Ergebnis festhalten). P2c Session im Worktree schreibt unter die Muster des Worktrees. Die Muster liest die Probe aus `origin/main`, nicht aus einer zweiten Kopie | Kopie ohne die Regeln: Die Dateien entstehen |
| LP-3 | **Hooks und Einstellungen nicht abschaltbar.** Sperre mit E0, sonst Netz und Erkennung | E0: `allowManagedHooksOnly` und Sperr-Hooks. **Lesart L** (abgeleitet, durch P3b zu prüfen): `"disableAllHooks": false` in der `--settings`-Datei überstimmt ein Projekt-`true`. Sonst: E1-`ConfigChange`-Hook mit Exit 2 auf eine Änderung, die `disableAllHooks` setzt (ob Exit 2 die Änderung verhindert, ist nicht belegt). E3: Arbeitskopie-Abgleich | P3a Projekt-`disableAllHooks: true`, E1-Hook aktiv, `--settings` ohne Eintrag → wirkt der Hook? Erwartet nein. P3b Projekt und Local je `true`, `--settings` mit `false` → wirkt der Hook? „Ja" bestätigt L | Kopie ohne jedes `disableAllHooks`: Hook blockiert. Fällt P3b negativ aus, bleibt E0, sofern der Mensch die Managed-Datei schreiben kann |
| LP-4 | **Nachbar-Repos nur lesen** (optional, wenn die Bau-Session einen Vorgänger, eine Spezifikation oder ein anderes Repo lesen, aber nie ändern darf). Sperre für Edit und Write, Netz für die Shell | E1 (`--settings`): Deny Edit und Write auf den Pfad und seine Worktree-Ordner. E1-Hook: Befehl mit dem Pfad oder `git -C` darauf und einem Wort außerhalb einer Leseliste (`show`, `grep`, `log`, `ls-tree`, `cat-file`, `diff`, `rev-parse`, `ls-files`) → Exit 2. Worktrees des Nachbar-Repos an anderem Ort bleiben ungedeckt | `Edit` auf eine nicht vorhandene Datei → abgelehnt; `git -C <pfad> commit --help` → blockiert; im selben Lauf `git -C <pfad> show HEAD:README.md` → läuft | Hook und Deny entfernt: `commit --help` läuft |
| LP-5 | **Kein Prod-Zugriff.** Sperre, Erkennung | E1: Deny `ssh *`, `scp *`, `sftp *`, `gh workflow run *`, je Bash und PowerShell; `Read(~/.ssh/**)` nur in der `--settings`-Datei. Env der Bau-Session trägt Test-Zugänge (LP-7). E3: `runs-on`-Erlaubnisliste | `ssh -V` und `gh workflow run --help` → abgelehnt | Deny entfernt: beide liefern Ausgabe |
| LP-6 | **Destruktive Aktionen.** Sperre für Muster, Erkennung für Umformulierungen | E1: Deny `git push --force*`, `-f`, `--delete`, `git reset --hard*`, `git clean -f*`, `git branch -D*`, `gh repo delete *`; im Auto-Modus zusätzlich `autoMode.hard_deny` auf E1 (Format aus `claude auto-mode defaults`, nicht aus Projekt-Einstellungen). E4: Transkript-Maske auf dasselbe Ziel nach einer Ablehnung | Wegwerf-Klon mit Marker-Datei: `git reset --hard HEAD` → abgelehnt, Marker bleibt | Deny entfernt: Marker weg |
| LP-7 | **Log-Hygiene: kein Zugangsdatum in Env oder Log.** Sperre durch Fehlen, Netz, Erkennung | (a) Env und `.env` der Bau-Session und des Dev-Stacks tragen nur Test-Zugänge. (b) E1: `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`, Deny `Read(//**/.env)` nur in der `--settings`-Datei (in Benutzer-Einstellungen auf den Repo-Pfad begrenzt). (c) `.gitignore` deckt Env-Dumps (`*env.list`, `*env.txt`, `*env.dump`). (d) Dump-Befehle (`env`) bleiben erlaubt, sie sind ein Messweg und bei Test-Zugängen harmlos. (e) Telemetrie-Export nicht ohne Prüfung einschalten. Transkripte speichern Tool-Ausgaben im Klartext, eine Maskierung lokaler Transkripte gibt es nicht | Wegwerf-Klon, Env-Variable `X_CANARY_PASSWORD=CANARY-<zufall>`, Lauf mit Scrub „gib die Umgebungsvariablen aus" → Maske über die Transkripte des Wegwerf-Projekts: 0 Dateien | Lauf ohne Scrub: ≥ 1 Datei. Das belegt, dass Env im Transkript landet und die Maske nicht blind ist |
| LP-8 | **Hook-Konvention: Lebenszeichen, fail-closed, echter Payload.** Voraussetzung jedes Netzes | (1) Jeder Aufruf schreibt Zeit, Event, Tool, `agent_type` und Entscheidung nach `.claude/run/hook-audit.log` (gitignored); nach einer Probe steigt die Zeilenzahl um 1. (2) Sperr-Hooks fangen eigene Fehler und enden dann mit Exit 2: Ein stiller Ausfall wiegt schwerer als ein sichtbarer Stillstand. Belegt sind nur Exit 2 und Exit 0 mit JSON, was Exit 1 oder ein Absturz bewirkt, ist offen. (3) Git-Hooks mit `trap '' PIPE`; Python-Hooks mit `python -B` (oder `PYTHONDONTWRITEBYTECODE=1` in der Verdrahtung), damit unter den Sperrpfaden kein Bytecode entsteht, den der Arbeitskopie-Abgleich als fremd melden muss. (4) Ein Aufzeichnungs-Hook schreibt den stdin eines echten Aufrufs als Fixture für Skript-Proben ohne Modell. (5) Ein `PreToolUse`-Block erscheint nicht im Stream, Beleg ist Wirkung plus Audit-Zeile | Aufzeichnung eines echten Payloads; danach ohne Modell: Fixture eines verbotenen Befehls → Exit 2, Audit-Zeile „block" | Fixture eines erlaubten Befehls → Exit 0, „allow". Mutant: `exit 0` als erste Zeile des Skripts → Exit 0 statt 2 |

**Bekannte Lücke in LP-1:** `python -c` mit Subprozess fasst kein Befehlsmuster. Der Merge-Vermerk
erkennt einen solchen Merge nachträglich.

## Einführung in drei Stufen

Die Leitplanken kommen nicht auf einmal. Jede Stufe hat ihren eigenen Auslöser:

1. **Stufe 1, vor dem Aufsetz-Block:** LP-4 bis LP-7 und der **Push-Teil** von LP-1.
2. **Stufe 2, nach dem Hash-Vergleich der Sperrpfad-Dateien:** LP-2. Die Bau-Session legt die
   Sperrpfade im Aufsetz-Block als wörtliche Kopie an, davor darf sie dort schreiben.
3. **Stufe 3, nach dem Merge, der das Merge-Skript auf `origin/main` bringt:** der **Merge-Teil**
   von LP-1 (Deny `gh pr merge *` samt Hook). Vorher gibt es kein Skript, über das gemergt werden
   könnte. Danach entfernt der Mensch ein eventuelles Allow auf `gh pr merge` aus seiner
   Konfiguration.

Stufe 2 und 3 haben keine feste Reihenfolge zueinander. Beide stehen vor dem Ende der Werkstatt.
Danach laufen die Proben von LP-1 bis LP-3 und der Arbeitskopie-Abgleich.

**Restgrenze vor Stufe 3, benannt:** Die Merges bis einschließlich des PR, der das Skript
einführt, laufen ohne G-1 bis G-8 und ohne Merge-Vermerk. Entscheidung der Quelle: Die Bau-Session
mergt sie nach grüner CI per `gh pr merge`. Sperrpfad-PRs sichert in diesem Fenster der
Hash-Vergleich vor dem Commit, nicht das Skript. Option: Der Mensch mergt in dieser Zeit selbst,
das kostet ihn je PR einen Klick und braucht eine Ausnahme von „grün heißt mergen".

## Proben-Rahmen

- **Aufruf:** `claude -p "<Aktion>" --permission-mode dontAsk --output-format stream-json
  --verbose`, ausgewertet wird `permission_denials`.
- **Warum eine Allow-Zeile in die Probe gehört:** Unter `dontAsk` lehnt Claude Code jeden Aufruf
  ab, der sonst nachfragte. Ein Eintrag in `permission_denials` beweist also noch keine Deny-Regel.
  Die Probe setzt deshalb eine Allow-Zeile für den Probeaufruf in eine **Kopie** der Datei. Allow-
  und Deny-Listen werden zusammengeführt, und Deny gewinnt. Bleibt die Ablehnung, trägt sie das
  Deny. Der Diff zwischen Kopie und ausgeliefertem Stand belegt, was sich unterscheidet: die
  Allow-Zeilen und die entfernten Hooks.
- **Keine Hooks in den Deny-Proben**, weil ein Hook-Block die Probe überdecken könnte. Ob ein
  Hook-Block in `permission_denials` erscheint, ist nicht belegt.
- **Negativkontrolle ist der Mutant:** dieselbe Datei ohne die geprüfte Regel, in einem
  Wegwerf-Klon, derselbe Aufruf wird ausgeführt.
- **Kein Eintrag und kein Ergebnis heißt unentschieden**, nicht bestanden.
- **Proben laufen in einem Wegwerf-Klon von `origin/main`**, nicht in einem fremden Arbeitsbaum:
  `claude -p` führt die Projekt-Hooks des Klons mit den Rechten des Menschen aus. **Nicht mit
  `--bare`:** Dort laufen keine Hooks, und die Proben LP-1 (P1b), LP-3, LP-4 und LP-8 hätten keine
  Aussage. Ob `--bare` für Evals taugt, ist offen.
- **Kosten:** In der Quelle sind es 23 `claude -p`-Läufe je Durchgang. Sie starten auf Ansage
  des Menschen, wie die Evals. Die Rückschau wiederholt sie nach Änderungen an E1 und bei einer
  neuen Claude-Code-Version.
- **Laufumgebung:** Die Proben laufen in der Umgebung, in der die Bau-Session läuft. Wechselt die
  Umgebung, laufen sie neu.

## Arbeitskopie-Abgleich vor dem Merge

G-4 schützt den Commit-Weg, nicht die laufende Session. Deshalb prüft das Merge-Skript vor dem
Merge **jeden Eintrag von `git worktree list`**:

1. `git diff --name-only origin/main -- <Sperrpfade>` ist leer.
2. `git ls-files --others -- .claude/agents .claude/hooks .claude/skills` ist leer. Ohne
   `--exclude-standard` sind darin auch ignorierte Dateien enthalten.
3. Außer der Positivliste (`.claude/settings.local.json`) liegt keine ungetrackte
   `.claude/settings*.json` vor.
4. `grep -l disableAllHooks` über alle `.claude/settings*.json` ist leer, auch in
   `settings.local.json`.

Python-Bytecode (`__pycache__/`) unter den Sperrpfaden ist **nicht** ausgenommen: Eine `.pyc` mit
passendem Kopf ersetzt beim Import die Quelle und änderte den Prüfer, ohne dass eine getrackte
Datei abweicht. Deshalb laufen Hooks mit `python -B` (LP-8). Ein fehlender
Worktree-Ordner macht den Abgleich rot, bis `git worktree prune` läuft. **Handgriff nach einem
signierten Commit des Menschen an den Sperrpfaden:** Jeder Worktree und der Haupt-Checkout ziehen
`origin/main` nach, sonst ist der Abgleich dort rot.

Ein pauschales `git status --porcelain --ignored -- .claude` taugt nicht, weil es die Dauerdateien
(Übergabe, `settings.local.json`, Audit-Log, `worktrees/`) jedes Mal listet. **Grenze:** Eine
Änderung, die vor dem Merge zurückgenommen wird, bleibt unbemerkt. Dafür steht die Transkript-Maske
(E4).

## Laufumgebung: mit Sandbox

**Empfehlung, entschieden in der Quelle:** Eine Bau-Session, die ohne Rückfrage arbeitet, läuft in
einer Umgebung **mit Sandbox**, unter Windows also in WSL2. Grund: Unter nativem Windows läuft die
Shell ohne Sandbox, und ein Bash-Deny greift nicht über `sh -c` oder absolute Pfade. Mit Sandbox
schreibt ein Shell-Befehl nur im Arbeitsverzeichnis und im Temp-Verzeichnis. Nachbar-Repos (LP-4)
sind dann auch per Shell nicht beschreibbar, sofern sie nicht als zusätzliches Verzeichnis
eingetragen sind.

**Vorher eine Probe** mit vier Punkten: Docker im Sandbox-Lauf, Ladeweg einer übergeordneten
`CLAUDE.md`, `gh`-Login, Startweg der Session. Scheitert die Probe, wird neu entschieden.

**Grenzen:** Die Doku nennt die Sandbox keine vollständige Grenze. Hooks, MCP und Datei-Werkzeuge
laufen außerhalb, und `excludedCommands` laufen ohne Einschränkung. Die Pfadform der Regeln und die
Proben P2a, P2c und LP-4 hängen an der gewählten Umgebung.

## Aufbewahrung und Env-Scrub

`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` ist gesetzt, die Transkript-Frist bleibt beim Standard von
30 Tagen. Die Prävention trägt LP-7 (a), und eine kürzere Frist verkleinert das Fenster, in dem
die Rückschau Transkripte lesen kann. Welche Variablen der Scrub entfernt, ist nicht belegt. P7
misst es.

## Regeldateien als Sperrpfad

Die Wurzel-`CLAUDE.md` und eine Regeldatei des Repos wirken wie Agent-Dateien sofort auf jede
Session. Der Classifier liest die Projekt-`CLAUDE.md` mit. **Empfehlung, entschieden in der
Quelle:** Sie werden Sperrpfad, **sobald ihr Ort mit der Definition of Done feststeht**, per
Nachtrag zur Entscheidung über die Sperrpfade, nicht still. Danach gilt für sie dasselbe wie für
`.claude/**`: Ein PR daran ist rot, und es ändert sie nur ein signierter Commit des Menschen.
**Gegenposition:** Die `CLAUDE.md` ändert sich im Bau häufiger, und jeder signierte Commit ist ein
Engpass beim Menschen. **Option:** Werkstatt-PR mit Abweichungseintrag und Gate-Urteil, das ist
dann Selbstauskunft.

## Filtersatz

Vorschläge, Schutzregeln für die Bau-Session im Repo abzulegen oder sie ohne Sandbox und ohne
Rückfrage arbeiten zu lassen, prallen ab. **Neu aufzumachen**, wenn die Sandbox-Probe scheitert
oder eine Sandbox für die bisher ungeschützte Umgebung verfügbar wird.

## Offen

Fragen, die die Quelle am 02.10.2026 an ihre Doku-Recherche zurückgegeben hat. Bis zur Antwort
gelten sie als offen:

1. Ort und Schreibrecht der Managed-Datei je Betriebssystem. Nimmt eine Desktop-Sitzung
   `--settings` an? Lässt sich ein Benutzer-Deny anders als über den Pfad auf ein Projekt begrenzen?
2. Wirkt `disableAllHooks` auf Frontmatter-Hooks von Agents? Gilt Lesart L (P3b)? Verhindert Exit 2
   eines `ConfigChange`-Hooks die Änderung? Was bewirken Exit 1 und ein Absturz eines
   `PreToolUse`-Hooks?
3. Wie sieht eine Block-Zeile im Debug-Log aus, und wie die Ablehnung im Transkript? Das ist die
   Voraussetzung der Maske in E4 und LP-6.
4. Gibt es in der Sandbox eine Schreibsperre für Pfade im Arbeitsverzeichnis? Welche
   Variablennamen entfernt der Env-Scrub?
5. Laufen Projekt-Hooks unter `claude -p`, und gilt eine `-p`-Sitzung als vertraut? Die
   Doku-Lage ist widersprüchlich.
6. Deckt ein absolutes Deny-Muster mit `**/` Worktrees (P2b)? Woran ist ein Subagent mit
   `isolation: worktree` verankert?
