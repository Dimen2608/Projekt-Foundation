"""Erzwingt die Repo-Regel: jede Pruefregel wird von einem Test geschuetzt.

Diese beiden Tests pruefen nicht das Verhalten des Validators, sondern die Vollstaendigkeit
seiner Absicherung. Sie ersetzen Mutation Testing, das fuer diesen Code das falsche Werkzeug
waere - siehe ADR-0009.
"""

from __future__ import annotations

import re
from pathlib import Path

from foundation_validate.validator import FINDING_IDS

_REPO = Path(__file__).resolve().parents[1]
_QUELLE = _REPO / "src" / "foundation_validate" / "validator.py"
_TESTS = Path(__file__).resolve().parent

#: Findet ID-Literale wie "STRUCT-004". Dynamisch erzeugte IDs (f-Strings) matchen nicht -
#: die sind an Konstantenlisten gebunden und wachsen mit ihnen.
_ID_RE = re.compile(r'"([A-Z]+-\d{3})"')

#: DEF- und ARCH- entstehen je Abschnitt bzw. Architekturbereich aus einer Konstantenliste.
#: Ein eigener Test je Listeneintrag waere Buerokratie ohne Erkenntnis; die Familien sind
#: als Ganzes abgedeckt (test_fehlender_pflichtabschnitt_in_project_md_blockiert,
#: test_unbekannte_authentifizierung_blockiert, test_nicht_bewerteter_unkritischer_bereich).
_FAMILIEN_OHNE_EINZELTEST = ("DEF-", "ARCH-")


def _ids_in_tests() -> set[str]:
    treffer: set[str] = set()
    for pfad in sorted(_TESTS.glob("test_*.py")):
        treffer |= set(_ID_RE.findall(pfad.read_text(encoding="utf-8")))
    return treffer


def test_jede_regel_wird_von_einem_test_geprueft() -> None:
    erwartet = {i for i in FINDING_IDS if not i.startswith(_FAMILIEN_OHNE_EINZELTEST)}
    fehlend = sorted(erwartet - _ids_in_tests())
    assert not fehlend, f"Pruefregeln ohne schuetzenden Test: {', '.join(fehlend)}"


def test_jede_id_im_quelltext_steht_im_register() -> None:
    """Verhindert, dass eine neue Regel am Register und damit am Abdeckungstest vorbeigeht."""
    im_code = set(_ID_RE.findall(_QUELLE.read_text(encoding="utf-8")))
    fehlend = sorted(im_code - set(FINDING_IDS))
    assert not fehlend, f"Finding-IDs ohne Registereintrag: {', '.join(fehlend)}"
