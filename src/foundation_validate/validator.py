"""Strukturelle Pruefungen der Foundation-Dateien eines Projekts.

Der Validator prueft ausschliesslich, was maschinell entscheidbar ist:
Existenz, Struktur, erlaubte Statuswerte und Widersprueche zwischen den
Source-of-Truth-Dateien. Sein Ergebnis heisst FOUNDATION VALID -- nicht
FOUNDATION READY. Ob eine Foundation inhaltlich taugt, kann dieser Code nicht
entscheiden; das ist Aufgabe des Reviews (Skill) und des Menschen (ADR-0010).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from foundation_validate.model import (
    ADR_STATES,
    AREA_STATES,
    DOMAIN_STATES,
    Domain,
    Finding,
    Severity,
)

MANIFEST_NAME = ".project-foundation.yml"

#: Pflichtstellen: je Eintrag die ID, die Frage, die erlaubten Dateien und die Domaene.
#:
#: Eine Datei steht hier, weil eine Frage ohne sie unbeantwortet bleibt -- nicht, weil
#: sie zum Standardsatz gehoert (ADR-0011). Die erste Datei ist die kanonische; weitere
#: sind gleichwertige Antworten auf dieselbe Frage. Die ID steht im Tupel, damit sie
#: stabil bleibt, wenn sich die Reihenfolge aendert. STRUCT-002 (STATUS.md) ist
#: entfallen und wird nicht neu vergeben.
REQUIRED_FILES: tuple[tuple[str, str, tuple[str, ...], Domain], ...] = (
    ("STRUCT-001", "Wie starte und benutze ich das Projekt?", ("README.md",), Domain.DOCUMENTATION),
    (
        "STRUCT-003",
        "Was muss ein AI-Agent wissen?",
        ("CLAUDE.md", "AGENTS.md"),
        Domain.AI_FOUNDATION,
    ),
    (
        "STRUCT-004",
        "Was bauen wir, und was ausdruecklich nicht?",
        ("docs/PROJECT.md",),
        Domain.PROJECT_DEFINITION,
    ),
    (
        "STRUCT-005",
        "Wie ist das System strukturiert?",
        ("docs/ARCHITECTURE.md",),
        Domain.ARCHITECTURE,
    ),
    (
        "STRUCT-006",
        "Woran erkennt ein Werkzeug die Foundation?",
        (MANIFEST_NAME,),
        Domain.DOCUMENTATION,
    ),
)

#: Dateien, die eine fehlende Pflichtstelle offenbar vertreten.
#:
#: Ausschliesslich fuer die Fehlermeldung. Ein Treffer erfuellt die Pflicht NIE --
#: der Validator bleibt strikt, sagt aber, was er stattdessen gefunden hat (ADR-0008).
NEAR_MISS_GLOBS: dict[str, tuple[str, ...]] = {
    "README.md": ("[Rr][Ee][Aa][Dd][Mm][Ee]*.md", "docs/README.md"),
    "CLAUDE.md": ("docs/CLAUDE.md", ".claude/CLAUDE.md", ".github/copilot-instructions.md"),
    "docs/PROJECT.md": (
        "docs/*[Pp]roject*.md",
        "docs/*[Pp]rojekt*.md",
        "docs/*[Kk]onzept*.md",
        "PROJECT.md",
        "KONZEPT.md",
    ),
    "docs/ARCHITECTURE.md": (
        "docs/*[Aa]rchitect*.md",
        "docs/*[Aa]rchitekt*.md",
        "ARCHITECTURE.md",
        "ARCHITEKTUR.md",
    ),
    MANIFEST_NAME: (
        ".project-foundation.yaml",
        "project-foundation.yml",
        ".foundation.yml",
    ),
}

#: Domaenen, fuer die dieser Code keine eigene Regel hat.
#:
#: Sie erscheinen im Report als NOT CHECKED statt als OK. "Development Setup: OK" waere
#: eine Behauptung ueber etwas, das nie geprueft wurde - genau die Sorte falsches
#: Qualitaetsversprechen, die der Validator nicht abgeben darf (ADR-0010). Meldet
#: STATUS.md eine dieser Domaenen als BLOCKED, wird das als STAT-002 trotzdem sichtbar.
UNCHECKED_DOMAINS = (Domain.DEVELOPMENT_SETUP, Domain.CICD_INFRASTRUCTURE)

#: Verzeichnisnamen, unter denen Projekte ihre ADRs ueblicherweise ablegen.
DECISION_DIR_CANDIDATES = ("adr", "adrs", "decisions", "entscheidungen", "architecture-decisions")

#: Mehr Kandidaten nennt der Report nicht -- sonst wird aus der Meldung ein Verzeichnisdump.
MAX_NEAR_MISSES = 3

#: Abschnitte, die docs/PROJECT.md zwingend braucht.
PROJECT_SECTIONS_REQUIRED = (
    "Purpose",
    "Problem",
    "Target Users",
    "Scope",
    "MVP",
    "Out of Scope",
)
#: Abschnitte, deren Fehlen nur eine Warnung ist - weil ihr Fehlen eine Risikofrage
#: offenlaesst (gibt es Vorgaben von aussen? steht eine Entscheidung aus?).
#:
#: Die ID steht im Tupel, damit sie stabil bleibt. DEF-050 (Core Value) und DEF-051
#: (Functional Requirements) sind entfallen: Ein Miniprojekt ohne diese Abschnitte ist
#: korrekt, und vier Warnungen auf einem korrekten Projekt trainieren nur, Warnungen zu
#: ueberlesen. Die IDs werden nicht neu vergeben.
PROJECT_SECTIONS_OPTIONAL: tuple[tuple[str, str], ...] = (
    ("DEF-052", "Constraints"),
    ("DEF-053", "Open Decisions"),
)

#: Zeile in ARCHITECTURE.md, die erklaert, ob dieses Projekt ADRs braucht.
#:
#: Ohne diese Erklaerung koennte der Validator nur raten: "kein ADR" heisst entweder
#: "es gab keine tragende Entscheidung" oder "sie wurde nicht festgehalten". Die beiden
#: Faelle sind maschinell nicht unterscheidbar, also wird die Antwort verlangt statt
#: unterstellt (ADR-0011).
DECISION_LABEL = "Architecture Decisions"
#: Nur diese beiden Werte zaehlen als Antwort. Alles andere - auch ein ausdrueckliches
#: UNKNOWN - ist keine Antwort und faellt in dieselbe Warnung wie eine fehlende Zeile.
DECISION_STATES = ("REQUIRED", "NOT REQUIRED")

#: Architektur-Bereiche, die bewertet sein muessen.
CORE_AREAS = (
    "Application Architecture",
    "Frontend",
    "Backend",
    "Database",
    "Data Model",
    "Authentication",
    "Authorization",
    "APIs",
    "External Services",
    "Deployment",
    "Security",
    "Configuration",
    "Secrets",
)
#: Bereiche, bei denen UNKNOWN oder fehlende Bewertung BLOCKING ist.
SECURITY_CRITICAL_AREAS = ("Authentication", "Authorization", "Secrets")

#: Pflichtschluessel des Manifests, als Punktpfade.
#:
#: Nur das, was der Validator tatsaechlich braucht. Alles Weitere steht schon in den
#: Dokumenten; es zusaetzlich im Manifest zu verlangen wuerde eine zweite Quelle
#: erzeugen, die auseinanderdriftet (ADR-0004, ADR-0011). Optionale Bloecke
#: (ai_support, testing, foundation.blocking_issues) werden geprueft, wenn sie da sind.
MANIFEST_REQUIRED_KEYS = (
    "schema_version",
    "foundation.status",
)

ADR_FILENAME_RE = re.compile(r"^ADR-(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
ADR_SECTIONS = ("Context", "Decision", "Consequences")

#: Grosszuegiger als ADR_FILENAME_RE: erkennt auch fremde Nummerierungen wie
#: "0001-titel.md". Nur fuer die Beinahe-Treffer-Meldung, nicht fuer die Pruefung.
ADR_LIKE_RE = re.compile(r"^(?:ADR[-_]?)?\d{3,4}[-_]", re.IGNORECASE)


def _finding_id_register() -> tuple[str, ...]:
    """Jede Finding-ID, die der Validator erzeugen kann.

    Zweck ist der Abdeckungstest in tests/test_regelabdeckung.py: Er schlaegt fehl, sobald
    eine Regel ohne schuetzenden Test existiert oder eine ID am Register vorbei eingefuehrt
    wird. Damit ist die Repo-Regel "neue Blocking-Regel = neuer Test" erzwungen statt nur
    vorgenommen (ADR-0009).

    Die Familien DEF- und ARCH- entstehen je Abschnitt bzw. Bereich aus einer
    Konstantenliste und wachsen automatisch mit.
    """
    ids: list[str] = [finding_id for finding_id, _, _, _ in REQUIRED_FILES]
    ids += ["STRUCT-010", "STRUCT-011"]
    ids += [f"DEF-{i:03d}" for i in range(1, len(PROJECT_SECTIONS_REQUIRED) + 1)]
    ids += [finding_id for finding_id, _ in PROJECT_SECTIONS_OPTIONAL]
    ids += [f"ARCH-{i:03d}" for i in range(1, len(CORE_AREAS) + 1)]
    ids += [f"MAN-{i:03d}" for i in range(1, 5)]
    ids += [f"ADR-{i:03d}" for i in range(1, 5)]
    ids += ["ADR-010"]
    ids += ["STAT-001", "STAT-002"]  # STAT-003 zurueckgezogen, siehe _check_status
    ids += [f"SEC-{i:03d}" for i in range(1, 3)]
    ids += [f"CONS-{i:03d}" for i in range(1, 5)]
    return tuple(ids)


#: Register aller Finding-IDs. Stabil - eine bestehende ID wird nicht umgewidmet.
FINDING_IDS = _finding_id_register()


@dataclass
class Result:
    """Ergebnis eines Validierungslaufs."""

    findings: list[Finding]
    domain_status: dict[Domain, str]

    @property
    def blocking(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.BLOCKING]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity is Severity.WARNING]

    @property
    def valid(self) -> bool:
        """True, wenn kein struktureller Blocker offen ist.

        Ausdruecklich *nicht* `ready`: ueber FOUNDATION READY entscheidet der
        vollstaendige Prozess, nicht dieser Code (ADR-0010).
        """
        return not self.blocking


def _read(path: Path) -> str:
    # utf-8-sig, weil unter Windows erzeugte Dateien oft mit BOM beginnen -- die stuende
    # sonst vor der ersten Ueberschrift und liesse sie durch die Abschnittspruefung fallen.
    try:
        return path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError):
        return ""


def _dig(data: Any, dotted: str) -> Any:
    """Liest einen Punktpfad aus verschachtelten Dicts. None wenn nicht vorhanden."""
    current: Any = data
    for part in dotted.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _find_state(text: str, label: str, states: tuple[str, ...]) -> str | None:
    """Sucht `label ... STATE` auf einer Zeile und liefert den ersten Treffer."""
    alternatives = "|".join(re.escape(s) for s in states)
    pattern = re.compile(
        rf"{re.escape(label)}\s*[:|]?[^\S\n]*\|?[^\S\n]*[*_`]*({alternatives})\b",
        re.IGNORECASE,
    )
    match = pattern.search(text)
    if match is None:
        return None
    hit = match.group(1).upper()
    for state in states:
        if state.upper() == hit:
            return state
    return hit


def _near_misses(root: Path, relative: str) -> list[str]:
    """Dateien, die die fehlende Pflichtstelle offenbar vertreten sollen.

    Dient nur der Meldung: der Nutzer soll nicht raten muessen, ob der Validator seine
    vorhandene Doku uebersehen hat oder sie nur anders heisst.
    """
    treffer: dict[str, None] = {}
    for muster in NEAR_MISS_GLOBS.get(relative, ()):
        for pfad in sorted(root.glob(muster)):
            if pfad.is_file() and pfad != (root / relative):
                treffer[pfad.relative_to(root).as_posix()] = None
    return list(treffer)[:MAX_NEAR_MISSES]


def _decision_dir_near_misses(root: Path) -> list[tuple[str, int]]:
    """Verzeichnisse, die statt docs/decisions/ die ADRs enthalten, mit ihrer Dateizahl."""
    treffer: list[tuple[str, int]] = []
    basen = [root, root / "docs"]
    for basis in basen:
        if not basis.is_dir():
            continue
        for kandidat in sorted(p for p in basis.iterdir() if p.is_dir()):
            if kandidat == root / "docs" / "decisions":
                continue
            adrs = [p for p in kandidat.glob("*.md") if ADR_LIKE_RE.match(p.name)]
            passt = kandidat.name.lower() in DECISION_DIR_CANDIDATES
            if adrs or passt:
                treffer.append((kandidat.relative_to(root).as_posix() + "/", len(adrs)))
    return treffer[:MAX_NEAR_MISSES]


def _decision_dir_beschreibung(kandidaten: list[tuple[str, int]]) -> str:
    """Zaehlt die gefundenen Fremdverzeichnisse auf: 'docs/adr/ (14 ADR-Dateien)'."""
    return ", ".join(
        f"{pfad} ({anzahl} ADR-Dateien)" if anzahl else pfad for pfad, anzahl in kandidaten
    )


def _folgepruefung(relative: str) -> str:
    """Kuendigt an, was nach dem Anlegen dieser Pflichtstelle zusaetzlich geprueft wird.

    Ohne diesen Hinweis sieht es aus, als verschlechtere das Beheben eines Blockers die
    Lage: Solange docs/ARCHITECTURE.md fehlt, meldet der Validator einen Blocker -- sobald
    sie existiert, koennen drei blockierende ARCH-Befunde dazukommen. Die Zahlen stammen
    aus den Konstanten, damit der Hinweis nicht veraltet.
    """
    if relative == "docs/PROJECT.md":
        return (
            f" Danach werden {len(PROJECT_SECTIONS_REQUIRED)} Pflichtabschnitte geprueft: "
            f"{', '.join(PROJECT_SECTIONS_REQUIRED)}."
        )
    if relative == "docs/ARCHITECTURE.md":
        return (
            f" Danach werden {len(CORE_AREAS)} Architekturbereiche geprueft; "
            f"{', '.join(SECURITY_CRITICAL_AREAS)} blockieren, solange sie unbewertet "
            f"oder UNKNOWN sind. Ausserdem wird dort die Zeile '{DECISION_LABEL}' "
            "erwartet."
        )
    return ""


def _hinweis(treffer: list[str]) -> str:
    """Haengt die Beinahe-Treffer an eine Begruendung an. Leer, wenn es keine gibt."""
    if not treffer:
        return ""
    return f" Gefunden wurde stattdessen: {', '.join(treffer)}."


def _check_structure(root: Path, out: list[Finding]) -> None:
    for finding_id, frage, erlaubt, domain in REQUIRED_FILES:
        if any((root / kandidat).is_file() for kandidat in erlaubt):
            continue
        relative = erlaubt[0]
        alternative = f" Gleichwertig waere: {', '.join(erlaubt[1:])}." if len(erlaubt) > 1 else ""
        treffer = _near_misses(root, relative)
        out.append(
            Finding(
                finding_id=finding_id,
                severity=Severity.BLOCKING,
                domain=domain,
                reason=(
                    f"Die Frage '{frage}' hat keine Heimat: {relative} fehlt."
                    + alternative
                    + _hinweis(treffer)
                ),
                required_action=(
                    f"{relative} anlegen (Vorlage im Skill unter templates/)"
                    + (
                        f" - oder {treffer[0]} dorthin umbenennen, falls die Datei "
                        "dieselbe Rolle erfuellt."
                        if treffer
                        else "."
                    )
                    + _folgepruefung(relative)
                ),
                location=relative,
            )
        )


def _check_decisions(root: Path, out: list[Finding]) -> None:
    """Prueft ADRs nur, wenn das Projekt erklaert hat, dass es welche braucht.

    "Kein ADR vorhanden" ist fuer sich kein Mangel: ein kleines Projekt kann korrekt
    sein, ohne je eine tragende Entscheidung getroffen zu haben. Verlangt wird deshalb
    nicht das ADR, sondern die Aussage darueber (ADR-0011).
    """
    decisions = root / "docs" / "decisions"
    vorhandene_adrs = list(decisions.glob("ADR-*.md")) if decisions.is_dir() else []
    state = _find_state(_read(root / "docs" / "ARCHITECTURE.md"), DECISION_LABEL, DECISION_STATES)

    if state != "REQUIRED":
        if state is None and not vorhandene_adrs:
            # Kein ADR und keine Aussage: die Frage ist offen. Das ist eine Warnung,
            # kein Blocker - der Validator kann nicht wissen, ob hier etwas fehlt.
            #
            # Die Beinahe-Treffer gehoeren in die Meldung: Ein Projekt, dessen ADRs in
            # docs/adr/ liegen, bekaeme sonst zu hoeren, es habe keine - was schlicht
            # falsch ist und die Regel aus ADR-0008 verletzt. Gemessen am 02.09.2026
            # gegen ein Fremdprojekt mit 14 ADRs in docs/adr/.
            kandidaten = _decision_dir_near_misses(root)
            out.append(
                Finding(
                    finding_id="ADR-010",
                    severity=Severity.WARNING,
                    domain=Domain.ARCHITECTURE,
                    reason=(
                        "Es ist nicht beantwortet, ob dieses Projekt ADRs braucht: "
                        f"docs/ARCHITECTURE.md nennt fuer '{DECISION_LABEL}' weder "
                        "REQUIRED noch NOT REQUIRED. In docs/decisions/ liegt kein ADR."
                        + (
                            f" Gefunden wurde stattdessen: "
                            f"{_decision_dir_beschreibung(kandidaten)}."
                            if kandidaten
                            else ""
                        )
                    ),
                    required_action=(
                        f"'{DECISION_LABEL}' mit REQUIRED oder NOT REQUIRED beantworten. "
                        "NOT REQUIRED ist ein gueltiger Zustand - dann aber mit Begruendung."
                        + (
                            " Achtung vor REQUIRED: Die Pfadkonvention verlangt "
                            f"docs/decisions/; {kandidaten[0][0]} erfuellt sie nicht "
                            "und wuerde dann als Blocker gemeldet (ADR-0008)."
                            if kandidaten
                            else ""
                        )
                    ),
                    location="docs/ARCHITECTURE.md",
                )
            )
        return

    if not decisions.is_dir():
        kandidaten = _decision_dir_near_misses(root)
        beschreibung = _decision_dir_beschreibung(kandidaten)
        out.append(
            Finding(
                finding_id="STRUCT-010",
                severity=Severity.BLOCKING,
                domain=Domain.ARCHITECTURE,
                reason=(
                    f"docs/ARCHITECTURE.md sagt '{DECISION_LABEL}: REQUIRED', "
                    "aber das Verzeichnis docs/decisions/ fehlt."
                    + (f" Gefunden wurde stattdessen: {beschreibung}." if kandidaten else "")
                ),
                required_action=(
                    "docs/decisions/ anlegen und mindestens ein ADR schreiben"
                    + (
                        f" - oder {kandidaten[0][0]} dorthin umbenennen, falls dort "
                        "bereits die Architekturentscheidungen liegen."
                        if kandidaten
                        else "."
                    )
                    + f" Danach wird jedes ADR auf {', '.join(ADR_SECTIONS)} und einen "
                    "gueltigen Status geprueft."
                ),
                location="docs/decisions/",
            )
        )
    elif not vorhandene_adrs:
        out.append(
            Finding(
                finding_id="STRUCT-011",
                severity=Severity.BLOCKING,
                domain=Domain.ARCHITECTURE,
                reason=(
                    f"docs/ARCHITECTURE.md sagt '{DECISION_LABEL}: REQUIRED', "
                    "docs/decisions/ enthaelt aber kein einziges ADR."
                ),
                required_action=(
                    "Die tragende Entscheidung als ADR festhalten - oder, falls es keine "
                    f"gibt, '{DECISION_LABEL}' auf NOT REQUIRED setzen."
                ),
                location="docs/decisions/",
            )
        )


def _check_manifest(root: Path, out: list[Finding]) -> dict[str, Any]:
    path = root / MANIFEST_NAME
    if not path.is_file():
        return {}
    try:
        loaded = yaml.safe_load(_read(path))
    except yaml.YAMLError as error:
        out.append(
            Finding(
                finding_id="MAN-001",
                severity=Severity.BLOCKING,
                domain=Domain.DOCUMENTATION,
                reason=f"{MANIFEST_NAME} ist kein gueltiges YAML: {error}",
                required_action="YAML-Syntax korrigieren.",
                location=MANIFEST_NAME,
            )
        )
        return {}
    if not isinstance(loaded, dict):
        out.append(
            Finding(
                finding_id="MAN-002",
                severity=Severity.BLOCKING,
                domain=Domain.DOCUMENTATION,
                reason=f"{MANIFEST_NAME} enthaelt kein Mapping auf oberster Ebene.",
                required_action="Manifest gemaess Vorlage aufbauen.",
                location=MANIFEST_NAME,
            )
        )
        return {}

    manifest: dict[str, Any] = loaded
    missing = [key for key in MANIFEST_REQUIRED_KEYS if _dig(manifest, key) is None]
    if missing:
        out.append(
            Finding(
                finding_id="MAN-003",
                severity=Severity.BLOCKING,
                domain=Domain.DOCUMENTATION,
                reason=f"Pflichtfelder im Manifest fehlen: {', '.join(missing)}.",
                required_action="Fehlende Felder ergaenzen.",
                location=MANIFEST_NAME,
            )
        )

    status = _dig(manifest, "foundation.status")
    if status is not None and status not in ("READY", "NOT_READY"):
        out.append(
            Finding(
                finding_id="MAN-004",
                severity=Severity.BLOCKING,
                domain=Domain.DOCUMENTATION,
                reason=f"foundation.status hat unzulaessigen Wert {status!r}.",
                required_action="Auf READY oder NOT_READY setzen.",
                location=MANIFEST_NAME,
            )
        )
    return manifest


def _check_project(root: Path, out: list[Finding]) -> None:
    path = root / "docs" / "PROJECT.md"
    if not path.is_file():
        return
    text = _read(path)
    for index, section in enumerate(PROJECT_SECTIONS_REQUIRED, start=1):
        if not re.search(rf"^#{{1,6}}\s.*{re.escape(section)}", text, re.MULTILINE | re.IGNORECASE):
            out.append(
                Finding(
                    finding_id=f"DEF-{index:03d}",
                    severity=Severity.BLOCKING,
                    domain=Domain.PROJECT_DEFINITION,
                    reason=f"Abschnitt '{section}' fehlt in docs/PROJECT.md.",
                    required_action=f"Abschnitt '{section}' ergaenzen und inhaltlich fuellen.",
                    location="docs/PROJECT.md",
                )
            )
    for finding_id, section in PROJECT_SECTIONS_OPTIONAL:
        if not re.search(rf"^#{{1,6}}\s.*{re.escape(section)}", text, re.MULTILINE | re.IGNORECASE):
            out.append(
                Finding(
                    finding_id=finding_id,
                    severity=Severity.WARNING,
                    domain=Domain.PROJECT_DEFINITION,
                    reason=f"Abschnitt '{section}' fehlt in docs/PROJECT.md.",
                    required_action=f"Abschnitt '{section}' ergaenzen, sobald bekannt.",
                    location="docs/PROJECT.md",
                )
            )


def _check_architecture(root: Path, out: list[Finding]) -> None:
    path = root / "docs" / "ARCHITECTURE.md"
    if not path.is_file():
        return
    text = _read(path)
    for index, area in enumerate(CORE_AREAS, start=1):
        state = _find_state(text, area, AREA_STATES)
        critical = area in SECURITY_CRITICAL_AREAS
        domain = Domain.SECURITY if critical else Domain.ARCHITECTURE
        if state is None:
            out.append(
                Finding(
                    finding_id=f"ARCH-{index:03d}",
                    severity=Severity.BLOCKING if critical else Severity.WARNING,
                    domain=domain,
                    reason=f"Bereich '{area}' ist in ARCHITECTURE.md nicht bewertet.",
                    required_action=(
                        f"'{area}' mit RELEVANT, NOT REQUIRED, FUTURE oder UNKNOWN bewerten."
                    ),
                    location="docs/ARCHITECTURE.md",
                )
            )
        elif state == "UNKNOWN" and critical:
            out.append(
                Finding(
                    finding_id=f"ARCH-{index:03d}",
                    severity=Severity.BLOCKING,
                    domain=Domain.SECURITY,
                    reason=(f"Sicherheitsrelevanter Bereich '{area}' steht auf UNKNOWN."),
                    required_action=f"Entscheidung zu '{area}' treffen und als ADR dokumentieren.",
                    location="docs/ARCHITECTURE.md",
                )
            )


def _check_adrs(root: Path, out: list[Finding]) -> None:
    decisions = root / "docs" / "decisions"
    if not decisions.is_dir():
        return
    seen: dict[str, str] = {}
    for path in sorted(decisions.glob("*.md")):
        if path.name.upper().startswith("README"):
            continue
        match = ADR_FILENAME_RE.match(path.name)
        if match is None:
            out.append(
                Finding(
                    finding_id="ADR-001",
                    severity=Severity.WARNING,
                    domain=Domain.ARCHITECTURE,
                    reason=f"Dateiname {path.name} folgt nicht dem Muster ADR-NNNN-title.md.",
                    required_action="Datei umbenennen.",
                    location=str(path.relative_to(root)),
                )
            )
            continue
        number = match.group(1)
        if number in seen:
            out.append(
                Finding(
                    finding_id="ADR-002",
                    severity=Severity.BLOCKING,
                    domain=Domain.ARCHITECTURE,
                    reason=(
                        f"ADR-Nummer {number} ist doppelt vergeben ({seen[number]}, {path.name})."
                    ),
                    required_action="Eine der beiden Dateien neu nummerieren.",
                    location=str(path.relative_to(root)),
                )
            )
        seen[number] = path.name

        text = _read(path)
        missing = [
            section
            for section in ADR_SECTIONS
            if not re.search(rf"^#{{1,6}}\s.*{section}", text, re.MULTILINE | re.IGNORECASE)
        ]
        if missing:
            out.append(
                Finding(
                    finding_id="ADR-003",
                    severity=Severity.BLOCKING,
                    domain=Domain.ARCHITECTURE,
                    reason=f"{path.name} fehlen die Abschnitte: {', '.join(missing)}.",
                    required_action="Context, Decision und Consequences ergaenzen.",
                    location=str(path.relative_to(root)),
                )
            )
        if _find_state(text, "Status", ADR_STATES) is None:
            out.append(
                Finding(
                    finding_id="ADR-004",
                    severity=Severity.BLOCKING,
                    domain=Domain.ARCHITECTURE,
                    reason=f"{path.name} hat keinen gueltigen Status.",
                    required_action=f"Status setzen: {', '.join(ADR_STATES)}.",
                    location=str(path.relative_to(root)),
                )
            )


def _check_status(root: Path, out: list[Finding]) -> dict[Domain, str]:
    path = root / "STATUS.md"
    declared: dict[Domain, str] = {}
    if not path.is_file():
        return declared
    text = _read(path)
    fehlend: list[Domain] = []
    for domain in Domain:
        state = _find_state(text, domain.value, DOMAIN_STATES)
        if state is None:
            fehlend.append(domain)
            continue
        declared[domain] = state
        if state in ("BLOCKED", "UNKNOWN"):
            out.append(
                Finding(
                    finding_id="STAT-002",
                    severity=Severity.BLOCKING,
                    domain=domain,
                    reason=f"STATUS.md meldet '{domain.value}' als {state}.",
                    required_action="Blocker aufloesen oder Entscheidung treffen.",
                    location="STATUS.md",
                )
            )

    if len(fehlend) == len(Domain):
        # Keine einzige Domaenenzeile: Die Datei folgt nicht dieser Konvention, und sie
        # muss es auch nicht - STATUS.md ist optional (ADR-0011). Der Validator prueft
        # nur, was behauptet, in seinem Format zu sein. Frueher stand hier STAT-003; die
        # Warnung hatte fuer ein Projekt mit eigenem Statusformat keinen benennbaren
        # Nutzen und ist zurueckgezogen. Die ID wird nicht neu vergeben.
        return declared
    for domain in fehlend:
        out.append(
            Finding(
                finding_id="STAT-001",
                severity=Severity.WARNING,
                domain=Domain.DOCUMENTATION,
                reason=f"STATUS.md nennt keinen Status fuer '{domain.value}'.",
                required_action=f"'{domain.value}' mit {'/'.join(DOMAIN_STATES)} bewerten.",
                location="STATUS.md",
            )
        )
    return declared


def _check_secrets(root: Path, out: list[Finding]) -> None:
    """Prueft Secret-*Hygiene*, nicht Secrets.

    Der Validator liest keine Dateiinhalte auf Geheimnisse hin und kann daher nie sagen,
    dass ein Projekt frei von Secrets ist. Er prueft zwei strukturelle Bedingungen, deren
    Verletzung erfahrungsgemaess Secrets ins Repository traegt. Echtes Secret Scanning
    ist Aufgabe eines dafuer gebauten Werkzeugs (gitleaks, GitHub Secret Scanning).
    """
    if (root / ".env").is_file():
        out.append(
            Finding(
                finding_id="SEC-001",
                severity=Severity.BLOCKING,
                domain=Domain.SECURITY,
                reason="Eine .env-Datei liegt im Projektverzeichnis.",
                required_action=".env aus der Versionskontrolle nehmen und ignorieren.",
                location=".env",
            )
        )
    gitignore = _read(root / ".gitignore")
    if (root / ".env.example").is_file() and not re.search(r"^\.env\b", gitignore, re.MULTILINE):
        out.append(
            Finding(
                finding_id="SEC-002",
                severity=Severity.BLOCKING,
                domain=Domain.SECURITY,
                reason=(
                    "Das Projekt nutzt Environment-Variablen, aber .gitignore ignoriert .env nicht."
                ),
                required_action="'.env' in .gitignore aufnehmen.",
                location=".gitignore",
            )
        )


def _check_consistency(
    root: Path,
    manifest: dict[str, Any],
    declared: dict[Domain, str],
    out: list[Finding],
) -> None:
    if not manifest:
        return

    status = _dig(manifest, "foundation.status")
    bad = [d.value for d, s in declared.items() if s in ("BLOCKED", "UNKNOWN")]
    if status == "READY" and bad:
        out.append(
            Finding(
                finding_id="CONS-001",
                severity=Severity.BLOCKING,
                domain=Domain.DOCUMENTATION,
                reason=(
                    "Manifest meldet READY, STATUS.md meldet aber "
                    f"{', '.join(bad)} als BLOCKED/UNKNOWN."
                ),
                required_action="Widerspruch aufloesen - STATUS.md ist die Source of Truth.",
                location=MANIFEST_NAME,
            )
        )

    blocking_count = _dig(manifest, "foundation.blocking_issues")
    if status == "READY" and isinstance(blocking_count, int) and blocking_count > 0:
        out.append(
            Finding(
                finding_id="CONS-002",
                severity=Severity.BLOCKING,
                domain=Domain.DOCUMENTATION,
                reason=f"Manifest meldet READY, nennt aber {blocking_count} Blocking Issues.",
                required_action="Status oder Zaehler korrigieren.",
                location=MANIFEST_NAME,
            )
        )

    ai_files = {
        "claude_md": "CLAUDE.md",
        "agents_md": "AGENTS.md",
        "cursor_rules": ".cursor/rules",
    }
    for key, relative in ai_files.items():
        if _dig(manifest, f"ai_support.{key}") is True and not (root / relative).exists():
            out.append(
                Finding(
                    finding_id="CONS-003",
                    severity=Severity.BLOCKING,
                    domain=Domain.AI_FOUNDATION,
                    reason=f"Manifest behauptet ai_support.{key}, aber {relative} existiert nicht.",
                    required_action=f"{relative} anlegen oder das Manifest korrigieren.",
                    location=MANIFEST_NAME,
                )
            )

    levels = _dig(manifest, "testing.levels")
    command = _dig(manifest, "testing.command")
    if levels and not command:
        out.append(
            Finding(
                finding_id="CONS-004",
                severity=Severity.BLOCKING,
                domain=Domain.TESTING_QUALITY,
                reason="Es sind Test-Level definiert, aber kein testing.command.",
                required_action=(
                    "Test-Command eintragen - eine nicht ausfuehrbare Teststrategie ist wertlos."
                ),
                location=MANIFEST_NAME,
            )
        )


def _domain_status(findings: list[Finding]) -> dict[Domain, str]:
    """Leitet den Domaenenstatus ausschliesslich aus eigenen Befunden ab.

    Frueher galt hilfsweise der in STATUS.md erklaerte Wert - damit gab der Validator
    eine fremde Selbstauskunft als eigenes Urteil aus. Jetzt steht dort nur, was er
    selbst geprueft hat (ADR-0010).
    """
    result: dict[Domain, str] = {}
    for domain in Domain:
        severities = {f.severity for f in findings if f.domain is domain}
        if Severity.BLOCKING in severities:
            result[domain] = "BLOCKED"
        elif Severity.WARNING in severities:
            result[domain] = "WARNING"
        elif domain in UNCHECKED_DOMAINS:
            result[domain] = "NOT CHECKED"
        else:
            result[domain] = "OK"
    return result


def validate(root: Path) -> Result:
    """Fuehrt alle Pruefungen fuer das Projekt unter `root` aus."""
    findings: list[Finding] = []
    _check_structure(root, findings)
    manifest = _check_manifest(root, findings)
    _check_project(root, findings)
    _check_architecture(root, findings)
    _check_decisions(root, findings)
    _check_adrs(root, findings)
    declared = _check_status(root, findings)
    _check_secrets(root, findings)
    _check_consistency(root, manifest, declared, findings)
    return Result(findings=findings, domain_status=_domain_status(findings))
