from __future__ import annotations

from datetime import datetime

import pytest

from ops.timeutil import since_to_iso


def test_since_to_iso_is_in_the_past_and_parseable() -> None:
    parsed = datetime.fromisoformat(since_to_iso("2h"))
    assert parsed < datetime.now(parsed.tzinfo)


@pytest.mark.parametrize("spec", ["5x", "", "h", "abc"])
def test_since_to_iso_rejects_bad_input(spec: str) -> None:
    with pytest.raises(ValueError):
        since_to_iso(spec)
