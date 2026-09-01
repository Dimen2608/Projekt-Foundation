# ADR-0009: Regelabdeckung statt Mutation Testing

## Status

Accepted — 2026-09-01

## Context

`STATUS.md` führte seit dem Aufsetzen die Warnung W-1: „Mutation Testing ist nicht
konfiguriert." Die Warnung war als bewusst offener Punkt markiert, tauchte damit aber bei
jeder Prüfrunde erneut auf — genau das Muster, gegen das dieses Repo antritt.

Die eigentliche Sorge hinter W-1 steht in `CLAUDE.md`: *„Neue Blocking-Regel im Validator =
neuer Test, der genau diese Regel schützt. Keine Tests, die nur Coverage erzeugen."* Die
Frage ist nicht, ob ein bestimmtes Werkzeug fehlt, sondern ob man sich darauf verlassen
kann, dass jede Prüfregel abgesichert ist.

**Die Messung ergab, dass man sich darauf nicht verlassen konnte.** 25 Regeln existierten
als ID-Literal im Validator, 15 waren in Tests referenziert. Zehn Regeln — `STRUCT-001`,
`STRUCT-002`, `STRUCT-003`, `STRUCT-006`, `MAN-002`, `MAN-003`, `MAN-004`, `ADR-001`,
`ADR-004`, `CONS-002` — waren durch keinen Test geschützt. Die Regel in `CLAUDE.md` war ein
Vorsatz, kein Mechanismus.

## Decision

**Kein Mutation Testing. Stattdessen ein Register aller Finding-IDs plus zwei Meta-Tests.**

Gegen `mutmut` sprach die Beschaffenheit dieses Codes: Der Validator besteht zu einem großen
Teil aus Meldungstexten (`reason`, `required_action`, Hinweistexte). Mutationen daran
erzeugen überlebende Mutanten, die niemanden interessieren, und ertränken die wenigen echten
Funde. Dazu kämen Laufzeit im Minutenbereich und die dauerhafte Pflege einer Whitelist.

`FINDING_IDS` in `validator.py` listet jede ID, die der Validator erzeugen kann. Die
Familien `DEF-` und `ARCH-` werden aus den Konstantenlisten abgeleitet und wachsen mit
ihnen. Zwei Tests in `tests/test_regelabdeckung.py` sichern das ab:

1. **Jede registrierte Regel wird von einem Test geprüft.** Ausgenommen sind `DEF-` und
   `ARCH-`: Sie entstehen je Abschnitt bzw. Architekturbereich aus einer Liste, ein Test je
   Listeneintrag wäre Bürokratie ohne Erkenntnis. Die Familien sind als Ganzes abgedeckt.
2. **Jede ID im Quelltext steht im Register.** Verhindert, dass eine neue Regel am Register
   und damit am ersten Test vorbei eingeführt wird.

Die zehn fehlenden Tests wurden mit dieser Entscheidung geschrieben. Der Abdeckungstest ist
grün, weil die Lücke geschlossen ist — nicht, weil er nachgiebig wäre.

## Consequences

**Positiv**

- Die `CLAUDE.md`-Regel ist erzwungen statt vorgenommen: Wer eine Regel ergänzt und den Test
  vergisst, sieht es rot, und zwar mit Namen der ungeschützten Regel.
- Das Register macht die zweite `CLAUDE.md`-Regel sichtbar — Finding-IDs sind stabil und
  werden nicht umgewidmet. Vorher war das über 500 Zeilen verstreut.
- Laufzeit im Millisekundenbereich, keine zusätzliche Abhängigkeit. ADR-0003 bleibt unberührt.
- W-1 ist beantwortet, nicht wegdefiniert: Die Lücke war real und ist geschlossen.

**Negativ**

- Das Register muss bei neuen ID-Familien von Hand erweitert werden. Der zweite Meta-Test
  fängt das für Literale ab; eine neue *dynamische* Familie (wie `DEF-`) fiele durch beide
  Netze. Das ist die verbleibende Lücke, und sie ist bewusst in Kauf genommen — solche
  Familien entstehen selten und nie versehentlich.
- Ein Test, der auf Quelltext-Suche beruht, ist empfindlich gegen Formatierung: Eine ID, die
  nicht als Literal `"XXX-000"` geschrieben wird, sieht er nicht.
- Mutation Testing bliebe die gründlichere Prüfung. Sollte der Validator deutlich über 50
  Regeln wachsen oder der Anteil an Meldungstext sinken, ist diese Entscheidung neu zu
  bewerten (Status dann `Superseded`).
