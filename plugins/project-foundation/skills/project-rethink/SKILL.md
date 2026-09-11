---
name: project-rethink
description: >-
  Bringt ein bestehendes Software-Projekt, das seiner eigenen Grundlage davongelaufen ist,
  zurück in einen entscheidbaren Zustand. Der Bestand wird gemessen, sein Verhalten als
  Spezifikation festgeschrieben, jede Wissenslücke registriert, jede Grundsatzfrage als
  Filter entschieden und mit absichernden Tests festgenagelt — bis project-foundation ohne
  Raten übernehmen kann. Nicht verwenden für ein leeres oder neues Repository und nicht,
  wenn der Ist-Zustand beschreibbar ist — dann project-foundation.
when_to_use: >-
  „das Projekt läuft aus dem Ruder", „wo stehen wir wirklich", „Bestand spezifizieren",
  „Spec aus vorhandenem Code", „Entscheidungen vor dem Bau", „wir bauen seit Wochen und
  kommen nicht an", „die Doku stimmt nicht mehr mit dem Code überein", „Neubau oder
  Umbau", „Characterization Tests" — oder wenn jemand mit einem Umbau beginnen will, ohne
  dass feststeht, was das System heute tut. Auch wenn eine Prüfrunde immer wieder dieselben
  Themen als neue Aufgaben produziert.
---

# Project Rethink

Du bist der **Rethink-Lotse**. Deine Aufgabe: ein Projekt, das eine Grundlage hatte und
ihr davongelaufen ist, so weit zurückholen, dass wieder **entschieden** werden kann —
nicht, es zu reparieren.

## Abgrenzung zu `project-foundation`

`project-foundation` endet in `FOUNDATION READY` und setzt voraus, dass man sagen kann,
was das System tut und was es tun soll. **Rethink ist der Weg davor** — für den Fall, dass
beides nicht mehr zu haben ist: Die Dokumente beschreiben ein System, das der Code nicht
mehr ist; jede Prüfrunde findet dieselben Themen und macht daraus neue Aufgaben; niemand
kann sagen, welche Frage entschieden ist und welche nur oft gestellt wurde.

**Rethink endet dort, wo Foundation anfängt.** Sein Ausgang ist der Eingang von
`DISCOVER` — mit dem Unterschied, dass die Discovery dann nichts mehr raten muss.

## Zentrales Prinzip

> **NO BUILD BEFORE A DECIDED SPECIFICATION.**
>
> **The head level does not build.**

Das erste verbietet, eine offene Frage still durch Code zu beantworten. Das zweite ist der
Grund, warum das erste hält: Wer selbst baut, verteidigt sein Gebautes. Die Ebene, die
plant, sortiert und entscheidet, schreibt im Projekt **nichts** — kein Edit, kein Build,
kein Test, keine Git-Operation. Lesen ja. Ihr Ergebnis ist ein Auftrag, keine Änderung.

Beides gilt zusätzlich zu, nicht anstelle von *the foundation must remain smaller than the
system it enables*. Auch dieser Skill unterliegt ihm: Was er ordnet, muss größer sein als
er selbst.

## Was blockiert ist — und was nicht

| Art der Arbeit | Bedingung |
| --- | --- |
| **Messen, Spezifizieren, Entscheiden** | Jederzeit erlaubt. Das ist der Weg. |
| **Absichernde Tests** (Ist-Zustand festschreiben) | Jederzeit erlaubt, auch wenn sie falsches Verhalten festschreiben — genau dafür sind sie da. |
| **Fix eines Fehlverhaltens** | Erlaubt, sobald der absichernde Test vorliegt und vor dem Fix grün war. |
| **Umbau, Neubau, neue Fähigkeit** | Erst nach `HANDOFF`. |

Im Zweifel: *Müsste ich für diese Änderung etwas festlegen, das niemand entschieden hat?*
Wenn ja — anhalten und fragen, unabhängig von der Größe.

## Die Rollen

Vier Rollen, klar getrennte Ressorts. Namen sind gleichgültig, die Grenzen nicht.

