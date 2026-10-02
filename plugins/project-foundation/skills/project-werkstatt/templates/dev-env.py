"""dev_env -- isolierte Dev-Umgebung je Worktree. Skizze aus project-werkstatt.

Kopieren nach {{DEV_ENV_PFAD}} (normaler Pfad, kein Sperrpfad; siehe reference/isolation.md).

    python {{DEV_ENV_PFAD}} up       # Schritt 0 des Umsetzers, im Worktree
    python {{DEV_ENV_PFAD}} status
    python {{DEV_ENV_PFAD}} down     # nach dem Merge, vor `git worktree remove`
    python {{DEV_ENV_PFAD}} sweep    # laeuft auch bei jedem `up`

Je Worktree ein Slot (0 bis 9). Ein Slot ist belegt, wenn das Verzeichnis
<git-common-dir>/devenv/slot-<n> existiert; das gemeinsame Git-Verzeichnis sehen alle Worktrees.
Je Slot ein eigenes Compose-Projekt mit eigenem Volume, eigenem DB-Namen, Ports aus dem Slot an
127.0.0.1 und einem Wegwerf-Passwort, das mit `down` endet.

Vertrag mit der Dev-Compose-Datei ({{DEV_COMPOSE_DATEI}}): Sie nennt nur Variablen aus
.env.worktree (siehe ENV_PORTS und write_env_file), ohne Vorgabewerte wie ${DB_PORT:-5432}, bindet
jeden Port an 127.0.0.1 und setzt das Label {{PRAEFIX}}-slot=${SLOT}. Variablen des Betriebs
kommen darin nicht vor.

Offen (im Aufsetz-Block festzulegen, die Proben F-1 bis F-11 sind das Abnahmekriterium):
- PORT_BASIS gemessen waehlen: keine abhoerenden Ports, keine reservierten Bereiche, unterhalb
  des dynamischen Bereichs.
- Migrationen und Seed (MIGRATIONEN, SEED).
- Ob `docker compose -p <projekt> down` ohne Compose-Datei auf dem Zielrechner alles abbaut
  (Sweep einer Waise, deren Worktree fehlt).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

PRAEFIX = "{{PRAEFIX}}"  # kurz, [a-z0-9]
COMPOSE_DATEI = "{{DEV_COMPOSE_DATEI}}"  # relativ zur Wurzel des Worktrees
PORT_BASIS = 24000  # Vorschlag; 10 Slots x 10 Ports
SLOTS = 10
ENV_PORTS = {"DB_PORT": 0, "API_PORT": 1, "WEB_PORT": 2, "MAIL_UI_PORT": 3, "SMTP_PORT": 4}
RESERVE = range(5, 10)  # Versatz 5 bis 9, mitgeprueft, damit der Slot wachsen kann
VERALTET_TAGE = 7  # Vorschlag, nicht gemessen
MIGRATIONEN: list[str] = []  # z. B. ["alembic", "upgrade", "head"]
SEED: list[str] = []  # synthetischer Seed, nie ein Dump aus Prod oder Staging
ENV_DATEI = ".env.worktree"
KENNUNG = re.compile(r"^[a-z0-9-]{1,24}$")


class Abbruch(Exception):
    """Ein Schritt ist gescheitert; der Text sagt, welcher."""


def git(*args: str, cwd: Path | None = None) -> str:
    out = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)
    return out.stdout.strip()


def worktrees() -> list[Path]:
    porcelain = git("worktree", "list", "--porcelain")
    zeilen = porcelain.splitlines()
    return [Path(z.split(" ", 1)[1]).resolve() for z in zeilen if z.startswith("worktree ")]


def wurzel() -> Path:
    return Path(git("rev-parse", "--show-toplevel")).resolve()


def kennung_von(top: Path) -> str:
    kennung = "main" if top == worktrees()[0] else top.name
    if not KENNUNG.match(kennung):
        raise Abbruch(f"Kennung {kennung!r} passt nicht zu {KENNUNG.pattern}")
    return kennung


def slot_wurzel() -> Path:
    common = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir"))
    return common / "devenv"


def projekt(kennung: str) -> str:
    return f"{PRAEFIX}-{kennung}"


def ports(slot: int) -> dict[str, int]:
    return {name: PORT_BASIS + 10 * slot + versatz for name, versatz in ENV_PORTS.items()}


def port_frei(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


def info_schreiben(slot: int, info: dict[str, object]) -> None:
    """Atomar: erst eine Temp-Datei, dann umbenennen. Ein Leser sieht nie eine halbe Datei."""
    verzeichnis = slot_wurzel() / f"slot-{slot}"
    temp = verzeichnis / "info.json.tmp"
    temp.write_text(json.dumps(info), encoding="utf-8")
    os.replace(temp, verzeichnis / "info.json")


def belegte_slots() -> dict[int, dict[str, object]]:
    """Slot -> info. Ein Slot ohne lesbare info.json ist "in Anlage" (info leer), keine Waise."""
    belegt: dict[int, dict[str, object]] = {}
    for verzeichnis in slot_wurzel().glob("slot-*"):
        try:
            daten = json.loads((verzeichnis / "info.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            daten = {}
        belegt[int(verzeichnis.name.removeprefix("slot-"))] = daten
    return belegt


def aktivitaet_merken(top: Path) -> None:
    for slot, info in belegte_slots().items():
        if info.get("worktree") == str(top):
            info_schreiben(slot, {**info, "zuletzt": time.time()})


def slot_von(top: Path) -> int | None:
    for slot, info in belegte_slots().items():
        if info.get("worktree") == str(top):
            return slot
    return None


def beanspruchen(kennung: str, top: Path) -> int:
    start = int(hashlib.sha256(kennung.encode()).hexdigest(), 16) % SLOTS
    slot_wurzel().mkdir(parents=True, exist_ok=True)
    for i in range(SLOTS):
        slot = (start + i) % SLOTS
        alle = [PORT_BASIS + 10 * slot + v for v in (*ENV_PORTS.values(), *RESERVE)]
        if not all(port_frei(p) for p in alle):
            continue
        verzeichnis = slot_wurzel() / f"slot-{slot}"
        try:
            verzeichnis.mkdir()  # atomar: genau einer gewinnt
        except FileExistsError:
            continue
        info_schreiben(slot, {"kennung": kennung, "worktree": str(top), "zuletzt": time.time()})
        return slot
    raise Abbruch("keine freien Slots")


def env_datei_schreiben(top: Path, kennung: str, slot: int) -> Path:
    passwort = secrets.token_urlsafe(24)  # Wegwerf-Zugang, endet mit `down`
    db_name = f"{PRAEFIX}_{kennung.replace('-', '_')}"
    werte = {"SLOT": slot, "DB_NAME": db_name, "DB_PASSWORD": passwort, **ports(slot)}
    werte["DATABASE_URL"] = (
        f"postgresql://{PRAEFIX}:{passwort}@127.0.0.1:{werte['DB_PORT']}/{db_name}"
    )
    pfad = top / ENV_DATEI
    pfad.write_text("".join(f"{k}={v}\n" for k, v in werte.items()), encoding="utf-8")
    return pfad


def compose(top: Path, kennung: str, *args: str, mit_datei: bool = True) -> None:
    befehl = ["docker", "compose", "-p", projekt(kennung)]
    if mit_datei:
        befehl += ["-f", str(top / COMPOSE_DATEI), "--env-file", str(top / ENV_DATEI)]
    subprocess.run([*befehl, *args], cwd=top if top.exists() else None, check=True)


def abbauen(slot: int, info: dict[str, object]) -> bool:
    """Baut Container und Volume ab und gibt den Slot frei.

    Scheitert der Abbau (Docker fehlt, Daemon steht), bleibt der Slot belegt: Ein freier Slot mit
    laufenden Containern waere eine Port-Kollision. `status` zeigt ihn, der Mensch raeumt.
    """
    kennung = str(info.get("kennung", ""))
    top = Path(str(info.get("worktree", "")))
    if kennung:
        try:
            compose(top, kennung, "down", "-v", "--remove-orphans", mit_datei=False)
        except (subprocess.CalledProcessError, OSError) as fehler:
            print(f"Slot {slot} bleibt belegt, Abbau gescheitert: {fehler}")
            return False
    (top / ENV_DATEI).unlink(missing_ok=True)
    shutil.rmtree(slot_wurzel() / f"slot-{slot}", ignore_errors=True)
    return True


def letzte_aktivitaet(top: Path, info: dict[str, object]) -> float:
    zuletzt = float(str(info.get("zuletzt", 0)))
    try:
        commit = float(git("log", "-1", "--format=%ct", cwd=top) or 0)
    except subprocess.CalledProcessError:
        commit = 0.0
    return max(zuletzt, commit)


def sweep() -> None:
    lebende = {str(p) for p in worktrees()}
    grenze = time.time() - VERALTET_TAGE * 86400
    for slot, info in belegte_slots().items():
        if not info:
            continue  # in Anlage durch einen parallelen `up`, keine Waise
        pfad = str(info.get("worktree", ""))
        if pfad not in lebende or not Path(pfad).exists():
            print(f"sweep: Slot {slot} verwaist ({pfad}) -- wird abgebaut")
            abbauen(slot, info)
        elif letzte_aktivitaet(Path(pfad), info) < grenze:
            print(
                f"sweep: Slot {slot} still seit {VERALTET_TAGE} Tagen -- Stack wird abgebaut, "
                f"Worktree und Branch bleiben: {pfad}"
            )
            abbauen(slot, info)


def up() -> None:
    top = wurzel()
    kennung = kennung_von(top)
    sweep()
    if slot_von(top) is not None:
        raise Abbruch(f"{kennung} hat schon einen Slot -- erst `down`")
    slot = beanspruchen(kennung, top)
    try:
        env_datei_schreiben(top, kennung, slot)
        compose(top, kennung, "up", "-d", "--wait")
        for schritt in (MIGRATIONEN, SEED):
            if schritt:
                subprocess.run(schritt, cwd=top, check=True)
    except (subprocess.CalledProcessError, OSError) as fehler:
        frei = abbauen(slot, {"kennung": kennung, "worktree": str(top)})
        zustand = "wieder frei" if frei else "bleibt belegt, siehe status"
        raise Abbruch(f"up gescheitert, Slot {slot} {zustand}: {fehler}") from fehler
    print(f"up: {kennung} in Slot {slot}, Ports {ports(slot)}, Koordinaten in {ENV_DATEI}")


def down() -> None:
    top = wurzel()
    slot = slot_von(top)
    if slot is None:
        raise Abbruch("kein Slot fuer diesen Worktree")
    if not abbauen(slot, belegte_slots()[slot]):
        raise Abbruch(f"Slot {slot} bleibt belegt")
    print(f"down: Slot {slot} frei")


def status() -> None:
    aktivitaet_merken(wurzel())
    lebende = {str(p) for p in worktrees()}
    for slot, info in sorted(belegte_slots().items()):
        pfad = str(info.get("worktree", ""))
        zustand = "in Anlage" if not info else ("aktiv" if pfad in lebende else "verwaist")
        print(f"Slot {slot}: {info.get('kennung')} {zustand} {pfad} {ports(slot)}")
    belegt = {str(i.get("worktree")) for i in belegte_slots().values()}
    for pfad in sorted(lebende - belegt):
        print(f"ohne Slot: {pfad}")  # auch Worktrees, deren Stack der Sweep abgebaut hat


def main(argv: list[str]) -> int:
    befehle = {"up": up, "down": down, "status": status, "sweep": sweep}
    if len(argv) != 1 or argv[0] not in befehle:
        print(f"Aufruf: dev_env {{{'|'.join(befehle)}}}")
        return 2
    try:
        befehle[argv[0]]()
    except Abbruch as grund:
        print(f"ABBRUCH {grund}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
