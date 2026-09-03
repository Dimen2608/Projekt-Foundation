"""Prueft die Regeln, die ueber FOUNDATION VALID entscheiden.

Jeder Test schuetzt genau eine Blocking-Regel. Getestet wird das Verhalten des
Validators, nicht seine interne Struktur.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from foundation_validate.model import Domain, Finding, Severity
from foundation_validate.validator import (
    ADR_SECTIONS,
    CORE_AREAS,
    PROJECT_SECTIONS_REQUIRED,
    SECURITY_CRITICAL_AREAS,
    UNCHECKED_DOMAINS,
    validate,
)


def _ids(root: Path) -> set[str]:
    return {f.finding_id for f in validate(root).blocking}


def test_vollstaendiges_projekt_ist_valid(project: Path) -> None:
    result = validate(project)
    assert result.valid, [str(f) for f in result.blocking]


def test_fehlender_pflichtabschnitt_in_project_md_blockiert(project: Path) -> None:
    text = (project / "docs" / "PROJECT.md").read_text(encoding="utf-8")
    (project / "docs" / "PROJECT.md").write_text(
        text.replace("## Target Users", "## Irgendwas"), encoding="utf-8"
    )
    assert not validate(project).valid


def test_unbekannte_authentifizierung_blockiert(project: Path) -> None:
    path = project / "docs" / "ARCHITECTURE.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "| Authentication | NOT REQUIRED |", "| Authentication | UNKNOWN |"
        ),
        encoding="utf-8",
    )
    result = validate(project)
    assert not result.valid
    assert any(f.domain is Domain.SECURITY for f in result.blocking)


def test_nicht_bewerteter_unkritischer_bereich_ist_nur_warnung(project: Path) -> None:
    path = project / "docs" / "ARCHITECTURE.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("| Frontend | NOT REQUIRED |\n", ""),
        encoding="utf-8",
    )
    result = validate(project)
    assert result.valid
    assert any(f.severity is Severity.WARNING for f in result.warnings)


def test_doppelte_adr_nummer_blockiert(project: Path) -> None:
    quelle = project / "docs" / "decisions" / "ADR-0001-beispiel.md"
    (project / "docs" / "decisions" / "ADR-0001-zweitbeleg.md").write_text(
        quelle.read_text(encoding="utf-8"), encoding="utf-8"
    )
    assert "ADR-002" in _ids(project)


def test_adr_ohne_pflichtabschnitte_blockiert(project: Path) -> None:
    (project / "docs" / "decisions" / "ADR-0002-luecke.md").write_text(
        "# ADR-0002\n\n## Status\nProposed\n\n## Context\nNur Kontext.\n", encoding="utf-8"
    )
    assert "ADR-003" in _ids(project)


def test_kein_adr_trotz_required_blockiert(project: Path) -> None:
    """Wer 'Architecture Decisions: REQUIRED' erklaert, muss das ADR auch liefern."""
    (project / "docs" / "decisions" / "ADR-0001-beispiel.md").unlink()
    assert "STRUCT-011" in _ids(project)


def test_kein_adr_bei_not_required_ist_gueltig(project: Path) -> None:
    """Ein Projekt ohne tragende Entscheidung braucht kein ADR - der Kern von ADR-0011."""
    shutil.rmtree(project / "docs" / "decisions")
    path = project / "docs" / "ARCHITECTURE.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "| Architecture Decisions | REQUIRED |", "| Architecture Decisions | NOT REQUIRED |"
        ),
        encoding="utf-8",
    )
    assert validate(project).valid


def test_fehlende_aussage_zu_entscheidungen_ist_eine_warnung(project: Path) -> None:
    """Unbeantwortet ist nicht dasselbe wie beantwortet - aber auch kein Blocker."""
    shutil.rmtree(project / "docs" / "decisions")
    path = project / "docs" / "ARCHITECTURE.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("| Architecture Decisions | REQUIRED |\n", ""),
        encoding="utf-8",
    )
    result = validate(project)
    assert result.valid
    assert "ADR-010" in {f.finding_id for f in result.warnings}


def test_agents_md_erfuellt_die_ai_frage_ebenso(project: Path) -> None:
    """Die Pflicht haengt an der Frage, nicht am Dateinamen CLAUDE.md."""
    (project / "CLAUDE.md").rename(project / "AGENTS.md")
    manifest = project / ".project-foundation.yml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8")
        .replace("claude_md: true", "claude_md: false")
        .replace("agents_md: false", "agents_md: true"),
        encoding="utf-8",
    )
    assert validate(project).valid


def test_ungepruefte_domaenen_werden_nicht_als_ok_gemeldet(project: Path) -> None:
    """Ein OK fuer etwas, das nie geprueft wurde, waere ein falsches Qualitaetsversprechen."""
    status = validate(project).domain_status
    for domain in UNCHECKED_DOMAINS:
        assert status[domain] == "NOT CHECKED"


def test_status_blocked_blockiert(project: Path) -> None:
    path = project / "STATUS.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "| Architecture | PASS |", "| Architecture | BLOCKED |"
        ),
        encoding="utf-8",
    )
    assert "STAT-002" in _ids(project)


def test_manifest_ready_trotz_blockiertem_status_ist_konflikt(project: Path) -> None:
    path = project / "STATUS.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("| Security | PASS |", "| Security | UNKNOWN |"),
        encoding="utf-8",
    )
    assert "CONS-001" in _ids(project)


def test_manifest_luegt_ueber_agents_md(project: Path) -> None:
    path = project / ".project-foundation.yml"
    path.write_text(
        path.read_text(encoding="utf-8").replace("agents_md: false", "agents_md: true"),
        encoding="utf-8",
    )
    assert "CONS-003" in _ids(project)


def test_teststrategie_ohne_command_blockiert(project: Path) -> None:
    path = project / ".project-foundation.yml"
    path.write_text(
        path.read_text(encoding="utf-8").replace("  command: pytest\n", ""), encoding="utf-8"
    )
    assert "CONS-004" in _ids(project)


def test_committete_env_datei_blockiert(project: Path) -> None:
    (project / ".env").write_text("TOKEN=geheim\n", encoding="utf-8")
    assert "SEC-001" in _ids(project)


def test_env_example_ohne_gitignore_eintrag_blockiert(project: Path) -> None:
    (project / ".env.example").write_text("TOKEN=\n", encoding="utf-8")
    assert "SEC-002" in _ids(project)


def test_kaputtes_manifest_blockiert(project: Path) -> None:
    (project / ".project-foundation.yml").write_text("foundation: [unbalanced\n", encoding="utf-8")
    assert "MAN-001" in _ids(project)


def _finding(root: Path, finding_id: str) -> Finding:
    treffer = [f for f in validate(root).findings if f.finding_id == finding_id]
    assert treffer, f"{finding_id} nicht gemeldet"
    return treffer[0]


def test_beinahe_treffer_wird_in_der_meldung_genannt(project: Path) -> None:
    """Wer seine Doku anders benannt hat, soll nicht raten muessen, ob sie uebersehen wurde."""
    (project / "docs" / "PROJECT.md").unlink()
    (project / "KONZEPT.md").write_text("# Konzept\n", encoding="utf-8")
    finding = _finding(project, "STRUCT-004")
    assert "KONZEPT.md" in finding.reason
    assert "umbenennen" in finding.required_action


def test_fremdes_adr_verzeichnis_wird_mit_anzahl_genannt(project: Path) -> None:
    """docs/adr/ mit fremder Nummerierung (0001-titel.md) muss erkannt werden."""
    shutil.rmtree(project / "docs" / "decisions")
    fremd = project / "docs" / "adr"
    fremd.mkdir()
    for nummer in ("0001", "0002"):
        (fremd / f"{nummer}-eine-entscheidung.md").write_text("# ADR\n", encoding="utf-8")
    finding = _finding(project, "STRUCT-010")
    assert "docs/adr/" in finding.reason
    assert "2 ADR-Dateien" in finding.reason


def test_beinahe_treffer_erfuellt_die_pflicht_nicht(project: Path) -> None:
    """Der Validator bleibt strikt: der Hinweis ist eine Meldung, keine Anerkennung."""
    (project / "docs" / "ARCHITECTURE.md").rename(project / "docs" / "architektur.md")
    assert "STRUCT-005" in _ids(project)


def test_status_in_eigenem_format_bleibt_still(project: Path) -> None:
    """STATUS.md ist optional; ein fremdes Format ist kein Mangel und keine acht Warnungen."""
    (project / "STATUS.md").write_text("# Status\n\nAlles bestens.\n", encoding="utf-8")
    result = validate(project)
    assert not [f for f in result.findings if f.finding_id.startswith("STAT-")]


def test_einzelne_fehlende_domaene_bleibt_eine_einzelmeldung(project: Path) -> None:
    path = project / "STATUS.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("| Security | PASS |\n", ""), encoding="utf-8"
    )
    result = validate(project)
    stat = [f for f in result.warnings if f.finding_id.startswith("STAT-")]
    assert [f.finding_id for f in stat] == ["STAT-001"]
    assert "Security" in stat[0].reason


def test_fehlende_architecture_md_kuendigt_die_folgepruefung_an(project: Path) -> None:
    """Ohne Vorwarnung sieht es aus, als erzeuge das Beheben eines Blockers neue."""
    (project / "docs" / "ARCHITECTURE.md").unlink()
    aktion = _finding(project, "STRUCT-005").required_action
    assert str(len(CORE_AREAS)) in aktion
    for bereich in SECURITY_CRITICAL_AREAS:
        assert bereich in aktion


def test_fehlende_project_md_nennt_die_pflichtabschnitte(project: Path) -> None:
    (project / "docs" / "PROJECT.md").unlink()
    aktion = _finding(project, "STRUCT-004").required_action
    for abschnitt in PROJECT_SECTIONS_REQUIRED:
        assert abschnitt in aktion


def test_fehlendes_decisions_verzeichnis_nennt_die_adr_abschnitte(project: Path) -> None:
    shutil.rmtree(project / "docs" / "decisions")
    aktion = _finding(project, "STRUCT-010").required_action
    for abschnitt in ADR_SECTIONS:
        assert abschnitt in aktion


def test_fehlende_readme_blockiert(project: Path) -> None:
    (project / "README.md").unlink()
    assert "STRUCT-001" in _ids(project)


def test_fehlende_status_md_ist_kein_mangel(project: Path) -> None:
    """STATUS.md ist optional: ein Projekt ohne laufenden Zustandsbericht ist gueltig."""
    (project / "STATUS.md").unlink()
    assert validate(project).valid


def test_fehlende_claude_md_blockiert(project: Path) -> None:
    (project / "CLAUDE.md").unlink()
    assert "STRUCT-003" in _ids(project)


def test_fehlendes_manifest_blockiert(project: Path) -> None:
    (project / ".project-foundation.yml").unlink()
    assert "STRUCT-006" in _ids(project)


def test_manifest_ohne_mapping_blockiert(project: Path) -> None:
    """Eine YAML-Liste statt eines Mappings ist syntaktisch gueltig, aber unbrauchbar."""
    (project / ".project-foundation.yml").write_text("- eins\n- zwei\n", encoding="utf-8")
    assert "MAN-002" in _ids(project)


def test_manifest_ohne_pflichtfeld_blockiert(project: Path) -> None:
    path = project / ".project-foundation.yml"
    path.write_text(
        path.read_text(encoding="utf-8").replace("schema_version: 1\n", ""), encoding="utf-8"
    )
    assert "MAN-003" in _ids(project)


def test_unzulaessiger_foundation_status_blockiert(project: Path) -> None:
    path = project / ".project-foundation.yml"
    path.write_text(
        path.read_text(encoding="utf-8").replace("status: READY", "status: FAST_FERTIG"),
        encoding="utf-8",
    )
    assert "MAN-004" in _ids(project)


def test_manifest_ready_mit_blockern_ist_konflikt(project: Path) -> None:
    path = project / ".project-foundation.yml"
    path.write_text(
        path.read_text(encoding="utf-8").replace("blocking_issues: 0", "blocking_issues: 3"),
        encoding="utf-8",
    )
    assert "CONS-002" in _ids(project)


def test_adr_mit_falschem_dateinamen_ist_warnung(project: Path) -> None:
    """Der Dateiname ist Konvention, kein Blocker - der Inhalt entscheidet."""
    quelle = project / "docs" / "decisions" / "ADR-0001-beispiel.md"
    (project / "docs" / "decisions" / "entscheidung.md").write_text(
        quelle.read_text(encoding="utf-8"), encoding="utf-8"
    )
    result = validate(project)
    assert "ADR-001" in {f.finding_id for f in result.warnings}
    assert result.valid


def test_adr_ohne_status_blockiert(project: Path) -> None:
    (project / "docs" / "decisions" / "ADR-0002-ohne-status.md").write_text(
        "# ADR-0002\n\n## Context\nK.\n\n## Decision\nE.\n\n## Consequences\nF.\n",
        encoding="utf-8",
    )
    assert "ADR-004" in _ids(project)


def test_warnung_nennt_ein_fremdes_adr_verzeichnis(project: Path) -> None:
    """Wer seine ADRs in docs/adr/ hat, darf nicht hoeren, er habe keine (ADR-0008)."""
    shutil.rmtree(project / "docs" / "decisions")
    path = project / "docs" / "ARCHITECTURE.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("| Architecture Decisions | REQUIRED |\n", ""),
        encoding="utf-8",
    )
    fremd = project / "docs" / "adr"
    fremd.mkdir()
    for nummer in ("0001", "0002"):
        (fremd / f"{nummer}-eine-entscheidung.md").write_text("# ADR\n", encoding="utf-8")
    finding = _finding(project, "ADR-010")
    assert "docs/adr/" in finding.reason
    assert "2 ADR-Dateien" in finding.reason
    assert "docs/decisions/" in finding.required_action
