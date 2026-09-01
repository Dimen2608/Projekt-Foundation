# Gegen Overengineering

> **The foundation must remain smaller than the system it enables.**

Der teuerste Fehler beim Aufsetzen eines Projekts ist nicht zu wenig Struktur, sondern
Struktur, die niemand braucht und die trotzdem alle mitpflegen müssen.

## Grundfrage

Vor **jeder** Ergänzung — Test, Abstraktion, Dependency, Service, Dokument, Regel,
Infrastruktur:

> Welche konkrete Anforderung dieses Projekts macht das notwendig?

Gibt es keine benennbare Anforderung, wird es nicht hinzugefügt. „Best Practice",
„brauchen wir später sowieso" und „schadet ja nicht" sind keine Anforderungen.

## Tests

Vor dem Hinzufügen eines Tests:

1. Welches Verhalten schützt dieser Test?
2. Ist dieses Verhalten bereits abgedeckt?
3. Ist das die richtige Testebene?
4. Bietet der Test einen eigenständigen Nutzen?
5. Würde sein Entfernen den Schutz spürbar verringern?

> **Test value > test count.**

**Tests sollen:** wichtiges Verhalten schützen, Business-Logik absichern, Regressionen
verhindern, relevante Fehlerfälle abdecken.

**Tests sollen nicht:** Implementierungsdetails festschreiben, Coverage-Zahlen schönen,
andere Tests duplizieren, Framework-Verhalten prüfen, mechanisch jede Funktion abdecken.

Coverage ist ein Indikator, kein Ziel. Mutation Testing ist optional.

## Infrastruktur

> **Infrastructure complexity must be justified by project requirements.**

Eine kleine Anwendung braucht nicht automatisch Kubernetes, Microservices, Kafka, Service
Mesh, Redis, Terraform, Prometheus oder Grafana.

Als Faustregel: Wer die Frage „was passiert, wenn wir das weglassen?" nicht konkret
beantworten kann, braucht es nicht.

## Dokumentation

- Jede Information genau einmal. Sonst driften die Kopien auseinander.
- Optionale Dokumente nur mit konkretem Zweck.
- Kein Dokument, das nur wiederholt, was ein anderes schon sagt.
- Ein Dokument, das niemand liest und niemand pflegt, ist schlechter als keins — es lügt
  irgendwann.

## Agent Rules

- Kleine, fokussierte Regeln statt einer großen Regelwand.
- `globs` verwenden, wenn eine Regel nur bestimmte Dateien betrifft.
- `alwaysApply` nur, wenn die Regel wirklich global gilt.
- Keine Regel, die dasselbe sagt wie eine andere.
- Nicht jede Regel ist ein Skill. Skills sind für wiederverwendbare **Prozesse**.

## Abstraktionen

Ein Interface mit genau einer Implementierung, eine Factory für ein Objekt, eine
Konfigurationsschicht für einen konstanten Wert: das sind Kosten ohne Gegenwert. Erst
abstrahieren, wenn der zweite Fall tatsächlich existiert.
