"""Kommandozeilen-Einstieg: `foundation-validate [PFAD]`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from foundation_validate.report import render, stream_supports_box
from foundation_validate.validator import validate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="foundation-validate",
        description=(
            "Prueft die Foundation-Dateien eines Projekts auf das, was maschinell "
            "entscheidbar ist. Ergebnis: FOUNDATION VALID oder FOUNDATION INVALID - "
            "nicht FOUNDATION READY, darueber entscheidet das Review."
        ),
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Wurzelverzeichnis des zu pruefenden Projekts (Standard: aktuelles Verzeichnis).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Nur den Exit-Code liefern, keinen Report ausgeben.",
    )
    return parser


def _write(text: str) -> None:
    """Gibt den Report aus, auch auf Konsolen, die einzelne Zeichen nicht darstellen.

    Der Rahmen ist ueber `stream_supports_box` abgefangen; Dateinamen aus einem fremden
    Projekt sind es nicht. Ein Umlaut im Pfad soll den Lauf nicht abbrechen (ADR-0007).
    """
    try:
        sys.stdout.write(text)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "ascii"
        sys.stdout.write(text.encode(encoding, errors="replace").decode(encoding))


def main(argv: list[str] | None = None) -> int:
    """Exit-Code 0 wenn FOUNDATION VALID, sonst 1. 2 bei ungueltigem Pfad."""
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Kein Verzeichnis: {root}", file=sys.stderr)
        return 2
    result = validate(root)
    if not args.quiet:
        _write(render(result, ascii_only=not stream_supports_box(sys.stdout)))
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
