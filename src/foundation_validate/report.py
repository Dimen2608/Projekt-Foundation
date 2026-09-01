"""Erzeugt den Foundation-Audit-Report im festgelegten Format."""

from __future__ import annotations

from foundation_validate.model import Domain
from foundation_validate.validator import Result

BOX = "╔" + "═" * 38 + "╗\n║" + "       PROJECT FOUNDATION AUDIT       " + "║\n╚" + "═" * 38 + "╝"

_LABEL_WIDTH = 25


def render(result: Result) -> str:
    """Formatiert das Validierungsergebnis als Audit-Report."""
    lines = [BOX, ""]
    for domain in Domain:
        lines.append(f"{domain.value.ljust(_LABEL_WIDTH)}{result.domain_status[domain]}")
    lines += [
        "",
        f"Blocking Issues: {len(result.blocking)}",
        f"Warnings: {len(result.warnings)}",
        "",
        "=" * 40,
        "",
    ]

    if result.ready:
        lines += ["FOUNDATION READY", "", "Implementation may begin."]
    else:
        lines += ["FOUNDATION NOT READY", "", "Blocking Issues:", ""]
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
        lines.append("Implementation is blocked.")

    if result.warnings:
        lines += ["", "Warnings:", ""]
        for finding in result.warnings:
            where = f" ({finding.location})" if finding.location else ""
            lines.append(f"{finding.finding_id}  {finding.reason}{where}")

    return "\n".join(lines) + "\n"
