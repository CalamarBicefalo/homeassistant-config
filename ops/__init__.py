"""Production diagnostics toolkit for the Home Assistant instance.

Thin, typed CLI wrappers over the HA REST API, reusing the same long-lived token
as `codegen` (secrets/secrets.yaml). Run from the repo root, e.g.:

    python -m ops.logs --level ERROR
    python -m ops.state sensor.appdaemon_last_error
    python -m ops.appderrors --since 24h
"""
