"""Datentypen des Validators."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Severity(StrEnum):
    """Schweregrad eines Findings.

    BLOCKING verhindert FOUNDATION VALID, WARNING nicht.
    """

    BLOCKING = "BLOCKING"
    WARNING = "WARNING"


class Domain(StrEnum):
    """Die acht Pflicht-Domaenen des Foundation-Audits."""

    PROJECT_DEFINITION = "Project Definition"
    ARCHITECTURE = "Architecture"
    DEVELOPMENT_SETUP = "Development Setup"
    AI_FOUNDATION = "AI Foundation"
    DOCUMENTATION = "Documentation"
    TESTING_QUALITY = "Testing & Quality"
    CICD_INFRASTRUCTURE = "CI/CD & Infrastructure"
    SECURITY = "Security"


#: Status-Werte, die eine Domaene in STATUS.md annehmen darf.
DOMAIN_STATES = ("PASS", "WARNING", "BLOCKED", "UNKNOWN")

#: Status-Werte, die ein Architektur-Bereich in ARCHITECTURE.md annehmen darf.
AREA_STATES = ("RELEVANT", "NOT REQUIRED", "FUTURE", "UNKNOWN")

#: Status-Werte, die ein ADR annehmen darf.
ADR_STATES = ("Proposed", "Accepted", "Rejected", "Superseded", "Deprecated")


@dataclass(frozen=True)
class Finding:
    """Ein einzelner Befund des Validators.

    Attributes:
        finding_id: Stabile ID, z. B. "DOC-001". Wird im Report referenziert.
        severity: BLOCKING oder WARNING.
        domain: Betroffene Audit-Domaene.
        reason: Was ist falsch.
        required_action: Was muss getan werden, damit es PASS wird.
        location: Datei bzw. Pfad, auf den sich das Finding bezieht.
    """

    finding_id: str
    severity: Severity
    domain: Domain
    reason: str
    required_action: str
    location: str = ""

    def __str__(self) -> str:
        where = f" ({self.location})" if self.location else ""
        return (
            f"[{self.severity.value}] {self.finding_id} {self.domain.value}{where}: {self.reason}"
        )
