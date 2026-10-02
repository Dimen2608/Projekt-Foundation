# ADR-0020: `project-werkstatt` bekommt Leitplanken, ASVS-Baseline und Isolation

## Status

Accepted — 2026-10-02

## Context

ADR-0018 hat `project-werkstatt` mit dem Stand vom 01.10.2026 gebaut und drei Teile als offen
markiert: Leitplanken mit ASVS-Level (der Skill `sicherheits-katalog` war ein Gerüst), die
Isolation je Session und die Frage, wer den ersten Stand der gesperrten Skills und Hooks
schreibt.

Die Quelle (Werkstatt-Plan Atemluft V2) hat diese Teile am 02.10.2026 entschieden: ENT-203 P4
(Vorlagen-Muster für alle Sperrpfade), ENT-206 mit elf Punkten (Laufumgebung mit Sandbox,
Schutzdatei außerhalb des Repos, Env-Scrub, Merges vor dem Merge-Skript, ASVS L2 mit L3-Inseln,
Füllung des Katalogs in zwei Stufen, ein Datenbank-Container je Worktree, Worktree-Pflicht,
`dev_env` ohne Sperrpfad) und der Vierte Nachtrag zu ENT-202 (`CLAUDE.md` und Regeldatei werden
nach der Definition of Done Sperrpfad). Der Auftraggeber hat am 02.10.2026 beauftragt, den Skill
auf diesen Stand nachzuziehen, verallgemeinert für beliebige Projekte.

Zwei Randbedingungen kamen mit dem Auftrag: Atemluft-Spezifisches gehört nicht in den Skill, und
ASVS-Text wird nicht übernommen, weil die Lizenzpflichten der ASVS-CSV (CC BY-SA 4.0) in der Quelle
eine offene Rechtsfrage sind.

## Decision

1. **Nachziehen, nicht neu schneiden** (Grenze von ADR-0018). Ablauf, Rollen und Grün-Definition
   bleiben. Die drei Teile kommen in die bestehenden Schritte: KLÄREN fragt Laufumgebung,
   ASVS-Level und Worktree-Pflicht, RAHMEN richtet die Isolation ein, ROLLEN füllt den
   Sicherheitskatalog, SPERREN führt die Leitplanken in drei Stufen ein.
2. **Schutzregeln liegen außerhalb des Repos.** Was nicht fallen darf, ist eine Deny-Regel in
   einer `--settings`-Datei oder den Benutzer-Einstellungen des Menschen. Hooks im Repo sind
   Führung, keine Sperre; ein Hook außerhalb des Repos ist ein Netz. Jede Leitplanke nennt ihre Klasse: Sperre, Netz oder Erkennung.
   Neue Harte Regel und neue Stop-Condition im Skill.
3. **Arbeitskopie-Abgleich im Merge-Skript.** G-4 schützt den Commit-Weg, nicht die laufende
   Session. Die Skizze `merge-gruen.py` prüft vor dem Merge jeden Worktree auf geänderte oder
   ungetrackte Dateien unter den Sperrpfaden und auf `disableAllHooks`. Sie bekommt dazu eine leere
   Liste `LOCKED_FILES` für `CLAUDE.md` und die Regeldatei nach der Definition of Done.
4. **Sicherheitskatalog als Datei, Schutz durch Tests.** Der Skill liest eine `katalog.json` unter
   dem Sperrpfad mit Nummern aus ASVS 5.0.0 und eigenen Zeilen und dazu eine Nachweisdatei. Den
   Schutz tragen die Tests aus der Nachweisdatei über G-1, der Skill hilft beim Finden. Das
   Level wählt der Mensch als Risikoentscheidung. Inseln sind Zuschnitt, keine Vorgabe des
   Standards. Der Mandantentest steht als Beispiel für mehrmandantenfähige Projekte da, als Pflicht
   nicht.
