"""Merge-Skript der Werkstatt -- Skizze aus project-werkstatt.

Einziger Weg zum Merge. Laeuft immer in der Fassung von origin/main:

    git fetch origin && git show origin/main:{{MERGE_SKRIPT_PFAD}} | python - <pr-nummer>

Prueft G-1 bis G-8 in dieser Reihenfolge und bricht beim ersten Fehlschlag ab. Die Meldung
nennt den Punkt. Mit --pruefen laeuft alles ausser dem Merge (Pruefmodus fuer Proben und
Rueckschau).

Die geaenderten Dateien kommen aus einem lokalen `git diff --no-renames` gegen origin/main,
nicht aus `gh pr view --json files`: Die API-Liste kann gekappt sein, und eine Umbenennung aus
einem Sperrpfad heraus muss als Aenderung am alten Pfad zaehlen.

Offen (im Aufsetz-Block festzulegen, die Probe-PRs sind das Abnahmekriterium):
- G-2: Vergleich der SHA im Testbericht mit dem PR-Kopf (der Merge selbst ist per
  --match-head-commit gebunden).
- G-4: Waechter gegen aufgeweichte Tests und Workflow-Lockerung, Skip-Erlaubnisliste.
  Der Arbeitskopie-Abgleich (g4_working_copy) ist ausgefuehrt; seine Proben stehen in
  reference/leitplanken.md.
- G-5: Wie das Lebenszeichen je Check gelesen wird (Job-Zusammenfassung, Artefakt).
- G-7: Pruefung der Abweichungsliste.
- G-8: die Erlaubnisliste der Gate-Autoren. Das Marker-Format v1 steht (gleich gate_stop.py).
  Grenze: Schreibt das Gate unter derselben Identitaet, die mergt, bleibt der Marker
  Selbstauskunft; die Autorpruefung faengt nur Kommentare fremder Konten.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

REPO_SLUG = "{{REPO_SLUG}}"  # owner/name
REQUIRED_CHECKS_FILE = "{{PFLICHT_CHECK_LISTE}}"  # Datei im Repo, ein Check-Name je Zeile
WORKFLOW = "{{WORKFLOW_DATEI}}"  # z. B. pr.yml
WORKSHOP_PATHS = ("{{WERKSTATT_PFADE}}",)  # z. B. ".github/workflows/", Waechter, Listen
GATE_AUTHORS = ("{{GATE_AUTOREN}}",)  # Logins, deren Gate-Kommentare zaehlen
# Sperrpfade: die Pruefer (Agents, Skills, Hooks, Einstellungen) und jeder Ladeweg fuer
# Anweisungen -- CLAUDE.md, CLAUDE.local.md und AGENTS.md in jedem Ordner, .claude/rules/ in
# jedem Ordner, Output-Styles, Agent-Memory. Gleich der Liste in ci-werkstatt.yml (zweimal).
LOCKED_PATHS = re.compile(
    r"^\.claude/(agents|skills|hooks|output-styles)/|^\.claude/settings[^/]*\.json$"
    r"|^\.claude/agent-memory[^/]*/|(^|/)\.claude/rules/|(^|/)(CLAUDE|CLAUDE\.local|AGENTS)\.md$",
    re.IGNORECASE,
)
# Weitere einzelne Dateien des Projekts per Entscheidung, z. B. eine Token-Datei, die ein
# Bildvergleich byte-gleich verlangt. Regeldatei und jede CLAUDE.md deckt LOCKED_PATHS ab.
LOCKED_FILES: tuple[str, ...] = ()
LOCKED_DIRS = (
    ".claude/agents",
    ".claude/hooks",
    ".claude/skills",
    ".claude/output-styles",
    ":(glob).claude/agent-memory*/**",
)
LOADING_PATHS = (
    ":(glob,icase)**/CLAUDE.md",
    ":(glob,icase)**/CLAUDE.local.md",
    ":(glob,icase)**/AGENTS.md",
    ":(glob,icase)**/.claude/rules/**",
)
SETTINGS_GLOB = ":(glob).claude/settings*.json"
SETTINGS_ALLOWED_UNTRACKED = (".claude/settings.local.json",)
# Gate-Marker v1: erste Zeile des Kommentars, gleich dem Muster in gate_stop.py.
GATE_MARKER = re.compile(r"\A<!-- werkstatt-gate v1 sha=([0-9a-f]{40}) urteil=(ja|nein) -->$", re.M)
# Abschnitt "## Geprueft" reicht bis zur naechsten Ueberschrift "## ".
SCOPE_SECTION = re.compile(r"^## Gepr(?:ü|ue)ft[ \t]*$(.*?)(?=^## |\Z)", re.DOTALL | re.MULTILINE)
MIN_SCOPE_CHARS = 20  # Buchstaben/Ziffern im Abschnitt "Geprueft"
DEPENDABOT_LOGINS = ("dependabot[bot]", "app/dependabot", "dependabot")


class Red(Exception):
    """Ein G-Punkt ist nicht erfuellt; der Text nennt ihn."""


def run(*args: str) -> str:
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def gh_json(*args: str) -> object:
    return json.loads(run("gh", *args))


def required_checks() -> list[str]:
    text = run("git", "show", f"origin/main:{REQUIRED_CHECKS_FILE}")
    return [z.strip() for z in text.splitlines() if z.strip() and not z.startswith("#")]


def changed_files(pr: str, sha: str) -> list[str]:
    run("git", "fetch", "origin", f"pull/{pr}/head")
    fetched = run("git", "rev-parse", "FETCH_HEAD").strip()
    if fetched != sha:
        raise Red(f"G-2: PR-Kopf hat sich bewegt ({sha} gegen geholt {fetched}) -- neu starten")
    diff = run("git", "diff", "--no-renames", "--name-only", f"origin/main...{sha}")
    return [line for line in diff.splitlines() if line]


def g1_checks(sha: str) -> None:
    data = gh_json("api", f"repos/{REPO_SLUG}/commits/{sha}/check-runs", "--paginate")
    assert isinstance(data, dict)
    result = {r["name"]: r["conclusion"] for r in data["check_runs"]}
    for name in required_checks():
        if result.get(name) != "success":
            raise Red(f"G-1: Pflicht-Check {name!r} ist {result.get(name)!r}, nicht success")


def g3_up_to_date(sha: str) -> None:
    probe = subprocess.run(["git", "merge-base", "--is-ancestor", "origin/main", sha])
    if probe.returncode != 0:
        raise Red("G-3: PR-Kopf enthaelt origin/main nicht -- gh pr update-branch, kein Rebase")


def is_locked(path: str) -> bool:
    locked_files = {f.lower() for f in LOCKED_FILES}
    return bool(LOCKED_PATHS.search(path)) or path.lower() in locked_files


def g4_locked_paths(files: list[str]) -> None:
    touched = [f for f in files if is_locked(f)]
    if touched:
        raise Red(f"G-4: Sperrpfad beruehrt: {', '.join(touched)}")
    # Offen: Waechter und Skip-Erlaubnisliste aus origin/main gegen den PR-Diff ausfuehren.


def worktree_paths() -> list[str]:
    porcelain = run("git", "worktree", "list", "--porcelain")
    paths = [z.split(" ", 1)[1] for z in porcelain.splitlines() if z.startswith("worktree ")]
    missing = [p for p in paths if not os.path.isdir(p)]
    if missing:
        raise Red(f"G-4: Worktree fehlt ({', '.join(missing)}) -- git worktree prune, neu starten")
    return paths


def g4_working_copy() -> None:
    """Arbeitskopie-Abgleich: G-4 schuetzt den Commit-Weg, nicht die laufende Session."""
    locked = [*LOCKED_DIRS, *LOADING_PATHS, SETTINGS_GLOB, *LOCKED_FILES]
    for wt in worktree_paths():
        changed = run("git", "-C", wt, "diff", "--name-only", "origin/main", "--", *locked)
        if changed.strip():
            raise Red(f"G-4: Sperrpfad in der Arbeitskopie {wt} geaendert: {changed.splitlines()}")
        # Ohne --exclude-standard: ignorierte Dateien zaehlen mit.
        # Auch __pycache__ zaehlt: Eine passende .pyc ersetzt beim Import die Quelle. Hooks
        # laufen deshalb mit `python -B` (LP-8), dann entsteht legitim keine.
        untracked = run(
            "git", "-C", wt, "ls-files", "--others", "--", *LOCKED_DIRS, *LOADING_PATHS
        ).splitlines()
        if untracked:
            raise Red(f"G-4: ungetrackte Datei unter einem Sperrpfad in {wt}: {untracked}")
        settings = run("git", "-C", wt, "ls-files", "--others", "--", SETTINGS_GLOB).splitlines()
        foreign = [s for s in settings if s not in SETTINGS_ALLOWED_UNTRACKED]
        if foreign:
            raise Red(f"G-4: fremde ungetrackte Einstellungsdatei in {wt}: {foreign}")
        for name in [
            *settings,
            *run("git", "-C", wt, "ls-files", "--", SETTINGS_GLOB).splitlines(),
        ]:
            with open(f"{wt}/{name}", encoding="utf-8") as datei:
                if "disableAllHooks" in datei.read():
                    raise Red(f"G-4: disableAllHooks in {wt}/{name}")


def g6_main_green(labels: list[str]) -> None:
    runs = gh_json(
        "run", "list", "--workflow", WORKFLOW, "--branch", "main",
        "--status", "completed", "--limit", "1", "--json", "conclusion",
    )  # fmt: skip
    assert isinstance(runs, list)
    if runs and runs[0]["conclusion"] != "success" and "nacharbeit" not in labels:
        raise Red("G-6: main ist rot -- nur PRs mit Label nacharbeit")


def is_workshop(path: str) -> bool:
    return any(path.startswith(p) for p in WORKSHOP_PATHS)


def g7_workshop(files: list[str]) -> None:
    workshop = [f for f in files if is_workshop(f)]
    if workshop and len(workshop) != len(files):
        raise Red("G-7: Werkstatt-PR mit Dateien ausserhalb der Werkstatt-Pfade")
    # Offen: Lockerung nur mit genau einem vollstaendigen Abweichungseintrag; Werte aus
    # Entscheidungen nie lockerbar.


def scope_is_filled(body: str) -> bool:
    match = SCOPE_SECTION.search(body)
    if not match:
        return False
    return len(re.findall(r"[^\W_]", match.group(1))) >= MIN_SCOPE_CHARS


def g8_gate(pr: str, sha: str, author: str, files: list[str]) -> None:
    if author in DEPENDABOT_LOGINS and not any(is_workshop(f) for f in files):
        return
    data = gh_json("pr", "view", pr, "--json", "comments")
    assert isinstance(data, dict)
    verdicts: list[tuple[str, str, str]] = []
    for comment in data["comments"]:
        match = GATE_MARKER.search(comment["body"].strip())
        if not match:
            continue
        login = (comment.get("author") or {}).get("login")
        if login not in GATE_AUTHORS:
            continue  # Marker fremder oder geloeschter Konten zaehlen nicht
        verdicts.append((match.group(1), match.group(2), comment["body"]))
    if sum(1 for _, verdict, _ in verdicts if verdict == "nein") >= 2:
        raise Red("G-8: zweites Gate-nein im PR -- PR bleibt ungemergt, naechster Block")
    at_head = [v for v in verdicts if v[0] == sha]
    if len(at_head) != 1:
        raise Red(f"G-8: {len(at_head)} Gate-Marker zur Kopf-SHA, verlangt genau einer")
    _, verdict, body = at_head[0]
    if verdict != "ja":
        raise Red("G-8: Gate-Urteil zur Kopf-SHA ist nein")
    if not scope_is_filled(body):
        raise Red("G-8: Gate-Urteil ohne Pruefumfang")


def main(argv: list[str]) -> int:
    check_only = "--pruefen" in argv
    pr = next(a for a in argv if not a.startswith("--"))
    run("git", "fetch", "origin")
    info = gh_json("pr", "view", pr, "--json", "headRefOid,labels,author")
    assert isinstance(info, dict)
    sha: str = info["headRefOid"]
    labels = [label["name"] for label in info["labels"]]
    author: str = info["author"]["login"]
    try:
        files = changed_files(pr, sha)
        g1_checks(sha)
        # G-2: Merge per --match-head-commit; SHA-Vergleich des Testberichts offen (Docstring).
        g3_up_to_date(sha)
        g4_locked_paths(files)
        g4_working_copy()
        # G-5 offen: Lebenszeichen je Pflicht-Check > 0.
        g6_main_green(labels)
        g7_workshop(files)
        g8_gate(pr, sha, author, files)
    except Red as reason:
        print(f"ROT {reason}")
        return 1
    if check_only:
        print(f"GRUEN {sha} (Pruefmodus, kein Merge)")
        return 0
    run(
        "gh", "pr", "merge", pr, "--merge", "--match-head-commit", sha,
        "--body", f"Gemergt-durch: merge-gruen {sha}",
    )  # fmt: skip
    print(f"GEMERGT {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
