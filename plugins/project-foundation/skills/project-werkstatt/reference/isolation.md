# Isolation je Session — Worktree, Dev-Datenbank, Dev-Server, Zugangsdaten

> Wer die Werkstatt aufsetzt, liest diese Datei in Schritt 2 (RAHMEN). Die Skizze zum Kopieren
> ist [templates/dev-env.py](../templates/dev-env.py).

## Herkunft

Werkstatt-Plan Atemluft V2, Teilblock 100-4 (A-18), entschieden mit ENT-206 Punkt 9 bis 11 am
02.10.2026. Ports, Namen und Zahlen sind **Vorschlag**. Belegt ist nur, was eine Probe zeigt.

## Zweck und Abgrenzung

Parallele Läufe sollen sich keinen Datenbank-, Port- oder Branch-Zustand kaputtmachen. „Parallel"
heißt: Test-Autor und Rückschau laufen in eigenen Worktrees neben dem Umsetzer, dazu ein zweiter
Block oder ein Mensch, der von Hand arbeitet.

| | Test-Datenbank der Gates | **Dev-Umgebung (diese Datei)** | Staging |
| --- | --- | --- | --- |
| Ort | CI-Runner | Rechner der Bau-Session: Haupt-Checkout und Worktrees | eigene Umgebung |
| Zeitpunkt | Testlauf im Gate | während der Session, vor dem Push | nach dem Merge, automatisch |
| Lebensdauer | je Lauf | je Worktree, also je Block | dauerhaft |
| Daten | Template-DB aus Migrationen | leer, Migrationen, synthetischer Seed | Test-Zugänge |
| Wirkung auf den Merge | ja, G-1 bis G-5 | **keine**: kein Gate liest die Dev-DB, ein grüner Lauf hier ersetzt keinen G-Punkt | keine |

**Gemeinsamer Grundsatz:** Tests laufen nie gegen einen geteilten Dev-Container oder einen
gemounteten Haupt-Checkout. Die Isolation hier trägt das auf die lokale Seite.

## Was sie verhindert

- **Grün für den falschen Code:** Ein geteilter Container mountet den Haupt-Checkout, der Test aus
  dem Worktree läuft gegen fremden Stand.
- **Kollision an Port und Image:** Ein Stack mit festen Host-Ports und ohne Compose-Projektnamen.
  Ein Build aus einem Worktree überschreibt das gemeinsame Image, zwei Läufe teilen eine `.env`.
- **Branch unter der Session gewechselt:** Zwei schreibende Läufe im selben Checkout.
- **Zugangsdaten im Worktree:** Eine `.worktreeinclude` kopiert ignorierte Dateien wie `.env` in
  neue Worktrees, und Transkripte speichern ausgegebene Werte im Klartext.

## Worktree-Pflicht

Entschieden in der Quelle:

- **Test-Autor und Rückschau laufen in einem eigenen Worktree.** Das ist gesetzt, weil der
  Test-Autor den Feature-Diff nicht sehen soll und die Rückschau ihre Proben in einem Wegwerf-Baum
  fährt.
- **Pflicht für jeden zweiten gleichzeitig schreibenden Lauf.**
- **Der Umsetzer bleibt im Haupt-Checkout, bis Probe F-8 grün ist.** `/security-review` liest
  Status und Diff aus dem Arbeitsverzeichnis. Ob es im Worktree den Worktree sieht, ist nicht
  gemessen.

**Gegenposition:** Pflicht für jeden Block. Damit wird „Branch unter dir gewechselt" unmöglich statt
nur gemeldet. Der Preis sind Aufräumfallen unter Windows und die offene Probe. **Option:** Pflicht
für jeden Block ab dem Tag, an dem F-8 grün ist.

## Isolationsschema

| Ressource | Trennung | Mechanismus | Probe |
| --- | --- | --- | --- |
| Arbeitskopie | eigener Ordner `.claude/worktrees/<kennung>/`, `.git` gemeinsam | `claude --worktree <kennung>`; Deny-Verankerung siehe [leitplanken.md](leitplanken.md) | F-7, F-10 |
| Branch | `worktree-<kennung>`; Basis ist der Default-Branch des Remotes, mit `worktree.baseRef: "head"` der lokale HEAD | Test-Autor und Rückschau **ohne** `baseRef: head` | F-7 |
| Dev-DB | **ein Datenbank-Container je Worktree**, eigenes Compose-Projekt, eigenes Volume, eigener DB-Name, Passwort je `up` | `dev_env up` | F-2, F-3 |
| Dev-Server, Port | Host-Ports aus dem Slot, gebunden an `127.0.0.1`. Dienste laufen als Container (`up -d`), nicht als Hintergrund-Bash, die mit der Session endet | Slot-Verzeichnis als Sperre | F-1, F-6 |
| Zugangsdaten | `.env.worktree` je Worktree, erzeugt von `dev_env`, gitignored | Regeln unten | F-4 |
| Gedächtnis, Freigaben | Auto Memory teilen alle Worktrees eines Repos; `CLAUDE.local.md` gilt nur im eigenen | Regeln unten | F-9, F-8 |
| Logs | je Compose-Projekt; `.claude/run/` gitignored | Zugangsdaten-Regel 5 | F-4 |

