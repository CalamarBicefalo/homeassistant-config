from __future__ import annotations

import json
from typing import Optional

import typer

from ops import appderrors as appderrors_mod
from ops import codegen
from ops import dashboard as dashboard_mod
from ops import install as install_mod
from ops import logs as logs_mod
from ops.client import HaClient
from ops.timeutil import since_to_iso

app = typer.Typer(
    help="Home Assistant config toolkit: live diagnostics, type codegen, and dashboard sync.",
    no_args_is_help=True,
    add_completion=True,
)

dashboard_app = typer.Typer(
    help="Sync the Lovelace dashboard between HA and dashboard.yaml.",
    no_args_is_help=True,
)
app.add_typer(dashboard_app, name="dashboard")


def _print_json(data: object) -> None:
    typer.echo(json.dumps(data, indent=2, sort_keys=True, default=str))


# --- live diagnostics (ops/) ---


@app.command()
def logs(
    level: str = typer.Option("WARNING", help="Minimum level to show."),
    grep: Optional[str] = typer.Option(None, help="Only entries containing this substring (case-insensitive)."),
    tail: int = typer.Option(30, help="Show the most recent N entries."),
) -> None:
    """Show HA core warnings/errors (system_log via WebSocket)."""
    logs_mod.run(level=level, grep=grep, tail=tail)


@app.command()
def appderrors(
    since: str = typer.Option("24h", help="History window, e.g. 2h, 24h, 7d."),
) -> None:
    """Show AppDaemon app errors reported into HA by error_reporter."""
    appderrors_mod.run(since=since)


@app.command()
def state(
    entity_id: str = typer.Argument(..., help="e.g. sensor.living_room_illuminance"),
) -> None:
    """Show an entity's current state and attributes."""
    _print_json(HaClient().state(entity_id))


@app.command()
def history(
    entity_id: str = typer.Argument(..., help="e.g. input_select.living_room_activity"),
    since: str = typer.Option("2h", help="Lookback window, e.g. 30m, 2h, 1d."),
) -> None:
    """Show recorded state history for an entity."""
    _print_json(HaClient().history(entity_id, since_to_iso(since)))


@app.command()
def logbook(
    entity: Optional[str] = typer.Option(None, help="Filter to a single entity_id."),
    since: str = typer.Option("2h", help="Lookback window, e.g. 30m, 2h, 1d."),
) -> None:
    """Show Home Assistant logbook entries."""
    _print_json(HaClient().logbook(since_to_iso(since), entity))


@app.command()
def template(
    template: str = typer.Argument(..., help="e.g. \"{{ states('sensor.foo') }}\""),
) -> None:
    """Render a Jinja template against live HA state (debug conditions)."""
    typer.echo(HaClient().render_template(template))


# --- type codegen ---


@app.command()
def gen() -> None:
    """Regenerate AppDaemon type stubs from local config + live HA state."""
    codegen.generate()


@app.command()
def install(
    host: str = typer.Option(install_mod.DEFAULT_SSH_HOST, help="SSH host of the HA box."),
    path: Optional[str] = typer.Option(None, help="Repo checkout path on the box (else auto-detected)."),
    core: bool = typer.Option(False, "--core", help="Full HA restart instead of reload_all for config changes."),
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip the unpushed-changes confirmation."),
) -> None:
    """Deploy origin/main to the box: pull, then restart AppDaemon / reload config."""
    install_mod.run(host=host, path=path, core=core, assume_yes=yes)


# --- dashboard as code ---


@dashboard_app.command("pull")
def dashboard_pull(
    url_path: str = typer.Option(dashboard_mod.DEFAULT_URL_PATH, "--url-path", help="Dashboard url_path."),
    file: str = typer.Option(dashboard_mod.DEFAULT_FILE, help="Local YAML file."),
) -> None:
    """Snapshot the live dashboard into the YAML file."""
    dashboard_mod.pull(url_path, file)


@dashboard_app.command("push")
def dashboard_push(
    url_path: str = typer.Option(dashboard_mod.DEFAULT_URL_PATH, "--url-path", help="Dashboard url_path."),
    file: str = typer.Option(dashboard_mod.DEFAULT_FILE, help="Local YAML file."),
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip the overwrite confirmation prompt."),
) -> None:
    """Write the YAML file to the live dashboard (overwrites it)."""
    dashboard_mod.push(url_path, file, assume_yes=yes)


if __name__ == "__main__":
    app()
