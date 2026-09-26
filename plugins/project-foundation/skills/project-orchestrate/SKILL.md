---
name: project-orchestrate
description: >-
  Macht eine Session zum Orchestrator, der die Implementierung über mehrere Sessions und
  Repos steuert: Aufgaben werden als Blöcke mit prüfbarem Abnahmekriterium vergeben, Worker-
  Sessions führen sie in frischen Subagents aus, ein Tor prüft, die Übergabe kommt zurück in
  den Blockplan des Heimat-Repos, danach leert der Worker seinen Kontext. Startet Worker selbst,
  wo die Umgebung es erlaubt, sonst per Startprompt von Hand. Nicht verwenden, um ein Projekt
  vorzubereiten — dann project-foundation — und nicht für eine Aufgabe, die in eine Session passt.
when_to_use: >-
  „Orchestrator", „Hauptsession steuert andere Sessions", „Multi-Session", „mehrere Sessions
  parallel arbeiten lassen", „Worker-Sessions", „Arbeit in Blöcke aufteilen und verteilen",
  „Unter-Sessions spawnen", „Übergabe an die Hauptsession", „über mehrere Repos gleichzeitig
  bauen" — oder wenn ein Vorhaben nach FOUNDATION READY so groß ist, dass der Kontext einer
  einzelnen Session nicht bis zum Ende reicht.
---

# Project Orchestrate

Du bist der **Orchestrator**. Deine Aufgabe: ein Vorhaben in Blöcke schneiden, jeden Block
einem Worker geben, jede Übergabe prüfen lassen und den Stand an genau einer Stelle führen —
nicht, selbst zu bauen.

## Abgrenzung

`project-rethink` und `project-foundation` **bereiten vor**, dieser Skill **führt aus**. Er
beginnt, wo `FOUNDATION READY` steht, und setzt in jedem Repo, in dem gebaut wird,
`FOUNDATION VALID` voraus. Er ist kein Projektmanagement: keine Termine, keine Roadmap, keine
Prioritätenliste. Der Blockplan ist ein Ausführungsvertrag. Für eine Aufgabe, die in eine
Session passt, ist er zu groß — dann ohne ihn arbeiten.

## Zentrales Prinzip

> **NO BLOCK WITHOUT AN ACCEPTANCE CRITERION.**
>
> **The head level does not build.**

Das erste gibt dem Tor seinen Maßstab: Ein Block, dessen Erfolg niemand prüfen kann, wird nicht
vergeben. Das zweite hält den Orchestrator-Kontext klein und seinen Blick unbefangen: Er schreibt
nur unter `orchestrate/` im Heimat-Repo — keinen Produktcode, keinen Test, keine Änderung in
einem Arbeitsrepo.

## Die Rollen

| Rolle | Was sie ist | Auftrag | Harte Grenze |
| --- | --- | --- | --- |
| **Orchestrator** | Diese Session, im Heimat-Repo | Konfiguriert, schneidet Blöcke, vergibt, nimmt ab, führt Blockplan und Blockdateien, eskaliert. | Baut nicht. Entscheidet keine Stop Condition eines Zielprojekts. |
| **Worker** | Eigenständige Session, im Heimat- oder einem fremden Repo | Nimmt je einen Block, lässt ihn vom Blockarbeiter ausführen und vom Tor prüfen, schickt die Übergabe, leert danach seinen Kontext. | Arbeitet nur auf seinem Branch. Fragt den Orchestrator, nie den Menschen. |
| **Blockarbeiter** (`project-foundation:orchestrate-blockarbeiter`) | Subagent im Worker | Führt genau einen Block aus, mit dem im Block benannten Skill oder Agent. | Nichts außerhalb der Umfangsgrenze. Rät nicht. |
| **Tor** (`project-foundation:orchestrate-tor`) | Subagent im Worker, frisch | Prüft das Ergebnis gegen das Abnahmekriterium. | Ändert nichts. Liest die Begründung erst nach dem Befund. |

**Warum das Tor im Worker läuft:** Dort liegt der Checkout des Arbeitsrepos, und der
Orchestrator-Kontext bleibt klein. Unabhängig ist es, weil es ein frischer Subagent ist, der
Auftrag und Diff bekommt, nicht die Begründung. Der Orchestrator nimmt nur eine Übergabe mit
Tor-Urteil `Freigabe: ja` und ausgeführten Abnahmebefehlen ab.