**Warum ein Container je Worktree und keine gemeinsame Instanz mit einer DB je Worktree**
(entschieden in der Quelle): Rollen, Extensions und Servereinstellungen sind Zustand des ganzen
Clusters. Hängt das Produkt an Rollen, Row-Level-Security oder Triggern, taugt Transaktions-Rollback
nicht, und `CREATE DATABASE … TEMPLATE` scheitert an offenen Verbindungen. **Gegenposition:** Eine
Instanz spart Container. RAM und Startzeit je Container sind nicht gemessen. **Option:** eigene
Instanz nur für Blöcke, die Rollen oder Policies ändern.

## Zuteilung (Vorschlag)

- **Kennung:** Name des Worktrees, Form `[a-z0-9-]{1,24}`, im Haupt-Checkout `main`. Gegen die
  Namensregeln von Compose prüfen.
- **Slot:** 10 Slots (0 bis 9). Gestartet wird bei Slot `hash(kennung) mod 10`, ist der belegt, wird
  der nächste freie genommen. Belegt heißt: `mkdir <git-common-dir>/devenv/slot-<n>` gelingt. Das
  Verzeichnis liegt im gemeinsamen Git-Verzeichnis und ist damit für alle Worktrees sichtbar. Darin
  stehen Kennung, Worktree-Pfad und Zeit. Vor dem Sperren prüft `up` alle Ports des Slots auf
  Bindbarkeit. Ist einer belegt, gilt der Slot als belegt. Ohne freien Slot endet `up` mit Exit ≠ 0.
- **Ports:** `{{PORT_BASIS}} + 10·Slot + Versatz` (0 Datenbank, 1 API, 2 Web, 3 und 4 Mail-Testdienst,
  5–9 Reserve), gebunden an `127.0.0.1`. Den Bereich wählt man **gemessen**: keine abhörenden Ports
  darin, keine reservierten Bereiche des Betriebssystems, unterhalb des dynamischen Bereichs. Die
  Messung wird am Aufsetz-Tag wiederholt.
- **Namen:** Compose-Projekt `{{PRAEFIX}}-<kennung>`, Datenbank `{{PRAEFIX}}_<kennung>` (`-` zu `_`),
  Container-Label `{{PRAEFIX}}-slot=<n>`.

## Lebenszyklus je Block

1. **Anlegen:** Zuerst `claude --worktree <kennung>`, dann `dev_env up` als **Schritt 0 des
   Umsetzers**. Der Ablauf von `up`: Kennung prüfen, Sweep, Slot und Ports sperren,
   Wegwerf-Passwort, `.env.worktree` schreiben, `docker compose -p <projekt> up -d --wait`,
   Migrationen und Seed. Scheitert ein Teilschritt, folgt `down` mit Exit ≠ 0. Scheitert auch der
   Abbau (etwa Docker steht), bleibt der Slot belegt und `status` zeigt ihn: Ein freier Slot mit
   laufenden Containern wäre eine Port-Kollision.
2. **Nutzen:** DB- und Server-Aufrufe lesen `.env.worktree`. Fehlt eine Variable, bricht der Lauf
   ab. **Es gibt keine Vorgabe** auf Standard-Ports (`${PORT:-5432}`). Nach einem Clear liest die
   Session `.env.worktree` und `dev_env status`, nicht das Gedächtnis.
3. **Aufräumen:** Nach dem Merge zuerst `dev_env down` (Container, Volume, Slot, `.env.worktree`),
   dann `git worktree remove`. Der Branch wird gelöscht, wenn der PR gemergt ist und nach dem Merge
   kein Commit folgte. **Sweep bei jedem `up`:**
   - **Waise:** Der Worktree-Pfad fehlt oder steht nicht mehr in `git worktree list --porcelain`.
     Dann wird der Slot abgebaut. Das deckt auch den Sweep von Claude Code, der Worktree-Ordner nach
     `cleanupPeriodDays` entfernt.
   - **Stehengeblieben:** `-p`-Läufe räumen ihren Worktree nicht auf. Ein Slot ohne Commit und ohne
     `dev_env`-Aufruf seit 7 Tagen wird abgebaut (die Zahl ist nicht gemessen). Worktree und Branch
     bleiben stehen, weil dort Arbeit liegen kann. `status` meldet sie als „ohne Slot“. Jeder
     `dev_env`-Aufruf zählt als Aktivität.
