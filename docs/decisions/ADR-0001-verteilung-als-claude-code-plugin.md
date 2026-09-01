# ADR-0001: Verteilung als Claude-Code-Plugin über einen Marketplace

## Status

Accepted — 2026-09-01

## Context

Das Toolkit soll auf *andere* Projekte angewendet werden. Es braucht also einen Weg, den
Skill samt Vorlagen in ein fremdes Repository zu bekommen. Drei Optionen standen zur Wahl:

1. **Copy-Paste / Repo klonen.** Nutzer kopiert `.claude/skills/…` von Hand.
   Null Infrastruktur, aber keine Updates: jede Kopie driftet sofort ab, und es gibt
   keinen Weg festzustellen, welche Version irgendwo liegt.
2. **Git-Submodule.** Versionierbar, aber Submodule sind erfahrungsgemäß eine dauerhafte
   Reibungsquelle und lösen das Problem der Skill-Erkennung durch Claude Code nicht.
3. **Claude-Code-Plugin mit Marketplace-Manifest.** Der Mechanismus, den Claude Code für
   genau diesen Zweck vorsieht: `/plugin marketplace add <repo>` und `/plugin install`.

## Decision

Wir verteilen als Plugin. Das Repository enthält `.claude-plugin/marketplace.json` als
Marketplace-Definition und das Plugin selbst unter `plugins/project-foundation/`.

Damit ist das Repository gleichzeitig Marketplace und Plugin-Quelle. Für ein Toolkit mit
genau einem Plugin ist eine getrennte Marketplace-Repo-Struktur unnötige Komplexität.

## Consequences

**Positiv**

- Installation in fremde Projekte mit zwei Befehlen, ohne Dateien zu kopieren.
- Updates über den normalen Plugin-Mechanismus.
- Die Verzeichnisstruktur unter `plugins/` ist vorgegeben und damit nicht diskutabel.

**Negativ**

- Die Struktur ist an Claude Codes Plugin-Konventionen gebunden. Ändern die sich, müssen
  wir nachziehen.
- Cursor kann Plugins nicht installieren. Für Cursor bleibt es beim Kopieren der Rule aus
  `templates/cursor-rule.mdc` — bewusst akzeptiert, weil Cursor-Rules ohnehin
  projektspezifisch angepasst werden müssen.

**Verworfen**

Option 1 und 2 aus den oben genannten Gründen.
