---
name: belastbar-messen
description: >-
  Belegpflicht für jede Aussage über einen Zustand in {{PROJEKT}}: gegen welchen Stand gemessen
  wurde, mit welchem ausgeführten Befehl, mit Positiv- und Negativkontrolle. Verwenden, wenn eine
  Aussage entstehen soll wie „ist schon deployt", „hat keine Treffer", „alle Tests laufen",
  „wie viele …" — nicht für reine Umbenennungen oder Formatierung.
---

<!--
Vorlage aus project-werkstatt (auslösender Skill). Kopieren nach
.claude/skills/belastbar-messen/SKILL.md. Höchstens 500 Zeilen.
Verhindert: „Abwesenheit sieht aus wie Bestätigung" und „Nachweis ohne Wirkung" in Befunden und
Vollzugsmeldungen. Die Gates schließen falschen Checkout, übersprungene Tests und verschluckte
Exit-Codes mechanisch; dieser Skill deckt die Aussage danach.
Eval: ein Fall „löst aus" (Zustandsfrage), einer „bleibt still" (Umbenennung).
Inhalt: Gerüst. Die ausführliche Fassung ist offen.
-->

# Belastbar messen

Eine Aussage über einen Zustand ist erst belegt, wenn drei Dinge feststehen.

## 1. Gegen welchen Stand?

Nenne Commit-SHA, Umgebung und Zeitpunkt. „Auf main" ist kein Stand, `origin/main` bei `<sha>` ist
einer. Ein Testbericht ohne SHA belegt nichts über den PR-Kopf.

## 2. Mit welchem Befehl?

Der Befehl steht wörtlich da und wurde **ausgeführt**, nicht gelesen. Eine Maske, die niemand
ausführt, ist eine Meinung.

## 3. Mit welcher Kontrolle?

- **Positivkontrolle:** Derselbe Befehl findet etwas, wo es da sein muss.
- **Negativkontrolle:** Er findet nichts, wo nichts sein darf.
- „0 Treffer" ohne Positivkontrolle ist keine Abwesenheit, sondern vielleicht ein kaputter Befehl.
- Pipes mit `set -o pipefail`; sonst verschluckt die Pipe den Exit-Code.

## Offen

- Zählregeln (Einheit je Zahl), Umgang mit Zahlen aus mehreren Quellen: folgt.
