from __future__ import annotations

from ops.logs import _format, _levels_at_or_above


def test_levels_at_or_above_includes_higher_levels() -> None:
    assert _levels_at_or_above("WARNING") == {"WARNING", "ERROR", "CRITICAL"}
    assert _levels_at_or_above("ERROR") == {"ERROR", "CRITICAL"}


def test_levels_at_or_above_unknown_level_is_passed_through() -> None:
    assert _levels_at_or_above("WARN") == {"WARN"}


def test_format_renders_level_source_and_repeat_count() -> None:
    line = _format({
        "timestamp": 0,
        "level": "ERROR",
        "source": ["components/automation/__init__.py", 42],
        "message": ["boom", "ignored second line"],
        "count": 3,
    })
    assert "ERROR" in line
    assert "components/automation/__init__.py" in line
    assert "boom" in line
    assert "(x3)" in line
