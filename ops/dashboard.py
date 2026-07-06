from __future__ import annotations

from typing import Any

import yaml

from ops.wsclient import call

# The storage-mode dashboard we keep mirrored as code. Its live config is edited
# by clicking around in the HA UI; `pull` snapshots that into DEFAULT_FILE and
# `push` writes DEFAULT_FILE back to the live dashboard.
DEFAULT_URL_PATH = "dashboard-playground"
DEFAULT_FILE = "dashboard.yaml"


def fetch_config(url_path: str) -> dict[str, Any]:
    """Fetch a dashboard's Lovelace config from live HA over WebSocket."""
    config: dict[str, Any] = call({"type": "lovelace/config", "url_path": url_path})
    return config


def save_config(url_path: str, config: dict[str, Any]) -> None:
    """Overwrite a dashboard's Lovelace config on live HA over WebSocket."""
    call({"type": "lovelace/config/save", "url_path": url_path, "config": config})


class _DashboardDumper(yaml.SafeDumper):
    """SafeDumper that renders multiline strings as literal block scalars."""


def _represent_str(dumper: yaml.Dumper, data: str) -> yaml.Node:
    # Jinja templates and CSS `styles` blocks are multiline; `|` keeps them
    # readable and diffable instead of one long double-quoted `\n`-laden line.
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_DashboardDumper.add_representer(str, _represent_str)


def dump_yaml(config: dict[str, Any]) -> str:
    """Serialize a config to deterministic YAML.

    Keys are sorted so the file is a stable, minimal-diff mirror regardless of
    the order HA happens to return them in — the whole point of a synced artifact.
    """
    text: str = yaml.dump(
        config,
        Dumper=_DashboardDumper,
        sort_keys=True,
        allow_unicode=True,
        default_flow_style=False,
        width=100,
    )
    return text


def load_yaml(path: str) -> dict[str, Any]:
    with open(path, "r") as stream:
        config = yaml.safe_load(stream)
    if not isinstance(config, dict) or "views" not in config:
        raise SystemExit(f"{path} does not look like a Lovelace config (no 'views' key).")
    return config


def pull(url_path: str, path: str) -> None:
    """Snapshot the live dashboard into a local YAML file."""
    config = fetch_config(url_path)
    with open(path, "w") as stream:
        stream.write(dump_yaml(config))
    print(f"Pulled '{url_path}' -> {path} ({len(config.get('views', []))} views)")


def push(url_path: str, path: str, assume_yes: bool = False) -> None:
    """Write a local YAML file to the live dashboard, overwriting it."""
    config = load_yaml(path)
    if not assume_yes:
        answer = input(
            f"Overwrite live dashboard '{url_path}' with {path} "
            f"({len(config['views'])} views)? [y/N] "
        )
        if answer.strip().lower() not in ("y", "yes"):
            print("Aborted.")
            return
    save_config(url_path, config)
    print(f"Pushed {path} -> '{url_path}' ({len(config['views'])} views)")
