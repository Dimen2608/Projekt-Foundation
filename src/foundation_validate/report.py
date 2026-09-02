"""Erzeugt den Report der maschinellen Foundation-Pruefung.

Bewusst nicht der Audit-Report: der Audit umfasst das inhaltliche Review und endet auf
FOUNDATION READY. Dieser Report endet auf FOUNDATION VALID (ADR-0010).
"""

from __future__ import annotations

from foundation_validate.model import Domain
from foundation_validate.validator import Result

_BOX_WIDTH = 38
_BOX_TITLE = "PROJECT FOUNDATION VALIDATION".center(_BOX_WIDTH)

BOX = "╔" + "═" * _BOX_WIDTH + "╗\n║" + _BOX_TITLE + "║\n╚" + "═" * _BOX_WIDTH + "╝"
BOX_ASCII = "+" + "-" * _BOX_WIDTH + "+\n|" + _BOX_TITLE + "|\n+" + "-" * _BOX_WIDTH + "+"

_LABEL_WIDTH = 25


def stream_supports_box(stream: object) -> bool:
    """True, wenn der Rahmen auf diesem Stream darstellbar ist.

    Konsolen mit einer Legacy-Codepage (Windows, cp1252) koennen die Rahmenzeichen
    nicht encoden — dort waere die Ausgabe sonst ein UnicodeEncodeError. Streams ohne
    eigenes Encoding (StringIO, pytest-Capture) sind nicht beschraenkt.
    """
    encoding = getattr(stream, "encoding", None)
    if not encoding:
        return True
    try:
        BOX.encode(encoding)
    except (UnicodeEncodeError, LookupError):
        return False
    return True


def render(result: Result, *, ascii_only: bool = False) -> str:
    """Formatiert das Validierungsergebnis."""
    lines = [BOX_ASCII if ascii_only else BOX, ""]
    for domain in Domain:
        lines.append(f"{domain.value.ljust(_LABEL_WIDTH)}{result.domain_status[domain]}")
    lines += [
        "",
        "OK = no structural finding. NOT CHECKED = no machine-checkable rule here.",
        "",
        f"Blocking Issues: {len(result.blocking)}",
        f"Warnings: {len(result.warnings)}",
        "",
        "=" * 40,
        "",
    ]

    if result.valid:
        lines += [
            "FOUNDATION VALID",
            "",
            "Structural requirements are met. This is not a statement about the",
            "quality of the foundation: scope, architecture and completeness are",
            "judged by the review, not by this program. FOUNDATION READY is the",
            "result of that review.",
        ]
    else:
        lines += ["FOUNDATION INVALID", "", "Blocking Issues:", ""]
        for finding in result.blocking:
            lines += [
                finding.finding_id,
                f"Affected Area: {finding.domain.value}"
                + (f" ({finding.location})" if finding.location else ""),
                "Reason:",
                finding.reason,
                "",
                "Required action:",
                finding.required_action,
                "",
            ]
        lines.append("Structural errors remain. Fix them before the review.")

    if result.warnings:
        lines += ["", "Warnings:", ""]
        for finding in result.warnings:
            where = f" ({finding.location})" if finding.location else ""
            lines.append(f"{finding.finding_id}  {finding.reason}{where}")

    return "\n".join(lines) + "\n"
