# Prinzip, Rollen und der Weg einer Änderung

> Erklärung zum Wiederverwenden. Wer die Werkstatt in einem neuen Projekt aufsetzt, liest diese
> Datei zuerst.

## Herkunft

Das Muster stammt aus dem Werkstatt-Plan eines Neubaus (Atemluft V2), entschieden in ENT-190,
ENT-201 und ENT-202 mit ihren Nachträgen, Stand 01.10.2026. Leitplanken, Sicherheitskatalog und
Isolation kamen mit ENT-203 P4, ENT-206 und dem Vierten Nachtrag zu ENT-202 dazu, Stand
02.10.2026 (Teilblock 100-4). Dort hat der Mensch festgelegt, dass
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
| **Umsetzer** | Baut, bis die Tests des Test-Autors grün sind; ruft `/simplify` und `/security-review`; öffnet den PR | `sonnet` / `high` | Read, Write, Edit, Grep, Glob, Bash, Skill, Agent — `Skill` darf nicht fehlen, `Agent` startet die Review-Agents von `/simplify` | keine (sieht den Feature-Branch) | — | `PostToolUse` auf `Skill` protokolliert, `Stop` verweigert bei falscher Reihenfolge |
| **Test-Autor** | Schreibt die Tests zum Abnahmekriterium **vor** dem Bau, gegen die Schnittstelle, mit Mutationsprobe | `sonnet` / `high` | Read, Grep, Glob, Edit, Write, Bash | `worktree` ohne `baseRef: head` — sieht den Feature-Diff nicht | `test-qualitaet` | `Stop`: Abgabe nur im Testverzeichnis |
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
Test-Autor → Umsetzer → commit → /simplify → Tests → /security-review → Wächter
  → Push, PR → Gate (Kopf-SHA) → CI → Merge-Skript → Staging
                                                      Prod: nur der Mensch
```

1. **Test-Autor** schreibt die Tests zum Abnahmekriterium im eigenen Worktree. Sie sind rot,
   solange das Feature fehlt — gewollt.
2. **Umsetzer** baut, bis alle Tests grün sind.
3. **Committen.** `/simplify` ändert Dateien; der Commit ist der Rückweg.
4. **`/simplify`** einmal am Blockende, ohne Flag. Danach die Tests erneut grün.
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

Die Reihenfolge 3 bis 5 trägt kein Satz im Prompt, sondern ein Hook (`PostToolUse` protokolliert
jeden Skill-Aufruf mit Baum-Hash, `Stop` verweigert das Beenden bei falscher Reihenfolge). Der Hook
belegt den **Aufruf**, nicht die Wirkung. Das Gate prüft das Protokoll selbst nach, damit ein
übersprungener Hook auffällt.

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
| `CLAUDE.md` und Regeldatei als Sperrpfad | entschieden (Vierter Nachtrag zu ENT-202), wirksam nach der Definition of Done | [leitplanken.md](leitplanken.md) |

## Offen

Diese Teile hat die Quelle am 02.10.2026 noch nicht entschieden. Sie **folgen aus der Quelle
(Atemluft V2), noch offen**, und werden dann hier nachgezogen.

| Teil | Stand | Folgt aus |
| --- | --- | --- |
| Definition of Done (feste Liste je Änderung mit Nachweisweg), Git-Ablauf | offen | Quelle, Teilblock 100-5 |
| Ausformulierte Agent-Texte (Prompt der vier Rollen) | offen — die Vorlagen hier sind Gerüste mit dem belegten Frontmatter | Quelle, Teilblock 100-6 |
| Hook-Skripte der Umsetzer-Kette, des Gates und der Leitplanken | offen — Konvention LP-8 steht, Verfahren legt der Aufsetz-Block fest | Aufsetz-Block |
| Format der Gate-Marker | offen — die Vorlage enthält einen Vorschlag | Aufsetz-Block |
| Proben der Leitplanken und der Isolation (P3b, P2b, F-10, F-11 u. a.) und die Doku-Fragen dazu | offen — Ergebnisse entscheiden über Ebene und Pfadform | [leitplanken.md](leitplanken.md), [isolation.md](isolation.md) |
| Stufe 2 des Sicherheitskatalogs (Auswahl aus der CSV), Lizenzpflichten der CSV | offen | [asvs-baseline.md](asvs-baseline.md) |
| `maxTurns` für das Stopp-Veto | offen — ob es eine Hook-Schleife beendet, ist nicht geprüft | Aufsetz-Block |
| Übergabe der Testdateien aus dem Worktree des Test-Autors | offen — Probe | Aufsetz-Block |
