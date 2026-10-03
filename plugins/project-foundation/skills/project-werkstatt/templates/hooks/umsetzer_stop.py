"""Stop-Hook des Umsetzers (im Subagent als SubagentStop) -- Vorlage aus project-werkstatt.

Ziel im Repo: `.claude/hooks/umsetzer_stop.py` (Sperrpfad).

Erlaubt das Beenden nur, wenn die Umsetzer-Kette zum jetzigen Baum B vollstaendig ist:
  1. es gibt eine Zeile `simplify`;
  2. danach eine Zeile `tests-gruen` mit B;
  3. danach eine Zeile `security-review` mit B;
  4. `.claude/run/sicherheitsbericht-B.md` und `.claude/run/sicherheitsvermerke-B.md` liegen vor
     (die Vermerkdatei auch mit der Zeile "keine Befunde");
  5. die Wachposten-Liste des Test-Autors liegt im Baum: erste Zeile `branch: <name>` gleich dem
     jetzigen Branch, danach je Zeile `<classname>::<name>` (JUnit) eines Tests, dessen
     Mutationsprobe vor dem Bau nicht moeglich war, sonst die Zeile "keine". Zu jedem Eintrag
     gibt es nach dem letzten `simplify` eine Zeile `mutant-rot` mit diesem Eintrag und einem
     Mutanten-Baum M ungleich B, und M unterscheidet sich von B in mindestens einer Datei
     ausserhalb des Testverzeichnisses (der Mutant sass im Produktcode und ist zurueck).
Rueckweg: Liegt zwischen dem letzten `simplify` und der letzten `security-review`-Zeile eine
weitere `security-review`-Zeile, wurde nach einem Bericht geaendert, ohne `/simplify` erneut zu
rufen.
Ausweg: `.claude/run/abbruch.md` mit Grund, juenger als die letzte Kette-Zeile.

Feuert-Nachweis (Proben ohne Modell, Fixture-Payload, Wegwerf-Repo): ohne `simplify`; nur rote
Tests; Berichte fehlen; Baum nach dem Bericht geaendert; Rueckweg ohne neues `simplify`; Abbruch
ein zweites Mal; Liste fehlt; Liste eines fremden Branchs; Mutationsprobe fehlt; Mutant ohne
Aenderung; Mutant ueberlebt; nur `error`; Mutant nur im Testverzeichnis -> Exit 2. Vollstaendige
Kette, "keine" in der Liste, Abbruch mit Grund -> Exit 0. Mutant des Hooks: `sys.exit(0)` als
erste Zeile -> die erste Probe muss das erkennen.
"""

from __future__ import annotations

import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import werkstatt_hook as wh  # noqa: E402

TESTVERZEICHNIS = "{{TESTVERZEICHNIS}}"  # z. B. "tests/", mit Schraegstrich am Ende
LISTE = TESTVERZEICHNIS + "wachposten-offen.txt"


def lies_kette(run: str) -> list[list[str]]:
    pfad = os.path.join(run, "kette.log")
    if not os.path.exists(pfad):
        return []
    with open(pfad, encoding="utf-8") as f:
        return [z.rstrip("\n").split("\t") for z in f if z.strip()]


def letzter(kette: list[list[str]], ereignis: str, ab: int = -1, b: str | None = None) -> int:
    treffer = [
        i for i, z in enumerate(kette) if i > ab and z[1] == ereignis and (b is None or z[2] == b)
    ]
    return max(treffer, default=-1)


def pruefe_kette(kette: list[list[str]], b: str, run: str) -> str | None:
    i_simplify = letzter(kette, "simplify")
    if i_simplify < 0:
        return "Kein Aufruf von /simplify protokolliert."
    i_tests = letzter(kette, "tests-gruen", i_simplify, b)
    if i_tests < 0:
        return f"Nach /simplify fehlt ein gruener Testlauf zum jetzigen Baum {b}."
    i_sr = letzter(kette, "security-review", i_tests, b)
    if i_sr < 0:
        return f"Nach dem gruenen Testlauf fehlt /security-review zum jetzigen Baum {b}."
    if any(z[1] == "security-review" for z in kette[i_simplify + 1 : i_sr]):
        return "Nach einer Behebung aus dem Sicherheitsbericht fehlt /simplify erneut (Rueckweg)."
    for name in ("sicherheitsbericht", "sicherheitsvermerke"):
        if not os.path.exists(os.path.join(run, f"{name}-{b}.md")):
            return f"Es fehlt .claude/run/{name}-{b}.md."
    return None


def pruefe_mutation(root: str, kette: list[list[str]], b: str) -> str | None:
    pfad = os.path.join(root, LISTE)
    if not os.path.exists(pfad):
        return f"Es fehlt {LISTE} (Liste des Test-Autors, sonst die Zeile 'keine')."
    with open(pfad, encoding="utf-8") as f:
        zeilen = [z.strip() for z in f if z.strip()]
    branch = wh.git(root, "rev-parse", "--abbrev-ref", "HEAD")
    if not zeilen or zeilen[0] != f"branch: {branch}":
        return f"{LISTE} gehoert nicht zu diesem Branch {branch} (erste Zeile)."
    namen = [z for z in zeilen[1:] if z != "keine"]
    i_simplify = letzter(kette, "simplify")
    gefangen = set()
    for z in kette[i_simplify + 1 :]:
        if z[1] == "mutant-rot" and len(z) > 3 and z[2] != b and z[3] in namen:
            geaendert = wh.git(root, "diff-tree", "-r", "--name-only", z[2], b).splitlines()
            if any(not d.startswith(TESTVERZEICHNIS) for d in geaendert):
                gefangen.add(z[3])
    offen = [n for n in namen if n not in gefangen]
    if offen:
        return f"Mutationsprobe im Produktcode fehlt oder blieb gruen fuer: {', '.join(offen)}."
    return None


def hauptteil(root: str, payload: dict[str, Any]) -> wh.Ergebnis:
    run = wh.run_dir(root)
    kette = lies_kette(run)
    seit = os.path.getmtime(os.path.join(run, "kette.log")) if kette else 0.0
    if wh.abbruch_annehmen(root, seit):
        return 0, "abbruch", "Abbruch mit Grund in .claude/run/abbruch.md"
    b = wh.baum(root)
    fehlt = pruefe_kette(kette, b, run) or pruefe_mutation(root, kette, b)
    if fehlt:
        return (
            2,
            "block",
            (
                f"Stopp verweigert: {fehlt} Fuehre die Kette zu Ende (.claude/rules/regeln.md, "
                "Abschnitt Kette) oder schreibe den Grund nach .claude/run/abbruch.md."
            ),
        )
    return 0, "allow", f"Kette vollstaendig zu {b}"


if __name__ == "__main__":
    wh.ausfuehren(hauptteil)
