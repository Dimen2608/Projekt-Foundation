"""Foundation Validate - prueft die Foundation-Dateien eines Projekts.

Das Paket implementiert die VALIDATE- und AUDIT-Phase des Project-Foundation-
Prozesses maschinell. Es ersetzt nicht das inhaltliche Review durch Mensch oder
Agent, sondern faengt strukturelle Fehler und Widersprueche ab.
"""

from foundation_validate.model import Domain, Finding, Severity
from foundation_validate.validator import validate

__all__ = ["Domain", "Finding", "Severity", "validate"]
__version__ = "0.1.0"