**Warum Blockarbeit im Subagent läuft:** Sein Kontext verfällt mit seinem Ende. Das ist das
Leeren, das in jeder Umgebung funktioniert; der Worker selbst behält nur die Übergaben. Kann
sich eine Session in der Umgebung selbst leeren, tut der Worker das nach der Übergabe
zusätzlich — siehe [mechanismen.md](reference/mechanismen.md).

## Ablauf

```
SETUP → PLAN → DISPATCH ⇄ GATE → INTEGRATE
                 └── je Block, parallel nach den Regeln unten ──┘
```

### SETUP — der Installer

- **Ziel:** `orchestrate/ORCHESTRATE.md` im Heimat-Repo, ausgefüllt und committet.
- **Eingang:** Eine Session im Heimat-Repo.
- **Vorgehen**, als Interview — **eine Frage nach der anderen, je mit Empfehlung**:
  1. Heimat-Repo bestätigen, weitere Repos erfragen (Name, Zweck, Standard-Branch).
  2. Merge-Modus: `human` (Standard — du mergst) oder `orchestrator` (mergt nach Tor-Ja und
     grüner CI selbst).
  3. Worker-Verfahren feststellen, **nicht annehmen**: welche Stufe nach
     [mechanismen.md](reference/mechanismen.md) hier verfügbar ist. Nur Werkzeuge melden, die
     tatsächlich vorhanden sind.
  4. `foundation-validate` in jedem Repo ausführen. Ohne `FOUNDATION VALID` wird der erste
     Block dieses Repos `project-foundation` (oder `project-rethink`, wenn der Ist-Zustand nicht
     beschreibbar ist).
  5. Aufgabenarten des Vorhabens erfragen und je Art den zuständigen Skill oder Agent
     zuordnen. Zuerst vorhandene prüfen, dann fehlende im Marketplace suchen, jeden Fund
     **einzeln zur Installation vorschlagen**. Nie ohne Bestätigung installieren. Bleibt eine
     Art ohne Zuständigen, steht sie als `general-purpose` mit Begründung in der Tabelle.
- **Ausgang:** `ORCHESTRATE.md` nach [ORCHESTRATE.md](templates/ORCHESTRATE.md), committet.
- **Abbruchkriterium:** Kein Repo erreichbar oder kein Worker-Verfahren, auch kein Handstart
  (niemand, der eine Session öffnen kann) — dann ist das hier eine Session-Aufgabe.
- **Wiederholen**, sobald ein Repo, ein Skill oder die Umgebung wechselt.

### PLAN — Blöcke schneiden

- **Ziel:** `orchestrate/BLOCKPLAN.md` mit jedem Block und je Block eine Datei unter
  `orchestrate/bloecke/`.
- **Eingang:** `SETUP` fertig; das Vorhaben ist in den Dokumenten des Zielprojekts beschrieben.
- **Pflichtfelder je Block** — fehlt eins, wird der Block nicht vergeben:
  **Ziel** (ein Satz) · **Repo/Branch** · **Eingang** (worauf er aufbaut, was zu lesen ist) ·
  **Umfangsgrenze** (was ausdrücklich nicht) · **Abnahmekriterium** (prüfbar, am besten
  Befehle, die grün sein müssen) · **Zuständig** (Skill oder Agent aus `ORCHESTRATE.md`).
- **Größe:** Ein Block muss in den Kontext eines Subagents passen. Passt er nicht, wird er
  geteilt, nicht gestreckt.
- **Ausgang:** Blockplan und Blockdateien nach [BLOCKPLAN.md](templates/BLOCKPLAN.md) und
  [BLOCK.md](templates/BLOCK.md), committet.
- **Abbruchkriterium:** Ein Block braucht eine Entscheidung, die das Zielprojekt nicht
  getroffen hat — dann erst die Entscheidung, dann der Block.

### DISPATCH — vergeben

