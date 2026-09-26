# Block `<ID>` — `<Kurzname>`

> Eine Datei je Block, abgelegt unter `orchestrate/bloecke/<ID>-<kurzname>.md`. Beantwortet:
> **Was genau ist der Auftrag, was wurde übergeben, was sagt das Tor?** Den Auftrag schreibt der
> Orchestrator vor der Vergabe; Übergabe und Tor trägt er aus der Nachricht des Workers ein.

## Auftrag

Wird wörtlich als `BLOCK <ID> AUFTRAG` an den Worker geschickt. Alle sechs Felder sind Pflicht.

- **Ziel:** `<ein Satz>`
- **Repo/Branch:** `<owner/repo>` · `<branch>`
- **Eingang:** Basis-Commit `<SHA>` · `<worauf der Block aufbaut: Vorgängerblock, Dateien, die zu
  lesen sind>`
- **Umfangsgrenze:** `<was ausdrücklich nicht dazugehört>`
- **Abnahmekriterium:** `<prüfbar — z. B. die Befehle, die grün sein müssen, und was sie zeigen>`
- **Zuständig:** `<Skill oder Agent aus ORCHESTRATE.md>`

**Für den Worker:** Ablauf, Rundenzählung und Übergabe wie im Startprompt (`WORKER-START.md`).
Ist `project-foundation` oder `project-rethink` zuständig, ist das ein **Vorbereitungsblock**: Du
führst ihn selbst aus, nicht im Blockarbeiter, und seine Fragen gehen an den Menschen.

## Übergabe

Vom Worker, als `BLOCK <ID> UEBERGABE <done|exhausted>`.

- **Status:** `<done | exhausted (fünf Runden ohne Freigabe)>`
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

## Fragen

| Datum | Frage (`BLOCK <ID> FRAGE`) | Antwort (`BLOCK <ID> ANTWORT`) | Grundlage |
| --- | --- | --- | --- |

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
