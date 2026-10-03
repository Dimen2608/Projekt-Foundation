---
name: test-qualitaet
description: "Handwerk zur Frage, ob ein Test in {{PROJEKT}} etwas wert ist: leer erfüllte Zusicherung, Test gegen die Schnittstelle, Negativkontrolle, Mutationsprobe je Wachposten. Verwende ihn, wenn ein Test beurteilt, geschärft, zusammengeführt oder gestrichen wird oder jemand „grün“ als Nachweis anführt, bei Fragen wie „Brauchen wir diesen Test noch?“, „Reicht grün als Nachweis?“, „Welcher Test kann weg?“, „Ist die Abdeckung gut?“. Nicht, wenn nur ein Feld, Endpunkt oder eine Funktion gebaut wird, und nicht für die CI-Gates."
---

<!--
Vorlage aus project-werkstatt (im Test-Autor per `skills:` vorgeladen, löst auch aus). Ziel:
.claude/skills/{{PLUGIN}}/skills/test-qualitaet/SKILL.md (Sperrpfad). Evals: e-4a (löst aus),
e-4b (bleibt still). Diesen Kommentar beim Kopieren entfernen.
-->

# Test-Qualität — was ein Test wert ist

Die Rolle `test-autor` (`.claude/agents/test-autor.md`) legt den Ablauf fest. Dieser Skill liefert
das Handwerk: woran du einen wertlosen Test erkennst, welchen Mutanten du setzt, wann ein Test weg
darf.

## 1. Die Kernfrage

> Welchen realistischen Fehler verhindert dieser Test, den die anderen Tests nicht schon verhindern?

Wer das nicht in einem Satz sagen kann, hat eine Zeile Coverage erzeugt, keinen Test. Grün heißt nur:
*diese* Tests laufen durch, nicht dass sie etwas prüfen. „Reicht grün als Nachweis?“ — nein, erst
die Mutationsprobe (Abschnitt 5) zeigt, ob der Test greift.

## 2. Gegen die Schnittstelle, nicht gegen den Code

- Geprüft wird über die Schnittstelle, die ein Aufrufer benutzt ({{SCHNITTSTELLE}}), gegen echte
  Abhängigkeiten, wo der Zustand zählt (echte Datenbank statt Fake). Tests ohne externe Abhängigkeit
  nur für reine Logik ohne Zustand.
- Probefrage: Wird der Test rot, wenn jemand die Umsetzung umbaut und das Verhalten gleich bleibt?
  Dann prüft er die Umsetzung.
- Geprüft wird beobachtbares Verhalten: Statuscode, Antwortkörper, Zustand nach dem Aufruf. Der
  Wortlaut eines Anzeigetexts ist nur Vertrag, wenn ein Konsument ihn braucht; der maschinenlesbare
  Nachbarwert (Code, Schlüssel) ist immer Vertrag.

## 3. Die leer erfüllte Zusicherung

**Eine Zusicherung auf Abwesenheit ist wertlos, solange nicht bewiesen ist, dass Anwesenheit möglich
war.** Sie wäre auch ohne die Umsetzung grün.

- `assert feld is None` nach einer Löschung, aber das Feld war nie gesetzt, weil in der Testumgebung
  ein Schlüssel fehlte.
- „Diese Einträge stehen nicht in der Liste“, und die Liste ist leer. Ein Test, der null Fälle
  sammelt, ist rot, nicht grün.

**Regel:** Jede Zusicherung auf Abwesenheit trägt im selben Test eine **Vorher-Prüfung** (das Feld
war vor der Aktion gesetzt) oder eine **Positivkontrolle** (etwas, das nicht verschwinden darf, ist
noch da). Bei Listen ist eine namentlich bekannte, nicht betroffene Zeile schärfer als eine
Mindestzahl.

## 4. Negativkontrolle und der richtige Grund für Rot

Ein **Wachposten** ist eine Prüfung, die etwas ablehnen oder verhindern soll. Je Wachposten zwei
Tests:

- Der Verstoß wird abgelehnt, und zwar **an der erwarteten Schranke**: Statuscode und Fehlerinhalt
  stammen aus dem Abnahmekriterium. Ein Test, der rot ist, weil Route oder Tabelle fehlen, beweist
  nichts.
- Die **Negativkontrolle**: derselbe Weg mit einer Eingabe knapp auf der erlaubten Seite geht durch.
  Ohne sie besteht auch ein Wachposten, der alles ablehnt.

## 5. Die Mutationsprobe je Wachposten

