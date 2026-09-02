# Review, Consistency Audit, AI-Readiness und Report

Dieser Teil ist **Ebene 2**. Der Validator (Ebene 1) hat vorher geprüft, was maschinell
entscheidbar ist, und `FOUNDATION VALID` gemeldet oder eben nicht. Hier wird beurteilt,
was ein Programm nicht beurteilen kann.

## 0 — Foundation Review

Jeder Punkt bekommt `PASS`, `WARNING` oder `BLOCKED` **mit Begründung**. Keine Punktzahl,
keine Prozentangabe, kein Score — eine Zahl würde Genauigkeit vortäuschen, die hier nicht
existiert.

| Prüfpunkt | Frage |
| --- | --- |
| Scope | Ist der Scope entscheidbar und abgegrenzt? Gibt es ein benanntes `Out of Scope`? |
| Anforderungen | Sind sie konkret genug, um daraus zu implementieren — oder Absichtserklärungen? |
| Architektur | Trägt die Struktur den beschriebenen Scope? Sind die Grenzen begründet? |
| Overengineering | Welche Komponente, Abhängigkeit, Schicht oder Infrastruktur hat keine benennbare Anforderung hinter sich? |
| Unterdimensionierung | Wo fehlt Struktur, die der Scope tatsächlich verlangt? |
| Dokumentationsqualität | Beantworten die Dokumente ihre Frage, oder sind sie nur ausgefüllt? Stehen noch Platzhalter drin? |
| Konsistenz | Siehe Abschnitt 1. |
| Teststrategie | Schützt sie das Risiko dieses Projekts — oder erzeugt sie Zahlen? |
| Security-Konzept | Sind Auth, Datengrenzen und Secret-Handhabung entschieden und dokumentiert? |
| Deployment | Ist der Weg in Betrieb beschrieben, inklusive Fehlschlag? |
| AI-Readiness | Siehe Abschnitt 2. |
| Offene kritische Entscheidungen | Steht etwas offen, das die Implementierung faktisch vorwegnehmen müsste? |

Zwei Regeln für dieses Review:

- **Nicht raten.** Was sich aus dem Repository nicht bestimmen lässt, wird gefragt —
  nicht wohlwollend interpretiert.
- **`NOT REQUIRED` wird geprüft, nicht geglaubt.** Sowohl bei Architektur-Bereichen als
  auch bei `Architecture Decisions`. Ein `NOT REQUIRED`, dem der Code widerspricht, ist
  ein Blocker.

## 1 — Consistency Audit

Vergleiche paarweise: `docs/PROJECT.md`, `docs/ARCHITECTURE.md`, `docs/decisions/`,
`CLAUDE.md`, `AGENTS.md`, `.cursor/rules/`, `STATUS.md`, `.project-foundation.yml` und den
tatsächlichen Code.

Gesucht wird nach:

| Widerspruchstyp | Beispiel |
| --- | --- |
| Technologie | ADR sagt PostgreSQL, ARCHITECTURE sagt MongoDB → **BLOCKED** |
| Architektur | ARCHITECTURE beschreibt Schichten, die im Code nicht existieren |
| Commands | README nennt `npm test`, das Projekt nutzt `pnpm` |
| Veraltete Entscheidung | ADR `Accepted`, aber die Umsetzung ging anders — Status auf `Superseded` und neues ADR |
| Fehlendes ADR | Tragende Entscheidung existiert im Code, aber nirgends dokumentiert - auch dann, wenn `Architecture Decisions` auf `NOT REQUIRED` steht |
| Doppelte Rules | Dieselbe Regel in `CLAUDE.md` und in einer Cursor-Rule |
| Architecture Drift | Code hat sich von der dokumentierten Struktur entfernt |
| Manifest-Konflikt | Manifest meldet `READY`, `STATUS.md` meldet `BLOCKED` |

Jeder gefundene Widerspruch ist ein Blocker, bis er aufgelöst ist. Bei Konflikten gewinnt
die Source of Truth aus `SKILL.md`; das Manifest verliert immer.

## 2 — AI Readiness Test

Ein Agent, der nur dieses Repository kennt, muss folgende Fragen beantworten können:

