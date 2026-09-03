# Progress — Projekt-Foundation

> Arbeitsprotokoll. **Niemals Source of Truth** für Architektur oder aktuellen Zustand —
> dafür sind `docs/ARCHITECTURE.md` und `STATUS.md` zuständig.
>
> Neueste Einträge oben.

## 2026-09-03 — Kleiner und stiller

**Anlass**

Nach dem Refinement war das Toolkit an drei Stellen weiter gewachsen als sein Zweck: `SKILL.md`
um gut die Hälfte, die Drei-Ebenen-Tabelle stand dreimal (SKILL, README, ARCHITECTURE), und der
Validator warnte bei einem optionalen `STATUS.md` in fremdem Format achtfach — im Fremdtest die
einzige Warnung, die übrig blieb.

**Geändert**

- `STAT-003`, `DEF-050`, `DEF-051` zurückgezogen (Nachtrag in ADR-0011). Der Validator kennt
  jetzt 45 Finding-IDs.
- `SKILL.md` ohne die Kurzfassung der Phasen, den Source-of-Truth-Block und den
  `STATUS.md`-Abschnitt — alles stand bereits in Phasentabelle, Fragentabelle bzw.
  `templates/STATUS.md`. Drei Ebenen nur noch dort definiert; README und ARCHITECTURE verweisen.
- Veraltete Behauptungen korrigiert: ARCHITECTURE nannte noch „Secret-Leaks", `CONS-004`
  sprach von `quality_gates`, das `Domain`-Docstring von `STATUS.md` als Pflicht.
- CI-Vorlage mit `permissions: contents: read`; Vorlagen `CLAUDE.md`/`README.md` markieren
  `STATUS.md` als optional.

**Nicht geändert:** die ADR-0008-Strenge (OD-2 bleibt offen), das Manifest-Schema, der
Report-Wortlaut.

## 2026-09-02 — Zweiter Fremdtest: das Werkzeug gegen sich selbst

**Anlass**

Nach dem Refinement wurde `foundation-validate` erneut gegen `AI-Idle-Agent` gerichtet — dasselbe
gewachsene Godot-Repo, das schon der erste Fremdtestfall war. Diesmal als Vorher/Nachher: Stand
`687a557` (vor dem Refinement) gegen `0.2.0`, beide gegen denselben Commit des Zielprojekts.
Gelesen wurde nur; im Zielprojekt wurde nichts geändert.

| | Blocker | Warnungen | Ergebnis |
| --- | --- | --- | --- |
| vorher | 1 (`STRUCT-010`) | 1 (`STAT-003`) | `FOUNDATION NOT READY` |
| nachher | 0 | 2 (`ADR-010`, `STAT-003`) | `FOUNDATION VALID` |

**Befund 1: Die neue Warnung sagte etwas Falsches**

`ADR-010` meldete „und es gibt kein ADR". Das Projekt hat 14 ADRs in `docs/adr/` — der Validator
kannte sie sogar, `_decision_dir_near_misses()` hatte sie im alten Blockertext korrekt als
„docs/adr/ (14 ADR-Dateien)" genannt. Die neue Meldung benutzte dieses Wissen nicht und behauptete
das Gegenteil. Das verletzt ADR-0008: den Beinahe-Treffer nennen, statt den Anwender raten zu
lassen.

Behoben. `ADR-010` nennt jetzt Verzeichnis und Anzahl und warnt zusätzlich vor dem Blocker, den
ein `REQUIRED` auslösen würde — dieselbe Vorwarnung, die `_folgepruefung()` schon für fehlende
Pflichtdateien gibt. Ein Test sichert es ab.

**Befund 2: Der Anreiz steht falsch herum**

Der Blocker verschwand nicht, weil jemand ihn für falsch hielt, sondern weil das Zielprojekt die
Zeile `Architecture Decisions` nicht hat. Trüge es ehrlich `REQUIRED` ein — und es hat tragende
Entscheidungen, dokumentiert bis ADR 0013 —, bekäme es `STRUCT-010` zurück. **Wer die Frage ehrlich
beantwortet, zahlt; wer schweigt, kommt billiger weg.** Beim Entwurf von ADR-0011 nicht bedacht.

