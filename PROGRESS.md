# Progress — Projekt-Foundation

> Arbeitsprotokoll. **Niemals Source of Truth** für Architektur oder aktuellen Zustand —
> dafür sind `docs/ARCHITECTURE.md` und `STATUS.md` zuständig.
>
> Neueste Einträge oben.

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
