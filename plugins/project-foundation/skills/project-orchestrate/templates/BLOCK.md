# Block `<ID>` — `<Kurzname>`

> Eine Datei je Block, abgelegt unter `orchestrate/bloecke/<ID>-<kurzname>.md`. Beantwortet:
> **Was genau ist der Auftrag, was wurde übergeben, was sagt das Tor?** Den Auftrag schreibt der
> Orchestrator vor der Vergabe; Übergabe und Tor trägt er aus der Nachricht des Workers ein.

## Auftrag

Wird wörtlich als `BLOCK <ID> AUFTRAG` an den Worker geschickt. Alle sechs Felder sind Pflicht.

- **Ziel:** `<ein Satz>`
- **Repo/Branch:** `<owner/repo>` · `<branch>`
- **Eingang:** `<worauf der Block aufbaut: Commit, Vorgängerblock, Dateien, die zu lesen sind>`
- **Umfangsgrenze:** `<was ausdrücklich nicht dazugehört>`
- **Abnahmekriterium:** `<prüfbar — z. B. die Befehle, die grün sein müssen, und was sie zeigen>`
- **Zuständig:** `<Skill oder Agent aus ORCHESTRATE.md>`

**Für den Worker:** Führe den Block mit `project-foundation:orchestrate-blockarbeiter` aus,
danach das Tor mit `project-foundation:orchestrate-tor` in einem frischen Aufruf, dem du
Auftrag und Diff gibst, nicht die Begründung. Fragen gehen als `BLOCK <ID> FRAGE` an den
Orchestrator, nie an den Menschen.

## Übergabe

Vom Worker, als `BLOCK <ID> UEBERGABE <done|blocked|aborted>`.

- **Status:** `<done | blocked | aborted>`
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
- **Ergebnis:** `<done | zurück an Worker (Runde n) | escalated>` · **Datum:** `<…>`
