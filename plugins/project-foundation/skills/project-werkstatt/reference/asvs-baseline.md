# Sicherheitskatalog — ASVS-Baseline mit Level-Wahl und Inseln

> Wer die Werkstatt aufsetzt, liest diese Datei in Schritt 1 (KLÄREN: Level) und Schritt 3
> (ROLLEN: Skill `sicherheits-katalog`). Vorlagen: [skills/sicherheits-katalog.md](../templates/skills/sicherheits-katalog.md),
> [sicherheit/katalog.json](../templates/sicherheit/katalog.json),
> [sicherheit/nachweise.json](../templates/sicherheit/nachweise.json).

## Herkunft

Werkstatt-Plan Atemluft V2, Teilblock 100-4 (A-16), entschieden mit ENT-206 Punkt 6 bis 8 am
02.10.2026. Bezug ist OWASP ASVS 5.0.0 (Mai 2025, 17 Kapitel). **Diese Datei und die Vorlagen
übernehmen keinen ASVS-Text.** Sie nennen nur Kapitel und Anforderungsnummern. Den Wortlaut holt
der Skill zur Laufzeit aus der unveränderten CSV des Projekts. Grund: Die CSV steht unter
CC BY-SA 4.0. Welche Pflichten daraus für ein Repo folgen, das sie ablegt, ist in der Quelle eine
offene Rechtsfrage.

## Die Leitfrage

Welche Sicherheitsanforderungen prüft das Projekt bei einer Änderung, und **woran zeigt sich,
dass die Prüfung greift?**

**Antwort, drei Teile:**

1. **Katalogdatei** (`katalog.json`): eine Zeile je Anforderung, aus ASVS und aus eigenen
   Entscheidungen. Sie liegt im Sperrpfad `.claude/skills/**`, weil eine Datei, in der die
   Bau-Session Zeilen streichen kann, die Prüfung selbst lockert.
2. **Nachweisdatei** (`nachweise.json`): nennt zu jeder geltenden Zeile den Test oder Check. Sie
   liegt im Repo, aber nicht gesperrt, denn die Bau-Session pflegt sie mit dem Code.
3. **Wirkungstests** in der Suite, etwa der Mandantentest unten. **Den Schutz tragen sie**, weil
   sie deterministisch sind und den Merge über G-1 halten. Katalog und Gate-Urteil sind
   Modellarbeit und damit Selbstauskunft.

Das folgt der Regel „kein Pflichtschritt in einem Skill". Der Skill hilft beim Finden, den Schutz
trägt der Test.

## Das Level

ASVS 5.0.0 kennt drei Level, beschrieben im Kapitel zu den Levels. **L1** ist der kleinste Teil,
**L2** gilt dort als Regelfall für die meisten Anwendungen (mit L1 zusammen grob 70 % der
Anforderungen), **L3** ist für Anwendungen mit höchstem Schutzbedarf gedacht; das Beispiel des
Standards ist eine Bank. Die Wahl ist eine **Risikoentscheidung des Menschen**, keine
Tabellenablesung: Sensibilität der Daten, Angreifer und Folgen.

**Inseln.** Der Standard erlaubt einem Projekt, seine eigene Auswahl zu treffen und nicht
zutreffende Abschnitte wegzulassen. „L2 für die Anwendung, L3 für einzelne Bereiche" steht so nicht
im Primärtext, sondern in Sekundärquellen. Dort sind die üblichen Inseln Anmeldung, Kryptographie und Zahlung. Eine Insel
ist also **Zuschnitt**, keine Vorgabe des Standards, und das Projekt begründet sie.

**Entscheidung der Quelle** (Gesundheitsdaten, mehrere Mandanten): **L2 für die Anwendung, dazu
L3-Inseln für Anmeldung, Kryptographie und Mandantengrenze.** Zahlung wurde **keine** Insel, weil
die Anwendung kein Geld annimmt. Filtersatz dort: Vorschläge, die ganze Anwendung auf L3 zu heben,
prallen ab. Neu aufzumachen, wenn ein Kunde L3 für die ganze Anwendung verlangt.

**Für ein neues Projekt** fragt Schritt 1 (KLÄREN) den Menschen:

- **Welches Level für die Anwendung?** Faustregel dieses Skills, nicht aus dem Standard: L2, wenn
  personenbezogene Daten oder mehrere Kunden im Spiel sind; L1 nur, wenn beides fehlt und die
  Risikoanalyse es trägt.
- **Welche Inseln auf L3, und warum?** Ein Bereich wird Insel, wenn die Entscheidungen oder das
  Threat Model ihn als höchstes Risiko benennen. Typisch sind Anmeldung und Kryptographie, bei
  mehreren Mandanten die Mandantengrenze, wenn das Projekt selbst Geld annimmt auch Zahlung.
- **Bedingung zum Neuaufmachen**, etwa eine neue Datenklasse oder ein Pentest-Fund außerhalb der
  Inseln.

Die Entscheidung kommt als ADR ins Ziel-Repo, mit Filtersatz.

## Die Katalogdatei

**Ort:** `.claude/skills/sicherheits-katalog/katalog.json`, also neben dem Skill und unter dem
Sperrpfad. Die ASVS-CSV liegt unverändert daneben. Der Katalog führt ihren SHA-256 und nimmt nur
Nummern und eigene Felder auf. Legacy-Dateien aus ASVS 4.x gehören nicht hinein: Die Nummern aus
4.0.3 lassen sich nicht auf 5.0.0 übertragen.

**Kopf:** `asvs_version` (`"5.0.0"`), `csv_datei`, `csv_sha256`, `auswahl_stand` (Datum), `level`
(etwa `"L2"`), `inseln` (Liste der Namen), `ausloeser_pfade` (je Kategorie die Pfadmuster des
Repos, sie entstehen mit dem Layout).

**Felder je Zeile:**

| Feld | Inhalt |
| --- | --- |
| `id` | `SK-<nnn>`, stabil, wird nie umgewidmet |
| `quelle`, `ref` | `asvs-5.0.0` mit der Anforderungsnummer aus der CSV (`req_id`); `entscheidung` mit Nummer und Punkt; `cheatsheet` mit dem Muster |
| `kapitel`, `stufe_csv` | Kapitelname und Level der CSV (`L` als Zahl 1, 2 oder 3) |
| `stufe_projekt` | `L1`, `L2` oder `L3-Insel:<name>` |
| `gilt` | `ja`, `nein` oder `bedingt`. Bei `nein` und `bedingt` sind `begruendung` und `bedingung` Pflicht |
| `pruefart` | `test` (Nachweis in der Suite), `gate` (Pflicht-Check aus G-1, etwa Secret-Scan oder statische Analyse), `bericht` (`/security-review`, Gate-Prüfpunkt 6), `extern` (Pentest) |
| `ausloeser` | Kategorien wie `endpunkt`, `datenmodell`, `auth`, `krypto`, `eingabe`, `log`, `abhaengigkeit` |
| `blockierend` | `ja`, wenn ein Verstoß eine Schutzschicht aushebelt. Das Gate urteilt dann bei offenem Befund „nein" |

**Die Nachweisdatei** (`docs/sicherheit/nachweise.json`, Vorschlag) hat je `id` die Felder `art`
(`test`, `check`, `vermerk`) und `ziel` (Testknoten, Name eines Pflicht-Checks oder Vermerk).

## Prüfung der Dateien

Das ist ein Test in der Suite, Teil des Checks `tests`, ohne eigenen Pflicht-Check:

- **SK-1:** Das Schema ist gültig.
- **SK-2:** Jede `ref` mit `quelle: asvs-5.0.0` steht als `req_id` in der CSV, `stufe_csv` ist
  gleich dem `L` der CSV, und der Hash der CSV stimmt. Nummern aus 4.x scheitern hier.
- **SK-3:** Zu jeder Zeile mit `gilt: ja` und `pruefart` `test` oder `gate` nennt
  `nachweise.json` ein Ziel, das existiert und nicht übersprungen wird.
- **SK-4:** `nein` oder `bedingt` ohne Begründung ist rot.
- **SK-5 (Lebenszeichen):** Die Zahl der Zeilen mit `gilt: ja` ist größer 0.

