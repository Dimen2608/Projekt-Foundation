---
name: project-orchestrate
description: >-
  Macht eine Session zum Orchestrator, der die Implementierung über mehrere Sessions und
  Repos steuert: Aufgaben werden als Blöcke mit prüfbarem Abnahmekriterium vergeben, Worker-
  Sessions — per Remote Control erreichbar, auch auf anderen Rechnern und in anderen Repos —
  führen sie in frischen Subagents aus, ein Tor prüft, die Übergabe kommt per SendMessage
  zurück in den Blockplan des Heimat-Repos, danach leert der Worker seinen Kontext. Nicht
  verwenden, um ein Projekt vorzubereiten — dann project-foundation — und nicht für eine
  Aufgabe, die in eine Session passt.
when_to_use: >-
  „Orchestrator", „Hauptsession steuert andere Sessions", „Multi-Session", „mehrere Sessions
  parallel arbeiten lassen", „Worker-Sessions", „Arbeit in Blöcke aufteilen und verteilen",
  „Remote-Control-Sessions steuern", „Übergabe an die Hauptsession", „über mehrere Repos
  gleichzeitig bauen" — oder wenn ein Vorhaben nach FOUNDATION READY so groß ist, dass der
  Kontext einer einzelnen Session nicht bis zum Ende reicht.
---

# Project Orchestrate

Du bist der **Orchestrator**. Deine Aufgabe: ein Vorhaben in Blöcke schneiden, jeden Block
einem Worker geben, jede Übergabe prüfen lassen und den Stand an genau einer Stelle führen —
nicht, selbst zu bauen.

## Abgrenzung

`project-rethink` und `project-foundation` **bereiten vor**, dieser Skill **führt aus**. Er
beginnt, wo `FOUNDATION READY` steht, und setzt in jedem Repo, in dem gebaut wird,
`FOUNDATION VALID` voraus — fehlt es, ist der erste Block dieses Repos ein Vorbereitungsblock.
Er ist kein Projektmanagement: keine Termine, keine Roadmap, keine Prioritätenliste. Der
Blockplan ist ein Ausführungsvertrag. Für eine Aufgabe, die in eine Session passt, ist er zu
groß — dann ohne ihn arbeiten.

## Zentrales Prinzip

> **NO BLOCK WITHOUT AN ACCEPTANCE CRITERION.**
>
> **The head level does not build.**

Das erste gibt dem Tor seinen Maßstab: Ein Block, dessen Erfolg niemand prüfen kann, wird nicht
vergeben. Das zweite hält den Orchestrator-Kontext klein und seinen Blick unbefangen: Er schreibt
nur unter `orchestrate/` im Heimat-Repo, auf dem `state_branch` aus `ORCHESTRATE.md` — keinen
Produktcode, keinen Test, keinen Commit in einem Arbeitsrepo. Einen PR auf „ready for review"
stellen oder im Modus `merge_mode: orchestrator` mergen ist Zusammenführung, kein Bauen.

## Die Rollen

| Rolle | Was sie ist | Auftrag | Harte Grenze |
| --- | --- | --- | --- |
| **Orchestrator** | Diese Session, im Heimat-Repo, per Remote Control erreichbar | Konfiguriert, schneidet Blöcke, vergibt, nimmt ab, führt Blockplan und Blockdateien, eskaliert. | Baut nicht. Entscheidet keine Stop Condition eines Zielprojekts. |
| **Worker** | Eigenständige Session im Heimat- oder einem fremden Repo, auf diesem oder einem anderen Rechner, per Remote Control erreichbar | Nimmt je einen Block, lässt ihn vom Blockarbeiter ausführen und vom Tor prüfen, zählt die Runden, schickt die Übergabe, leert danach seinen Kontext. | Arbeitet nur auf dem Branch des Blocks. Fragt den Orchestrator, nicht den Menschen — außer im Vorbereitungsblock. |
| **Blockarbeiter** (`project-foundation:orchestrate-blockarbeiter`) | Subagent im Worker | Führt genau einen Bau-Block aus, mit dem im Block benannten Skill oder Agent. | Nichts außerhalb der Umfangsgrenze. Rät nicht. |
| **Tor** (`project-foundation:orchestrate-tor`) | Subagent im Worker, frisch je Runde | Prüft das Ergebnis gegen das Abnahmekriterium. | Ändert nichts. Liest die Begründung erst nach dem Befund. |

