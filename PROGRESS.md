# Progress — Projekt-Foundation

> Arbeitsprotokoll. **Niemals Source of Truth** für Architektur oder aktuellen Zustand —
> dafür sind `docs/ARCHITECTURE.md` und `STATUS.md` zuständig.
>
> Neueste Einträge oben.

## 2026-10-03 — `project-werkstatt`: Definition of Done, Regeldateien, Vorlagen (0.10.0)

**Anlass**

Die Quelle (Werkstatt-Plan Atemluft V2) hat mit den Teilblöcken 100-5 und 100-6 und ENT-214 samt
zwei Nachträgen Git-Ablauf, Definition of Done, Regeldateien und die Vorlagen aller Sperrpfade
entschieden. Auftrag des Auftraggebers: beides in einem Lauf nachziehen, verallgemeinert.

**Entschieden (ADR-0021)**

Zwei neue Reference-Dateien (`git-und-dod.md`, `regeldateien.md`). Die vier Agent-Vorlagen tragen
den vollen Prompt; fünf Hook-Skripte unter `templates/hooks/`; die vier Skills auf dem Stand der
Quelle als Plugin mit Manifest und sieben Eval-Fällen; Vorlagen für Wurzel-`CLAUDE.md`, Regeldatei,
`settings.json` und Livegang-Liste. Jeder Ladeweg für Anweisungen ist Sperrpfad, in Merge-Skript,
CI und Deny-Regeln. Gate-Marker v1 in Gate, Stop-Hook und Merge-Skript. Mutationsprobe neuer
Wachposten durch den Umsetzer nach dem Bau. Keine Validator-Änderung, Beschreibung unverändert.

**Geprobt**

Hook-Skripte ohne Modell im Wegwerf-Repo: 24 Proben, 0 Abweichungen. Sperrpfad-Muster der CI und
des Merge-Skripts: 10 von 10 Ladewegen erkannt, 0 von 4 Negativfällen.

**Offen**

Hooks mit echtem Payload, Sperr-Hooks der Leitplanken, Proben der Leitplanken und der Isolation,
`maxTurns`, Übergabe der Testdateien aus dem Worktree, Fixture und Baseline der Evals, Stufe 2 des
Katalogs, Lizenzfrage der ASVS-CSV.

## 2026-10-02 — `project-werkstatt`: Leitplanken, ASVS-Baseline, Isolation (0.9.0)

**Anlass**

Die Quelle (Werkstatt-Plan Atemluft V2, Teilblock 100-4) hat Leitplanken, ASVS-Level und Isolation
mit ENT-203 P4, ENT-206 und dem Vierten Nachtrag zu ENT-202 entschieden. Auftrag des
Auftraggebers: den Skill darauf nachziehen, verallgemeinert, ohne ASVS-Text.

**Entschieden (ADR-0020)**

Drei neue Reference-Dateien (`leitplanken.md`, `asvs-baseline.md`, `isolation.md`) und vier neue
Vorlagen (`LEITPLANKEN.md`, `dev-env.py`, `sicherheit/katalog.json`, `sicherheit/nachweise.json`).
Gefüllt wurde der Skill `sicherheits-katalog`. `merge-gruen.py` bekommt den Arbeitskopie-Abgleich
und `LOCKED_FILES`. SKILL.md fragt in KLÄREN nach Laufumgebung, ASVS-Level und Worktree-Pflicht und
führt die Leitplanken in SPERREN in drei Stufen ein. Neu sind zwei Harte Regeln und drei
Stop-Conditions. Der erste Stand aller Sperrpfade kommt aus einer geprüften Vorlage. Keine
Validator-Änderung.

**Offen**

Definition of Done und Git-Ablauf, Agent-Texte, Hook-Skripte, Gate-Marker-Format, die Proben der
Leitplanken und der Isolation, Stufe 2 der Katalogauswahl und die Lizenzfrage zur ASVS-CSV.