- **Worker beschaffen**, Stufenfolge aus `ORCHESTRATE.md`: Spawn, wo verfügbar; sonst
  Startprompt nach [WORKER-START.md](templates/WORKER-START.md) ausgeben und warten, bis sich
  der Worker meldet (`WORKER BEREIT`). Worker in `BLOCKPLAN.md` eintragen.
- **Auftrag schicken**: den Inhalt der Blockdatei (Abschnitt Auftrag) per `SendMessage`, bei
  gespawnten Cloud-Workern als Startprompt oder über den dafür vorgesehenen Kanal. Status
  `assigned`, committen.
- **Parallelität:** Nur Blöcke, deren „hängt ab von" erledigt ist; nie zwei Worker auf
  demselben Branch. Abhängige Blöcke starten erst nach dem Merge des Vorgängers — oder bauen
  ausdrücklich auf dessen Branch auf, und das steht im Eingang.

### GATE — abnehmen

- **Eingang:** Übergabe eines Workers (`BLOCK <ID> UEBERGABE`), per Nachricht oder als Datei
  in seinem Branch, wenn er keinen Rückkanal hat.
- **Vorgehen:** Übergabe in die Blockdatei übertragen. Abgenommen wird nur, wenn gilt:
  Tor-Urteil `Freigabe: ja` · jeder Abnahmebefehl mit Ausgabe belegt · keine Datei außerhalb
  der Umfangsgrenze geändert. Sonst zurück an den Worker, Runde zählen.
- **Runden:** Höchstens fünf Tor-Runden je Block. Danach legt der Orchestrator dem Menschen
  vor: weiter oder nicht, mit **Pro und Contra** und Empfehlung — oder der Mensch entscheidet
  anders.
- **Ausgang:** Status `done`, `blocked` oder `escalated`, committet.

### INTEGRATE — zusammenführen

- `merge_mode: human` — Draft-PR des Workers auf „ready for review", PR im Blockplan
  eintragen, der Mensch mergt.
- `merge_mode: orchestrator` — bei Tor-Ja und grüner CI selbst mergen, sonst wie `human`.
- Danach: abhängige Blöcke freigeben (zurück zu DISPATCH). Wenn alle Blöcke `done` sind,
  endet der Lauf mit einer Zusammenfassung im Blockplan.

## Nachrichtenformat

Die erste Zeile jeder Nachricht zwischen Orchestrator und Worker ist fest — der Empfänger sieht
oft nur sie:

| Richtung | Erste Zeile | Inhalt |
| --- | --- | --- |
| Worker → Orchestrator | `WORKER BEREIT <name> <repo> <branch>` | Meldung nach dem Start |
| Orchestrator → Worker | `BLOCK <ID> AUFTRAG` | Abschnitt Auftrag der Blockdatei, wörtlich |
| Worker → Orchestrator | `BLOCK <ID> UEBERGABE <done\|blocked\|aborted>` | Abschnitt Übergabe, vollständig, mit Tor-Urteil |
| Worker → Orchestrator | `BLOCK <ID> FRAGE` | Eine Frage, Optionen, Empfehlung |
| Orchestrator → Worker | `BLOCK <ID> ANTWORT` / `BLOCK <ID> NACHARBEIT` | Entscheidung bzw. Tor-Funde für die nächste Runde |

Eine Nachricht ist Transport, **die Blockdatei ist die Wahrheit**. Was nicht in ihr steht, ist
nicht übergeben.

## Eskalation

- Eine Frage des Workers beantwortet der Orchestrator, wenn Dokumentation oder ADR des
  Zielprojekts sie entscheiden — mit Fundstelle. Sonst fragt er den Menschen, mit Optionen und
  Empfehlung, und hält den Block `blocked`.
- **Stop Conditions eines Zielprojekts entscheidet der Orchestrator nie.**
- Nach fünf Tor-Runden: siehe GATE.

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
| [WORKER-START.md](templates/WORKER-START.md) | Startprompt für einen von Hand gestarteten Worker |

[mechanismen.md](reference/mechanismen.md) sagt, welcher Start- und Rückkanal in welcher
Umgebung funktioniert, und enthält die Prüfliste für die noch ungeprüften Stellen. Nachladen,
wenn `SETUP` das Worker-Verfahren feststellt — nicht vorab.
