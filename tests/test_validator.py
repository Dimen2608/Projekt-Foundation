"""Prueft die Regeln, die ueber FOUNDATION READY entscheiden.

Jeder Test schuetzt genau eine Blocking-Regel. Getestet wird das Verhalten des
Validators, nicht seine interne Struktur.
"""

from __future__ import annotations

from pathlib import Path

from foundation_validate.model import Domain, Severity
from foundation_validate.validator import validate


def _ids(root: Path) -> set[str]:
    return {f.finding_id for f in validate(root).blocking}


def test_vollstaendiges_projekt_ist_ready(project: Path) -> None:
    result = validate(project)
    assert result.ready, [str(f) for f in result.blocking]


def test_fehlende_pflichtdatei_blockiert(project: Path) -> None:
    (project / "docs" / "PROJECT.md").unlink()
    result = validate(project)
    assert not result.ready
    assert any(f.domain is Domain.PROJECT_DEFINITION for f in result.blocking)


def test_fehlender_pflichtabschnitt_in_project_md_blockiert(project: Path) -> None:
    text = (project / "docs" / "PROJECT.md").read_text(encoding="utf-8")
    (project / "docs" / "PROJECT.md").write_text(
        text.replace("## Target Users", "## Irgendwas"), encoding="utf-8"
    )
    assert not validate(project).ready


def test_unbekannte_authentifizierung_blockiert(project: Path) -> None:
    path = project / "docs" / "ARCHITECTURE.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "| Authentication | NOT REQUIRED |", "| Authentication | UNKNOWN |"
        ),
        encoding="utf-8",
    )
    result = validate(project)
    assert not result.ready
    assert any(f.domain is Domain.SECURITY for f in result.blocking)


def test_nicht_bewerteter_unkritischer_bereich_ist_nur_warnung(project: Path) -> None:
    path = project / "docs" / "ARCHITECTURE.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("| Frontend | NOT REQUIRED |\n", ""),
        encoding="utf-8",
    )
    result = validate(project)
    assert result.ready
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


def test_kein_adr_vorhanden_blockiert(project: Path) -> None:
    (project / "docs" / "decisions" / "ADR-0001-beispiel.md").unlink()
    assert "STRUCT-011" in _ids(project)


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