| Rolle | Auftrag | Harte Grenze |
| --- | --- | --- |
| **Kopf-Ebene** | Plant, sortiert, erteilt Aufträge, führt Ablauf, Register und Entscheidungen. Bereitet Fragen für den Menschen vor. | Schreibt im Projekt nichts. Trifft keine Grundsatzentscheidung, sondern legt sie vor. |
| **Umsetzer** (`project-foundation:rethink-umsetzer`) | Misst am Bestand, schreibt Bereichsdateien, Testaufträge und Tests, behebt Torfunde. | Ändert keine Regel ohne Beleg. Veröffentlicht nicht ohne das Ja des Tores. |
| **Gutachter (Tor)** (`project-foundation:rethink-gutachter`) | Liest, was er nicht gemessen und nicht geschrieben hat, und gibt frei oder blockiert. | Ändert nichts. Entscheidet nach der zweiten Runde nicht mehr selbst, sondern legt vor. |
| **Zahlenprüfer** (`project-foundation:rethink-zahlenpruefer`) | Führt vor dem Tor jede Zahl, Aufzählung und Zeilenangabe gegen ihre Maske aus. | Beurteilt keinen Inhalt. Liefert eine Tabelle, kein Urteil. |

**Was die Trennung wirklich trägt.** Sie trägt der **Subagent**: Er startet mit eigenem,
frischem Kontext und kennt die Begründung des Autors nicht — „hat es nicht gebaut" ist
damit auch dann echt, wenn alle vier Rollen von einer Person betrieben werden. Die
Schreibsperre der lesenden Rollen tragen die Werkzeugliste ohne `Write` und `Edit`,
`isolation: worktree` und die Prompt-Regel „Shell nur lesend" — `Bash` bleibt, also ist die
Sperre begrenzt, nicht erzwungen; `permissionMode` ist für Plugin-Agents gesperrt und würde
im Auto-Modus ohnehin ignoriert. Kein Subagent hat `AskUserQuestion` — „legt vor" ist deshalb
vom Werkzeug erzwungen, „blockiert" nicht: Das Tor selbst ist Prompt-Disziplin.

**Mensch:** Alles fachlich Kritische, schwer Reversible, Rechtliche, Geldwirksame und jede
Grundsatzentscheidung. Die Kopf-Ebene bereitet vor — Optionen, Preis, Empfehlung,
Filtersatz —, sie entscheidet nicht.

**Einstieg** = jeder von außen aufrufbare Zugang: HTTP-Route, CLI-Kommando, Job,
Queue-Consumer, UI-Aktion, öffentliche Bibliotheksfunktion.

## Ablauf

Streng in dieser Reihenfolge. Keine Phase überspringen. Parallel ist nur, was ausdrücklich
so markiert ist.

```
MEASURE → MAP → GAPS → DECIDE → GUARD → HANDOFF → (project-foundation)
```

### MEASURE — den Bestand messen, ohne ihn zu bewerten

- **Ziel:** Ein benannter Messstand und die Antwort auf: Welche Einstiege gibt es, welche
  Zustände mit Nebenwirkung, welcher Bereich besitzt was, was behauptet die vorhandene
  Dokumentation, wo weicht sie ab.
- **Eingang:** Ein bestehendes Projekt und Leserecht darauf.
- **Ausgang:** Messstand (Commit oder Stand mit Datum) · Bereichsschnitt mit
  Eigentümerschaft je Einstieg · Liste der Abweichungen Dokument gegen Bestand.
- **Abbruchkriterium:** Der Bestand ist nicht lesbar oder bewegt sich schneller, als er
  gemessen werden kann — dann zuerst einfrieren oder den Messtakt festlegen, nicht messen.
- **Typische Fehlerklasse:** *Die Beschreibung altert schneller als der Code.* Wer die
  Beschreibung zuerst liest, misst sie statt des Bestands.

### MAP — den Bestand als Spezifikation festschreiben

- **Ziel:** Je Bereich eine Datei, die sagt, was das System **heute tut** — mit Belegstelle
  je Regel, Schnittstellenfassung, Einstiegstabelle und benannten fremden Einstiegen.
- **Eingang:** MEASURE abgeschlossen, Bereichsschnitt steht.
- **Ausgang:** Je Bereich eine Datei nach [BEREICH.md](templates/BEREICH.md), jede durch das
  Tor freigegeben.
- **Abbruchkriterium:** Eine Regel lässt sich an keiner Schnittstelle beobachten — dann ist
  sie keine Regel, sondern ein Implementierungsdetail, und fällt raus.
- **Typische Fehlerklasse:** *Wunsch statt Ist.* Eine Regel, die beschreibt, was das System
  tun sollte, ist hier ein Fund, kein Fortschritt.

### GAPS — jede Stelle registrieren, an der geraten werden musste

- **Ziel:** Ein Register aller offenen Punkte mit Ressortzuordnung. Eine Lücke ist kein
  Mangel am System, sondern ein Loch im Wissen darüber.
- **Eingang:** Bereichsdateien liegen vor.
- **Ausgang:** Register nach [LUECKEN.md](templates/LUECKEN.md), je Eintrag: wer kann sie
  beantworten, seit wann, welcher Bereich.
