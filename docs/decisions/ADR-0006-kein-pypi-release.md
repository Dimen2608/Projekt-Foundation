# ADR-0006: Kein PyPI-Release und kein Build-Artefakt

## Status

Accepted — 2026-09-01

## Context

Der Validator ist ein installierbares Python-Paket. Die naheliegende Fortsetzung wäre ein
Release auf PyPI mit Versionierung, Changelog, Release-Workflow und Signaturen.

Der reale Nutzerkreis ist aber: dieses Repo und Projekte, die das Plugin ohnehin per
`/plugin marketplace add` einbinden — und dabei die Quelle vollständig lokal haben.

Ein Release-Prozess wäre damit Infrastruktur ohne Anforderung, die sie rechtfertigt.

## Decision

Kein PyPI-Release, kein Build-Schritt in CI, kein Release-Workflow.

Die Nutzung erfolgt als:

```
pip install -e .                  # im geklonten Repo
python -m foundation_validate ..  # oder direkt, ohne Installation
```

`pyproject.toml` bleibt trotzdem vorhanden — es definiert Abhängigkeiten, Tool-Konfiguration
und den Konsolen-Einstiegspunkt und ist unabhängig vom Publishing sinnvoll.

Die CI-Pipeline validiert daher `Install → Format → Lint → Typecheck → Test`. Der
Build-Schritt entfällt bewusst, weil es kein zu bauendes Artefakt gibt.

## Consequences

**Positiv**

- Kein Release-Overhead, keine Versionspflege in mehreren Dateien, keine Publishing-Secrets.
- Die CI bleibt kurz und schnell.

**Negativ**

- Kein `pip install foundation-validate` aus dem Netz. Nutzer brauchen das Repo.
- Sollte sich später externe Nachfrage zeigen, ist dieses ADR durch ein neues zu ersetzen
  (Status dann `Superseded`).
