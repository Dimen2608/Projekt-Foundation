# ADR-0008: Pfadkonvention bleibt strikt, Beinahe-Treffer werden nur gemeldet

## Status

Accepted — 2026-09-01

## Context

Beim ersten Einsatz gegen ein fremdes Projekt (ein gewachsenes Godot-Repo) meldete der
Validator vier Blocker, von denen zwei reine Benennungsdifferenzen waren:

| Erwartet | Vorhanden |
| --- | --- |
| `docs/decisions/` | `docs/adr/` mit 11 ADR-Dateien |
| `docs/ARCHITECTURE.md` | `docs/v2-architektur.md` |
| `docs/PROJECT.md` | `KONZEPT.md` |

Inhaltlich war die Substanz da. Der Validator sah sie nicht und meldete „fehlt" — was
formal stimmt, aber wie ein Fehlalarm wirkt und den Nutzer im Unklaren lässt, ob das
Werkzeug seine Doku übersehen hat oder sie nur anders heißt.

Drei Wege standen zur Wahl:

1. **Aliase im Manifest** — das Projekt deklariert seine Pfade in `.project-foundation.yml`.
2. **Feste Aliase im Validator** — `docs/adr/` ≙ `docs/decisions/` fest verdrahtet.
3. **Strikt bleiben, besser melden.**

Gegen (1) spricht ein struktureller Einwand: Im konkreten Fall fehlte `.project-foundation.yml`
selbst — es war Blocker Nummer drei. Eine Konfiguration, die erst existiert, wenn das Projekt
bereits konform ist, hilft dem nicht-konformen Projekt nicht. Zusätzlich dürfte jedes Projekt
die Konvention neu erfinden; der Validator prüfte dann nur noch Selbstkonsistenz statt einer
gemeinsamen Struktur.

Gegen (2) spricht, dass die Alias-Liste mit jedem neuen Projekt wächst und am Ende niemand
mehr sagen kann, was eigentlich gilt.

## Decision

**Die Pfadkonvention bleibt Pflicht. Kein Alias erfüllt sie — weder konfiguriert noch
eingebaut.**

Der Validator sucht bei einer fehlenden Pflichtstelle jedoch nach plausiblen Kandidaten
(`NEAR_MISS_GLOBS`, `DECISION_DIR_CANDIDATES`) und nennt sie in der Meldung:

```
Verzeichnis docs/decisions/ fehlt. Gefunden wurde stattdessen: docs/adr/ (11 ADR-Dateien).

Required action:
docs/decisions/ anlegen und mindestens ein ADR schreiben - oder docs/adr/ dorthin
umbenennen, falls dort bereits die Architekturentscheidungen liegen.
```

Zwei Eigenschaften sind dabei wesentlich:

- **Der Treffer ist eine Meldung, keine Anerkennung.** Das Finding bleibt BLOCKING. Ein Test
  sichert das ab, damit aus dem Hinweis nicht schleichend eine Duldung wird.
- **Die Formulierung bleibt im Konjunktiv** („falls die Datei dieselbe Rolle erfüllt"). Der
  Validator kann nicht wissen, ob `KONZEPT.md` wirklich eine Projektdefinition ist. Er
  behauptet es deshalb nicht, sondern legt die Entscheidung dem Menschen vor.

Höchstens drei Kandidaten werden genannt (`MAX_NEAR_MISSES`), sonst wird aus der Meldung
ein Verzeichnisdump.

## Consequences

**Positiv**

- „Foundation" bleibt eine Konvention statt einer Geschmacksfrage. Zwei Projekte mit grünem
  Validator haben dieselbe Struktur — das ist der ganze Zweck des Werkzeugs.
- Der Nutzer erfährt in derselben Zeile, was fehlt *und* was er vermutlich stattdessen hat.
  Der Weg von NOT READY zu READY ist damit eine Umbenennung, kein Rätsel.

**Negativ**

- Bestehende Projekte müssen umbenennen, auch wenn ihre Doku inhaltlich vollständig ist.
  Das ist der bewusst in Kauf genommene Preis. Bei einem Projekt mit gewachsener, umfangreicher
  Dokumentation kann das Widerstand erzeugen.
- Die Kandidatenlisten sind Heuristik und werden nie vollständig sein. Sie dürfen wachsen,
  aber nur als Hinweisquelle — sobald ein Eintrag anfängt, eine Pflicht zu *erfüllen*, ist
  dieses ADR verletzt.
