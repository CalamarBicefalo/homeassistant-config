"""Supporting toolkit for the Home Assistant config repo.

A single Typer CLI (`python -m ops`, aliased to `ha`) over one HTTP/WebSocket
client (`ops.client`, `ops.wsclient`): live diagnostics, dashboard-as-code sync
(`ops.dashboard`), and AppDaemon type-stub generation (`ops.codegen`). Auth uses
the long-lived token in `secrets/secrets.yaml`. Run from the repo root.
"""