## 2026-10-01 — Vierter Skill `project-werkstatt` (0.8.0)

**Anlass**

Entscheidung des Auftraggebers: Das Werkstatt-Muster aus dem Neubau Atemluft V2 (Stand
01.10.2026) wird ein eigener, wiederverwendbarer Skill mit Erklärung — jetzt mit dem entschiedenen
Stand, Offenes sichtbar markiert.

**Entschieden (ADR-0018, ADR-0019)**

Skill `project-werkstatt`: vier Rollen als Agent-Vorlagen (Umsetzer, Test-Autor, Gate, Rückschau),
vier Skill-Vorlagen, CI-Skizze mit Sperrpfad-Wächter und Merge-Vermerk, Merge-Skript-Skizze mit
G-1 bis G-8 und Gate-SHA-Prüfung, Aufsetz-Checkliste; fünf Reference-Dateien (Prinzip und Rollen,
Grün und Gate, Schutz und Deploy, eingebaute Skills und Evals, Walking Skeleton). Die
Agent-Vorlagen dürfen `skills` und `hooks` tragen (ADR-0019); für die Plugin-Agents gilt ADR-0013
unverändert. Keine Validator-Änderung, keine Finding-ID.

**Offen**

Leitplanken und ASVS-Level, Definition of Done, ausformulierte Agent-Texte, Hook-Skripte,
Gate-Marker-Format, wer den ersten Stand der gesperrten Skills und Hooks schreibt. Auslöse-Test
am 2026-10-01 bestanden (STATUS.md), mit geladenem Plugin zu wiederholen.

## 2026-09-26 — ADR-Format: fremde Nummerierung und deutsche Gliederung (0.7.0)

**Anlass**

Im Aufräum-Block eines Bestandsprojekts (21 deutsche ADRs als `0001-titel.md` unter
`docs/adr/`) war „0 Warnungen" nicht erreichbar: 21 × ADR-001, nach einem Umbenennen bis zu 42
Blocker. Entscheidung des Auftraggebers: beides zulassen.

**Entschieden (ADR-0017)**

`NNNN-titel.md` gleichwertig zu `ADR-NNNN-titel.md`; Kontext/Entscheidung/Folgen bzw.
Konsequenzen gleichwertig zu Context/Decision/Consequences; deutsche Statuswörter; Markdown um
den Status stört nicht mehr. Keine neue Finding-ID, keine Verschiebung von BLOCKING/WARNING.

**Geprüft**