Entschieden: Die Strenge aus ADR-0008 wird nicht auf Verdacht aufgeweicht. Die Schieflage ist als
`OD-2` in `docs/PROJECT.md` festgehalten und wird neu aufgemacht, wenn ein zweites Fremdprojekt
zeigt, dass sie in der Praxis beißt.

**Nebenbei bestätigt**

- Rückwärtskompatibilität: Das dortige Manifest hat noch alle elf früher verlangten Felder und
  läuft anstandslos durch. „Es entfallen nur Anforderungen" stimmt nicht nur auf dem Papier.
- Windows: Lauf gegen ein gewachsenes Repo, ASCII-Rahmen, kein Absturz (NFR-5).
- Das Manifest des Zielprojekts ist jetzt veraltet (`blocking_issues: 1` für einen Blocker, den es
  nicht mehr gibt). Kein `CONS`-Befund, weil nur „READY trotz Blockern" geprüft wird — richtig so,
  `READY` ist eine Ebene-2-Aussage. Nachzuziehen ist das drüben, nicht hier.

**Lehre**

Die Selbstprüfung konnte beides nicht finden. Beide Befunde brauchten ein Repo, das nicht mit
diesem Werkzeug gebaut wurde — wie schon beim ersten Mal.

## 2026-09-02 — Ehrlichkeit statt Reichweite

**Anlass**

Eine Architektur- und Produktkritik am eigenen Werkzeug. Kern: Das Toolkit behauptete an
drei Stellen mehr, als es belegen kann, und zwang jedem Projekt denselben Umfang auf.

**1. Der Validator sagte READY**

