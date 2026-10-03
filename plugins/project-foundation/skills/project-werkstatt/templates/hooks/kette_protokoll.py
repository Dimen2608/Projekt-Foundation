"""PostToolUse-Hook des Umsetzers (Matcher `Skill|Bash`) -- Vorlage aus project-werkstatt.

Ziel im Repo: `.claude/hooks/kette_protokoll.py` (Sperrpfad).

Schreibt je Ereignis eine Zeile nach `.claude/run/kette.log`:
    <zeit> TAB <ereignis> TAB <baum-hash> [TAB <testfall>]
Ereignisse:
- `simplify`, `security-review`: Aufruf des Skills ueber das Skill-Werkzeug.
- `tests-gruen`, `tests-rot`: ein Bash-Befehl mit `--junitxml=.claude/run/testbericht.xml`.
  Gruen heisst: mindestens ein Test, null failures, null errors. Der Bericht wird danach zu
  `testbericht-<baum>.xml`, damit ein alter Bericht nie ein zweites Mal zaehlt.
- `mutant-rot`, `mutant-gruen`: Mutationsprobe nach dem Bau, ein Bash-Befehl mit
  `--junitxml=.claude/run/mutationsbericht.xml`. Je Testfall mit `failure` eine Zeile
  `mutant-rot` mit `<classname>::<name>` in der vierten Spalte; ein `error` (etwa ein
  Syntaxfehler) zaehlt nicht als Fang. Ohne `failure`: eine Zeile `mutant-gruen`.

Grenze: Der Hook belegt den Aufruf, nicht die Wirkung, und nicht die Echtheit der Zeilen --
`.claude/run/` ist fuer den Umsetzer per Bash beschreibbar. Netze: Gate Punkt 0, volle Suite in
der CI (G-1, G-5), Transkript-Maske der Rueckschau.
Offen (Probe beim Aufsetzen, echter Payload): ob das Skill-Werkzeug den Namen im Feld `skill`
uebergibt und mit oder ohne Namensraum.
"""

from __future__ import annotations

import os
import sys
import xml.etree.ElementTree as ET
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import werkstatt_hook as wh  # noqa: E402

KETTE_SKILLS = ("simplify", "security-review")
BERICHT = os.path.join(".claude", "run", "testbericht.xml")
MUTATION = os.path.join(".claude", "run", "mutationsbericht.xml")


def skill_name(tool_input: dict[str, Any]) -> str:
    name = str(tool_input.get("skill") or tool_input.get("name") or "").strip().lstrip("/")
    return name.split(":")[-1]


def zaehle(pfad: str) -> tuple[int, int]:
    wurzel = ET.parse(pfad).getroot()
    suiten = [wurzel] if wurzel.tag == "testsuite" else wurzel.findall("testsuite")
    tests = sum(int(s.get("tests", 0)) for s in suiten)
    rot = sum(int(s.get("failures", 0)) + int(s.get("errors", 0)) for s in suiten)
    return tests, rot


def rote_faelle(pfad: str) -> list[str]:
    return [
        f"{f.get('classname', '')}::{f.get('name', '')}"
        for f in ET.parse(pfad).getroot().iter("testcase")
        if f.find("failure") is not None
    ]


def hauptteil(root: str, payload: dict[str, Any]) -> wh.Ergebnis:
    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input") or {}
    befehl = str(tool_input.get("command", ""))
    ereignis: str | None = None
    namen: list[str] = []
    bericht: str | None = None
    if tool == "Skill":
        name = skill_name(tool_input)
        if name in KETTE_SKILLS:
            ereignis = name
    elif tool == "Bash" and "--junitxml=.claude/run/testbericht.xml" in befehl:
        bericht = BERICHT
        if not os.path.exists(os.path.join(root, bericht)):
            return 2, "kein-bericht", f"Testlauf ohne Bericht unter {bericht}: nicht protokolliert."
        tests, rot = zaehle(os.path.join(root, bericht))
        ereignis = "tests-gruen" if tests > 0 and rot == 0 else "tests-rot"
    elif tool == "Bash" and "--junitxml=.claude/run/mutationsbericht.xml" in befehl:
        bericht = MUTATION
        if not os.path.exists(os.path.join(root, bericht)):
            return 2, "kein-bericht", f"Mutationsprobe ohne Bericht unter {bericht}."
        namen = rote_faelle(os.path.join(root, bericht))
        ereignis = "mutant-rot" if namen else "mutant-gruen"
    if ereignis is None:
        return 0, "ohne-ereignis", str(tool)
    b = wh.baum(root)
    if bericht:
        ziel = os.path.basename(bericht).replace(".xml", f"-{b}.xml")
        os.replace(os.path.join(root, bericht), os.path.join(wh.run_dir(root), ziel))
    zeilen = [[wh.jetzt(), ereignis, b, n] for n in namen] or [[wh.jetzt(), ereignis, b]]
    with open(os.path.join(wh.run_dir(root), "kette.log"), "a", encoding="utf-8") as f:
        f.writelines("\t".join(z) + "\n" for z in zeilen)
    return 0, "protokolliert", f"{ereignis} {b}"


if __name__ == "__main__":
    wh.ausfuehren(hauptteil)