4. **Nichts geht verloren:** Die Dev-DB entsteht aus Migrationen und Seed neu. Was nur dort
   stünde, wäre ein Fehler.

**Anlage per `WorktreeCreate`-Hook statt `dev_env up`:** Der Hook ersetzt die git-Anlage ganz,
dann wird auch `.worktreeinclude` nicht verarbeitet. Aber er bekommt kein `baseRef` mit, räumt nur
mit eigenem `WorktreeRemove`, und ob er bei `EnterWorktree` feuert, ist nicht dokumentiert (F-11).
Darum ist `dev_env up` als ausdrücklicher Schritt die Empfehlung, denn dort fällt sein Fehlen an F-3
auf.

## Zugangsdaten in Dev-Umgebungen

1. **Nur Wegwerf-Zugänge.** Das DB-Passwort entsteht zufällig bei `up`, gilt für einen Container
   an `127.0.0.1` und endet mit `down`. Zugänge des Betriebs (Prod, Staging) und Zugangsdaten von
   Kunden gehören nicht hinein. Dienste mit Außenwirkung laufen als Test-Double oder im Testmodus,
   wie bei Staging.
2. **Die Dev-DB startet leer**, danach kommen Migrationen und ein synthetischer Seed. Ein Dump von
   Prod oder Staging im Worktree ist untersagt, weil ein Dev-Lauf PR-Code ausführt.
3. **Die Dev-Compose-Datei nennt nur Variablen aus `.env.worktree`.** Variablen des Betriebs kommen
   darin nicht vor, damit die Umgebung des Aufrufers nicht in die Container fließt.
4. **Keine `.worktreeinclude`, die `.env*` nennt.** `.env.worktree` entsteht nur durch
   `dev_env up`. Ein Wächter-Eintrag macht eine solche Datei rot, ohne ihn ist die Regel nur
   Disziplin.
5. **Fehler- und SQL-Logs ohne Parameterwerte** (etwa Postgres `log_error_verbosity=terse`, ORM
   mit ausgeblendeten Parametern). Ein Wegwerf-Passwort, das ins Transkript geraten ist, ist nach
   `down` wertlos. Das ist die Antwort auf die fehlende Maskierung lokaler Transkripte.

**Restgrenze:** Zugangsdaten in der Shell-Umgebung des Menschen werden an Subprozesse der Session
vererbt. Der Env-Scrub fängt nur bekannte Muster. Das gehört zu den Leitplanken (LP-7).

## Gedächtnis, Freigaben, Sandbox

- **Gedächtnis:** Ein Port, Slot oder DB-Name im Auto Memory ist für den parallelen Lauf lesbar und
  falsch, Lauf B schriebe dann in die Datenbank von A. **Regel:** Koordinaten stehen in
  `.env.worktree` und in `dev_env status`, nicht im Gedächtnis. Notizen, die nur einem Worktree
  gehören, kommen in `CLAUDE.local.md`. Das ist Disziplin, F-9 misst sie.
- **Freigaben:** Ein neuer Worktree beginnt ohne geklickte Freigaben. Ein Lauf ohne den Menschen
  steht dann an der Rückfrage oder wird unter `dontAsk` abgelehnt, das ist sichtbar, nicht still.
  Regeln, auf die die Bau-Session angewiesen ist, gehören in die Benutzer-Einstellungen oder die
  `--settings`-Datei des Menschen.
- **Sandbox:** Die Ressourcen-Trennung (DB, Port, Volume) beruht auf Compose-Projekt und Slot, nicht
  auf der Sandbox. Für den Schreibschutz zwischen Worktrees zählt die Sandbox. Ohne sie schützt die
  Isolation vor Versehen, nicht vor einem fehlgeleiteten Lauf: Wer `docker compose` ausführen darf,
  wählt Projektname und Mounts selbst.

## `dev_env` liegt nicht auf einem Sperrpfad

Entschieden in der Quelle: Das Skript liegt an einem normalen Pfad und ändert sich über G-1 bis
G-8. Kein Gate liest die Dev-DB, ein geschwächtes Skript gefährdet also den Merge nicht. Die
Rückschau wiederholt F-1 bis F-9 gegen `main`. **Gegenposition:** Die Zugangsdaten-Regeln halten
nur, wenn das Skript sie nicht lockern kann. **Option:** unter `.claude/hooks/` und damit gesperrt.

