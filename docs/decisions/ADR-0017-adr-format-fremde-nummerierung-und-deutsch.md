# ADR-0017: Fremde ADR-Nummerierung und deutsche Gliederung sind gleichwertig

## Status

Accepted — 2026-09-26. Ergänzt ADR-0008 und ADR-0012.

## Context

Ein Bestandsprojekt (AI-Idle-Agent, 21 ADRs unter `docs/adr/`) führt seine ADRs als
`0001-titel.md` mit deutscher Gliederung: `## Kontext`, `## Entscheidung`, `## Folgen`,
Status als `**Status:** angenommen — …`. Der Ort ist dort per ADR entschieden, die Pfade stehen
in 69 Verweisen, 14 davon im Produktivcode.

Der Validator ging damit widersprüchlich um:

- Beim **Finden** erkennt `ADR_LIKE_RE` fremde Nummerierung (ADR-0008, Beinahe-Treffer).
- Beim **Format** verlangt `ADR_FILENAME_RE` das Präfix `ADR-`: 21 Warnungen ADR-001.
- Nach einem Umbenennen hätte die Formatprüfung englische Überschriften und einen englischen
  Status verlangt: bis zu 42 Blocker (ADR-003, ADR-004) für Entscheidungen, die inhaltlich
  vollständig sind.
- Auch `**Status:** Accepted` in Fettschrift wurde nicht erkannt, nur `Status: Accepted` oder
  der Status unter einer eigenen Überschrift.

ADR-0012 hat dieselbe Lage beim Ort schon so gelöst: Ein Bestandsprojekt kann nicht einfach
umbenennen, also ist der Ort deklarierbar. ADR-0005 (englische Struktur-Keywords) regelt die
Dateien, die dieses Toolkit selbst erzeugt, nicht fremde Bestände.

## Decision

1. **Dateiname:** `ADR-NNNN-titel.md` bleibt die Konvention für neue ADRs (Vorlage). `NNNN-titel.md`
   ohne Präfix ist gleichwertig und keine Warnung mehr. Andere Formen (drei Ziffern,
   Unterstrich) bleiben ADR-001.
2. **Gliederung:** Je Pflichtabschnitt gilt die englische oder die deutsche Überschrift —
   Context oder Kontext, Decision oder Entscheidung, Consequences oder Folgen bzw.
   Konsequenzen. Fehlt ein Abschnitt in beiden Sprachen, bleibt es ADR-003.
3. **Status:** Neben Proposed, Accepted, Rejected, Superseded, Deprecated gelten Vorgeschlagen,
   Angenommen, Abgelehnt, Abgelöst, Ersetzt, Veraltet, Überholt. Ein anderes Wort bleibt
   ADR-004.
4. **Markdown um den Status** (`**Status:** **angenommen**`) stört die Erkennung nicht mehr.

Keine neue Finding-ID, keine Änderung an BLOCKING oder WARNING, `schema_version` bleibt `1`.
Die Ausgabetexte bleiben ASCII (ADR-0007): Die deutschen Statuswörter stehen nur in der
Erkennung, nicht in Meldungen. Je Regel ein Test (ADR-0009). Version 0.7.0.

Verworfene Alternativen:

- **Nur die Nummerierung zulassen.** Das Bestandsprojekt hätte dann 21 ADRs umgliedern müssen,
  ohne inhaltlichen Gewinn.
- **Beim Standard bleiben (ADR-0005).** Dann trägt jedes deutsche Bestandsprojekt dauerhaft
  Warnungen, die niemand auflöst — Warnungen ohne benennbaren Nutzen (`reference/audit.md`).
- **Sprache deklarierbar machen** (wie den Ort in ADR-0012). Mehr Mechanik für denselben
  Effekt; die Überschriften sind eindeutig genug, um beide Sprachen gleichzeitig zu erkennen.

## Consequences

**Positiv**

- Deutsche Bestandsprojekte laufen ohne Umbau durch die Formatprüfung. Das Bestandsprojekt,
  das den Anlass gab, kommt von 21 Warnungen auf 0.
- Die Prüfung findet dort jetzt einen echten Mangel: ein ADR ohne Abschnitt „Entscheidung".

**Negativ**

- Der Validator kennt jetzt zwei Sprachen. Eine dritte käme nur mit neuem ADR.

**Grenze**

Neu zu bewerten, wenn ein Projekt eine weitere Sprache oder ein anderes Nummernschema braucht
— dann ist die deklarierbare Form (verworfene Alternative 3) die bessere.
