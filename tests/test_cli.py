"""Prueft die Schnittstelle, auf die sich CI und Agents verlassen: Exit-Code und Report."""

from __future__ import annotations

from pathlib import Path

import pytest

from foundation_validate.cli import main


def test_ready_liefert_exitcode_null(project: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(project)]) == 0
    ausgabe = capsys.readouterr().out
    assert "PROJECT FOUNDATION AUDIT" in ausgabe
    assert "FOUNDATION READY" in ausgabe
    assert "NOT READY" not in ausgabe


def test_blocker_liefert_exitcode_eins_und_nennt_massnahme(
    project: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (project / "CLAUDE.md").unlink()
    assert main([str(project)]) == 1
    ausgabe = capsys.readouterr().out
    assert "FOUNDATION NOT READY" in ausgabe
    assert "Required action:" in ausgabe
    assert "Affected Area:" in ausgabe


def test_ungueltiger_pfad_liefert_exitcode_zwei(tmp_path: Path) -> None:
    assert main([str(tmp_path / "gibtsnicht")]) == 2
