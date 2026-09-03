"""Foundation Validate - prueft die Foundation-Dateien eines Projekts.

Das Paket implementiert Level 1 des Project-Foundation-Prozesses: die maschinell
entscheidbaren Pruefungen. Level 2 (inhaltliches Review durch einen Agenten) und
Level 3 (Entscheidung durch den Menschen) liegen ausserhalb dieses Codes.
"""

from foundation_validate.model import Domain, Finding, Severity
from foundation_validate.validator import validate

__all__ = ["Domain", "Finding", "Severity", "validate"]
__version__ = "0.3.0"
