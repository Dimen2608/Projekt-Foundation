"""Gemeinsame Teile der Werkstatt-Hooks -- Vorlage aus project-werkstatt.

Ziel im Repo: `.claude/hooks/werkstatt_hook.py` (Sperrpfad). Nur Standardbibliothek.

Konvention LP-8 (reference/leitplanken.md):
1. Jeder Aufruf schreibt eine Zeile nach `.claude/run/hook-audit.log`.
2. Ein eigener Fehler endet mit Exit 2 (fail-closed), die Meldung geht nach stderr.
3. `.claude/run/` ist gitignored und geht nicht in den Baum-Hash ein.
4. Der letzte Payload je Event liegt als Fixture in `.claude/run/payload-<event>.json`, ohne
   `tool_response` (LP-7). Aus ihm entstehen die Proben mit echtem Payload.

Voraussetzungen: Python 3, git ab 2.31 (`rev-parse --path-format`), `.gitignore` mit
`.claude/run/` und `.claude/worktrees/`. Aufruf mit `python3 -B`, damit kein `__pycache__` unter
dem Sperrpfad entsteht (Arbeitskopie-Abgleich im Merge-Skript).
"""

from __future__ import annotations

import contextlib
import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Callable
from typing import Any

Ergebnis = tuple[int, str, str]  # (Exit-Code, Entscheidung, Meldung)


def git(root: str, *args: str, env: dict[str, str] | None = None) -> str:
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def wurzel(payload: dict[str, Any]) -> str:
    """Wurzel des Arbeitsbaums der Rolle: aus `cwd` des Payloads, damit eine Rolle im eigenen
    Worktree dort geprueft wird (Probe beim Aufsetzen), sonst CLAUDE_PROJECT_DIR."""
    start = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    return git(str(start), "rev-parse", "--show-toplevel")


def run_dir(root: str) -> str:
    d = os.path.join(root, ".claude", "run")
    os.makedirs(d, exist_ok=True)
    return d


def jetzt() -> str:
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def baum(root: str) -> str:
    """Hash des Arbeitsbaums samt ungetrackter, nicht ignorierter Dateien; der Index bleibt
    unberuehrt (Kopie unter GIT_INDEX_FILE)."""
    index = git(root, "rev-parse", "--path-format=absolute", "--git-path", "index")
    with tempfile.TemporaryDirectory() as tmp:
        kopie = os.path.join(tmp, "index")
        if os.path.exists(index):
            shutil.copyfile(index, kopie)
        env = dict(os.environ, GIT_INDEX_FILE=kopie)
        git(root, "add", "-A", env=env)
        return git(root, "write-tree", env=env)


def abbruch_annehmen(root: str, nicht_aelter_als: float = 0.0) -> bool:
    """Ausweg aus einem Stopp-Veto: `.claude/run/abbruch.md` mit Grund. Gilt genau einmal und
    wird zu `abbruch-<zeit>.md`; die Bau-Session liest den Grund dort."""
    run = run_dir(root)
    pfad = os.path.join(run, "abbruch.md")
    if not os.path.exists(pfad) or os.path.getmtime(pfad) < nicht_aelter_als:
        return False
    with open(pfad, encoding="utf-8") as f:
        if not f.read().strip():
            return False
    os.replace(pfad, os.path.join(run, f"abbruch-{jetzt().replace(':', '')}.md"))
    return True


def audit(root: str, payload: dict[str, Any], entscheidung: str, grund: str) -> None:
    zeile = "\t".join(
        [
            jetzt(),
            str(payload.get("hook_event_name", "")),
            str(payload.get("tool_name", "")),
            str(payload.get("agent_type", "")),
            os.path.basename(sys.argv[0]),
            entscheidung,
            grund.replace("\n", " ")[:300],
        ]
    )
    with open(os.path.join(run_dir(root), "hook-audit.log"), "a", encoding="utf-8") as f:
        f.write(zeile + "\n")


def aufzeichnen(root: str, payload: dict[str, Any]) -> None:
    ohne = {k: v for k, v in payload.items() if k != "tool_response"}
    name = f"payload-{payload.get('hook_event_name', 'unbekannt')}.json"
    with open(os.path.join(run_dir(root), name), "w", encoding="utf-8") as f:
        json.dump(ohne, f, ensure_ascii=False, indent=1)


def ausfuehren(hauptteil: Callable[[str, dict[str, Any]], Ergebnis]) -> None:
    """Liest den Payload, ruft hauptteil(root, payload) und endet mit dessen Exit-Code.
    Exit 2 bei eigenem Fehler; die Meldung liest das Modell auf stderr."""
    payload: dict[str, Any] = {}
    root = os.getcwd()
    with contextlib.suppress(Exception):
        sys.stderr.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    try:
        payload = json.load(sys.stdin)
        root = wurzel(payload)
        aufzeichnen(root, payload)
        code, entscheidung, meldung = hauptteil(root, payload)
    except Exception as e:  # fail-closed
        code, entscheidung, meldung = 2, "fehler", f"Hook-Fehler (fail-closed): {e!r}"
    try:
        audit(root, payload, entscheidung, meldung)
    except Exception as e:
        code, meldung = 2, f"{meldung} | Audit-Zeile nicht geschrieben: {e!r}"
    if code == 2:
        print(meldung, file=sys.stderr)
    sys.exit(code)
