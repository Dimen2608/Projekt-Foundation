---
name: sicherheits-katalog
description: >-
  Prüfkatalog für sicherheitsrelevante Änderungen in {{PROJEKT}}: liest katalog.json (ASVS 5.0.0,
  Level {{ASVS_LEVEL}} mit L3-Inseln {{INSELN}}), ordnet den Diff den Katalogzeilen zu und nennt je
  Zeile Prüfart und Nachweis. Verwenden, wenn ein Endpunkt, eine Berechtigung, Anmeldung,
  Kryptographie, eine Datenquelle oder eine Abhängigkeit auf Sicherheit geprüft werden soll, nicht
  für Formatierung oder Umbenennungen.
---

<!--
Vorlage aus project-werkstatt (auslösender Skill). Kopieren nach
.claude/skills/sicherheits-katalog/SKILL.md, daneben katalog.json (Vorlage
templates/sicherheit/katalog.json) und die unveränderte ASVS-5.0.0-CSV. Alles unter dem
Sperrpfad .claude/skills/**: Nach dem Einspielen ändert es nur ein signierter Commit des Menschen.
Bewusst NICHT „security-review" genannt: Ob ein Projekt-Skill dieses Namens den eingebauten
Befehl /security-review ersetzt, ist nicht dokumentiert.
Kein ASVS-Text in dieser Datei und im Katalog, nur Nummern; den Wortlaut liest der Skill aus der
CSV (Lizenz CC BY-SA 4.0, Pflichten offen; siehe reference/asvs-baseline.md).
Eval: E-löst-aus („Prüfe den neuen Endpunkt auf Rechteprüfung"), E-bleibt-still
(„Formatiere die Datei"). 5 Läufe, Schwelle 0,8.
Verhindert: ein Sicherheitsbericht ohne feste Liste, der nicht sagt, was er nicht geprüft hat.
Den Schutz trägt nicht dieser Skill, sondern die Tests aus nachweise.json (G-1).
-->

# Sicherheitskatalog

## Was gilt

- **Level:** {{ASVS_LEVEL}} für die Anwendung, L3-Inseln: {{INSELN}}. Entschieden in
  {{LEVEL_ENTSCHEIDUNG}}.
- **Katalog:** `.claude/skills/sicherheits-katalog/katalog.json`. Je Zeile: `id`, `quelle`, `ref`,
  `gilt`, `pruefart`, `ausloeser`, `blockierend`.
- **Nachweise:** `{{NACHWEIS_PFAD}}`, je `id` ein Testknoten, ein Pflicht-Check oder ein Vermerk.
- **Wortlaut:** in der CSV neben dem Katalog, Spalte `req_id` gleich `ref`.

## Vorgehen

1. Den Diff gegen `origin/main` holen: `git diff --name-only origin/main...HEAD`.
2. Die Kategorien des Diffs bestimmen: Pfade gegen `ausloeser_pfade` im Kopf des Katalogs.
3. Alle Zeilen mit `gilt: ja` oder `bedingt` wählen, deren `ausloeser` eine dieser Kategorien
   enthält. Bei `bedingt` prüfen, ob die `bedingung` zutrifft, und das Ergebnis nennen.
4. Je Zeile den Wortlaut der Anforderung in der CSV nachschlagen (nur lesen, nicht in den Bericht
   kopieren, die Nummer genügt) und am Diff prüfen.
5. Je Zeile den Nachweis aus der Nachweisdatei nennen und prüfen, dass der Test oder Check
   existiert und nicht übersprungen wird. Löscht oder schwächt der Diff einen Nachweis, ist das ein
   Fund.

## Ausgabe

Eine Tabelle: `id` · `ref` · `pruefart` · Nachweis · Befund (`ok`, `fehlt`, `geschwächt`,
`bedingt nicht erfüllt`) · `blockierend`. Darunter **nicht geprüft**: die Kategorien des Diffs ohne
Katalogzeile. Der Skill ändert nichts.

## Grenzen

- Der Skill findet, er schützt nicht. Den Schutz tragen die Tests aus der Nachweisdatei, die den
  Merge über G-1 halten. Das Gate liest den Katalog selbst (Prüfpunkt 5).
- Neue Angriffswege auf die fertige Lösung fängt kein Katalog. Das trägt der externe Pentest.

## Offen

- {{OFFENE_PUNKTE}} (Stufe 2 der Auswahl aus der CSV, Lizenzfrage).
