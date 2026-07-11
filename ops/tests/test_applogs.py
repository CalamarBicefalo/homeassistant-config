from __future__ import annotations

from ops.applogs import _format, _levels_at_or_above, parse


def test_levels_at_or_above_includes_higher_levels() -> None:
    assert _levels_at_or_above("INFO") == {"INFO", "WARNING", "ERROR", "CRITICAL"}
    assert _levels_at_or_above("ERROR") == {"ERROR", "CRITICAL"}


def test_parse_splits_header_into_app_and_message() -> None:
    (entry,) = parse("2026-07-11 17:44:34.543540 INFO AppDaemon: App init complete")
    assert entry.level == "INFO"
    assert entry.app == "AppDaemon"
    assert entry.message == "App init complete"


def test_parse_attaches_continuation_lines_to_previous_entry() -> None:
    raw = (
        "2026-07-11 17:37:13.719 ERROR Error: boom\n"
        '  File "app.py", line 63, in __init__\n'
        "    raise TypeError()\n"
    )
    (entry,) = parse(raw)
    assert entry.extra == ['  File "app.py", line 63, in __init__', "    raise TypeError()"]
    assert "TypeError" in entry.text  # continuation lines are searchable via --grep


def test_parse_strips_ansi_and_drops_boot_noise() -> None:
    raw = (
        "\x1b[34m banner line with no header \x1b[0m\n"
        "2026-07-11 17:44:34.543540 INFO Kitchen activity: ready\n"
    )
    entries = parse(raw)
    assert len(entries) == 1
    assert entries[0].app == "Kitchen activity"


def test_parse_header_without_app_prefix_keeps_full_message() -> None:
    (entry,) = parse("2026-07-11 17:44:34.543540 INFO no colon here")
    assert entry.app == ""
    assert entry.message == "no colon here"


def test_format_plain_renders_time_level_app_and_message() -> None:
    (entry,) = parse("2026-07-11 17:44:34.543540 WARNING Away monitor: nobody home")
    line = _format(entry, colour=False)
    assert "17:44:34.543" in line
    assert "WARNING" in line
    assert "Away monitor: nobody home" in line
