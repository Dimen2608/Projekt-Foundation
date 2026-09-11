# ADR-0013: Ein zweiter Skill `project-rethink` im selben Plugin — und das Plugin liefert Agents aus

## Status

Accepted — 2026-09-11

## Context

Das Plugin lieferte bis 0.3.0 genau einen Skill. `project-foundation` führt
`DISCOVER → ASSESS → ASK → DECIDE → GENERATE → VALIDATE → AUDIT` und endet in
`FOUNDATION READY`. Das setzt voraus, dass jemand sagen kann, **was das System heute tut** und
**was es tun soll**.

In einem realen Projekt war genau das nicht mehr zu haben: Die Dokumente beschrieben ein
System, das der Code nicht mehr war; jede Prüfrunde fand dieselben Themen und machte daraus neue
Aufgaben; niemand konnte unterscheiden, welche Frage entschieden war und welche nur oft gestellt.
Dort ist ein eigener Prozess entstanden — `MEASURE → MAP → GAPS → DECIDE → GUARD → HANDOFF` —,
der den Bestand misst, sein Ist-Verhalten als Spezifikation festschreibt, jede Wissenslücke
registriert, jede Grundsatzfrage als Filter entscheidet und mit absichernden Tests festnagelt.
Er hat sich dort bewährt und liegt vollständig entprojektiert als Entwurf vor. Sein Ausgang ist
der Eingang von `DISCOVER`: Er erzeugt genau das Wissen, das die Discovery sonst raten müsste.

`docs/PROJECT.md` hatte weitere Skills auf V1 vertagt — „sobald sie sich in der Anwendung als
wiederkehrend erweisen, nicht vorab". Dieser Fall ist eingetreten, wenn auch nicht als
Review-Skill, sondern als Prozess **vor** der Foundation.

Der Einbau wirft vier Fragen auf: Gehört der Skill ins selbe Plugin? Wie trennen sich die
Trigger? Ändert sich etwas am Validator? Und: Der Prozess lebt von getrennten Rollen — Umsetzer,
Gutachter als Tor, Zahlenprüfer. Sind das Textbausteine oder Agents?

## Decision

**1. Zweiter Skill im selben Plugin**, unter `plugins/project-foundation/skills/project-rethink/`.
Derselbe Zweck (ein Projekt arbeitsfähig machen), dieselben Leitsätze (*the foundation must
remain smaller than the system it enables*; *the head level does not build* als Rethink-Fassung
von *no feature work on an unresolved foundation*), und ein Prozess, der ohne den ersten nicht
endet. ADR-0002 gilt unverändert: genau eine Kopie, unter `plugins/`.

**2. Die Abgrenzung lebt in beiden `description`-Feldern.** Zwei Skills desselben Plugins
liegen auf derselben Ebene; eine Vorrangregel gibt es nur zwischen Ebenen. `project-rethink`
schließt mit „Nicht verwenden für ein leeres oder neues Repository und nicht, wenn der
Ist-Zustand beschreibbar ist — dann project-foundation." `project-foundation` schließt mit
„Nicht verwenden, wenn niemand sagen kann, was das System heute tut, oder wenn Dokumente und
Code so weit auseinanderlaufen, dass der Ist-Zustand nicht mehr beschreibbar ist — dann zuerst
project-rethink." Beide Sätze benutzen dasselbe Kriterium — beschreibbarer Ist-Zustand —, damit
Foundation bei einem Bestandsprojekt mit gewöhnlicher Drift nicht mehr abgibt, als es soll. Die
Trigger-Phrasen von Rethink stehen in `when_to_use`, die `description` trägt nur den Zweck.

**3. Keine Validator-Änderung.** Rethink erzeugt Artefakte, die der Validator nicht kennt
(`ABLAUF.md`, `BEREICH.md`, `LUECKEN.md`, `ENTSCHEIDUNGEN.md`, `TESTAUFTRAG.md`). Sie werden
**nicht** zu Pflichtstellen: Nach ADR-0011 ist ein Artefakt Pflicht, wenn ohne es eine
notwendige Frage unbeantwortet bliebe — und die Fragen, die Rethink beantwortet, stellt ein
Projekt ohne dieses Problem gar nicht. Keine neue Finding-ID, keine Änderung an `FINDING_IDS`,
`schema_version` bleibt `1`. Damit entsteht nach ADR-0009 auch kein Test: Ein Skill ist
Prompt-Material, kein ausführbarer Code.

