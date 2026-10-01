---
name: code-gutachten
description: >-
  Handwerk des Gates in {{PROJEKT}}: wie ein Diff gegen den Bestand auf Redundanz, tote Pfade,
  Abstraktionshöhe, Layer und Regelverstöße geprüft und als BLOCKIEREND, VORSCHLAG oder NOTIZ
  belegt wird. Wird vom Gate per skills vorgeladen; nicht für Umsetzungsaufträge.
---

<!--
Vorlage aus project-werkstatt (vorgeladen im Gate per `skills:`). Kopieren nach
.claude/skills/code-gutachten/SKILL.md. Nicht mit disable-model-invocation: true markieren — ob
das Vorladen dann scheitert, ist nicht belegt.
Verhindert: „lokal korrekt, global redundant" — Doppelbau, toter Pfad, zu früh oder zu spät
verallgemeinert, Verstoß gegen eine Regel des Repos.
Liegt unter einem Sperrpfad (.claude/skills/**): Nach dem Einspielen ändert ihn nur ein
signierter Commit des Menschen.
Eval: ein Fall „bleibt still" im Umsetzer; das Auslösen prüfen die Probe-PRs des Gates.
Inhalt: so weit die Quelle ihn trägt, Rest offen.
-->

# Code-Gutachten

## Die Fehlersignatur

Ein Diff kann für sich korrekt und im Bestand falsch sein: Er baut nach, was es schon gibt, legt
einen Pfad an, den niemand aufruft, oder verallgemeinert, bevor ein zweiter Fall da ist. Diese
Fehler sieht nur, wer den Bestand liest, nicht nur den Diff. **Belege, statt zu vermuten:** Ein Fund
nennt die Stelle im Diff **und** die Stelle im Bestand.

## BLOCKIEREND nur bei

- **Doppelbau:** gleiche Logik existiert schon (auch mit umbenannten Bezeichnern).
- **Neuer toter Pfad:** Funktion, Endpunkt oder Zweig ohne Aufrufer.
- **Layer-Verstoß mit Folge:** eine Schicht greift über ihre Grenze, und das hat eine benennbare
  Wirkung.
- **Musterbruch an einer Schutzschranke:** ein etabliertes Sicherheits- oder Prüfmuster wird an
  einer Stelle umgangen.
- **Verstoß gegen eine Entscheidung** (ADR) oder Regel des Repos.
- **Sicherheitsbefund** ohne Behebung und ohne tragenden Vermerk.

Alles andere ist VORSCHLAG (darf in einem Satz abgelehnt werden) oder NOTIZ.

## Werkzeuge

- Klon-Messung, Import-Grenzen (`import-linter` oder Gegenstück), Lint: Befehle `{{GUTACHTEN_BEFEHLE}}`.
- `/code-review` taugt als Zulieferer mit ausdrücklicher Stufe, nicht als Urteil.

## Ausgabeform

**Geprüft** (ausgeführte Befehle, gelesene Stellen) · **Blockierend** (Fund · Stelle im Diff ·
Stelle im Bestand · warum) · **Vorschläge** · **Notizen** · **Sicherheitsbericht** ·
**Freigabe: ja / nein**. Höchstens sieben Funde.

## Offen

- Schwellen der Klon-Messung, Liste der Schutzschranken des Repos: folgen beim Aufsetzen.
