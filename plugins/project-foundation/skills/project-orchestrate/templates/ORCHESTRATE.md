# Orchestrierung — Konfiguration

> Ergebnis von `SETUP`. Beantwortet: **Welche Repos, wer mergt, wie starten Worker, wer ist für
> welche Aufgabenart zuständig?** Der YAML-Block ist für den Orchestrator, der Text darunter für
> Menschen. Bei jeder Änderung an Repos, Skills oder Umgebung `SETUP` wiederholen.

```yaml
orchestrate:
  folder: orchestrate            # Ort von BLOCKPLAN.md und bloecke/
  home_repo: <owner/repo>
  repos:
    - name: <owner/repo>
      purpose: <ein Satz>
      default_branch: <main>
      foundation: <VALID | NOT VALID — erster Block ist project-foundation/-rethink>
  merge_mode: human              # human | orchestrator
  worker_start: <cloud_spawn | local_bg | manual>
  back_channel: <send_message | branch_file>
  gate_max_rounds: 5
  responsibilities:
    - task_type: <z. B. Backend-Endpunkt>
      handled_by: <Skill- oder Agent-Name>
      source: <vorhanden | installiert am JJJJ-MM-TT | general-purpose, weil …>
```

## Repos

`<Je Repo ein Satz: wofür es da ist und warum es eingebunden ist.>`

## Worker-Verfahren

- **Festgestellt am:** `<Datum>` · **Umgebung:** `<Cloud | Desktop | CLI lokal>` ·
  **Claude Code:** `<Version>`
- **Stufe:** `<welche Stufe aus mechanismen.md, und warum die höheren nicht verfügbar sind>`
- **Rückkanal:** `<SendMessage | Übergabe-Datei im Worker-Branch>`
- **Selbst leeren:** `<möglich und geprüft | nicht verfügbar>`

## Zusammenführung

`<human: Du mergst jeden PR. | orchestrator: Der Orchestrator mergt nach Tor-Ja und grüner CI —
warum hier vertretbar.>`

## Zuständigkeiten

| Aufgabenart | Zuständig | Herkunft | Warum dieser |
| --- | --- | --- | --- |
| `<Art>` | `<Skill/Agent>` | `<vorhanden / installiert am … / general-purpose>` | `<ein Satz>` |

**Vorgeschlagen, nicht installiert:** `<Name — warum abgelehnt oder vertagt>`
