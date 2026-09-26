# ADR-0016: Das Review prüft die Werkzeug-Abdeckung

## Status

Accepted — 2026-09-26

## Context

Die Foundation prüft in der Domäne AI Foundation, ob ein Agent die Regeln des Projekts kennt
(`CLAUDE.md`, `AGENTS.md`, Cursor-Regeln). Sie prüft nicht, ob es für die wiederkehrenden
Aufgaben des Projekts passende Skills oder Agents gibt. Ein Projekt kann damit
`FOUNDATION READY` sein und trotzdem jede Testdatei, jeden Export und jede Migration von Hand
bauen lassen, obwohl ein passendes Werkzeug im Marketplace liegt.

Das Verfahren existierte bisher nur in `project-orchestrate`, `SETUP` Schritt 6 (ADR-0014): Es
ordnet Aufgabenarten Skills oder Agents zu, sucht fehlende im Marketplace und schlägt jeden
Fund einzeln vor. Das greift aber nur, wenn orchestriert wird. Anlass für die Frage war ein
Projekt mit anderem Stack (Godot/GDScript) als das, in dem der Workflow entstanden ist.

## Decision

1. **Werkzeug-Abdeckung ist Teil des Reviews (Ebene 2)**, Domäne AI Foundation, eigener
   Prüfpunkt in der Review-Tabelle und eigener Abschnitt in `reference/audit.md` (nach dem AI
   Readiness Test, nicht darin): Aufgabenarten bestimmen (nur wiederkehrende), Vorhandenes erfassen,
   zuordnen, Lücken im Marketplace suchen, jeden Fund einzeln vorschlagen, nie ohne Bestätigung
   installieren, Ergebnis festhalten.
2. **Nicht im Validator.** Die Marketplace-Suche braucht Werkzeuge der Session und Netz; der
   Validator läuft ohne Netz (Constraint). Keine Finding-ID, `schema_version` bleibt `1`.
3. **Keine Pflichtdatei.** Das Ergebnis steht als optionaler Abschnitt `Werkzeuge` in
   `CLAUDE.md` — nicht in `AGENTS.md`, weil Skills und Agents Claude-spezifisch sind und das
   AGENTS-Template Werkzeugspezifisches ausschließt. Nach ADR-0011 mit der Frage, die er
   beantwortet: „Welcher Skill oder Agent übernimmt welche wiederkehrende Aufgabenart?" Nötig
   nur, wenn das Projekt eigene Skills oder Agents hat (`.claude/skills/`, `.claude/agents/`),
   sich auf Plugins verlässt oder das Review eine Lücke mit Fund findet — nicht schon, weil
   jede Session eingebaute Agents hat.
4. **Nur WARNING, nie BLOCKING.** Eine Lücke ist eine Warnung nur, wenn für eine benannte
   Aufgabenart ein konkreter Fund mit benennbarem Nutzen vorliegt. „Kein Skill für X" ohne
   Fund ist keine Warnung — sonst erzeugt der Audit Aufgaben, deren einziger Zweck es ist, den
   Audit zu beruhigen (`reference/audit.md`, Abschnitt 3). Die Grenze zwischen BLOCKING und
   WARNING verschiebt sich nicht.
5. **Abgelehnte Funde werden notiert**, damit das nächste Review sie nicht wieder vorschlägt —
   dieselbe Logik wie Entscheidungen als Filter.
6. **`project-orchestrate` verweist darauf**, statt ein zweites Verfahren zu führen; ein
   vorhandener Abschnitt `Werkzeuge` ist der Ausgangspunkt für `SETUP` Schritt 6.

Der Wortlaut des Audit-Reports bleibt unverändert (Constraint): Die Werkzeug-Abdeckung
erscheint dort wie jede andere Warnung unter AI Foundation. Version 0.6.0.

Verworfene Alternativen:

- **Als Frage im AI Readiness Test.** Dort gilt „kritische Frage offen → NOT READY"; eine
  fehlende Werkzeugzuordnung macht ein Projekt nicht unbaubar.
- **Als Validator-Regel.** Braucht Netz und Session-Werkzeuge; der Validator behauptet nur,
  was er geprüft hat (ADR-0010).
- **Nur in `project-orchestrate` lassen.** Dann bleibt jedes Projekt ohne Orchestrierung ohne
  die Prüfung.

## Consequences

**Positiv**

- Jedes Projekt bekommt im Review einmal die Frage gestellt, welche Werkzeuge seine
  wiederkehrenden Aufgaben übernehmen.
- Ein Verfahren statt zwei: Foundation und Orchestrate nutzen dieselbe Beschreibung.

**Negativ**

- Das Review wird länger, und die Marketplace-Suche hängt an den Werkzeugen der Session.
  Ergebnisse veralten; der Abschnitt `Werkzeuge` trägt deshalb die Herkunft je Eintrag.

**Grenze**

Neu zu bewerten, wenn das Review regelmäßig Vorschläge ohne Nutzen erzeugt — dann ist die
Warnschwelle zu niedrig.