5. **Kein ASVS-Text.** Skill, Katalog-Vorlage und Doku nennen nur Kapitel und Nummern. Den
   Wortlaut liest der Skill zur Laufzeit aus der unveränderten CSV des Zielprojekts.
6. **Isolation als Referenz und Skizze.** `reference/isolation.md` und `templates/dev-env.py`
   (Slots im gemeinsamen Git-Verzeichnis, Ports aus dem Slot an `127.0.0.1`, Wegwerf-Passwort,
   Sweep). Die Skizze läuft wie `merge-gruen.py` durch `ruff`, nicht durch `mypy` und `pytest`.
7. **Umfang nach ADR-0011**, je neue Vorlage die Frage:

   | Frage | Vorlage |
   | --- | --- |
   | Welche Regel setzt der Mensch wann wo, und welche Probe zeigt, dass sie greift? | `LEITPLANKEN.md` |
   | Welche Sicherheitsanforderungen gelten, und welcher Test belegt sie? | `sicherheit/katalog.json`, `sicherheit/nachweise.json`, `skills/sicherheits-katalog.md` (gefüllt) |
   | Wie laufen parallele Sessions, ohne sich Datenbank, Port oder Branch kaputtzumachen? | `dev-env.py` |

   Dazu drei Dateien unter `reference/`: `leitplanken.md`, `asvs-baseline.md`, `isolation.md`.
8. **Offen bleibt und ist markiert:** Definition of Done und Git-Ablauf, ausformulierte
   Agent-Texte, Hook-Skripte, Gate-Marker-Format, die Proben der Leitplanken und der Isolation
   samt den Doku-Fragen dazu, Stufe 2 der Katalogauswahl und die Lizenzfrage.
9. **Keine Validator-Änderung.** Keine neue Pflichtstelle, keine Finding-ID, `schema_version`
   bleibt `1`.
10. **Version 0.9.0.**

Verworfene Alternativen:

- **Die Deny-Regeln als `.claude/settings.json` ins Zielrepo.** Die Arbeitskopie-Änderung wirkt
  sofort, ein Commit-Schutz greift zu spät. Das widerspricht dem Kern der Leitplanken.
- **ASVS-Anforderungen als Text im Katalog.** Bequemer zu lesen, aber die Lizenzfrage ist offen.
  Nummern plus CSV im Zielprojekt liefern dasselbe ohne Kopie.
- **Mandantentest als Pflicht.** Viele Projekte haben keine Mandanten. Nach ADR-0011 wäre das eine
  Pflicht ohne Frage.
- **Ein eigener fünfter Skill für Leitplanken.** Die Leitplanken gelten nur, wo eine KI-Session
  selbst mergt, und das ist genau die Frage der Werkstatt.

## Consequences

**Positiv**

- Ein Projekt bekommt eine geprüfte Antwort auf „wo liegt die Sperre, und wie zeigt sie, dass sie
  greift?", samt Einstellungsblöcken je Stufe und Probenliste.
- Der Sicherheitskatalog ist kein Gerüst mehr, und sein Schutz hängt an Tests, nicht am Modell.
- Parallele Sessions haben eine benannte Isolation statt einer Seriell-Grenze.

**Negativ**

- Viele Aussagen über Claude Code stammen aus einer Doku-Recherche vom 02.10.2026 und sind als
  Probe markiert. Sie veralten mit jeder Claude-Code-Version, und die Proben kosten Läufe auf dem
  Kontingent des Menschen.
- Der Skill wird länger: drei Reference-Dateien und vier Vorlagen mehr.
- `dev-env.py` setzt Docker Compose voraus. Ein Projekt ohne Container braucht nur den
  Slot-Teil.

**Grenze**

Neu zu bewerten, wenn die Quelle Definition of Done und Agent-Texte entscheidet (nachziehen), wenn
eine Probe eine Doku-Aussage widerlegt (Ebene oder Pfadform ändern), oder wenn die Lizenzfrage
erlaubt, ASVS-Text abzulegen.
