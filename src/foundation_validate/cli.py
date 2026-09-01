"""Kommandozeilen-Einstieg: `foundation-validate [PFAD]`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from foundation_validate.report import render
from foundation_validate.validator import validate


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="foundation-validate",
        description="Prueft die Foundation-Dateien eines Projekts und erzeugt den Audit-Report.",
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


def main(argv: list[str] | None = None) -> int:
    """Exit-Code 0 wenn FOUNDATION READY, sonst 1. 2 bei ungueltigem Pfad."""
    args = build_parser().parse_args(argv)
    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Kein Verzeichnis: {root}", file=sys.stderr)
        return 2
    result = validate(root)
    if not args.quiet:
        print(render(result), end="")
    return 0 if result.ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