## Feuert-Nachweis (Aufsetz-Block)

Zwei Worktrees A und B, zwei Prozesse gleichzeitig. Je Probe ein Mutant, der die geprüfte
Bedingung entfernt. Bleibt er grün, ist die Probe blind.

| # | Probe | Erwartung | Mutant |
| --- | --- | --- | --- |
| F-1 | A und B starten `dev_env up` gleichzeitig | zwei Slots, zwei DB-Ports im Bereich, beide bereit, Bindung an `127.0.0.1` | fester Slot 0 → zweiter `up` scheitert oder beide teilen den Slot |
| F-2 | A legt eine Zeile an und wendet eine Wegwerf-Migration an, B liest | B sieht weder Zeile noch Migration | A und B mit derselben `DATABASE_URL` → B sieht die Zeile |
| F-3 | `.env.worktree` entfernen, Compose und App starten | Abbruch mit Meldung, kein Start auf einem Standard-Port | Vorgabe `${…:-5432}` eingebaut → Start auf dem Standard-Port |
| F-4 | Köder `DEV_CANARY_<zufall>` in Basis-Umgebung und `.env` des Haupt-Checkouts; Worktree anlegen, `up`; Maske über Worktree-Ordner, `docker inspect` und Debug-Log | 0 Treffer; Positivkontrolle: Köder im Haupt-Checkout gefunden | `.worktreeinclude` mit `.env*` → Köder im Worktree |
| F-5 | `dev_env down` | 0 Container und 0 Volumes (Label-Filter), Slot-Verzeichnis weg, Ports frei | `git worktree remove` ohne `down` → Reste |
| F-6 | Worktree-Ordner von Hand löschen, `git worktree prune`, `up` in B; dann 11 Kennungen gleichzeitig | Sweep baut den verwaisten Slot ab; der 11. `up` endet mit „keine freien Slots" | Sweep entfernt → Slot bleibt; 11. Kennung teilt einen Slot |
| F-7 | Commit in A; Anlegen und Entfernen eines Agents mit `isolation: worktree` | `HEAD` von B unverändert, `git config --show-origin core.hooksPath` unverändert | `core.hooksPath` von Hand auf einen absoluten Pfad → gemeldet |
| F-8 | Gestagte Command Injection im Worktree, `/security-review` aus einem Subagent mit dem Worktree als Arbeitsverzeichnis | Befund gemeldet | Injection nur im Haupt-Checkout → kein Befund (das Verzeichnis zählt) |
| F-9 | Nach einem Lauf: Maske über das Memory-Verzeichnis auf Ports, DB-Namen und Werte aus `.env.worktree` | 0 Treffer | Port von Hand in eine Memory-Datei → ≥ 1 |
| F-10 | Deny auf `.claude/agents/**` in der gewählten Form; Edit (a) in der Worktree-Session auf den Worktree, (b) aus dem Haupt-Checkout auf `.claude/worktrees/<name>/.claude/agents/x.md` | (a) abgelehnt; (b) Ergebnis festhalten, die Doku sagt es nicht | Regel ohne Verankerung in Benutzer-Einstellungen → (a) nicht abgelehnt |
| F-11 | Wegwerf-Repo mit `WorktreeCreate`-Hook, der jeden Aufruf protokolliert, und `.worktreeinclude` mit Köder; Worktree per `EnterWorktree` | Eintrag ja oder nein, Köder kopiert ja oder nein, beides festhalten | Positivkontrolle: `claude --worktree` schreibt einen Eintrag |

## Offen

- RAM und Startzeit je Slot, Zustand des Docker-Daemons: nicht gemessen.
- Ein Slot „in Anlage“ (Verzeichnis ohne `info.json`, etwa nach einem Absturz zwischen beiden
  Schritten) räumt der Sweep nicht, damit er keinen parallelen `up` trifft. Er bleibt in `status`
  sichtbar und wird von Hand entfernt.
- Ob ein Deny des Haupt-Checkouts den Worktree von außen deckt (F-10 b), ob `WorktreeCreate` bei
  `EnterWorktree` feuert (F-11), ob der Sweep von Claude Code `WorktreeRemove` auslöst: Proben.
- Wie zwei gleichzeitige Läufe in dasselbe Auto Memory schreiben: nicht belegt.
- Ob ein Worktree ein eigenes Transkript-Verzeichnis unter `~/.claude/projects/` hat: nicht
  belegt.
