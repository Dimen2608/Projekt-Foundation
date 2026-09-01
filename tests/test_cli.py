"""Prueft die Schnittstelle, auf die sich CI und Agents verlassen: Exit-Code und Report."""

from __future__ import annotations

import io
import sys
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


def _lauf_mit_konsole(project: Path, monkeypatch: pytest.MonkeyPatch, encoding: str) -> str:
    """Ruft die CLI mit einer Konsole der angegebenen Codepage auf und liefert die Ausgabe."""
    puffer = io.BytesIO()
    strom = io.TextIOWrapper(puffer, encoding=encoding, newline="")
    monkeypatch.setattr(sys, "stdout", strom)
    assert main([str(project)]) == 0
    strom.flush()
    return puffer.getvalue().decode(encoding)


def test_report_laeuft_auf_konsole_ohne_utf8(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Windows-Standardkonsole (cp1252): kein Absturz, ASCII-Rahmen statt Rahmenzeichen."""
    ausgabe = _lauf_mit_konsole(project, monkeypatch, "cp1252")
    assert "PROJECT FOUNDATION AUDIT" in ausgabe
    assert "+" + "-" * 38 + "+" in ausgabe
    assert "?" not in ausgabe


def test_report_behaelt_den_rahmen_auf_utf8_konsole(
    project: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    ausgabe = _lauf_mit_konsole(project, monkeypatch, "utf-8")
    assert "╔" + "═" * 38 + "╗" in ausgabe
