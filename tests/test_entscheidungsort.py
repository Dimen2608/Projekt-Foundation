"""Der Ort der Architekturentscheidungen ist deklarierbar (ADR-0012).

Die Zeile `Architecture Decisions | REQUIRED | <Ort>` darf sagen, wo die ADRs liegen. Ohne
Angabe gilt docs/decisions/ wie bisher; diese Tests sichern beides.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from foundation_validate.model import Finding
from foundation_validate.validator import validate

ADR_TEXT = (
    "# ADR-0001: Beispiel\n\n## Status\nAccepted\n\n## Context\nK.\n\n"
    "## Decision\nE.\n\n## Consequences\nF.\n"
)


def _ids(root: Path) -> set[str]:
    return {f.finding_id for f in validate(root).findings}


def _finding(root: Path, finding_id: str) -> Finding:
    treffer = [f for f in validate(root).findings if f.finding_id == finding_id]
    assert treffer, f"{finding_id} nicht gemeldet"
    return treffer[0]


def _entscheidungsort_erklaeren(project: Path, ort: str) -> None:
    """Traegt den Ort in die dritte Spalte der Architecture-Decisions-Zeile ein."""
    shutil.rmtree(project / "docs" / "decisions")
    path = project / "docs" / "ARCHITECTURE.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "| Architecture Decisions | REQUIRED |",
            f"| Architecture Decisions | REQUIRED | `{ort}` |",
        ),
        encoding="utf-8",
    )


def test_erklaertes_adr_verzeichnis_erfuellt_required(project: Path) -> None:
    """Wer den Ort nennt, braucht docs/decisions/ nicht."""
    _entscheidungsort_erklaeren(project, "docs/adr/")
    (project / "docs" / "adr").mkdir()
    (project / "docs" / "adr" / "ADR-0001-beispiel.md").write_text(ADR_TEXT, encoding="utf-8")
    result = validate(project)
    assert result.valid
    assert not [f for f in result.findings if f.finding_id.startswith("STRUCT-01")]


def test_erklaertes_verzeichnis_wird_wie_docs_decisions_geprueft(project: Path) -> None:
    """Die Formatpruefung folgt dem Ort - ein erklaertes Verzeichnis ist kein Freibrief."""
    _entscheidungsort_erklaeren(project, "docs/adr/")
    (project / "docs" / "adr").mkdir()
    (project / "docs" / "adr" / "ADR-0001-luecke.md").write_text(
        "# ADR-0001\n\n## Status\nProposed\n\n## Context\nNur Kontext.\n", encoding="utf-8"
    )
    assert "ADR-003" in _ids(project)


def test_erklaerte_sammeldatei_erfuellt_required(project: Path) -> None:
    """Ein Projekt darf seine ADRs in einer Datei fuehren; gezaehlt werden die Eintraege."""
    _entscheidungsort_erklaeren(project, "docs/architektur/decisions.md")
    (project / "docs" / "architektur").mkdir()
    (project / "docs" / "architektur" / "decisions.md").write_text(
        "# Entscheidungen\n\n## ADR-001: Monolith\n\nText.\n\n## ADR-002: RLS\n\nText.\n",
        encoding="utf-8",
    )
    result = validate(project)
    assert result.valid
    assert not [f for f in result.findings if f.finding_id.startswith("STRUCT-01")]


def test_erklaerte_sammeldatei_ohne_eintraege_blockiert(project: Path) -> None:
    _entscheidungsort_erklaeren(project, "docs/architektur/decisions.md")
    (project / "docs" / "architektur").mkdir()
    (project / "docs" / "architektur" / "decisions.md").write_text(
        "# Entscheidungen\n\nNoch keine.\n", encoding="utf-8"
    )
    finding = _finding(project, "STRUCT-011")
    assert "docs/architektur/decisions.md" in finding.reason
    assert "## ADR-001" in finding.reason


def test_erklaerter_ort_der_fehlt_blockiert_und_wird_genannt(project: Path) -> None:
    _entscheidungsort_erklaeren(project, "docs/entscheidungen/")
    finding = _finding(project, "STRUCT-010")
    assert "docs/entscheidungen/" in finding.reason
    assert "existiert nicht" in finding.reason


def test_erklaerter_ort_ausserhalb_des_projekts_blockiert(project: Path) -> None:
    """Ein Ort ausserhalb des Projekts ist keine Antwort, sondern ein Ausbruch."""
    _entscheidungsort_erklaeren(project, "../anderswo/decisions/")
    finding = _finding(project, "STRUCT-010")
    assert "aus dem Projekt heraus" in finding.reason


def test_ohne_ortsangabe_gilt_docs_decisions(project: Path) -> None:
    """Die Default-Konvention bleibt; ADR-0012 ist eine Erlaubnis, keine Aenderung."""
    shutil.rmtree(project / "docs" / "decisions")
    (project / "docs" / "adr").mkdir()
    (project / "docs" / "adr" / "ADR-0001-beispiel.md").write_text(ADR_TEXT, encoding="utf-8")
    finding = _finding(project, "STRUCT-010")
    assert "docs/decisions/ fehlt" in finding.reason
    assert "als Ort eintragen" in finding.required_action


def test_begruendung_ohne_pfad_erklaert_keinen_ort(project: Path) -> None:
    """'ADR-0001 haelt die Wahl fest.' ist eine Begruendung, kein Ort."""
    path = project / "docs" / "ARCHITECTURE.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "| Architecture Decisions | REQUIRED |",
            "| Architecture Decisions | REQUIRED | ADR-0001 haelt die Wahl der Persistenz fest. |",
        ),
        encoding="utf-8",
    )
    assert validate(project).valid