## Wie Skill und Gate den Katalog lesen

- **Der Skill** löst aus, wenn eine Änderung auf Sicherheit geprüft werden soll. Er liest
  `katalog.json` und vergleicht die Kategorien mit dem Diff gegen `origin/main`. Für jede getroffene
  Zeile mit `gilt: ja` oder `bedingt` schlägt er den Text in der CSV nach und gibt Zeile,
  `pruefart` und Nachweis aus. Er ändert nichts.
- **Das Gate** liest beide Dateien selbst. Sein Prüfpunkt 5 („Verstoß gegen eine Entscheidung
  oder Regel") umfasst jede Katalogzeile mit `gilt: ja`, deren `ausloeser` der Diff trifft. „Nein"
  heißt: Der Nachweis fehlt, oder der Diff löscht oder schwächt ihn, und die Zeile trägt
  `blockierend: ja`. **Grenze:** Das Urteil ist Modellarbeit. Die Zeilen mit `pruefart: test` trägt
  der Test, nicht das Gate.

## Füllung in zwei Stufen

1. **Stufe 1, beim Aufsetzen:** Format, Prüfung SK-1 bis SK-5, Skill und die Zeilen aus eigenen
   Entscheidungen. Damit ist das Lebenszeichen größer 0. Geschrieben wird die Vorlage wie jeder
   Sperrpfad: geprüfte Vorlage, wörtliche Kopie, Hash-Vergleich.
2. **Stufe 2, nach Threat Model, Mandanten-Mechanik und Identität:** die Auswahl aus der CSV, als
   signierter Commit des Menschen. Vorher wären `gilt: nein` und `bedingt` geraten. Entscheidung
   der Quelle: Stufe 2 ist ein eigener Block nach diesen Entscheidungen. **Option:** Zeilen, deren
   Nummern schon feststehen, kommen in Stufe 1.

## Beispiel: Mandantentest (wenn mehrmandantenfähig)

Ein Beispiel für Teil 3. Es ist **keine Pflicht**, sondern gilt nur, wenn das Projekt mehrere
Mandanten hat. Die Katalogzeilen dazu verweisen auf ASVS V8.2.2 und V8.4.1 (Kapitel V8
Authorization), dazu auf V15.3.3 für das Umetikettieren. Hinzu kommen Muster aus dem OWASP Multi
Tenant Security Cheat Sheet (`quelle: cheatsheet`).

**Aufbau:** zwei Mandanten A und B, je ein Konto mit **echtem Token über den Anmeldeweg der
Anwendung**, ohne die Authentifizierung im Test zu überschreiben. Die Zeilen von A tragen einen
eindeutigen Marker. Die Operationen kommen aus dem API-Vertrag (OpenAPI), nicht aus einer
Namenssuche.

| Fall | Prüft | Positivkontrolle |
| --- | --- | --- |
| T-a Einzelobjekt | B liest, ändert und löscht mit der ID aus A: 4xx, kein Marker im Body, die Zeile von A ist danach unverändert | A sendet dasselbe: 2xx, Marker da |
| T-b Liste | Kollektionen als B: Marker von A fehlt | Liste von A enthält ihn |
| T-c Fremd-Fremdschlüssel | B legt an oder ändert mit einer ID aus A im Body: 4xx, nichts entsteht, nichts verknüpft sich | derselbe Body mit einer ID aus B: 2xx |
| T-d Umetikettieren | PATCH oder PUT mit einem Mandantenfeld im Body: ignoriert oder 4xx | erlaubtes Feld: 2xx |
| T-e Pool | Pool der Größe 1, gleiche Rolle und Konfiguration wie in Produktion; A, B, A, B über dieselbe Verbindung, auch nach einem Fehler und nach einem Zwischen-Commit: B sieht A nicht | A sieht die eigenen Marker |
| T-f weitere Zugänge | dieselbe Matrix über weitere Schnittstellen, die dieselben Handler erreichen | wie T-a |
| T-g echte Tokens | Token über den Produktionsweg, mit Test-Zugängen | Token von A wird akzeptiert |
| T-h Abdeckung | Operation mit Ressourcen-ID ohne Matrixzeile und nicht auf der Ausnahmeliste: rot. Der Test meldet die Zahl geprüfter Operationen. Die Ausnahmeliste hat das Ziel „leer" und wird aus `origin/main` gelesen | Operation mit Zeile: grün |

**Bei Row-Level-Security** kommt Schicht B dazu: App-Rolle ohne Superuser und ohne Bypass, als
Selbstkontrolle geprüft, eine Matrix je Tabelle und die Abdeckung aus den Metadaten der
Datenbank. Schicht B ordnet einen Fehler zu, wenn Schicht A rot wird, sie ersetzt sie nicht.

**Negativkontrolle:** je Fall die Positivkontrolle, sonst ist der Test vakuum-wahr. Skip-Zahl 0,
ein Skip im Mandantentest ist rot.

**Mutationsprobe** (Wegwerf-Worktree):

| Mutant | Erwartung |
| --- | --- |
| Mandantenfilter in einem Lesepfad entfernt (bei zwei Schichten mit neutralisierter DB-Schicht) | T-a oder T-b rot |
| Prüfung des Fremdschlüssels im Anlegen entfernt | T-c rot |
| Kontext nach Zwischen-Commit nicht erneuert | T-e rot |
| Operation ohne Matrixzeile hinzugefügt | T-h rot |
| Policy auf „immer wahr" (bei RLS) | Matrix rot |
| App-Rolle mit Bypass (bei RLS) | Selbstkontrolle rot |

Bleibt ein Mutant grün, ist der Test blind. Bei zwei tragenden Schichten darf der erste Mutant im
normalen Lauf grün bleiben, deshalb gibt es den Lauf mit neutralisierter DB-Schicht.

## Feuert-Nachweis

- **F-1, Prüfung der Dateien:** eine `ref`, die in der CSV fehlt → rot; veränderte CSV (Hash) →
  rot; `nein` ohne Begründung → rot; `ja` mit `pruefart: test` ohne Nachweis → rot; Katalog ohne
  Zeile `gilt: ja` → rot. Negativkontrolle: unveränderter Katalog grün.
- **F-2, Sperre:** ein PR an `katalog.json`, auch mit Abweichungseintrag, ist rot nach G-4.
- **F-3, Skill:** Eval „löst aus" (neuer Endpunkt) und „bleibt still" (Formatierung), 5 Läufe,
  Schwelle 0,8. Ein verdorbener Skill fällt unter die Schwelle. Inhaltsprobe: ein Diff mit neuem
  Endpunkt nennt die Zeilen der Kategorie `endpunkt`.
- **F-4, Gate:** Probe-PR mit neuem Endpunkt ohne Nachweis zu einer `blockierend: ja`-Zeile →
  „nein". Negativkontrolle: derselbe PR mit Nachweis → „ja".
- **F-5, Wirkungstest:** jeder Mutant rot; Endpunkt ohne Matrixzeile rot; ein Skip rot.
- **F-6, Wirkung auf den Merge:** Ein roter Wirkungstest hält den Merge über G-1. Das ist der
  Unterschied zu F-4, wo ein Modell urteilt.

## Was kein Katalog fängt

Katalog und Tests decken feste Fälle. Die Suche nach neuen Angriffswegen auf die fertige Lösung
trägt ein **externer Pentest** vor dem Go-live, mit der Mandantentrennung als Pflichtziel, wo es
sie gibt. Das ist eine Voraussetzung des Menschen, keine Rolle der Werkstatt.

## Offen

- **Lizenz der CSV im Repo** (CC BY-SA 4.0): Welche Pflichten trägt die abgelegte Datei, und
  genügt die Trennung von Katalog (nur Nummern) und CSV? Rechtsfrage, offen in der Quelle.
- Die Zahl der Anforderungen je Level zählt der Aufsetz-Block aus der CSV aus (Feld `L`). Die hier
  genannten Anteile stammen aus dem Primärtext, nicht aus einer Zählung.
- Welche Kapitel Anforderungen mit Mandantenbezug haben, ist in der Quelle nur für einen Teil
  durchgesehen. Der Rest wird bei Stufe 2 gegen die vollständige CSV geprüft.
