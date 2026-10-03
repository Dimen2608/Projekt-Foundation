---
name: sicherheits-katalog
description: "Prüft eine Änderung in {{PROJEKT}} gegen den Sicherheitskatalog (ASVS 5.0.0, Level {{ASVS_LEVEL}} mit L3-Inseln {{INSELN}}, dazu Zeilen aus eigenen Entscheidungen): welche Katalogzeilen der Diff gegen origin/main trifft, welche Prüfart sie haben und ob ihr Nachweis existiert. Verwenden, wenn ein Endpunkt, eine Berechtigung, Anmeldung, Kryptographie, Mandantentrennung, eine Datenquelle, Log-Inhalt oder eine Abhängigkeit auf Sicherheit geprüft werden soll. Nicht für Formatierung, Umbenennen, Tippfehler oder Änderungen ohne Bezug zu Daten, Rechten oder Logs. Ändert nichts, liefert eine Liste."
---

<!--
Vorlage aus project-werkstatt (auslösender Skill). Ziel:
.claude/skills/{{PLUGIN}}/skills/sicherheits-katalog/SKILL.md, daneben katalog.json (Vorlage
templates/sicherheit/katalog.json) und die unveränderte ASVS-5.0.0-CSV; alles unter dem Sperrpfad.
Bewusst nicht „security-review“ genannt: Ob ein Projekt-Skill dieses Namens den eingebauten
Befehl ersetzt, ist nicht dokumentiert. Kein ASVS-Text hier und im Katalog, nur Nummern (Lizenz
der CSV: CC BY-SA 4.0, Pflichten offen). Evals: e-5 (löst aus), e-6 (bleibt still). Den Schutz
trägt nicht dieser Skill, sondern die Tests aus der Nachweisdatei (G-1). Diesen Kommentar beim
Kopieren entfernen.
-->

# Sicherheitskatalog

Du prüfst eine Änderung gegen eine **feste Liste**, nicht aus dem Gedächtnis. Der Bericht sagt, was
geprüft wurde und was nicht; eine Prüfung ohne Liste sagt das nicht. Du änderst keine Datei.

## Die Dateien

- **Katalog:** `.claude/skills/{{PLUGIN}}/skills/sicherheits-katalog/katalog.json`. Gesperrt; ändern
  kann ihn nur ein signierter Commit des Menschen. Je Zeile: `id`, `quelle` (`asvs-5.0.0`,
  `entscheidung`, `cheatsheet`), `ref`, bei `entscheidung` und `cheatsheet` der `text`,
  `stufe_projekt`, `gilt` (`ja`, `nein`, `bedingt` mit `begruendung` und `bedingung`), `pruefart`
  (`test`, `gate`, `bericht`, `extern`), `ausloeser` (Kategorien), `blockierend`.
- **CSV:** Den Anforderungstext der Zeilen mit `quelle: asvs-5.0.0` liest du in der Datei aus
  `csv_datei`, Spalten `req_id` und `req_description`. Stimmt ihr SHA-256 nicht mit `csv_sha256`
  überein, nennst du das als ersten Befund. Steht `csv_sha256` auf `null` (Stufe 1), hat der Katalog
  noch keine ASVS-Zeilen; das sagst du im Bericht und prüfst nur die übrigen.
- **Nachweise:** `{{NACHWEIS_PFAD}}`, je `id` die Felder `art` (`test`, `check`, `vermerk`) und `ziel`.
- **Level:** {{ASVS_LEVEL}}, L3-Inseln {{INSELN}}, entschieden in {{LEVEL_ENTSCHEIDUNG}}.

## Ablauf

1. `git fetch origin`, dann `git diff --name-only origin/main...HEAD` und `git diff origin/main...HEAD`.
   Nenne die Kopf-SHA und die SHA von `origin/main`.
2. Kategorien des Diffs bestimmen. Ist `ausloeser_pfade` im Katalog gefüllt, ordnest du nach dieser
   Tabelle zu. Ist sie leer, ordnest du nach dem Inhalt zu und schreibst **„Zuordnung nach Inhalt,
   Pfadtabelle fehlt“** in den Bericht:
   - `endpunkt`: neue oder geänderte Route, Parameter, Antwortfeld;
   - `datenmodell`: Tabelle, Spalte, Migration, Policy, Rolle;
   - `auth`: Anmeldung, Token, Rechte, Mandantenkontext;
   - `krypto`: Schlüssel, Hash, Signatur, Verschlüsselung;
   - `eingabe`: Validierung, Upload, Parser;
   - `log`: Logzeile, Audit-Eintrag, Fehlermeldung nach außen;
   - `abhaengigkeit`: Paket, Datenbank- oder Treiber-Einstellung.
3. Je Katalogzeile mit `gilt: ja` oder `bedingt`, deren `ausloeser` eine Kategorie des Diffs trifft:
   Text nachschlagen (CSV oder `text`; nur lesen, nicht in den Bericht kopieren, die Nummer genügt),
   bei `bedingt` prüfen, ob die `bedingung` erfüllt ist, und den Nachweis suchen.
4. Nachweis prüfen, nicht nur finden: Das `ziel` existiert (Testknoten per `grep`, Check-Name in der
   CI-Datei), es ist nicht übersprungen (`skip`, `xfail`), und der Diff löscht oder schwächt es nicht
   (Zusicherung entfernt, Bedingung gelockert, Ausnahme ergänzt).

## Bericht

Eine Tabelle, eine Zeile je getroffener Katalogzeile:

| `id` | Kategorie | `pruefart` | Nachweis (`ziel`) | Zustand | `blockierend` |
| --- | --- | --- | --- | --- | --- |

Zustand ist genau einer von: **vorhanden**, **fehlt**, **im Diff geschwächt**, **übersprungen**,
**Bedingung nicht erfüllt** (bei `bedingt`). Danach drei Zeilen:

- **Nicht geprüft:** Kategorien des Diffs ohne Katalogzeile, und Zeilen mit `pruefart: extern` oder
  `bericht`.
- **Blockierend offen:** jede Zeile mit `blockierend: ja` und Zustand fehlt, geschwächt oder
  übersprungen.
- **Stand:** Kopf-SHA, `origin/main`, `auswahl_stand` des Katalogs.

## Grenzen

- Du urteilst nicht über den Merge. Das Urteil schreibt das Gate; es liest denselben Katalog selbst
  (Prüfpunkt 5).
- Zeilen mit `pruefart: test` trägt der Test in der Suite, nicht dein Bericht. „Vorhanden“ heißt nur,
  dass das Ziel existiert und nicht übersprungen ist.
- Neue Angriffswege auf die fertige Lösung fängt kein Katalog; das trägt der externe Pentest vor dem
  Livegang.
- Fehlt eine Zeile, die du für nötig hältst, schlägst du sie im Bericht vor. Den Katalog änderst du
  nicht.
