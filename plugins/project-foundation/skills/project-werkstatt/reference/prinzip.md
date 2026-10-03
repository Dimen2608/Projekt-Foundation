# Prinzip, Rollen und der Weg einer Änderung

> Erklärung zum Wiederverwenden. Wer die Werkstatt in einem neuen Projekt aufsetzt, liest diese
> Datei zuerst.

## Herkunft

Das Muster stammt aus dem Werkstatt-Plan eines Neubaus (Atemluft V2), entschieden in ENT-190,
ENT-201 und ENT-202 mit ihren Nachträgen, Stand 01.10.2026. Leitplanken, Sicherheitskatalog und
Isolation kamen mit ENT-203 P4, ENT-206 und dem Vierten Nachtrag zu ENT-202 dazu, Stand
02.10.2026 (Teilblock 100-4). Git-Ablauf, Definition of Done und Regeldateien kamen mit ENT-214,
die ausformulierten Vorlagen der Sperrpfade (Agents, Hook-Skripte, Skills mit Evals, Einstellungen,
Wurzel-`CLAUDE.md`, Regeldatei), der Gate-Marker v1, die Livegang-Liste und die Mutationsprobe nach
dem Bau mit ihren beiden Nachträgen dazu, Stand 03.10.2026 (Teilblöcke 100-5 und 100-6). Dort hat
der Mensch festgelegt, dass
die Bau-Session jeden grünen PR ohne Rückfrage mergt und die Prüfungen den ganzen Schutz tragen,
den vorher die Einzelfreigabe getragen hat. Das Vorgängerprojekt hatte 25 Agent-Rollen und 15
Skills; geblieben sind vier Rollen und vier Skills. Die Vorlagen hier sind entprojektiert und
tragen keinen Fachinhalt.

## Das Prinzip

**Wenige, unabhängige, blockierende Prüfungen statt vieler Berichts-Agents.**

1. **Unabhängigkeit vor Masse.** Eine Prüfung ist nur so viel wert wie ihr Abstand zum Prüfling.
   Das Gate hat den Code nicht gebaut, startet mit frischem Kontext und liest die Begründung des
   Umsetzers erst nach seinem Befund. Fünf Agents, die denselben Diff mit derselben Begründung
   lesen, sind eine Prüfung, nicht fünf. Dass das Gate in der Quelle Opus statt Sonnet nutzt, ist
   dort über die Regel „Prüfen eine Effort-Stufe höher" begründet, **nicht** als Unabhängigkeit;
   eine Gegenprüfung durch fremde Modelle hat die Quelle ausdrücklich abgelehnt.
2. **Blockierend oder gar nicht.** Ein Bericht, den niemand beachten muss, ist ein Nachweis ohne
   Wirkung. Jede Prüfung der Werkstatt hält den Merge an, oder sie hat einen benannten Leser, der
   ihn anhält (der Sicherheitsbericht hat das Gate als Leser).
3. **Jede Prüfung muss nachweisen, dass sie feuert.** Konfiguriert ist nicht geprüft. Zu jeder
   Prüfung gehört eine Probe, die sie absichtlich auslöst, und eine Negativkontrolle, die
   durchgeht. Ein Check, der null Einheiten geprüft hat, ist rot (Lebenszeichen).
4. **Kein Pflichtschritt in einem Skill.** Skills tragen Handwerk, das helfen kann. Was immer
   laufen muss, steht in einer Rolle oder einem Hook. Rollen, die einen Skill immer brauchen,
   laden ihn per `skills:` vor.
5. **Ein Bestandteil ohne benannten Fehler kommt nicht hinein.** Wer einen Pflichtschritt
   einführt, nennt den, den er ersetzt.

## Die vier Rollen

Die Bau-Session ist der Lead: Sie plant, schreibt den Auftrag und ruft die Rollen als Subagents
auf. Alle Rollen laufen mit dem Projekt-Repo als Arbeitsverzeichnis. Modell und Effort sind
**Vorschlag** aus der Quelle; sie stehen ausdrücklich im Frontmatter, weil eine Session ohne den
Menschen läuft und ein fehlender Wert sonst den der Session erbt.

