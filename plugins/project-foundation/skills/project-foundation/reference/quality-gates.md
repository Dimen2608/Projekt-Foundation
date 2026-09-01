# Quality Gates

Ein Gate ist eine Menge von Bedingungen, die vor einem bestimmten Schritt erfüllt sein
müssen. Gates werden nicht „meistens" eingehalten — sonst sind sie keine Gates.

Nur die Gates definieren, die im Projekt tatsächlich greifen. Ein Gate ohne Durchsetzung
ist Dekoration.

## Foundation Gate

**Wann:** Vor jeder Implementierung.

- Alle Pflichtdomänen `PASS`
- Null Blocking Issues
- Command-Chain nachweislich ausgeführt
- Keine Widersprüche zwischen den Source-of-Truth-Dateien
- AI-Readiness-Test bestanden

## Change Gate

**Wann:** Vor jedem Commit oder Merge.

- Relevante Tests laufen grün
- Lint besteht
- Typecheck besteht
- Build besteht (sofern das Projekt einen Build hat)
- Keine bekannte Regression
- `STATUS.md` stimmt noch

## Architecture Gate

**Wann:** Bei Änderungen an Struktur, Schnittstellen, Datenmodell oder Abhängigkeitsrichtung.

- Änderung ist begutachtet
- ADR erstellt oder ein bestehendes aktualisiert
- `docs/ARCHITECTURE.md` nachgezogen
- Bestehende Grenzen respektiert — oder die Verschiebung ist im ADR begründet
- `.project-foundation.yml` aktualisiert, falls betroffen

## Security Gate

**Wann:** Bei Änderungen an Authentication, Authorization, Secrets, Datenzugriff,
Eingabeverarbeitung oder Mandantentrennung.

- Authentication geprüft
- Authorization geprüft — insbesondere: prüft jeder Zugriffspfad die Berechtigung?
- Secrets geprüft: nichts im Diff, nichts im Log, nichts in Fehlermeldungen
- Datenisolation geprüft; bei SaaS zusätzlich Tenant-Isolation und Cross-Tenant-Zugriff
- Eingabevalidierung an der Systemgrenze geprüft
- Abhängigkeiten auf bekannte Schwachstellen geprüft

Eine offene sicherheitsrelevante Frage ist **BLOCKING**, nie `WARNING`.