Ein Programm, das Dateien und Statuswerte liest, gab denselben Satz aus, mit dem der
vollständige Prozess endet. Der Warnsatz daneben („ein grüner Validator ist keine gute
Foundation") verliert diesen Wettbewerb — zitiert wird, was auf dem Bildschirm steht.

Jetzt: `FOUNDATION VALID` / `FOUNDATION INVALID`, Kopfzeile `PROJECT FOUNDATION
VALIDATION`. Dazu zwei kleinere Unehrlichkeiten beseitigt: Der Domänenstatus übernahm
hilfsweise den in `STATUS.md` **erklärten** Wert (fremde Selbstauskunft als eigenes
Urteil), und `Development Setup` sowie `CI/CD & Infrastructure` wurden als `PASS`
gemeldet, obwohl es für sie keine einzige Regel gibt — jetzt `NOT CHECKED`. Siehe
ADR-0010.

**2. Jedes Projekt brauchte mindestens ein ADR**

`ADR count == 0 → BLOCKED` behandelt „es gab keine tragende Entscheidung" wie „sie wurde
verschwiegen". Bei kleinen Projekten ist der erste Fall der Normalfall, und die Regel
produzierte dort Alibi-ADRs.

Jetzt beantwortet das Projekt die Frage selbst: eine Zeile `Architecture Decisions` mit
`REQUIRED` oder `NOT REQUIRED` in `docs/ARCHITECTURE.md`. Bei `REQUIRED` blockiert ein
fehlendes ADR wie bisher, bei `NOT REQUIRED` nicht. Fehlt die Aussage ganz und gibt es
kein ADR: Warnung `ADR-010`. Dieselbe Logik traf `STATUS.md` — jetzt optional
(`STRUCT-002` zurückgezogen) — und die AI-Frage, die `AGENTS.md` genauso beantwortet wie
`CLAUDE.md`. Siehe ADR-0011.

**3. Das Manifest wuchs zur zweiten Dokumentation**

Elf Pflichtfelder, vier davon gelesen. `stack`, `architecture`, `infrastructure`,
`quality_gates`, `project.type`, `project.maturity` standen doppelt — einmal im Dokument,
einmal maschinenlesbar. Pflicht sind jetzt `schema_version` und `foundation.status`;
alles andere wird geprüft, wenn es da ist. Bestehende Manifeste bleiben gültig, es
entfallen nur Anforderungen, deshalb weiter `schema_version: 1`.

**Nebenbei**

- „NO CODING BEFORE FOUNDATION READY" ist präzisiert: Foundation Work immer erlaubt,
  Bugfixes mit bekanntem Scope erlaubt, nur Feature-Arbeit wartet. Die Regel richtet sich
  gegen stillschweigend durch Code getroffene Architekturentscheidungen, nicht gegen
  einen Einzeiler.
- Secret-*Hygiene* heißt jetzt so und wird nicht mehr „Secret-Erkennung" genannt. Für
  echtes Scanning wird auf `gitleaks` und GitHub Secret Scanning verwiesen, ohne selbst
  eine Engine zu bauen.
- Windows: Dateien werden als `utf-8-sig` gelesen (BOM), die Ausgabe fängt
  `UnicodeEncodeError` ab, und die CI läuft zusätzlich auf `windows-latest`.
- Tests: zwei redundante entfernt (eine zweite Prüfung derselben Pflichtdatei, eine
  Abwesenheitsprüfung, die die positive Variante schon abdeckt), fünf für die neuen
  Regeln ergänzt. 44 Tests.
- Version auf `0.2.0`. Die Ausgabe hat sich gebrochen geändert (`FOUNDATION READY` →
  `FOUNDATION VALID`, `Result.ready` → `Result.valid`); wer dagegen skriptet, soll das
  an der Nummer sehen und nicht erst am Laufen. Ein Release-Artefakt gibt es weiterhin
  nicht (ADR-0006) — die Nummer steht nur in den Manifesten.

**Nicht geändert**

Der Audit-Report des Skills bleibt Wort für Wort, inklusive `FOUNDATION READY`. Er gehört
zu Ebene 2 — dort ist der Satz richtig. Geändert wurde nur, wer ihn sagen darf.

## 2026-09-01 — Folgeprüfungen werden angekündigt

**Anlass**

Rückmeldung aus dem Projekt, das als erster Fremdtestfall diente: Das Erfüllen von
STRUCT-005 erzeugte dort drei *neue* Blocker (ARCH-006, ARCH-007, ARCH-013). Die
Blockerzahl stieg von 4 auf 6, bevor sie fiel.

**Ursache**

`_check_architecture()` und `_check_project()` kehren sofort zurück, wenn ihre Datei fehlt.
Solange sie fehlt, meldet der Validator genau einen Blocker; sobald sie existiert, kommen
bis zu drei blockierende und zehn warnende ARCH-Befunde hinzu. Für den Anwender sieht das
aus, als habe das Beheben eines Blockers die Lage verschlechtert.

Dieselbe Falle steckt in `docs/PROJECT.md` (sechs Pflichtabschnitte) und in
`docs/decisions/` (ADR-Format). Bei PROJECT.md war sie bekannt und wurde dem Fremdprojekt
vorab mitgeteilt — aber eben mündlich, aus dem Kopf dessen, der den Validator kennt. Genau
dieses Wissen fehlt jedem, der das Werkzeug zum ersten Mal benutzt.

**Änderung**

`required_action` kündigt jetzt an, was nach dem Anlegen zusätzlich geprüft wird. Die Zahlen
und Namen stammen aus den Konstanten (`PROJECT_SECTIONS_REQUIRED`, `CORE_AREAS`,
`SECURITY_CRITICAL_AREAS`, `ADR_SECTIONS`), damit der Hinweis nicht veraltet, wenn jemand
eine Prüfregel ergänzt.

Keine neue Prüfregel, keine geänderte Schwere — nur der Aufwand ist vorher sichtbar.

## 2026-09-01 — Erster Einsatz gegen ein Fremdprojekt

**Anlass**

Das Toolkit wurde zum ersten Mal gegen ein Repo gerichtet, das nicht mit ihm gebaut wurde
(ein gewachsenes Godot-Projekt). Drei Mängel traten sofort zutage — alle drei erst dann,
weil das Repo bis dahin nur sich selbst geprüft hatte.

**1. Der Validator lief unter Windows überhaupt nicht**

`UnicodeEncodeError` beim allerersten Aufruf, ausgelöst von den Rahmenzeichen der Kopfzeile
auf einer cp1252-Konsole. Behoben durch `stream_supports_box()` mit ASCII-Rahmen als
Rückfallebene; als Regel festgehalten in ADR-0007. Der Regressionstest erzwingt die Codepage
über einen `TextIOWrapper` und läuft damit auch auf dem Linux-CI.

**2. Vier Blocker, davon zwei reine Benennungsdifferenzen**

`docs/adr/` statt `docs/decisions/`, `docs/v2-architektur.md` statt `docs/ARCHITECTURE.md`.
Die Substanz war da, der Validator sah sie nicht. Entschieden wurde gegen Aliase und für
strikte Pfade mit aussagekräftiger Meldung (ADR-0008): Das Finding bleibt BLOCKING, nennt
aber den gefundenen Kandidaten samt Anzahl der ADR-Dateien. Aliase im Manifest schieden aus,
weil im konkreten Fall das Manifest selbst fehlte — eine Konfiguration, die Konformität
voraussetzt, hilft dem nicht-konformen Projekt nicht.

**3. Eine Ursache erzeugte acht identische Warnungen**

Wenn `STATUS.md` dem Format gar nicht folgt, meldete der Validator achtmal STAT-001, einmal
je Domäne. Jetzt gibt es dafür eine einzige Warnung STAT-003; STAT-001 bleibt für den Fall,
dass tatsächlich nur einzelne Domänen fehlen.

**Nebenbei**

Die `STRUCT-`IDs hingen an der Position in `REQUIRED_FILES` und hätten sich beim Umsortieren
verschoben — trotz Docstring „stabile ID". Sie stehen jetzt im Tupel.

**Stand**

24 Prüfregeln, 26 Tests, alle Gates grün. Die Selbstprüfung bleibt `FOUNDATION READY`.

## 2026-09-01 — Foundation aufgesetzt

**Ausgangslage**

Leeres Repository: kein Commit, keine Dateien außer `.git`. Der Discovery-Report ergab
für jede Domäne `UNKNOWN` und fünf Blocker — kein verwertbares Signal, also wurde vor der
Generierung nachgefragt statt geraten.

**Getroffene Entscheidungen**

Vier Grundsatzfragen wurden vom Auftraggeber beantwortet und als ADRs festgehalten:

- Verteilung als Claude-Code-Plugin über einen Marketplace → ADR-0001
- Skill existiert nur unter `plugins/`, keine zweite Kopie → ADR-0002
- Python 3.11 mit genau einer Laufzeit-Abhängigkeit für den Validator → ADR-0003
- Manifest ist Index, nicht Source of Truth → ADR-0004
- Deutscher Fließtext mit englischen Struktur-Keywords → ADR-0005
- Kein PyPI-Release und kein Build-Schritt → ADR-0006

**Was gebaut wurde**

- Skill `project-foundation` mit `SKILL.md` und vier Reference-Dateien
- 13 Vorlagen für die Foundation-Dateien
- Validator mit 23 Prüfregeln, Audit-Report und Exit-Codes
- 18 Tests: je einer pro Blocking-Regel, drei für die CLI-Schnittstelle
- Plugin- und Marketplace-Manifest
- Beispielprojekt `examples/taskflow` als vollständig ausgefüllte Referenz
- Foundation dieses Repos selbst (Dogfooding)

**Validierung**

`install → format → lint → typecheck → test` lokal ausgeführt, alles grün.
`foundation-validate` läuft für dieses Repo und für das Beispiel ohne Blocker.

**Offen geblieben**

- Ob weitere Review-Skills nötig sind, entscheidet sich erst durch Anwendung (OD-1).

## 2026-09-01 — CI verifiziert

Nach dem Push lief die CI erstmals auf GitHub: Run
[#1](https://github.com/Dimen2608/Projekt-Foundation/actions/runs/33540491731),
Jobs `quality` und `foundation`, beide `success`. Damit war W-2 nur eine
Momentaufnahme vor dem ersten Push und ist erledigt — in `STATUS.md` entfernt.
W-1 (Mutation Testing) bleibt bewusst offen: eine Warning ohne benennbaren
Nutzen zu schließen wäre selbst Overengineering.