| Rolle | Zweck | Modell / Effort | Werkzeugrechte | Isolation | Vorgeladen | Hooks |
| --- | --- | --- | --- | --- | --- | --- |
| **Umsetzer** | Baut, bis die Tests des Test-Autors grün sind; ruft `/simplify` und `/security-review`; öffnet den PR | `sonnet` / `high` | Read, Write, Edit, Grep, Glob, Bash, Skill, Agent — `Skill` darf nicht fehlen, `Agent` startet die Review-Agents von `/simplify` | keine (sieht den Feature-Branch) | — | `PostToolUse` und `PostToolUseFailure` auf `Skill\|Bash` protokollieren Skills, Testläufe und Mutationsproben; `Stop` verweigert bei falscher Reihenfolge oder fehlender Mutationsprobe |
| **Test-Autor** | Schreibt die Tests zum Abnahmekriterium **vor** dem Bau, gegen die Schnittstelle, mit Mutationsprobe; führt die Liste der Wachposten, deren Probe erst nach dem Bau geht | `sonnet` / `high` | Read, Grep, Glob, Edit, Write, Bash | `worktree` ohne `baseRef: head` — sieht den Feature-Diff nicht | `test-qualitaet` | `Stop`: Abgabe nur im Testverzeichnis |
| **Gate** | Urteilt zur PR-Kopf-SHA blockierend: Redundanz, tote Pfade, Abstraktionshöhe, Layer, Regelverstoß, Sicherheitsbericht | in der Quelle `claude-opus-5-5` / `high` (Prüfen eine Effort-Stufe höher) | Read, Grep, Glob, Bash (lesend, `gh pr view/diff/comment`) — kein Edit, Write, Agent | keine (muss den Endstand sehen) | `code-gutachten` | `Stop`: Arbeitsbaum unverändert, Urteil vollständig |
| **Rückschau** | Prüft periodisch, ob Gates noch feuern, ob Lockerungen begründet sind, ob abgelehnte PRs wiederkommen | in der Quelle `claude-opus-5-5` / `medium` | Read, Grep, Glob, Bash, Agent (Fan-out lesender Agents) | `worktree` (prüft `main`, Proben bleiben im Wegwerf-Baum) | — | keine |

Die Rückschau heißt in der Quelle nach ihrer Vorgänger-Rolle; hier ist sie neutral benannt. Sie
meldet nur und setzt nichts um — eine Sperre ist sie nicht. Ihr Takt (Vorschlag der Quelle): nach
jedem gemergten Werkstatt-PR mit Abweichungseintrag, am Ausgang jeder Phase, auf Zuruf.

**Warum `Bash` keine Schreibsperre ist:** Laut Doku ist die Werkzeugliste keine
Sicherheitsgrenze. Deshalb prüft beim Gate ein `Stop`-Hook, dass Arbeitsbaum und Index unverändert
sind. Ein Muster in `disallowedTools` wie `Bash(git push *)` entzieht laut Quelle das ganze
Werkzeug, nicht nur den Befehl; einzelne Befehle sperrt `permissions.deny`, und das setzt der
Mensch.

**Warum die Agents nicht ins Plugin gehören:** Plugin-Subagents ignorieren `hooks`. Die Skills
dürfen als Plugin verpackt werden (dann prüfbar mit `claude plugin validate --strict`), die Agents
bleiben Dateien unter `.claude/agents/`.

**Workspace-Trust:** Frontmatter-Hooks eines Projekt-Agents laufen nur nach Workspace-Trust für
genau diesen Ordner. Ob eine `claude -p`-Sitzung als vertraut gilt und Projekt-Hooks ausführt, ist
in der Doku-Lage widersprüchlich belegt ([leitplanken.md](leitplanken.md), Offen 5). Umsetzer und
Gate laufen deshalb als Subagent einer interaktiven Bau-Session, nicht aus einem Skript. Proben mit
`claude -p` laufen in einem Klon von `origin/main`, weil sie dessen Projekt-Hooks mit den Rechten
des Menschen ausführen könnten.

## Der Weg einer Änderung

```
Test-Autor → Umsetzer → commit → /simplify → Tests → Mutationsprobe → /security-review
  → Wächter → Push, PR → Gate (Kopf-SHA) → CI → Merge-Skript → Staging
                                                                Prod: nur der Mensch
```

1. **Test-Autor** schreibt die Tests zum Abnahmekriterium im eigenen Worktree. Sie sind rot,
   solange das Feature fehlt — gewollt. Wachposten, die es auf `main` noch nicht gibt, trägt er in
   `wachposten-offen.txt` ein; deren Mutationsprobe ist vor dem Bau nicht möglich.
