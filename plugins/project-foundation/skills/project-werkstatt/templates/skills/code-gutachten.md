---
name: code-gutachten
description: "Handwerk für das Gutachten über einen fertigen Diff oder PR in {{PROJEKT}}: Redundanz gegen den Bestand belegen statt vermuten, tote Pfade nachweisen, Abstraktionshöhe und Layer beurteilen, Verstöße gegen Entscheidungen, Regeln oder den Sicherheitskatalog finden, den Sicherheitsbericht prüfen. Verwende ihn beim Begutachten, Reviewen und Prüfen einer konkreten Änderung und bei Fragen wie „Gibt es diese Logik schon?“, „Ist das doppelt gebaut?“, „Brauchen wir das überhaupt?“. Nicht beim Umsetzen eines Auftrags oder Kriteriums."
---

<!--
Vorlage aus project-werkstatt (im Gate per `skills:` vorgeladen). Ziel:
.claude/skills/{{PLUGIN}}/skills/code-gutachten/SKILL.md (Sperrpfad). Nicht mit
disable-model-invocation: true markieren; ob das Vorladen dann scheitert, ist nicht belegt.
Eval: e-3 (bleibt still im Umsetzungsauftrag); das Auslösen prüfen die Probe-PRs des Gates.
Diesen Kommentar beim Kopieren entfernen.
-->

# Code-Gutachten — ein Diff, ein Urteil

Der Agent `gate` (`.claude/agents/gate.md`) legt Reihenfolge, Urteilsformat und Marker fest. Dieser
Skill liefert, wie du je Prüfpunkt suchst und belegst; den Ablauf wiederholt er nicht. Die Nummern
sind die des Gates. Punkt 0 (Kette) steht dort vollständig.

## 1. Warum es dieses Gutachten gibt

KI-gebauter Code hat eine eigene Fehlersignatur: **lokal korrekt, global redundant.** Jede Stelle
besteht jeden Test, und dieselbe Logik steht trotzdem dreimal da. Kein Linter und keine Suite findet
das, nur ein Leser, der den Bestand kennt. Dazu kommen tote Pfade und Kommentare, die plausibel
klingen und nicht stimmen. Deshalb **erst der Bestand, dann der Diff**. Ein Fund ist ein Befehl mit
seiner Ausgabe, kein Eindruck; Objekt (SHA, Datei:Zeile) und Maske stehen dabei.

## 2. Wovon du die Finger lässt

- Was ein Pflicht-Check entscheidet, ist kein Fund: Stil und Format, Typen, Importrichtung,
  Skip-Zahl, Wächter, Diff-Coverage, bekannte Schwachstellen und Geheimnisse.
- Race Conditions und Performance: Ein Leser belegt keine Race, ohne Messung ist Performance
  Vermutung. Ausnahme: eine strukturell sichtbare N+1-Abfrage im Diff.
- Eigene Sicherheitsfunde suchst du nicht; du prüfst, was Katalog (5) und Bericht (6) verlangen.
  Fällt dir sonst etwas auf: Notiz mit Datei:Zeile. Umgeht der Diff eine Schutzschranke, ist das
  Punkt 4.

## 3. Punkt 1: Redundanz belegen

- **Bestand ist `origin/main`**, nicht dein Arbeitsbaum: Dort steht der neue Code selbst und „findet“
  sich als Treffer. `git grep -n -e "<name>" origin/main`.
- Eine Kopie mit umbenannten Bezeichnern findet der Name nicht. Suche, was eine Kopie behält:
  Literale, Konstanten, Spaltennamen, Statuswerte, Fehlertexte, SQL-Bruchstücke, den Fachbegriff aus
  der Spezifikation.
- Auch Helfer, Fixtures und Bibliotheken zählen: Eine neue Abhängigkeit, die wenige Zeilen ersetzt
  oder kann, was eine vorhandene schon kann, nennst du mit beiden Namen.
- Liefert das Repo ein Messwerkzeug für Klone ({{GUTACHTEN_BEFEHLE}}), ist ein Treffer ein Anlass,
  kein Urteil.
- **Gegenprobe vor jedem Zusammenführungsvorschlag:** Ändern sich beide Stellen aus demselben Anlass?
  Ähnliche Form bei verschiedenem Grund ist kein Fund. Zwillingspfade, die eine Entscheidung bewusst
  trennt, sind kein Doppelbau: Lies die Regel, bevor du blockierst.
- Ein Negativbefund („das gibt es nicht“) nennt Suchraum und Befehl.

## 4. Punkt 2: Tote Pfade

Neu entstehend und nicht trivial: Endpunkt, Zweig, Funktion, Konfigurationsschlüssel, Spalte, die
niemand liest. „Wird nie gerufen“ braucht beide Wege: den direkten Aufruf (`git grep` auf
`origin/main` und im Diff) **und** die dynamischen (Router-Registrierung, `getattr`, `importlib`,
Migrationen, Workflow-YAML, Konfigurationsdateien). Ein Aufrufer nur in den Tests belegt keinen
lebenden Pfad. Wer nur einen Weg gesucht hat, schreibt „nicht gefunden in <Suchraum>“, nicht „tot“.
Toter Bestand, den der Diff nur berührt, ist Notiz.

## 5. Punkt 3: Abstraktionshöhe