Der Mutant ist **eine** Änderung an der geprüften Bedingung: entfernen, umkehren (`==` zu `!=`, `>` zu
`<=`, `and` zu `or`) oder eine Filterklausel durch „keine“ ersetzen. Der Test muss rot werden, an der
Schranke aus Abschnitt 4.

- **Bleibt der Test grün**, ist der Test schwach, nicht der Mutant „belanglos“. Schärfen, oder den
  eigenen neuen Test streichen und begründen.
- **Fehlt der Wachposten auf `main`** (das Feature bringt ihn erst), hast du nichts zu mutieren. Schreibe
  in die Rückmeldung „Mutationsprobe nicht möglich: Wachposten fehlt auf `main`“, halte den Test an der
  erwarteten Schranke und trage ihn in `{{TESTVERZEICHNIS}}wachposten-offen.txt` ein. Die Probe führt
  dann der Umsetzer nach dem Bau; sein Stop-Hook prüft das.

**Muster, an denen Mutanten oft überleben.** Frag jeden Test danach:

1. **Neutraler Wert in der Fixture.** 0 oder 1 macht Operator-Mutanten unsichtbar (`x * 1 == x / 1`).
2. **`and` zu `or` im Mehrfach-Guard.** Test „nur eines von zwei Feldern gesetzt“, je Richtung einer.
3. **Rundung.** Ein Geldbetrag mit einem Wert, der bei falscher Rundung abweicht.
4. **Der nie durchlaufene Default.** Jeder Default-Parameter braucht einen Aufruf, der ihn greifen lässt.
5. **Mandanten- oder Rechteprädikat in der Abfrage.** Bleibt der Test beim umgekehrten Prädikat grün,
   hält nur eine tiefere Schicht; die Schutzlinie darüber ist ungeprüft. Das ist ein Fund für die
   Rückmeldung.

## 6. Überlebender Mutant im Nachtlauf ({{MUTATIONSWERKZEUG}})

Der Nachtlauf meldet nur. Jeder überlebende Mutant bekommt **genau eine** von drei Marken:

- **Echte Lücke:** Der mutierte Zustand kann im Betrieb eintreten **und** ein Konsument sähe den
  Unterschied.
- **Belanglos**, nur mit benannter Begründung: äquivalent, unerreichbarer Eingaberaum, nachgelagerter
  Guard fängt es ab (im Code geprüft, nicht angenommen), reiner Diagnosetext.
- **Nicht eingeordnet:** angesehen, nicht entschieden. Die richtige Marke, wenn du unsicher bist.

**Prüffrage:** *Wie sähe der Test aus, der diesen Mutanten tötet?* Eine Überlebensrate nennst du nie
ohne die Zusammensetzung ihrer Überlebenden.

## 7. Was du nicht tust

- Kein Test, der grün gemacht wird, indem er schwächer wird. Der Wächter ist rot bei neuem `skip`,
  `skipif`, `xfail`, `noqa`, `type: ignore`, `pragma: no cover` und wenn die Zahl der Zusicherungen
  einer Testfunktion auf null sinkt.
- Kein Test gegen Anzeigetexte nur, um einen Mutanten zu töten.
- Keine Zielmarke „alle Mutanten getötet“: Äquivalente sind nicht tötbar.
- Keine Rechtfertigung „erhöht die Coverage“. Die Diff-Coverage ist ein Gate, keine Antwort auf die
  Kernfrage.

## 8. „Brauchen wir diesen Test noch?“

Bewertet wird nur, was einen Anlass hat: die Datei, die du ohnehin anfasst; ein Test, der bei
harmloser Änderung rot wird; ein Verdacht auf Doppelung. Je bewertetem Test eine von vier
Entscheidungen:

| | |
| --- | --- |
| **BEHALTEN** | Beantwortet die Kernfrage in einem Satz. |
| **VERBESSERN** | Prüft das Richtige zu schwach, oder ein Muster aus Abschnitt 5. |
| **ZUSAMMENFÜHREN** | Prüft dasselbe wie ein anderer Test in anderer Datei. |
| **PRÜFEN** | Sieht überflüssig aus, der Beleg fehlt. Im Zweifel diese Marke. |

Es gibt kein LÖSCHEN auf Verdacht. Lies vor dem Zusammenführen den Dateikopf: Steht dort eine
Begründung für die Trennung, ist sie Absicht. Der Wächter sieht den Namen: Eine gelöschte
Testfunktion ist rot; Umbenennen und Aufteilen gehen mit einem Abweichungseintrag, der alten und
neuen Namen nennt.