2. **Umsetzer** baut, bis alle Tests grün sind.
3. **Committen.** `/simplify` ändert Dateien; der Commit ist der Rückweg.
4. **`/simplify`** einmal am Blockende, ohne Flag. Danach die Tests erneut grün, danach die
   **Mutationsprobe** je Eintrag der Liste im Produktcode: Mutant setzen, der Test wird mit
   `failure` rot, Mutant zurück. Das Protokoll hält je Fang den Mutanten-Baum fest; der Stop-Hook
   prüft, dass er sich außerhalb der Tests vom Endstand unterscheidet. Im Neubau ist das fast jeder
   Wachposten; ohne diesen Schritt fiele die Probe bis zu einem nächtlichen Mutationslauf still weg.
5. **`/security-review`** ohne Argument, Ergebnis als Bericht in eine Datei unter `.claude/run/`
   (gitignored). Jeder Befund wird behoben (dann ab 3 erneut) oder in einer Vermerkdatei mit
   „nicht zutreffend, weil …" markiert.
6. **Wächter lokal** als Vorwarnung — dieselbe Prüfung, die das Merge-Skript ausführt.
7. **Push, PR.** Behebt der PR einen Fehler eines schon gemergten PR, setzt der Umsetzer das Label
   `nacharbeit` und nennt den Verursacher.
8. **Gate** auf der Kopf-SHA. Erstes „nein": zurück zu 2, neue SHA, neues Urteil. Zweites „nein"
   im PR: rot, der PR bleibt ungemergt, die Bau-Session nimmt den nächsten unabhängigen Block.
9. **CI abwarten, Merge nur über das Merge-Skript.**
10. **Staging** automatisch aus `main`. **Prod** löst nur der Mensch aus.

Die Reihenfolge 3 bis 5 trägt kein Satz im Prompt, sondern ein Hook (`PostToolUse` und
`PostToolUseFailure` — ein roter Testlauf ist ein fehlgeschlagener Aufruf — protokollieren jeden
Skill-Aufruf, Testlauf und jede Mutationsprobe mit Baum-Hash, `Stop` verweigert das Beenden bei
falscher Reihenfolge). Der Hook belegt den **Aufruf**, nicht die Wirkung, und nicht die Echtheit
der Zeilen: `.claude/run/` ist für den Umsetzer per Bash beschreibbar. Netze: Das Gate prüft das
Protokoll selbst nach (Punkt 0), die CI fährt die volle Suite, die Rückschau sieht einen
Schreibbefehl auf das Protokoll im Transkript. Vorlagen: `templates/hooks/`.

`/simplify`, `/security-review`, Gate und Evals laufen **nie in der CI**: Sie sind nicht
deterministisch und kosten Kontingent des Menschen.

## Entschieden seit 0.8.0

| Teil | Stand | Wo |
| --- | --- | --- |
| Leitplanken: Schichtung, Freigabeliste, LP-1 bis LP-8, drei Stufen, Arbeitskopie-Abgleich, Laufumgebung mit Sandbox, Env-Scrub | entschieden (ENT-206 P1 bis P5) | [leitplanken.md](leitplanken.md), Vorlage `LEITPLANKEN.md` |
| ASVS-Level und Sicherheitskatalog: Level-Wahl mit L3-Inseln, Katalog- und Nachweisdatei, Prüfung SK-1 bis SK-5, Füllung in zwei Stufen | entschieden (ENT-206 P6 bis P8) | [asvs-baseline.md](asvs-baseline.md), Vorlagen unter `sicherheit/` und `skills/sicherheits-katalog.md` |
| Isolation je Session: Worktree-Pflicht, Container je Worktree, Slots, Zugangsdaten-Regeln | entschieden (ENT-206 P9 bis P11) | [isolation.md](isolation.md), Vorlage `dev-env.py` |
| Wer den ersten Stand der gesperrten Skills, Hook-Skripte und Hook-Verdrahtung schreibt | entschieden (ENT-203 P4): dasselbe Muster wie bei den Agents | [schutz-und-deploy.md](schutz-und-deploy.md) |
| Deny-Regel für `gh pr merge`: Ort und Wortlaut | entschieden: `--settings`-Datei, Stufe 3 | [leitplanken.md](leitplanken.md) |
| `CLAUDE.md` und Regeldatei als Sperrpfad | entschieden (Vierter Nachtrag zu ENT-202, ENT-214 P4 bis P6): mit ihnen **jeder Ladeweg** im Repo, Auto-Memory aus, übergeordnete `CLAUDE.md` ausgeschlossen; Regeldatei `.claude/rules/regeln.md` | [regeldateien.md](regeldateien.md), Vorlagen `wurzel-CLAUDE.md`, `rules/regeln.md`, `settings.json` |