1. Was bauen wir?
2. Was ist ausdrücklich außerhalb des Scopes?
3. Wie ist die Architektur?
4. Welche Technologien werden verwendet?
5. Wie installiere ich das Projekt?
6. Wie starte ich es?
7. Wie teste ich es?
8. Welche Regeln muss ich befolgen?
9. Wo sind wichtige Entscheidungen dokumentiert?
10. Wie ist der aktuelle Status?
11. Wann muss ich anhalten und fragen?

Kann eine kritische Frage nicht beantwortet werden: **NOT READY**.

Der Test wird ehrlich geführt: „steht sinngemäß irgendwo" zählt nicht. Es muss eine
benennbare Datei geben, die die Frage beantwortet.

## 3 — Blocker und Warnings

**BLOCKING** — unter anderem:

- Kritische Architekturentscheidung offen
- Anwendung lässt sich nicht bauen
- Anwendung lässt sich nicht starten
- Authentication undefiniert (bei Projekten mit Nutzern)
- Authorization undefiniert
- Erforderliche Datenbankstrategie undefiniert
- Erforderliche Deployment-Strategie undefiniert
- Secrets-Strategie fehlt
- Kritische Anforderungen unklar
- Source-of-Truth-Konflikt
- Agent kann wesentliche Constraints nicht bestimmen

**WARNING** — unter anderem:

- Optionale Dokumentation fehlt, obwohl ein Zweck erkennbar wäre
- Ein bewusst hingenommener Zustand ist nirgends als solcher festgehalten
- Staging fehlt, ist aber nicht erforderlich
- Optionale Automatisierung fehlt

Warnings blockieren nicht. Sie werden trotzdem genannt.

Eine Warnung braucht einen benennbaren Nutzen ihrer Auflösung. „Werkzeug X ist nicht
konfiguriert" ist keine Warnung, solange niemand sagen kann, wovor X hier schützen würde
— sonst erzeugt der Audit Aufgaben, deren einziger Zweck es ist, den Audit zu beruhigen.

## 4 — Report-Format

Am Ende **immer exakt** dieses Format ausgeben.

### Ohne Befunde

```
╔══════════════════════════════════════╗
║       PROJECT FOUNDATION AUDIT       ║
╚══════════════════════════════════════╝

Project Definition       PASS
Architecture             PASS
Development Setup        PASS
AI Foundation            PASS
Documentation            PASS
Testing & Quality        PASS
CI/CD & Infrastructure   PASS
Security                 PASS

Blocking Issues: 0
Warnings: 0

========================================

FOUNDATION READY

Implementation may begin.
```

### Mit Befunden

```
╔══════════════════════════════════════╗
║       PROJECT FOUNDATION AUDIT       ║
╚══════════════════════════════════════╝

Project Definition       PASS
Architecture             BLOCKED
Development Setup        PASS
AI Foundation            PASS
Documentation            PASS
Testing & Quality        WARNING
CI/CD & Infrastructure   PASS
Security                 PASS

Blocking Issues: 1
Warnings: 1

========================================

FOUNDATION NOT READY

Blocking Issues:

ARCH-001
Reason:
Authentication architecture is unresolved.

Required action:
Make and document the authentication decision.

Implementation is blocked.
```

Jeder Blocker nennt: **ID**, **Reason**, **Required Action**, **Affected Area**.

Dieser Report ist der **Audit** (Ebene 2) und endet auf `FOUNDATION READY` /
`FOUNDATION NOT READY`. Der Validator gibt einen eigenen, ähnlich aufgebauten Report aus,
der auf `FOUNDATION VALID` / `FOUNDATION INVALID` endet. Die beiden werden nicht
vermischt und nicht gegeneinander ausgetauscht: kein Programm gibt `FOUNDATION READY`
aus, und kein Review gibt `FOUNDATION VALID` aus.

## 5 — Endentscheidung

Es gibt keinen Prozentwert. Nicht `92% READY`. Nur:

```
FOUNDATION READY
```

oder

```
FOUNDATION NOT READY
```

`FOUNDATION READY` nur wenn:

```
ALL REQUIRED DOMAINS PASS
+ ZERO BLOCKING ISSUES
+ REQUIRED VALIDATION PASSED   (Command-Chain ausgeführt, Validator FOUNDATION VALID)
+ NO UNRESOLVED CRITICAL DECISION
```

**Nichts verschweigen.** Ein verschwiegener Blocker taucht später als Fehler in der
Implementierung wieder auf — dann teurer.
