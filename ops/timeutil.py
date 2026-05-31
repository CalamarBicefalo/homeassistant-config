from __future__ import annotations

from datetime import datetime, timedelta, timezone

# Single-letter duration suffixes accepted by the --since flags.
_UNITS = {"m": "minutes", "h": "hours", "d": "days"}


def since_to_iso(spec: str) -> str:
    """Turn a relative duration like '30m', '2h', '1d' into an ISO8601 UTC start.

    Used by history/logbook/appderrors to build the `period` path segment.
    """
    spec = spec.strip().lower()
    if not spec or spec[-1] not in _UNITS:
        raise ValueError(f"Unknown duration '{spec}'. Use e.g. 30m, 2h, 1d.")
    amount = int(spec[:-1])
    start = datetime.now(timezone.utc) - timedelta(**{_UNITS[spec[-1]]: amount})
    return start.isoformat()