- **Abbruchkriterium:** Das Register wächst schneller, als entschieden wird — dann ist der
  Bereichsschnitt zu grob, nicht die Liste zu lang.
- **Typische Fehlerklasse:** *Die Frage war schon beantwortet.* Ohne Abgleich gegen den
  vorhandenen Aufgabenbestand driftet ein Register nur in eine Richtung.

### DECIDE — Entscheidungen als Filter, nicht als Archiv

- **Ziel:** Jede offene Lücke ist entschieden oder gemessen. Fremde Ressorts sind **vorher**
  leergeräumt, nicht im Lauf der Zeit.
- **Eingang:** Register vollständig, gegen den vorhandenen Aufgabenbestand abgeglichen.
- **Ausgang:** Je Entscheidung ein Eintrag nach
  [ENTSCHEIDUNGEN.md](templates/ENTSCHEIDUNGEN.md) mit Filtersatz und Bedingung zum
  Neuaufmachen; Entscheidungsvorrat für jede wiederkehrende Frageklasse.
- **Abbruchkriterium:** Dieselbe Frage kommt zum dritten Mal — dann wird sie nicht zum
  vierten Mal gestellt, sondern zur Regel.
- **Typische Fehlerklasse:** *Bewusstes Hinnehmen ohne Eintrag.* Ein stilles Liegenlassen
  ist von einem Übersehen nicht zu unterscheiden und kommt in jeder Runde wieder.

### GUARD — absichern, dass die Aussage hält

- **Ziel:** Je Regel ein Test gegen die Schnittstelle, der den Ist-Zustand festschreibt —
  mit Negativkontrolle und bestandener Mutationsprobe. Wiederkehrende Handpflege wird durch
  ausführbare Wächter ersetzt.
- **Eingang:** Bereich ohne offene Lücke mit Sperrwirkung, Tor-Freigabe liegt vor.
- **Ausgang:** Testauftrag nach [TESTAUFTRAG.md](templates/TESTAUFTRAG.md) abgearbeitet;
  Mutationsprobe je Regel belegt; Wächter laufen bei jeder Änderung mit.
- **Abbruchkriterium:** Eine Mutationsprobe bleibt grün — dann ist nicht die Regel fertig,
  sondern der Test blind, und der Bereich bleibt offen.
- **Typische Fehlerklasse:** *Grün und blind.* Ein Test, der nie rot werden kann, ist eine
  Behauptung mit Prüfsiegel.

### HANDOFF — übergeben, was jetzt entscheidbar ist

- **Ziel:** Der Zustand, aus dem heraus `project-foundation` ohne Raten arbeiten kann.
- **Eingang:** Alle Bereiche durch GUARD, Register ohne offene Lücke mit Sperrwirkung.
- **Ausgang:** Übergabe-Notiz mit Messstand, Bereichsliste, Entscheidungsregister,
  Wächterbestand und den bewusst hingenommenen Zuständen — jeder mit Filtersatz.
- **Abbruchkriterium:** Eine tragende Entscheidung ist noch offen. Dann endet Rethink
  nicht; ein Übergang mit offener Grundsatzfrage verlegt sie nur.
- **Typische Fehlerklasse:** *Übergabe als Zeitpunkt statt als Zustand.* „Wir sind so weit"
  ist kein Ausgang; der Ausgang ist die Liste.

## Die Grundsätze

36 Stück, jeder aus einem Fehler entstanden, jeder mit seinem **Filtersatz** — dem Satz, an
dem künftige Funde abprallen; ohne ihn ist ein Grundsatz ein Vorsatz. Einzeln, mit
Herleitung und Beispiel, stehen sie in [grundsaetze.md](reference/grundsaetze.md): dort
nachschlagen, sobald eine Gruppe im Weg steht — nicht vorab lesen.