## Entschieden seit 0.10.0

| Teil | Stand | Wo |
| --- | --- | --- |
| Git-Ablauf: acht Schritte, PR-Vorlage, kein Rebase eines gepushten Branches, Aufräumen per Repo-Einstellung | entschieden (ENT-214 P7) | [git-und-dod.md](git-und-dod.md) |
| Definition of Done D-1 bis D-10, Design-Gate mit Bildvergleich in zwei Stufen, Soll-Bilder und Token-Datei als Sperrpfad | entschieden (ENT-214 P1 bis P3); D-7 und D-8 projektabhängig | [git-und-dod.md](git-und-dod.md) |
| Release-Prüfung und Livegang-Liste vor dem ersten Prod-Deploy | angelegt in der Quelle (100-6) | [git-und-dod.md](git-und-dod.md), Vorlage `LIVEGANG.md` |
| Agent-Texte der vier Rollen | ausformuliert (100-6a) | `templates/agents/` |
| Hook-Skripte der Umsetzer-Kette, des Test-Autors und des Gates | geschrieben (100-6a, 100-6c), Konvention LP-8; ohne Modell geprobt, in der Quelle 37 Proben, hier 24 an der verallgemeinerten Fassung | `templates/hooks/` |
| Format der Gate-Marker | entschieden: v1 | [gruen-und-gate.md](gruen-und-gate.md), `gate.md`, `gate_stop.py`, `merge-gruen.py` |
| Skill-Vorlagen als Plugin mit sieben Auslöse-Evals | geschrieben (100-6b) | `templates/skills/`, [eingebaute-skills.md](eingebaute-skills.md) |
| Mutationsprobe neuer Wachposten | entschieden (Zweiter Nachtrag zu ENT-214 P2): der Umsetzer nach dem Bau, protokolliert, Stop-Hook prüft, Gate liest; Liste schreibt der Test-Autor | oben, Weg einer Änderung |
| Umfang der Vorlagen | entschieden (Zweiter Nachtrag zu ENT-214 P1 mit Berichtigung): je Vorlage ein eigener Rahmen, ein Skill höchstens 500 Zeilen; Plan und Vorlagen zusammen kürzer als die Spezifikation | — |

## Offen

Diese Teile hat die Quelle am 03.10.2026 noch nicht entschieden oder nicht gemessen. Sie werden
hier nachgezogen, sobald sie es sind.

| Teil | Stand | Folgt aus |
| --- | --- | --- |
| Hooks mit echtem Payload: mit und ohne Workspace-Trust, unter `claude -p`, mit Projekt-`disableAllHooks`; Name im Feld `skill`; `cwd` im Worktree-Subagent; roter Testlauf feuert `PostToolUseFailure` | offen — Proben | Aufsetz-Block |
| Sperr-Hooks der Leitplanken (LP-1 `sh -c`, LP-2 Shell, LP-4) | offen — Konvention LP-8 steht | Aufsetz-Block |
| Proben der Leitplanken und der Isolation (P3b, P2b, F-10, F-11 u. a.) und die Doku-Fragen dazu | offen — Ergebnisse entscheiden über Ebene und Pfadform | [leitplanken.md](leitplanken.md), [isolation.md](isolation.md) |
| Stufe 2 des Sicherheitskatalogs (Auswahl aus der CSV) | offen — eigener Teilblock nach Threat Model und Architektur | [asvs-baseline.md](asvs-baseline.md) |
| Lizenzpflichten der ASVS-CSV (CC BY-SA 4.0) | offen — rechtliche Frage | [asvs-baseline.md](asvs-baseline.md) |
| `maxTurns` für das Stopp-Veto | offen — Vorschlag der Quelle 200 (Umsetzer) und 60 (Gate); ob es eine Hook-Schleife beendet, ist nicht geprüft, deshalb nicht in den Vorlagen | Aufsetz-Block |
| Übergabe der Testdateien aus dem Worktree des Test-Autors | offen — Probe | Aufsetz-Block |
| Fixture je Eval-Fall, Eval-Baseline, Namensraum in `skills:` und `input_match` | offen — kommt mit der Baseline | Aufsetz-Block |
| Ob `claudeMdExcludes` eine Elterndatei auch unter WSL2 ausschließt | offen — Probe | Aufsetz-Block |
