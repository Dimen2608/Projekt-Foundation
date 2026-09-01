"""Strukturelle Pruefungen der Foundation-Dateien eines Projekts.

Der Validator prueft ausschliesslich, was maschinell entscheidbar ist:
Existenz, Struktur, erlaubte Statuswerte und Widersprueche zwischen den
Source-of-Truth-Dateien. Inhaltliche Qualitaet bleibt Aufgabe des Reviews.
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

#: Dateien, ohne die keine Foundation vollstaendig ist.
#: Die ID steht im Tupel, damit sie stabil bleibt, wenn sich die Reihenfolge aendert.
REQUIRED_FILES: tuple[tuple[str, str, Domain], ...] = (
    ("STRUCT-001", "README.md", Domain.DOCUMENTATION),
    ("STRUCT-002", "STATUS.md", Domain.DOCUMENTATION),
    ("STRUCT-003", "CLAUDE.md", Domain.AI_FOUNDATION),
    ("STRUCT-004", "docs/PROJECT.md", Domain.PROJECT_DEFINITION),
    ("STRUCT-005", "docs/ARCHITECTURE.md", Domain.ARCHITECTURE),
    ("STRUCT-006", MANIFEST_NAME, Domain.DOCUMENTATION),
)

#: Dateien, die eine fehlende Pflichtstelle offenbar vertreten.
#:
#: Ausschliesslich fuer die Fehlermeldung. Ein Treffer erfuellt die Pflicht NIE --
#: der Validator bleibt strikt, sagt aber, was er stattdessen gefunden hat (ADR-0008).
NEAR_MISS_GLOBS: dict[str, tuple[str, ...]] = {
    "README.md": ("[Rr][Ee][Aa][Dd][Mm][Ee]*.md", "docs/README.md"),
    "STATUS.md": ("docs/STATUS.md", "*[Ss]tatus*.md"),
    "CLAUDE.md": ("docs/CLAUDE.md", ".claude/CLAUDE.md", "AGENTS.md"),
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
#: Abschnitte, deren Fehlen nur eine Warnung ist.
PROJECT_SECTIONS_OPTIONAL = (
    "Core Value",
    "Functional Requirements",
    "Constraints",
    "Open Decisions",
)

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
MANIFEST_REQUIRED_KEYS = (
    "schema_version",
    "project.name",
    "project.type",
    "project.maturity",
    "stack.language",
    "architecture",
    "ai_support",
    "testing",
    "infrastructure",
    "quality_gates",
    "foundation.status",
)

ADR_FILENAME_RE = re.compile(r"^ADR-(\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*\.md$")
ADR_SECTIONS = ("Context", "Decision", "Consequences")

#: Grosszuegiger als ADR_FILENAME_RE: erkennt auch fremde Nummerierungen wie
#: "0001-titel.md". Nur fuer die Beinahe-Treffer-Meldung, nicht fuer die Pruefung.
ADR_LIKE_RE = re.compile(r"^(?:ADR[-_]?)?\d{3,4}[-_]", re.IGNORECASE)


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
    def ready(self) -> bool:
        return not self.blocking


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
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


def _hinweis(treffer: list[str]) -> str:
    """Haengt die Beinahe-Treffer an eine Begruendung an. Leer, wenn es keine gibt."""
    if not treffer:
        return ""
    return f" Gefunden wurde stattdessen: {', '.join(treffer)}."


def _check_structure(root: Path, out: list[Finding]) -> None:
    for finding_id, relative, domain in REQUIRED_FILES:
        if not (root / relative).is_file():
            treffer = _near_misses(root, relative)
            out.append(
                Finding(
                    finding_id=finding_id,
                    severity=Severity.BLOCKING,
                    domain=domain,
                    reason=f"Pflichtdatei {relative} fehlt." + _hinweis(treffer),
                    required_action=(
                        f"{relative} anlegen (Vorlage im Skill unter templates/)"
                        + (
                            f" - oder {treffer[0]} dorthin umbenennen, falls die Datei "
                            "dieselbe Rolle erfuellt."
                            if treffer
                            else "."
                        )
                    ),
                    location=relative,
                )
            )
    decisions = root / "docs" / "decisions"
    if not decisions.is_dir():
        kandidaten = _decision_dir_near_misses(root)
        beschreibung = ", ".join(
            f"{pfad} ({anzahl} ADR-Dateien)" if anzahl else pfad for pfad, anzahl in kandidaten
        )
        out.append(
            Finding(
                finding_id="STRUCT-010",
                severity=Severity.BLOCKING,
                domain=Domain.ARCHITECTURE,
                reason=(
                    "Verzeichnis docs/decisions/ fehlt."
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
                ),
                location="docs/decisions/",
            )
        )
    elif not list(decisions.glob("ADR-*.md")):
        out.append(
            Finding(
                finding_id="STRUCT-011",
                severity=Severity.BLOCKING,
                domain=Domain.ARCHITECTURE,
                reason="docs/decisions/ enthaelt kein einziges ADR.",
                required_action=(
                    "Mindestens die tragende Architekturentscheidung als ADR festhalten."
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
    for index, section in enumerate(PROJECT_SECTIONS_OPTIONAL, start=50):
        if not re.search(rf"^#{{1,6}}\s.*{re.escape(section)}", text, re.MULTILINE | re.IGNORECASE):
            out.append(
                Finding(
                    finding_id=f"DEF-{index:03d}",
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
        # Eine Ursache, eine Warnung: die Datei folgt dem Format gar nicht. Acht
        # gleichlautende Zeilen wuerden nur den Report fluten.
        out.append(
            Finding(
                finding_id="STAT-003",
                severity=Severity.WARNING,
                domain=Domain.DOCUMENTATION,
                reason=(
                    "STATUS.md nennt fuer keine einzige Domaene einen Status - die Datei "
                    "folgt dem erwarteten Format nicht."
                ),
                required_action=(
                    "STATUS.md nach der Vorlage aufbauen: je Domaene eine Zeile mit "
                    f"{'/'.join(DOMAIN_STATES)}."
                ),
                location="STATUS.md",
            )
        )
    else:
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
                reason="Es sind Test-Level definiert, aber kein ausfuehrbares testing.command.",
                required_action=(
                    "Test-Command eintragen - eine nicht ausfuehrbare Teststrategie ist wertlos."
                ),
                location=MANIFEST_NAME,
            )
        )


def _domain_status(findings: list[Finding], declared: dict[Domain, str]) -> dict[Domain, str]:
    result: dict[Domain, str] = {}
    for domain in Domain:
        severities = {f.severity for f in findings if f.domain is domain}
        if Severity.BLOCKING in severities:
            result[domain] = "BLOCKED"
        elif Severity.WARNING in severities:
            result[domain] = "WARNING"
        else:
            result[domain] = declared.get(domain, "PASS")
    return result


def validate(root: Path) -> Result:
    """Fuehrt alle Pruefungen fuer das Projekt unter `root` aus."""
    findings: list[Finding] = []
    _check_structure(root, findings)
    manifest = _check_manifest(root, findings)
    _check_project(root, findings)
    _check_architecture(root, findings)
    _check_adrs(root, findings)
    declared = _check_status(root, findings)
    _check_secrets(root, findings)
    _check_consistency(root, manifest, declared, findings)
    return Result(findings=findings, domain_status=_domain_status(findings, declared))
