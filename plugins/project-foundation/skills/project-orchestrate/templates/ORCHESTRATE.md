# Orchestrierung — Konfiguration

> Ergebnis von `SETUP`. Beantwortet: **Welche Repos, wer mergt, wie kommen Worker dazu, wer ist
> für welche Aufgabenart zuständig?** Der YAML-Block ist für den Orchestrator, der Text darunter
> für Menschen. Bei jeder Änderung an Repos, Skills oder Umgebung `SETUP` wiederholen.

```yaml
orchestrate:
  folder: orchestrate            # Ort von BLOCKPLAN.md und bloecke/
  home_repo: <owner/repo>
  state_branch: <orchestrate>    # hier committet der Orchestrator, nie auf einem Worker-Branch
  orchestrator_session: <Name, wie ListAgents ihn zeigt>
  repos:
    - name: <owner/repo>
      purpose: <ein Satz>
      default_branch: <main>
      machine: <auf welchem Rechner der Worker läuft>
      foundation: <VALID | NOT VALID — erster Block ist ein Vorbereitungsblock | unbekannt>
  merge_mode: human              # human | orchestrator
  worker_start: attach           # attach | attach+local_bg
  gate_max_rounds: 5
  responsibilities:
    - task_type: <z. B. Backend-Endpunkt>
      handled_by: <Skill- oder Agent-Name>
      source: <vorhanden | installiert am JJJJ-MM-TT | general-purpose, weil …>
```

## Repos

`<Je Repo ein Satz: wofür es da ist, warum es eingebunden ist, auf welchem Rechner.>`

## Erreichbarkeit

- **Festgestellt am:** `<Datum>` · **Orchestrator läuft in:** `<Claude Desktop | CLI>` ·
  **Claude Code:** `<Version>`
- **Remote Control am Orchestrator:** `<verbunden — wie eingeschaltet>`
- **Worker-Verfahren:** `<attach | attach+local_bg — warum>`
- **Selbst leeren im Worker:** `<möglich und geprüft | nicht verfügbar>`

## Zusammenführung

`<human: Der Mensch mergt jeden PR. | orchestrator: Der Orchestrator mergt nach Tor-Ja und
grüner CI — warum hier vertretbar.>`

## Zuständigkeiten

| Aufgabenart | Zuständig | Herkunft | Warum dieser |
| --- | --- | --- | --- |
| `<Art>` | `<Skill/Agent>` | `<vorhanden / installiert am … / general-purpose>` | `<ein Satz>` |

**Vorgeschlagen, nicht installiert:** `<Name — warum abgelehnt oder vertagt>`
