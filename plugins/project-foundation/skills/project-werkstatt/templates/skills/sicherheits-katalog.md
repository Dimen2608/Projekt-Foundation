---
name: sicherheits-katalog
description: >-
  Prüfkatalog für sicherheitsrelevante Änderungen in {{PROJEKT}} (Rechte, Eingaben, Geheimnisse,
  Mandantentrennung falls mehrmandantenfähig). Verwenden, wenn ein Endpunkt, eine Berechtigung oder eine Datenquelle
  auf Sicherheit geprüft werden soll, nicht für Formatierung oder Umbenennungen.
---

<!--
Vorlage aus project-werkstatt (auslösender Skill). Kopieren nach
.claude/skills/sicherheits-katalog/SKILL.md.
Bewusst NICHT „security-review" genannt: Ob ein Projekt-Skill dieses Namens den eingebauten
Befehl /security-review ersetzt, ist nicht dokumentiert. Mit eigenem Namen gibt es keinen
Konflikt, und die Umsetzer-Kette ruft den eingebauten Befehl beim Namen.
Eval: E-löst-aus („Prüfe den neuen Endpunkt auf Rechteprüfung"), E-bleibt-still
(„Formatiere die Datei").
Inhalt: OFFEN (Leitplanken und ASVS-Level, siehe reference/prinzip.md, Abschnitt „Offen"). Bis
dahin ein Gerüst; der Skill belegt einen Platz im Beschreibungsbudget.
-->

# Sicherheitskatalog

## Status

**Offen.** Katalog, Level und Prüfpunkte sind nicht entschieden. Bis dahin gilt: Der eingebaute
`/security-review` läuft in der Umsetzer-Kette als Bericht, das Gate liest ihn, und die CI prüft
Secret-Scan, Abhängigkeiten und statische Analyse.

## Gliederung (Gerüst)

1. **Level:** `{{ASVS_LEVEL}}` — offen.
2. **Prüfpunkte je Bereich:** Authentifizierung, Autorisierung, falls mehrmandantenfähig
   Mandantentrennung (auch bei wiederverwendeten Verbindungen), Eingabevalidierung, Geheimnisse in Env und Log — offen.
3. **Nachweis je Prüfpunkt:** welcher Test oder welcher CI-Check ihn belegt, Skip-Zahl 0 — offen.
4. **Was kein Katalog fängt:** Die Suche nach neuen Angriffswegen auf die fertige Lösung ist ein
   benannter Rest — offen.