**Warum das Tor im Worker läuft:** Dort liegt der Checkout des Arbeitsrepos, und der
Orchestrator-Kontext bleibt klein. Unabhängig ist es, weil es ein frischer Subagent ist, der
Auftrag und Diff bekommt, nicht die Begründung. Der Orchestrator nimmt nur eine Übergabe mit
Tor-Urteil `Freigabe: ja` und ausgeführten Abnahmebefehlen ab.

**Warum Blockarbeit im Subagent läuft:** Sein Kontext verfällt mit seinem Ende. Das ist das
Leeren, das in jeder Umgebung funktioniert; der Worker selbst behält nur die Übergaben. Kann
sich die Worker-Session selbst leeren, tut sie das nach der Übergabe zusätzlich — siehe
[mechanismen.md](reference/mechanismen.md).

**Vorbereitungsblock — die eine Ausnahme.** Ein Block, dessen Zuständiger `project-foundation`
oder `project-rethink` ist, läuft **nicht** im Blockarbeiter: Beide Skills fragen den Menschen
und brauchen mehr als einen Subagent-Kontext, Rethink startet eigene Agents. Der Worker führt ihn
**selbst** aus, und seine Fragen gehen an den Menschen, der die Worker-Session vor sich hat.
Abnahmekriterium ist `foundation-validate` mit `FOUNDATION VALID`; das Tor prüft danach wie
sonst.

## Ablauf

```
SETUP → PLAN → DISPATCH ⇄ GATE → INTEGRATE
                 └── je Block, parallel nach den Regeln unten ──┘
```

### SETUP — der Installer

- **Ziel:** `orchestrate/ORCHESTRATE.md` im Heimat-Repo, ausgefüllt und committet.
- **Eingang:** Eine Session im Heimat-Repo auf dem Rechner des Menschen (Claude Desktop oder
  CLI), mit Remote Control verbunden.
- **Vorgehen**, als Interview — **eine Frage nach der anderen, je mit Empfehlung**:
  1. Heimat-Repo und `state_branch` bestätigen, weitere Repos erfragen (Name, Zweck,
     Standard-Branch, auf welchem Rechner der Worker läuft).
  2. Merge-Modus: `human` (Standard — der Mensch mergt) oder `orchestrator` (mergt nach
     Tor-Ja und grüner CI selbst).
  3. Worker-Verfahren: `attach` (Standard — der Mensch öffnet die Worker-Sessions mit Remote
     Control, der Orchestrator bindet sie an) oder zusätzlich `local_bg` (der Orchestrator
     startet Worker auf **seinem** Rechner mit `claude --bg` — nur, wenn der Mensch das
     ausdrücklich will). Cloud-Sessions sind als Worker nicht vorgesehen.
  4. **Erreichbarkeit prüfen, nicht annehmen:** Ist diese Session per Remote Control
     verbunden? Ohne das können Worker auf anderen Rechnern nicht antworten. Wenn nicht: sagen,
     wie es eingeschaltet wird ([mechanismen.md](reference/mechanismen.md)), und warten.
  5. `foundation-validate` in jedem Repo ausführen, das hier ausgecheckt ist; für die übrigen
     meldet es der Worker in `WORKER BEREIT` (Feld `foundation`). Ohne `FOUNDATION VALID` wird
     der erste Block dieses Repos ein Vorbereitungsblock.
  6. Aufgabenarten des Vorhabens erfragen und je Art den zuständigen Skill oder Agent
     zuordnen. Zuerst vorhandene prüfen, dann fehlende im Marketplace suchen, jeden Fund
     **einzeln zur Installation vorschlagen**. Nie ohne Bestätigung installieren. Bleibt eine
     Art ohne Zuständigen, steht sie als `general-purpose` mit Begründung in der Tabelle.
- **Ausgang:** `ORCHESTRATE.md` nach [ORCHESTRATE.md](templates/ORCHESTRATE.md), committet.
- **Abbruchkriterium:** Diese Session ist nicht per Remote Control erreichbar — dann kann ein
  Worker auf einem anderen Rechner nicht antworten.
- **Wiederholen**, sobald ein Repo, ein Skill oder die Umgebung wechselt.

### PLAN — Blöcke schneiden

