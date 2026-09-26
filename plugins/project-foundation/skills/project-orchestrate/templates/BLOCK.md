# Block `<ID>` — `<Kurzname>`

> Eine Datei je Block, abgelegt unter `orchestrate/bloecke/<ID>-<kurzname>.md`. Beantwortet:
> **Was genau ist der Auftrag, was wurde übergeben, was sagt das Tor?** Den Auftrag schreibt der
> Orchestrator vor der Vergabe; Übergabe und Tor trägt er aus der Nachricht des Workers ein.

## Auftrag

Wird wörtlich als `BLOCK <ID> AUFTRAG` an den Worker geschickt, mit dem Worker-Kopf als zweiter
Zeile — der Auftrag muss auch für einen Worker verständlich sein, der gerade geleert wurde.
Denselben Worker-Kopf tragen `ANTWORT` und `NACHARBEIT`. Alle
sechs Felder sind Pflicht.

`Worker <name> · Orchestrator <orchestrator-name> · zuerst .claude/worker.md lesen; fehlt sie, nichts tun, an <orchestrator-name> per SendMessage „WORKER UNBEKANNT <name>" melden und auf den Startprompt warten`

- **Ziel:** `<ein Satz>`
- **Repo/Branch:** `<owner/repo>` · `<branch>`
- **Eingang:** Basis-Commit `<SHA>` · `<worauf der Block aufbaut: Vorgängerblock, Dateien, die zu
  lesen sind>`
- **Umfangsgrenze:** `<was ausdrücklich nicht dazugehört>`
- **Abnahmekriterium:** `<prüfbar — z. B. die Befehle, die grün sein müssen, und was sie zeigen>`
- **Zuständig:** `<Skill oder Agent aus ORCHESTRATE.md>`

**Für den Worker:** Ablauf, Rundenzählung und Übergabe wie in deinem Startprompt, den
`.claude/worker.md` wörtlich enthält.
Ist `project-foundation` oder `project-rethink` zuständig, ist das ein **Vorbereitungsblock**: Du
führst ihn selbst aus, nicht im Blockarbeiter, und seine Fragen gehen an den Menschen.

## Übergabe

Vom Worker, als `BLOCK <ID> UEBERGABE <done|exhausted>`.

- **Status:** `<done | exhausted (fünf Runden ohne Freigabe, oder NACHARBEIT nach der fünften Runde)>`
- **Runden:** `<Anzahl Tor-Aufrufe in diesem Block>`
- **Ergebnis:** `<drei Sätze, was jetzt anders ist>`
- **Commits / PR:** `<SHA … · PR-Link>`
- **Geänderte Dateien:** `<Liste>`
- **Abnahmebefehle mit Ausgabe:**

  ```
  <Befehl>
  <gekürzte Ausgabe, Ergebnis>
  ```

- **Entscheidungen im Block:** `<was entschieden wurde und auf welcher Grundlage — oder „keine">`
- **Offen / für Folgeblöcke:** `<höchstens fünf Zeilen, die ein Nachfolger wissen muss>`

## Fragen und Wartestellen

| Datum | Art | Frage (`FRAGE`) oder Wartestelle (`WARTET freigabe\|befehl`) | Antwort (`ANTWORT`) oder Ausgang (`WEITER`) | Grundlage |
| --- | --- | --- | --- | --- |

## Tor

| Runde | Datum | Blockierend | Freigabe |
| --- | --- | --- | --- |
| 1 | `<Datum>` | `<Anzahl, Kurzform>` | `<ja / nein>` |

`<Schlussurteil des Tores in seiner Ausgabeform: Geprüft · Blockierend · Vorschläge · Notizen ·
Freigabe>`

## Abnahme durch den Orchestrator

- [ ] Tor-Urteil `Freigabe: ja`
- [ ] Jeder Abnahmebefehl mit Ausgabe belegt
- [ ] Keine Datei außerhalb der Umfangsgrenze geändert
- **Ergebnis:** `<done | NACHARBEIT (was fehlt) | escalated>` · **Datum:** `<…>`