Vier neue Tests. Gegenprobe gegen den alten Code: Dateiname, deutsche Gliederung
(einschließlich `Konsequenzen` und `**Status:** Accepted` in Fettschrift) und deutsche
Statuswörter scheitern ohne die Änderung; die beiden Negativtests tragen `ADR-`-Namen, damit sie
die Abschnitts- und die Statusregel unabhängig vom Dateinamen treffen. Mutationsprobe durch das
Tor: jeder Alias wird von einem Test geschützt. Die Status-Erkennung überspringt nach Doppelpunkt
oder Tabellenstrich keine Zeilenumbrüche. Am Bestandsprojekt: 21 Warnungen → 0, dafür ein
echter Fund (ein ADR ohne Abschnitt „Entscheidung").

## 2026-09-26 — `plugin-dev` installiert

Vorschlag aus der Werkzeug-Abdeckung angenommen: Der Auftraggeber hat `plugin-dev` (Anthropic
Directory) installiert. Es ist jetzt für „Skill, Agent oder Vorlage schreiben oder ändern"
zuständig (`CLAUDE.md`, Abschnitt Werkzeuge); die Warnung in `STATUS.md` ist aufgelöst.

## 2026-09-26 — Werkzeug-Abdeckung im Review (0.6.0)

**Anlass**

Frage des Auftraggebers: Prüft das Toolkit, ob einem Projekt passende Skills oder Agents fehlen?
Antwort: nur `project-orchestrate` in `SETUP` Schritt 6, also nur beim Orchestrieren. Anlass
war ein Fremdprojekt mit anderem Stack (Godot/GDScript).

**Entschieden (ADR-0016)**

Werkzeug-Abdeckung als Review-Schritt der Domäne AI Foundation (`reference/audit.md`):
wiederkehrende Aufgabenarten → vorhandener Skill/Agent → Lücke → Marketplace-Suche → einzeln
vorschlagen, nie ohne Bestätigung installieren. Nur WARNING, und nur bei konkretem Fund mit
benennbarem Nutzen. Ergebnis im optionalen Abschnitt `Werkzeuge` von `CLAUDE.md`.
Kein Validator-Teil, keine Finding-ID, keine Pflichtdatei. Orchestrate verweist darauf.

**Geändert**

`project-foundation`: `SKILL.md` (Fragentabelle), `reference/audit.md`, `reference/phases.md`,
`templates/CLAUDE.md`; `project-orchestrate/SKILL.md` Schritt 6; `docs/PROJECT.md` FR-14;
ARCHITECTURE, STATUS; Version 0.6.0.

## 2026-09-26 — Start per Chip geprüft (0.5.3)

Prüfliste 7 ausgeführt: Chip mit `cwd` eines fremden Repos angeklickt. Die Session startete in
einem neuen Worktree dieses Repos mit Remote Control, führte den Startprompt als ersten Turn aus
und meldete sich per `SendMessage`; `list_sessions` fand sie unter dem Worktree-Pfad,
`set_session_title` machte den Worker-Namen sofort zur Adresse. Nebenbefund: Im Worktree fehlte
ein ignoriertes Test-Addon, die Tests liefen dort nicht. Daraus: `WORKER BEREIT` meldet
`befehle`, fehlendes Einrichten ist ein eigener Block; Auflösen der Session-ID am Präfix des
Worktree-Pfads.

## 2026-09-26 — Worker-Verfahren `chip`, Befund zu `start_session` (0.5.2)

**Anlass**

Der Orchestrator sollte eine Worker-Session selbst starten. Auf Claude Desktop fehlt dafür das
Werkzeug `start_session`, das andere Werkzeugbeschreibungen der App nennen.

**Befund**

Im Code der App (Claude Desktop 2.9939.2, Windows) sitzen `start_session`, `hand_off_to_session`
und `list_start_targets` im Server `ccd_session` neben `spawn_task`, geschaltet über ein
serverseitiges Feature-Flag: an → `start_session` statt `spawn_task`, aus → nur der Chip. Kein
Schalter beim Nutzer; die Freigabe ist als anthropics/claude-code#94697 „not planned"
geschlossen, die Doku nennt die Werkzeuge nicht.

**Geändert**

Worker-Verfahren `chip` (`spawn_task` mit `cwd` des Ziel-Repos, Start per Klick) in `SKILL.md`,
`ORCHESTRATE.md`, `BLOCKPLAN.md`, `WORKER-START.md`; Befund und Prüfliste 7 in
`mechanismen.md`; Nachtrag in ADR-0015; Version 0.5.2.

## 2026-09-26 — `project-orchestrate` übernimmt die Lehren aus dem Desktop-Betrieb (0.5.1)

**Anlass**

Gegenlesen von ADR-0014 gegen einen laufenden Betrieb auf Claude Desktop (Kopf-Session plus zwei
Arbeits-Sessions, seit 2026-08-28). Fünf Lücken, eine davon bricht den Ablauf: Ein Worker, der
sich nach der Übergabe leert, verliert mit dem Startprompt seine Rolle.

**Entschieden (ADR-0015)**

Worker-Gedächtnis `.claude/worker.md` (nie committet) plus Worker-Kopf in jedem Auftrag und
`WORKER UNBEKANNT` als Rückfall; Session-Werkzeug von Claude Desktop in `mechanismen.md` (Wecken
per Session-ID, Transkript lesen, Selbst-Leeren — geprüft 2026-09-23); erst lesen, dann schicken;
eine Nachricht ist nie eine Freigabe, Freigaben holt der Worker direkt beim Menschen und meldet
`BLOCK <ID> WARTET freigabe`; gesperrte Befehle nicht umgehen, sondern als exakten Befehl an den
Menschen (`WARTET befehl`); `max_parallel_blocks` als Kontingent-Bremse.

**Geändert**

`SKILL.md`, alle vier Vorlagen, `reference/mechanismen.md`, Agent `orchestrate-blockarbeiter`
(Sperren nicht umgehen); Version 0.5.1; ARCHITECTURE, STATUS nachgezogen.

**Geprüft**

Format, Lint, Typecheck und 54 Tests grün; `foundation-validate .` und `examples/taskflow`
weiterhin `FOUNDATION VALID`; `claude plugin validate --strict` grün für Plugin und Marketplace.
Gegenlesung durch einen Opus-Gutachter in drei Runden: Runde 1 drei blockierende Funde
(Blockarbeiter-`blocked` lief als `FRAGE` über den Orchestrator, `WORKER UNBEKANNT` unerreichbar,
Selbst-Leeren über Rechnergrenzen ohne Wecken), Runde 2 einer (`NACHARBEIT` erreicht einen
geleerten Worker nicht), Runde 3 Freigabe; alle Funde und Vorschläge eingearbeitet.

## 2026-09-26 — Dritter Skill `project-orchestrate`: eine Hauptsession steuert Worker in Blöcken (0.5.0)

**Anlass**

Wunsch des Auftraggebers: ein Multi-Session-System — ein Orchestrator steuert andere Sessions,
echte Sessions auch in anderen Repos, per Remote Control erreichbar und per `SendMessage`
ansprechbar; Aufgaben immer als Blöcke; am Ende jedes Blocks eine
Übergabe an die Hauptsession, danach leert die Unter-Session ihren Kontext. Vorher prüfen, was
Claude Code heute kann, und offene Fragen per Interview klären.

**Geprüft, bevor entschieden wurde** (Cloud-Session, Claude Code 2.1.283, und code.claude.com/docs)

- `claude -p --session-id` und `--resume`: ausgeführt, Start mit fester ID, JSON-Rückgabe,
  Wiederaufnahme mit erhaltenem Kontext.
- `claude --bg`: vorhanden; scheiterte außerhalb des Repos am Workspace-Vertrauen, mit
  `bypassPermissions` vom Auto-Mode-Klassifikator abgelehnt — nicht umgangen.
- Cloud-Session per Remote-API: gestartet, Status gelesen, archiviert. Die Antwort der
  Kind-Session ist vom Starter aus nicht lesbar — daraus folgt die Übergabe über Datei statt Chat.
- Subagent-Tiefe in der Cloud 1 (Doku: 3); Agent Teams experimentell; kein Werkzeug zum
  Selbst-Leeren in der Cloud.

**Entschieden (ADR-0014)**, in einem Interview mit 20 Fragen, je mit Empfehlung

Worker sind eigenständige Sessions, Blockarbeit läuft in einem Subagent (dessen Ende ist das
Leeren); Worker werden angebunden, nicht gespawnt — der Mensch öffnet sie mit Remote Control,
`claude --bg` nur auf Wunsch, Cloud-Sessions sind als Worker nicht vorgesehen; der Orchestrator
läuft mit Remote Control; Heimat-Repo plus fremde Repos, alles unter `orchestrate/` auf einem
`state_branch` committet; Übergabe per `SendMessage`, die Blockdatei ist die Wahrheit; der
Orchestrator baut nicht; Tor je Block, Runden zählt nur der Worker, höchstens fünf, dann
`exhausted` und Vorlage mit Pro und Contra; Vorbereitungsblöcke laufen im Worker selbst; parallel nur
ohne offene Abhängigkeit und nie zwei Worker auf einem Branch; sechs Pflichtfelder je Block;
Merge-Modus konfigurierbar (Standard: der Mensch mergt); `SETUP` als Installer-Interview, das
Skills sucht und einzeln zur Installation vorschlägt; `FOUNDATION VALID` je Repo, sonst ist der
erste Block die Foundation. Keine Validator-Änderung, keine Finding-ID, `schema_version` bleibt 1.

**Geändert**

- Neu: `skills/project-orchestrate/` mit `SKILL.md`, vier Vorlagen (`ORCHESTRATE.md`,
  `BLOCKPLAN.md`, `BLOCK.md`, `WORKER-START.md`) und `reference/mechanismen.md` (Befunde mit
  Datum und Version, Prüfliste für die ungeprüften Stellen).
- Neu: Agents `orchestrate-blockarbeiter` (`sonnet`/`high`) und `orchestrate-tor`
  (`opus`/`high`, lesend, `isolation: worktree`).
- `plugin.json`, `marketplace.json`, `pyproject.toml`, `__init__.py`: 0.5.0. README, PROJECT
  (Scope, V1, Out of Scope abgegrenzt, FR-13), ARCHITECTURE, STATUS, AGENTS, CLAUDE nachgezogen.

**Geprüft**

Format, Lint, Typecheck und 54 Tests grün; `foundation-validate .` und `examples/taskflow`
weiterhin `FOUNDATION VALID`; `claude plugin validate --strict` grün für Plugin und
Marketplace. Headless mit `--plugin-dir`: alle fünf Agents registriert. Gegenlesung durch einen
Opus-Gutachter: vier blockierende Funde — Runden doppelt gezählt und Statuswerte uneindeutig,
Cloud-Worker ohne durchgehenden Kanal, Übergabe-Datei im Worker-Branch außerhalb der
Umfangsgrenze, Foundation-Block im Subagent nicht ausführbar —, alle behoben (die letzten drei
durch die Entscheidungen „keine Cloud-Worker" und „Vorbereitungsblock im Worker"); dazu
Push vor dem Tor, Basis-Commit im Eingang, FR-1-Zitat, `Purpose` und ADR-Zählung. **Auslöse-Test**, je ein
Satz, der nicht wörtlich in den Beschreibungen steht: Foundation-Satz → `project-foundation`,
Rethink-Satz → `project-rethink`, „Hauptsitzung soll die Arbeit aufteilen, andere Sitzungen in
Frontend- und Backend-Repo beauftragen und die Ergebnisse einsammeln" → `project-orchestrate`,
„Tippfehler in der README" → keiner. Nach der Änderung der `description` (Remote Control)
wiederholt, mit „auf Notebook und Desktop je eine Sitzung in unterschiedlichen Repos, diese soll
sie steuern, Arbeitspakete schicken, Ergebnisse einsammeln" → `project-orchestrate`; die übrigen
unverändert.

**Offen**

Die Prüfliste in `reference/mechanismen.md` — vor allem Rückkanal über Rechnergrenzen und
Selbst-Leeren auf Claude Desktop, die aus der Cloud-Session nicht prüfbar waren.

## 2026-09-11 — Zweiter Skill `project-rethink`, das Plugin liefert Agents aus (0.4.0)

**Anlass**

Ein Prozess, der in einem Fremdprojekt entstanden ist und sich dort bewährt hat, lag
entprojektiert als Entwurf vor: `MEASURE → MAP → GAPS → DECIDE → GUARD → HANDOFF` für Projekte,
deren Dokumente und Code auseinandergelaufen sind. `project-foundation` setzt voraus, dass jemand
sagen kann, was das System heute tut — Rethink ist der Weg davor und endet in `DISCOVER`. Der
Einbau lief nach dem eigenen Prozess, nicht durch Kopieren.

**Entschieden (ADR-0013)**

Zweiter Skill im selben Plugin; Abgrenzung in beiden `description`-Feldern; keine
Validator-Änderung, keine Finding-ID, `schema_version` bleibt 1; die drei Rollen (Umsetzer,
Gutachter als Tor, Zahlenprüfer) als Agent-Definitionen unter `plugins/project-foundation/agents/`,
weil nur Agents Isolation und eine erzwungene Werkzeugliste bekommen. Gegen die Stop Condition zu
ADR-0001 geprüft: `agents/` ist Teil der vorgegebenen Plugin-Konvention, keine Änderung daran.

**Geändert**

- Neu: `skills/project-rethink/` mit `SKILL.md`, `reference/grundsaetze.md` (36 Grundsätze) und
  sieben Vorlagen. Aus dem Entwurf nicht übernommen: `BOARD.md` (keine eigene Frage,
  Projektmanagement ist `Out of Scope`) und `reference/herkunft.md` (nur für den Auftraggeber).
  `TOR-PROMPT.md` um das gekürzt, was die Agent-Definition ohnehin trägt; Maintainer-Notizen zu
  Modell und Effort aus den Agent-Prompts ins ADR verschoben.
- Foundation-`description` um den Satz ergänzt, der Rethink-Fälle abgibt.
- `plugin.json`, `marketplace.json`, `pyproject.toml`, `__init__.py`: 0.4.0. README, PROJECT
  (Scope, V1, FR-12), ARCHITECTURE (Plugin-Schnitt, Agents, Prüfung von Prompt-Material),
  STATUS, AGENTS, CLAUDE (Faktenstand, eine verschärfende Stop Condition) nachgezogen.

**Geprüft**

`claude plugin validate --strict` grün für Plugin und Marketplace; Format, Lint, Typecheck und
54 Tests grün; `foundation-validate .` weiterhin `FOUNDATION VALID`. Plugin lokal aus dem
eigenen Marketplace installiert (ADR-0002); `claude plugin details` zeigt zwei Skills und drei
Agents. Gegenlesung durch einen Opus-Gutachter: drei blockierende Funde (zwei divergente
Phasentore in `ABLAUF.md`, ein toter Verweis „Maskenverzeichnis" im Zahlenprüfer, `STATUS.md`
ohne den offenen Auslöse-Test), alle behoben; dazu der Foundation-Abgrenzungssatz auf Rethinks
Kriterium „Ist-Zustand nicht mehr beschreibbar" verschärft, damit er bei gewöhnlicher Drift nicht
zu viel abgibt.

**Auslöse-Test**, je ein Satz, der nicht wörtlich in den Beschreibungen steht, ausgeführt als
Subagenten in einer Session mit geladenem Plugin (`claude -p` war an einer abgelaufenen
CLI-Anmeldung gescheitert):

- „Ich will hier mit der Implementierung anfangen. Ist das Repo dafür vorbereitet, und was fehlt
  noch an Grundlagen?" → `project-foundation`. Befund: `FOUNDATION READY`, nichts nachzuziehen.
- „Bei uns beschreiben die Dokumente ein System, das der Code längst nicht mehr ist, und jede
  Prüfrunde macht aus denselben Themen neue Tickets. Niemand kann sagen, was das System heute
  wirklich tut. …" → `project-rethink`. Befund auf diesem gesunden Repo: Drift nicht messbar,
  Finding-ID-Zahl in `STATUS.md` gegen `FINDING_IDS` nachgezählt und stimmig; der Skill hat sich
  mit seinem eigenen Abgrenzungssatz für unzuständig erklärt und **keine Arbeit erzeugt** — die
  Probe aus dem Einbau-Auftrag („wenn er auf einem gesunden Projekt Arbeit erzeugt, ist er zu
  groß") ist damit bestanden.

## 2026-09-03 — OD-2 entschieden: der Entscheidungsort ist deklarierbar (0.3.0)

**Anlass**

Atemluft.Cloud führt 45 ADRs in einer Sammeldatei mit eigenem Indexwerkzeug. Bei ehrlichem
`REQUIRED` hätte das Projekt umbauen, lügen oder ein Alibi-ADR ablegen müssen. ADR-0008 hatte als
Preis „umbenennen" angenommen; das trifft hier nicht. Gleichzeitig hat der Test gezeigt, dass die
Strenge bei `docs/PROJECT.md` und `docs/ARCHITECTURE.md` genau die Fragen erzwingt, die dem Projekt
fehlten (`Out of Scope`, Security-Tabelle). Also nicht die Konvention aufgeben, sondern die eine
Stelle öffnen, an der sie keine Frage beantwortet.

**Entschieden (ADR-0012)**

Die Zeile `Architecture Decisions | REQUIRED | <Ort>` darf den Ort nennen. Verzeichnis: geprüft
wie `docs/decisions/`. Sammeldatei: nur Einträge gezählt, Format ausdrücklich nicht geprüft. Ort
fehlt oder zeigt aus dem Projekt: `STRUCT-010`. Ohne Angabe bleibt alles wie bisher. Acht neue
Tests in `tests/test_entscheidungsort.py`, keine neue Finding-ID. Version 0.3.0, weil sich das
Verhalten des Validators ändert.

**Wirkung auf Atemluft:** mit einer Zeile in einer künftigen `docs/ARCHITECTURE.md` ehrlich
`REQUIRED` — und damit ein Blocker weniger, ohne eine Datei zu verschieben.

## 2026-09-03 — Dritter Fremdtest: Atemluft.Cloud, und drei Modelle auf Ebene 2

**Anlass**

Erster Lauf des Werkzeugs gegen ein großes, produktives Projekt (Monorepo, 45 ADRs, 18 Workflows,
eigene Doku-Struktur) — und zugleich die erste Ausführung von Ebene 2 durch Agenten. Frage
dahinter: reicht ein günstigeres Modell für das Review? Nur gelesen, im Zielprojekt nichts geändert.

**Ebene 1**

Fünf Blocker, davon einer falsch: `SEC-001` meldete ein lokales `.env`, das `.gitignore` per
`.env*` ausschließt — der Normalfall jedes Checkouts. Behoben (#12). Die vier übrigen sind
Pfad-Blocker aus der eigenen Doku-Struktur des Projekts; alle drei Reviewer hielten die Fragen
dahinter für beantwortet. Das ist OD-2 in Reinform, unverändert offen.

**Ebene 2, Aufbau**

Eine Discovery (Sonnet, 33 Dateien, ~296k Tokens), dann drei Reviews mit wortgleichem Auftrag auf
demselben Report, Budget 15 Dateien. Jeder Blocker wurde vom PA an der Fundstelle nachgelesen.

| | Sonnet | Opus | Fable |
| --- | --- | --- | --- |
| Blocker, belegt | 2 | 6 | 7 |
| Falsche Befunde | 1 | 0 | 0 |
| Tokens | ~171k | ~190k | ~180k |

**Befund**

- Opus und Fable liegen nah beieinander, Sonnet weit dahinter. Erst die Vereinigung von Opus und
  Fable ergibt das vollständige Bild (10 belegte Blocker, bester Einzelner 7). Zwei verschiedene
  Reviewer schlagen ein besseres Modell.
- Sonnets Fehler: „Rollback fehlt" nach Durchsuchen von zwei Dateien; er stand in einer dritten.
  Daraus eine Regel in `reference/audit.md`: *Nicht gefunden ist nicht fehlt.*
- Alle drei haben die Warnungsregel („benennbarer Nutzen") angewendet und die vier Pfad-Blocker
  bewusst nicht wiederholt. Die Ebene-2-Logik aus ADR-0011 trägt.
- Das Werkzeug hat in Atemluft neun belegte Widersprüche gefunden, fast alle vom Typ „richtig
  entschieden, am zweiten Fundort nicht nachgezogen". Der Auftrag dorthin folgt, sobald das
  Toolkit sauber ist.

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
