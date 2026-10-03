"""Stop-Hook des Test-Autors (im Subagent als SubagentStop) -- Vorlage aus project-werkstatt.

Ziel im Repo: `.claude/hooks/test_autor_stop.py` (Sperrpfad).

Der Test-Autor laeuft im eigenen Worktree (`isolation: worktree`). Erlaubt das Beenden nur, wenn
  1. gegenueber `origin/main` (Commits und Arbeitsbaum) nur Dateien im Testverzeichnis geaendert
     sind und keine unter SPERRPFADE_IN_TESTS -- damit ist jeder Mutant zurueckgenommen und keine
     Produktdatei beruehrt;
  2. mindestens eine Testdatei geaendert ist.
Ausweg: `.claude/run/abbruch.md` mit Grund, etwa "Kriterium nicht testbar".

Feuert-Nachweis: nichts geaendert; Mutant im Produktcode; Datei unter einem Sperrpfad im
Testverzeichnis -> Exit 2. Nur Tests, unkommittet und kommittet -> Exit 0.
"""

from __future__ import annotations

import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import werkstatt_hook as wh  # noqa: E402

TESTVERZEICHNIS = "{{TESTVERZEICHNIS}}"  # z. B. "tests/", mit Schraegstrich am Ende
# Sperrpfade innerhalb des Testverzeichnisses, z. B. abgenommene Soll-Bilder eines Bildvergleichs.
SPERRPFADE_IN_TESTS: tuple[str, ...] = ()


def geaendert(root: str) -> list[str]:
    basis = wh.git(root, "merge-base", "HEAD", "origin/main")
    namen = set(wh.git(root, "diff", "--name-only", basis).splitlines())
    namen |= set(wh.git(root, "ls-files", "--others", "--exclude-standard").splitlines())
    return sorted(n for n in namen if n)


def hauptteil(root: str, payload: dict[str, Any]) -> wh.Ergebnis:
    if wh.abbruch_annehmen(root):
        return 0, "abbruch", "Abbruch mit Grund in .claude/run/abbruch.md"
    namen = geaendert(root)
    fremd = [
        n for n in namen if not n.startswith(TESTVERZEICHNIS) or n.startswith(SPERRPFADE_IN_TESTS)
    ]
    if fremd:
        return (
            2,
            "block",
            (
                f"Stopp verweigert: Dateien ausserhalb von {TESTVERZEICHNIS} oder unter einem "
                f"Sperrpfad geaendert: {', '.join(fremd[:10])}. Mutanten zuruecknehmen, "
                "Produktdateien nicht anfassen."
            ),
        )
    if not namen:
        return (
            2,
            "block",
            (
                "Stopp verweigert: keine Testdatei geaendert. Tests schreiben oder den Grund nach "
                ".claude/run/abbruch.md."
            ),
        )
    return 0, "allow", f"{len(namen)} Testdateien"


if __name__ == "__main__":
    wh.ausfuehren(hauptteil)