**4. Das Plugin liefert Agents aus.** Drei Definitionen unter
`plugins/project-foundation/agents/`, registriert als `project-foundation:rethink-umsetzer`,
`…:rethink-gutachter` und `…:rethink-zahlenpruefer`. Der Ort ist nicht wählbar: Nur von dort
lädt Claude Code sie als Agents. Als Textbausteine in einer `reference/rollen.md` wären sie
Prosa — kein eigener frischer Kontext, keine erzwungene Werkzeugliste, keine Isolation. Genau
das trägt aber die Rollentrennung: Ein Subagent kennt die Begründung des Autors nicht, „hat es
nicht gebaut" ist damit echt, auch wenn alle Rollen von einer Person betrieben werden.

Gegen die Stop Condition zu ADR-0001 geprüft: `agents/` ist ein Verzeichnis, das Claude Codes
Plugin-Konvention neben `skills/` vorsieht. Die Verzeichnisstruktur wird nicht **geändert**,
sondern ein weiterer Teil der **vorgegebenen** Struktur benutzt. Die Bindung an die Konvention,
die ADR-0001 als Preis nennt, wird damit enger, nicht anders.

Frontmatter nur mit `name`, `description`, `tools`, `model`, `effort`, `isolation`. `hooks`,
`mcpServers` und `permissionMode` sind für Plugin-Agents nicht zulässig; sie zu ergänzen bleibt
eine Stop Condition. Modell und Effort stehen je Rolle fest, statt geerbt zu werden:

| Rolle | Modell / Effort | Warum | Schreibsperre |
| --- | --- | --- | --- |
| Gutachter (Tor) | `opus` / `high` | Die einzige Rolle, die einen Fehler findet, den niemand vermutet hat. An ihr zu sparen verlagert die Kosten in die Runden danach. | Werkzeugliste ohne `Write`/`Edit`, `isolation: worktree` |
| Umsetzer | `sonnet` / `high` | Effort liegt auf dem teureren der beiden Blocktypen: Messen käme mit weniger aus, eine Regel formulieren nicht. | keine — er schreibt |
| Zahlenprüfer | `sonnet` / `medium` | Verschiebt Aufwand dorthin, wo er billig ist — ein Lauf statt drei Torrunden. Ein teures Modell hier hebt den Nutzen der Regel auf. | Werkzeugliste ohne `Write`/`Edit`, `isolation: worktree` |

Die Schreibsperre der lesenden Rollen ist Werkzeugliste ohne `Write`/`Edit`, Isolation und die
Prompt-Regel „Shell nur lesend" — begrenzt, nicht erzwungen, weil `Bash` bleibt;
`permissionMode` steht nicht zur Verfügung. Kein Subagent hat `AskUserQuestion` — „legt vor" ist vom Werkzeug
erzwungen, „blockiert" ist Prompt-Disziplin.

**5. Umfang nach ADR-0011.** Sieben Vorlagen, jede gegen die Frage geprüft, die sie beantwortet:

| Frage | Vorlage |
| --- | --- |
| Wo steht das Projekt, was ist als Nächstes dran? | `ABLAUF.md` |
| Was tut das System heute in diesem Bereich? | `BEREICH.md` |
| Wie wird jede Regel abgesichert? | `TESTAUFTRAG.md` |
| Wo musste geraten werden? | `LUECKEN.md` |
| Was ist entschieden, woran prallt der nächste Fund ab? | `ENTSCHEIDUNGEN.md` |
| Was prüft das Tor an diesem Block, mit welchem Maßstab? | `TOR-PROMPT.md` |
| Wie sieht eine Maske aus, die ausgeführt wird statt gelesen? | `MASKE.sh` |

Dazu `reference/grundsaetze.md`, keine Vorlage, sondern Vertiefung: Sie beantwortet „Warum gilt
dieser Grundsatz, und woran erkenne ich, dass er bricht?" — je Grundsatz Herleitung, Beispiel und
Filtersatz. `SKILL.md` nennt nur die Gruppen; die Datei wird gezielt nachgeladen, nicht vorab.