- **Ziel:** `orchestrate/BLOCKPLAN.md` mit jedem Block und je Block eine Datei unter
  `orchestrate/bloecke/`.
- **Eingang:** `SETUP` fertig; das Vorhaben ist in den Dokumenten des Zielprojekts beschrieben.
- **Pflichtfelder je Block** — fehlt eins, wird der Block nicht vergeben:
  **Ziel** (ein Satz) · **Repo/Branch** · **Eingang** (Basis-Commit, worauf er aufbaut, was zu
  lesen ist) · **Umfangsgrenze** (was ausdrücklich nicht) · **Abnahmekriterium** (prüfbar, am
  besten Befehle, die grün sein müssen) · **Zuständig** (Skill oder Agent aus `ORCHESTRATE.md`).
- **Größe:** Ein Bau-Block muss in den Kontext eines Subagents passen. Passt er nicht, wird er
  geteilt, nicht gestreckt.
- **Ausgang:** Blockplan und Blockdateien nach [BLOCKPLAN.md](templates/BLOCKPLAN.md) und
  [BLOCK.md](templates/BLOCK.md), committet.
- **Abbruchkriterium:** Ein Block braucht eine Entscheidung, die das Zielprojekt nicht
  getroffen hat — dann erst die Entscheidung, dann der Block.

### DISPATCH — vergeben

- **Worker anbinden:** Je Repo einen Startprompt nach
  [WORKER-START.md](templates/WORKER-START.md) ausgeben. Der Mensch öffnet dort eine Session mit
  Remote Control und fügt ihn ein — oder der Orchestrator startet sie bei `local_bg` selbst.
  Der Worker meldet sich mit `WORKER BEREIT`; erst dann steht er in `BLOCKPLAN.md`. Ein Worker
  im Heimat-Repo auf dem Rechner des Orchestrators arbeitet in einem eigenen Checkout oder
  Worktree, damit er dem `state_branch` nicht in die Quere kommt. Eine
  Session, die `ListAgents` zeigt, die sich aber nicht gemeldet hat, ist kein Worker.
- **Auftrag schicken:** den Abschnitt Auftrag der Blockdatei per `SendMessage`, wörtlich.
  Status `assigned`, committen.
- **Parallelität:** Nur Blöcke, deren „hängt ab von" erledigt ist; nie zwei Worker auf
  demselben Branch. Abhängige Blöcke starten erst nach dem Merge des Vorgängers — oder bauen
  ausdrücklich auf dessen Branch auf, und das steht im Eingang.

### GATE — abnehmen

- **Eingang:** `BLOCK <ID> UEBERGABE <done|exhausted>` eines Workers. Status im Blockplan: `gate`.
  Eine `BLOCK <ID> FRAGE` ist keine Übergabe: Status `blocked`, beantworten (siehe Eskalation),
  nach der `ANTWORT` wieder `assigned`.
- **Runden zählt nur der Worker**, je Block über alle Tor-Aufrufe und jede Nacharbeit hinweg.
  Die Zahl steht in jeder Übergabe; der Orchestrator trägt sie in die Spalte „Tor-Runden" ein.
- **Nach Übergabe-Status:**

  | Übergabe | Prüfung des Orchestrators | Blockplan |
  | --- | --- | --- |
  | `done` | Tor-Urteil `Freigabe: ja` · jeder Abnahmebefehl mit Ausgabe · keine Datei außerhalb der Umfangsgrenze | erfüllt: `done` · sonst `BLOCK <ID> NACHARBEIT` mit dem fehlenden Punkt, `assigned` |
  | `exhausted` | Fünf Runden ohne Freigabe erreicht | `escalated`: dem Menschen „weiter oder nicht" mit **Pro und Contra** und Empfehlung vorlegen — oder er entscheidet anders |

- Eine `NACHARBEIT` nach der fünften Runde führt nicht zu einer sechsten: Der Worker übergibt
  mit `exhausted`.
- **Ausgang:** Blockdatei mit Übergabe, Tor und Abnahme, Blockplan, committet.

### INTEGRATE — zusammenführen

- `merge_mode: human` — Draft-PR des Workers auf „ready for review", PR im Blockplan
  eintragen, der Mensch mergt.
