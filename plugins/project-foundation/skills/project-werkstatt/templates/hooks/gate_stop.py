"""Stop-Hook des KI-Review-Gates (im Subagent als SubagentStop) -- Vorlage aus project-werkstatt.

Ziel im Repo: `.claude/hooks/gate_stop.py` (Sperrpfad).

Erlaubt das Beenden nur, wenn
  1. Arbeitsbaum und Index unveraendert sind: `git status --porcelain` ist leer (das Gate laeuft
     nach Push und PR, der Baum ist sauber; `.claude/run/` ist ignoriert);
  2. `.claude/run/gate-urteil.md` mit einem Gate-Marker v1 beginnt, zur Kopf-SHA
     `git rev-parse HEAD`;
  3. die Abschnitte "Geprueft", "Sicherheitsbericht" und "Freigabe" nicht leer sind und die
     Freigabe dem Urteil im Marker entspricht;
  4. bei urteil=ja unter "Blockierend" nichts oder "keine" steht.
Ausweg: `.claude/run/abbruch.md` mit Grund; dann gibt es kein Urteil, und ein Abbruch ist kein ja.
Ob der Kommentar im PR steht, prueft das Merge-Skript (G-8), nicht dieser Hook.

Feuert-Nachweis: Urteil fehlt; "Geprueft" leer; Freigabe gegen Marker; fremde SHA; Baum
geaendert; "ja" mit Fund -> Exit 2. Gueltiges Urteil; "nein" mit Fund; Abbruch -> Exit 0.
"""

from __future__ import annotations

import os
import re
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import werkstatt_hook as wh  # noqa: E402

# Gleich dem Muster in merge-gruen.py; beide aendern sich nur zusammen.
GATE_MARKER = re.compile(r"^<!-- werkstatt-gate v1 sha=([0-9a-f]{40}) urteil=(ja|nein) -->$")
PFLICHT = ("Geprüft", "Sicherheitsbericht", "Freigabe")


def abschnitte(text: str) -> dict[str, list[str]]:
    teile: dict[str, list[str]] = {}
    name: str | None = None
    for zeile in text.splitlines()[1:]:
        m = re.match(r"^## (.+?)\s*$", zeile)
        if m:
            name = m.group(1)
            teile[name] = []
        elif name is not None and zeile.strip():
            teile[name].append(zeile.strip())
    return teile


def hauptteil(root: str, payload: dict[str, Any]) -> wh.Ergebnis:
    if wh.abbruch_annehmen(root):
        return 0, "abbruch", "Abbruch ohne Urteil, Grund in .claude/run/abbruch.md"
    status = wh.git(root, "status", "--porcelain", "--untracked-files=all")
    if status:
        return 2, "block", "Stopp verweigert: Das Gate hat den Arbeitsbaum geaendert:\n" + status
    pfad = os.path.join(wh.run_dir(root), "gate-urteil.md")
    if not os.path.exists(pfad):
        return 2, "block", "Stopp verweigert: .claude/run/gate-urteil.md fehlt."
    with open(pfad, encoding="utf-8") as f:
        text = f.read()
    m = GATE_MARKER.match(text.splitlines()[0] if text else "")
    if not m:
        return 2, "block", "Stopp verweigert: erste Zeile ist kein Gate-Marker v1."
    kopf = wh.git(root, "rev-parse", "HEAD")
    if m.group(1) != kopf:
        return 2, "block", f"Stopp verweigert: Marker-SHA {m.group(1)} ist nicht HEAD {kopf}."
    teile = abschnitte(text)
    leer = [p for p in PFLICHT if not teile.get(p)]
    if leer:
        return 2, "block", "Stopp verweigert: leere Abschnitte: " + ", ".join(leer)
    freigabe = teile["Freigabe"][0]
    if freigabe.lower() != m.group(2):
        meldung = f"Stopp verweigert: Freigabe {freigabe!r} widerspricht urteil={m.group(2)}."
        return 2, "block", meldung
    blockierend = [z for z in teile.get("Blockierend", []) if z.lower() != "keine"]
    if m.group(2) == "ja" and blockierend:
        return 2, "block", "Stopp verweigert: urteil=ja, aber 'Blockierend' nennt Funde."
    return 0, "allow", f"Urteil {m.group(2)} zu {kopf}"


if __name__ == "__main__":
    wh.ausfuehren(hauptteil)