Aus dem Entwurf **nicht** übernommen: `BOARD.md` (Heute / Diese Woche / Wartet auf / Backlog).
Es beantwortet keine eigene Frage — „Läuft", „Wartet auf" und „Als Nächstes" trägt `ABLAUF.md`
im Abschnitt „Jetzt" —, und Projektmanagement steht in `docs/PROJECT.md` unter `Out of Scope`.
`reference/herkunft.md` (Zuordnung jedes Grundsatzes zu einem Vorfall im Ursprungsprojekt)
bleibt beim Auftraggeber. Aus `TOR-PROMPT.md` sind Arbeitsweise und Ausgabeform des Tores
gestrichen: Sie stehen in der Agent-Definition, die der Gutachter ohnehin trägt. Die Begründung
für Modell und Effort steht in diesem ADR statt als Notiz im Agent-Prompt — ein Agent liest
seinen Prompt, ein Maintainer liest ADRs.

`MASKE.sh` wird als `.sh` ausgeliefert, nicht als Markdown mit eingebettetem Skript: Eine Maske
wird ausgeführt, nicht gelesen, und ein Skript, das erst aus einer Prosa-Datei herausgeschnitten
werden muss, ist genau die Hürde, die der Grundsatz „eine Maske, die niemand ausführt, ist eine
Meinung" abbauen will. Sie liegt wie jede andere Vorlage ohne Ausführungsrecht im Repository;
ausführbar wird die Kopie im Zielprojekt. Kein eigenes `README-templates.md`: Bei sieben
Vorlagen genügt die Tabelle in `SKILL.md`.

**6. Sprache nach ADR-0005.** Die Phasen `MEASURE … HANDOFF` stehen englisch und unübersetzt
wie `DISCOVER … AUDIT`. `BLOCKIEREND` / `VORSCHLAG` / `NOTIZ` in `TOR-PROMPT.md` und im
Gutachter bleiben deutsch: Kein Programm liest sie, und die Trennlinie von ADR-0005 ist genau
die — englisch ist, was der Validator liest.

Verworfene Alternativen:

- **Eigenes Plugin `project-rethink`.** Verdoppelt Marketplace-Eintrag, Version und
  Installationsschritt für einen Prozess, der ohne den ersten nicht endet — und trennt zwei
  Skills, deren Abgrenzung gerade daraus lebt, dass beide `description`-Felder aufeinander zeigen.
- **Rollen als Prosa in `reference/rollen.md`.** Siehe 4: keine Isolation, keine erzwungene
  Werkzeugliste. Das Tor wäre Zeremonie.
- **Rethink-Vorlagen als Pflichtstellen des Validators.** Widerspricht ADR-0011 und zwänge
  jedes gesunde Projekt zu Artefakten, die es nicht braucht.

## Consequences

**Positiv**

- Ein Projekt, das nicht mehr sagen kann, was es tut, hat einen Weg zur Foundation — statt einer
  Discovery, die rät.
- Validator, Finding-IDs und Manifest-Schema bleiben unberührt. Bestehende Zielprojekte merken
  von 0.4.0 nichts, außer dass ein zweiter Skill da ist.
- Die Rollentrennung des Prozesses ist Werkzeug, nicht Vorsatz.

**Negativ**

- Zwei Trigger-Beschreibungen im selben Plugin können sich überlappen. Die Abgrenzung lebt
  allein in den beiden `description`-Feldern und im Abschnitt „Abgrenzung" von `SKILL.md`.
  Prüfbar ist sie nur durch Lesen — und durch den Auslöse-Test, den jede Änderung an einer der
  beiden Beschreibungen wiederholt: ein Satz, der Foundation ziehen muss, einer, der Rethink
  ziehen muss.
- Das Plugin trägt Prompt-Material für zwei Prozesse. Der Leitsatz gilt für beide: Was der Skill
  ordnet, muss größer sein als er selbst.
- Änderungen an einer Agent-Definition wirken erst nach `/reload-plugins` oder Neustart;
  Skill-Änderungen sofort. Wer nach einem Einbau „den Agent gibt es nicht" sieht, hat meist nur
  das vergessen.
- Die Bindung an Claude Codes Plugin-Konvention (ADR-0001) umfasst jetzt auch das Agent-Format
  und seine erlaubten Felder.

**Grenze**

Neu zu bewerten, wenn ein Auslöse-Test zeigt, dass derselbe Satz beide Skills oder den falschen
zieht — dann sind die Beschreibungen zu schärfen, nicht die Skills zu trennen. Und wenn Rethink
auf einem gesunden Projekt Arbeit erzeugt: Dann ist er zu groß.