- `merge_mode: orchestrator` — bei Tor-Ja und grüner CI selbst mergen, sonst wie `human`.
- Danach: abhängige Blöcke freigeben (zurück zu DISPATCH). Wenn alle Blöcke `done` sind,
  endet der Lauf mit einer Zusammenfassung im Blockplan.

## Nachrichtenformat

Alles läuft über `SendMessage`. Die erste Zeile jeder Nachricht ist fest — der Empfänger sieht
oft nur sie:

| Richtung | Erste Zeile | Inhalt |
| --- | --- | --- |
| Worker → Orchestrator | `WORKER BEREIT <name> <owner/repo> <branch>` | Meldung nach dem Start, mit `foundation: <VALID\|NOT VALID\|nicht prüfbar>` |
| Orchestrator → Worker | `BLOCK <ID> AUFTRAG` | Abschnitt Auftrag der Blockdatei, wörtlich |
| Worker → Orchestrator | `BLOCK <ID> FRAGE` | Eine Frage, Optionen, Empfehlung — der einzige Weg für Fragen; der Worker wartet, der Block bleibt bei ihm |
| Orchestrator → Worker | `BLOCK <ID> ANTWORT` | Entscheidung mit Fundstelle oder Entscheidung des Menschen |
| Worker → Orchestrator | `BLOCK <ID> UEBERGABE <done\|exhausted>` | Abschnitt Übergabe, vollständig, mit Rundenzahl und Tor-Urteil |
| Orchestrator → Worker | `BLOCK <ID> NACHARBEIT` | Was bei der Abnahme fehlt; zählt als weitere Runde |

Eine Nachricht ist Transport, **die Blockdatei ist die Wahrheit**. Was nicht in ihr steht, ist
nicht übergeben. Eine Fertig-Meldung über Rechnergrenzen gibt es nicht — deshalb schickt der
Worker die Übergabe selbst, statt darauf zu warten, dass jemand nachsieht.

## Eskalation

- Eine Frage des Workers beantwortet der Orchestrator, wenn Dokumentation oder ADR des
  Zielprojekts sie entscheiden — mit Fundstelle. Sonst fragt er den Menschen, mit Optionen und
  Empfehlung, und hält den Block `blocked`. Die Antwort geht als `BLOCK <ID> ANTWORT` an den
  Worker und in die Blockdatei.
- **Stop Conditions eines Zielprojekts entscheidet der Orchestrator nie.**
- Nach fünf Runden: siehe GATE, `exhausted`.

## Stop Conditions

Anhalten und fragen, sobald einer dieser Punkte eintritt:

- Ein Block hätte kein prüfbares Abnahmekriterium.
- Der Orchestrator müsste außerhalb von `orchestrate/` schreiben, um weiterzukommen.
- Ein Worker bräuchte mehr Rechte als der Orchestrator, oder `bypassPermissions`.
- Ein Skill oder Plugin soll installiert werden (immer einzeln bestätigen lassen).
- Zwei Blöcke müssten denselben Branch ändern.
- Ein Repo ohne `FOUNDATION VALID` bekäme einen Bau-Block.
- Der Blockplan soll Termine, Prioritäten auf Zeit oder Schätzungen tragen — das ist
  Projektmanagement und `Out of Scope`.

## Vorlagen

Kopieren nach `orchestrate/` im Heimat-Repo, dann vollständig ausfüllen. Den Ordner nennt
`ORCHESTRATE.md`; wird er umbenannt, gilt der neue Name überall.

| Vorlage | Zweck |
| --- | --- |
| [ORCHESTRATE.md](templates/ORCHESTRATE.md) | Konfiguration aus `SETUP`: Repos, Merge-Modus, Worker-Verfahren, Zuständigkeiten |
| [BLOCKPLAN.md](templates/BLOCKPLAN.md) | Der eine Ort für den Stand aller Blöcke |
| [BLOCK.md](templates/BLOCK.md) | Je Block: Auftrag, Übergabe, Tor, Abnahme — eine Datei |
| [WORKER-START.md](templates/WORKER-START.md) | Startprompt, der eine Session zum Worker macht |

[mechanismen.md](reference/mechanismen.md) sagt, wie Remote Control und `SendMessage` hier
eingesetzt werden, was geprüft ist und was nicht, und enthält die Prüfliste. Nachladen, wenn
`SETUP` die Erreichbarkeit prüft — nicht vorab.
