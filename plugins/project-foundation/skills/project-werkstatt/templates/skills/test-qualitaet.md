---
name: test-qualitaet
description: >-
  Handwerk für Tests mit Wirkung in {{PROJEKT}}: gegen die Schnittstelle statt gegen die
  Implementierung, Mutationsprobe je Wachposten, keine leer erfüllte Zusicherung. Wird vom
  Test-Autor per skills vorgeladen; löst auch aus bei Fragen wie „brauchen wir diesen Test noch".
---

<!--
Vorlage aus project-werkstatt (vorgeladen im Test-Autor per `skills:`). Kopieren nach
.claude/skills/test-qualitaet/SKILL.md.
Verhindert: einen Test ohne Wirkung — einer, der die Implementierung nachzeichnet, und die leer
erfüllte Zusicherung.
Eval: E-löst-aus („Brauchen wir diesen Test noch, oder reicht grün als Nachweis?"),
E-bleibt-still („Füge dem Endpunkt ein Pflichtfeld hinzu.").
Inhalt: so weit die Quelle ihn trägt, Rest offen.
-->

# Test-Qualität

## Gegen die Schnittstelle

Teste über die Schnittstelle, die ein Aufrufer benutzt (HTTP, öffentliche Funktion), gegen echte
Abhängigkeiten, wo der Zustand zählt (echte Datenbank statt Fake). Tests ohne externe
Abhängigkeit nur für reine Logik ohne Zustand.

## Mutationsprobe je Wachposten

Ein Wachposten ist eine Bedingung, die einen Fehler verhindern soll. Zu jedem:

1. Bedingung entfernen oder umkehren (Mutant).
2. Test läuft → **muss rot werden**.
3. Mutant zurücknehmen → grün.

Bleibt der Test beim Mutanten grün, hat er keine Wirkung. Später ersetzt ein nächtlicher
Mutationslauf (`{{MUTATIONSWERKZEUG}}`) die Handprobe.

## Leer erfüllte Zusicherung

- Ein `assert` über eine leere Liste („alle Elemente erfüllen X") ist immer wahr.
- Ein Test, der null Fälle sammelt, ist rot, nicht grün.
- Prüfe vor der Zusicherung, dass die Menge nicht leer ist.

## Was der Wächter rot macht

Neue `skip`/`xfail` außerhalb der Erlaubnisliste, gelöschte Testfunktionen, Asserts auf null,
gesenkte Schwellen. `xfail` nur mit `strict=True` und Anlass.

## Offen

- Zeitbudget je Stufe, Flaky-Quarantäne mit Frist: folgen beim Aufsetzen.