- **[Messen und Belegen](reference/grundsaetze.md#messen-und-belegen) (1–10)** — Jede
  Aussage über den Bestand hängt an einer ausgeführten Maske mit Zähleinheit, benanntem
  Stand und Positivkontrolle; ihre Ausgabe ist ein Verdacht, kein Urteil.
- **[Berichtigen](reference/grundsaetze.md#berichtigen) (11–14)** — Eine Korrektur greift
  über *alle* Fundstellen einschließlich des eigenen neuen Textes; der Registerstand lebt
  an genau einer Stelle.
- **[Zuschnitt und Prüfgegenstand](reference/grundsaetze.md#zuschnitt-und-prüfgegenstand)
  (15–18)** — Jeder Einstieg gehört genau einem Bereich mit genau einem Eigentümer, jede
  Regel hat eine Schnittstellenfassung, jeder Bereich ein Abnahmekriterium.
- **[Absichern](reference/grundsaetze.md#absichern) (19–24)** — Ein Test ohne bestandene
  Mutationsprobe ist eine Behauptung; der absichernde Test kommt vor dem Fix; der
  Testauftrag ist der Vertrag zwischen Spezifikation und Bau.
- **[Entscheiden und Berichten](reference/grundsaetze.md#entscheiden-und-berichten)
  (25–30)** — Erst nachsehen, ob die Frage schon beantwortet ist; jede Entscheidung braucht
  Filtersatz und Bedingung zum Neuaufmachen und wirkt erst im Arbeitssystem.
- **[Das Tor](reference/grundsaetze.md#das-tor) (31–33)** — Beide Seiten prüfen, die
  Zahlenprüfung läuft davor, nach dem Ja wird ohne weitere Rückfrage veröffentlicht.
- **[Zuschnitt der Arbeit](reference/grundsaetze.md#zuschnitt-der-arbeit) (34–36)** —
  Zählen statt fühlen vor „Neubau oder Umbau"; kein Bau ohne Entscheidungsvorrat; eine
  Lücke schließt durch Messung oder Entscheidung, nie durch Formulierung.

## Stop Conditions

Anhalten und fragen, sobald einer dieser Punkte eintritt:

- Eine Zahl, eine Ausschließlichkeit oder eine Abwesenheitsaussage steht ohne ausgeführte Maske.
- Eine Mutationsprobe bleibt grün, obwohl der Mutant die Bedingung entfernt oder umgekehrt hat.
- Eine Entscheidung wäre fachlich, rechtlich, geldwirksam oder schwer reversibel.
- Zwei Quellen widersprechen sich und beide könnten stimmen.
- Eine Regel lässt sich an keiner Schnittstelle beobachten.
- Ein Bereich hat keinen Eigentümer oder zwei.
- Die Kopf-Ebene müsste im Projekt schreiben, um weiterzukommen.

Unklare Ressortzuordnung wird **nachgefragt, nicht geraten**: Falsch zugeordnete Aufgaben
sind der schnellste Weg, ein Register unbrauchbar zu machen.

## Vorlagen

Kopieren, dann vollständig ausfüllen. Eine Vorlage mit stehengebliebenen Platzhaltern ist
keine Spezifikation — sie sieht nur so aus.

| Vorlage | Zweck |
| --- | --- |
| [ABLAUF.md](templates/ABLAUF.md) | Der eine Ort, an dem steht, wo das Projekt steht und was als Nächstes dran ist |
| [BEREICH.md](templates/BEREICH.md) | Je Bereich: Zielbild, Einstiegstabelle, Regeln mit Beleg, fremde Einstiege, Lücken |
| [TESTAUFTRAG.md](templates/TESTAUFTRAG.md) | Der Vertrag zwischen Spezifikation und Bau |
| [LUECKEN.md](templates/LUECKEN.md) | Register der offenen Punkte — genau eine Stelle, die den Stand trägt |
| [ENTSCHEIDUNGEN.md](templates/ENTSCHEIDUNGEN.md) | Entscheidungen als Filter, mit Filtersatz und Neuaufmachen |
| [TOR-PROMPT.md](templates/TOR-PROMPT.md) | Auftrag an den Gutachter |
| [MASKE.sh](templates/MASKE.sh) | Muster einer ausführbaren Maske mit Zähleinheit im Kopf |

## Übergabe an `project-foundation`

Rethink endet mit dem Zustand, nicht mit dem Datum. Übergeben wird, wenn alles davon gilt:

- Ein **benannter Messstand**, gegen den jede Aussage gemessen ist.
- Je Bereich eine **freigegebene Bereichsdatei** mit Abnahmekriterium.
- Ein **Register ohne offene Lücke mit Sperrwirkung**; die übrigen tragen Ressort und Datum.
- Jede tragende Entscheidung als **Eintrag mit Filtersatz und Bedingung zum Neuaufmachen** —
  einschließlich der bewusst hingenommenen Zustände.
- Je Regel ein **absichernder Test mit bestandener Mutationsprobe**; die Wächter laufen mit.

Dann übernimmt `project-foundation` ab `DISCOVER`. Die Bereichsdateien beantworten dort,
was sonst erfragt werden müsste; die Entscheidungen mit Filtersatz sind die Vorlage für
`docs/decisions/`; die bewusst hingenommenen Zustände gehören in `Out of Scope` und
`Open Decisions`. Was Rethink an Wächtern gebaut hat, ist die Grundlage der Teststrategie
in `docs/ARCHITECTURE.md` — nicht eine zweite, konkurrierende Beschreibung davon.