Zu früh: eine Abstraktion (Basisklasse, Schalter, Erweiterungspunkt) für einen einzigen Fall. Zu
spät: die dritte oder vierte Kopie. Prüffrage: Wer ruft es, aus welchem Anlass, und was geschieht
beim zweiten Anlass? Kannst du den Unterschied nicht in einem Satz begründen, ist es Geschmack, also
Vorschlag. Drei enge Ränder, nur als Vorschlag: (a) Testbarkeit, wenn Zeit, Zufall, Netz oder
Datenbank fest verdrahtet sind, **mit** Gegenvorschlag; (b) ein stiller Fehlerpfad (`except: pass`,
ein nie geprüfter Rückgabewert), mit Zeile; (c) die neue Abhängigkeit aus Punkt 1.

## 6. Punkt 4: Layer und Musterbruch

- **Layer:** Die Schichtung steht in Architektur, Entscheidungen und im Vertrag des
  Architektur-Checks, nicht in deinem Gedächtnis. `git diff --stat origin/main...HEAD` zeigt, welche
  Schichten der Diff berührt. Du prüfst, was der Check nicht sieht: Fachlogik im HTTP-Handler,
  HTTP-Wissen in Fachcode, eine Transaktionsgrenze an der falschen Stelle. Blockierend nur **mit
  benennbarer Folge**, sonst Vorschlag.
- **Vorsicht vor dem Umkehrschluss:** Ein dünner Handler, der drei Zeilen selbst rechnet, ist kein
  Fund. Der Fund ist Fachlogik, die dort wächst, wo sie beim nächsten Endpunkt erneut entsteht.
- **Musterbruch** ist der zweite, für sich sinnvolle Weg neben dem, den die anderen Stellen gehen.
  Miss den etablierten Weg, statt ihn zu erinnern: `git grep -c "<Baustein>" origin/main` je Datei.
  Prüfstellen: Mandanten- und Rechteprüfung, Fehlerform, Feldnamen, Paginierung. Blockierend nur an
  einer **Schutzschranke** (eine eigene Rechteprüfung neben der zentralen, oder eine, die der Diff
  auf einem Weg aushebelt). Sonst Vorschlag.

## 7. Punkt 5: Entscheidungen, Regeln, Sicherheitskatalog

- **Das Soll steht in `{{SPEC_ORT}}`** und im Entscheidungsprotokoll `{{ENTSCHEIDUNGSORT}}`. Nimm die
  Quellen aus dem Auftrag, suche aber auch den Fachbegriff des Diffs in der Spezifikation: Der Auftrag
  kann eine Regel nicht nennen, die der Diff trifft.
- **Ob eine Entscheidung gilt, entscheidet ihr Wortlaut samt Nachträgen und Berichtigungen,** nicht
  der erste Absatz. Eine Lockerung eines entschiedenen Werts (Schwelle, Frist, Grenze) ist ein Verstoß.
- Der Fund nennt Nummer, Wortlaut und Datei:Zeile im Diff. Blockierend, weil der Verstoß eine
  getroffene Entscheidung still zurücknimmt.
- **Sicherheitskatalog** (`.claude/skills/{{PLUGIN}}/skills/sicherheits-katalog/katalog.json`, du
  liest ihn selbst): (1) Kategorien des Diffs nach `ausloeser_pfade` im Katalog bestimmen; ist sie
  leer, nach Inhalt zuordnen und das im „Geprüft“ sagen. (2) Für jede getroffene Zeile mit `gilt: ja`
  den Nachweis in `{{NACHWEIS_PFAD}}` suchen. (3) `git diff origin/main...HEAD -- <ziel>`: Löscht oder
  schwächt der Diff den Nachweis, ist er übersprungen oder fehlt er? Mit `blockierend: ja` ist das
  „nein“. Bei `pruefart: test` trägt der Test, nicht dein Urteil.
- **PR-Text:** Fehlt „Wie verifiziert“ mit Befehl und Ergebnis, ist das ein Verstoß gegen die
  PR-Vorlage.

## 8. Punkt 6: Sicherheitsbericht

Du liest ihn zuletzt. Je Befund gilt eines von zwei: **behoben** (er steht nicht mehr im Bericht zum
Kopf, und die Stelle im Diff ist wirklich geändert: lies sie) oder ein **Vermerk** „nicht zutreffend,
weil …“, den du am Code prüfst. Der Vermerk trägt, wenn er eine Stelle (Datei:Zeile) nennt, die du
gelesen hast und die auf dem Weg des Befunds erreichbar ist. „Wird weiter unten abgefangen“ stimmt nur,
wenn der Guard dort steht und läuft. Ein Vermerk ohne Stelle trägt nicht. `/security-review` bewertet
nur neu hinzugefügten Code: Ein leerer Bericht sagt nichts über Bestandscode, den der Diff berührt.

## 9. Das Urteil bedienen (G-8)

- **Nur Blockierendes blockiert** (Liste in `gate.md`). Alles andere ist Vorschlag oder Notiz.
  Höchstens 7 Funde, sortiert nach Wirkung: „Was geschieht, wenn das durchgeht?“
- **Das „nein“ ist rot und verhandelt nicht.** Im PR steht über alle SHAs höchstens ein „nein“: Du hast
  genau einen Nachbesserungsversuch zu vergeben. Das erste „nein“ nennt deshalb **alle** blockierenden
  Funde auf einmal, jeden mit Datei:Zeile, Befehl und dem, was zu ändern ist.
- **Die Frage ist „ist es besser als jetzt?“,** nicht „ist es gut genug?“. Geschmack ist kein Befund.
- Du beurteilst den Diff, nicht die Codebase: Bestandsschulden, die er nur berührt, sind Notiz.
- **„Keine blockierenden Funde“ ist eine Freigabe und wird zitiert.** Sie trägt nur mit Prüfumfang:
  was du geprüft hast, in welchem Suchraum, und was nicht.
