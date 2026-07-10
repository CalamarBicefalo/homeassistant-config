"""Deploy the pushed `main` to the live HA box and restart/reload what changed.

Flow: verify local is pushed -> `git pull --ff-only` on the box over SSH ->
restart the AppDaemon add-on and/or reload HA's YAML config, depending on what
the pull touched. If the pull changed dashboard.yaml, it also offers to `ha
dashboard push` (prompted, since that overwrites live UI edits). Restarts/
reloads/pushes go over the HA API; only the git pull needs SSH.

The box's repo is root-owned, so git runs via `sudo` (the SSH user has
passwordless sudo) and authenticates to GitHub with a repo-local read-only
deploy key configured as `core.sshCommand` — no agent forwarding needed.

Requires the box on the local network (or a VPN into it): the public domain
exposes only 443/HA, not SSH. Off-LAN, the pull fails fast with a hint.
"""
from __future__ import annotations

import subprocess
from typing import Optional

from ops import dashboard
from ops.client import HaClient

DASHBOARD_FILE = "dashboard.yaml"

# LAN name for the box: the public domain (calamarbicefalo.uk) only routes 443,
# so the SSH pull needs the box on the local network (or a VPN into it). The
# restart/reload half runs over the HA API (443) and works from anywhere.
DEFAULT_SSH_HOST = "hassio@homeassistant.local"
APPDAEMON_ADDON = "a0d7b954_appdaemon"

# Paths on the box to probe for the repo checkout (first match wins).
REPO_CANDIDATES = ["/config", "/homeassistant", "/root/homeassistant-config", "$HOME/homeassistant-config"]

# --- classification: which pulled changes need which deploy action ---
# These are COUPLED TO THE REPO LAYOUT. If you move/rename these dirs in a
# refactor, update them here. `test_install.py` guards APPDAEMON_APPS_PREFIX
# (a stale value silently stops apps from restarting), and classify() fails
# safe otherwise: anything not ignored and not an app counts as HA config and
# triggers a (harmless) reload, so a missed ignore only over-reloads.
APPDAEMON_APPS_PREFIX = "appdaemon/apps/"

# Changed paths that never need a deploy action (dev tooling, docs, and the
# storage-mode dashboard which HA does not read from disk).
IGNORED_PREFIXES = (
    "ops/", "codegen/", "docs/", ".claude/", ".circleci/", ".idea/", "secrets/",
    "appdaemon/tests/", "appdaemon/.mypy_cache/", "appdaemon/.pytest_cache/",
)
IGNORED_FILES = (
    "dashboard.yaml", "README.md", "AGENTS.md", "Pipfile", "Pipfile.lock",
    "mypy.ini", ".gitignore", "ha", "generate.py",
)


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()


def local_push_warnings() -> list[str]:
    """Reasons the box would deploy something other than the user's current work."""
    warnings = []
    branch = _git("rev-parse", "--abbrev-ref", "HEAD")
    if branch != "main":
        warnings.append(f"you are on branch '{branch}', not 'main'")
    if _git("status", "--porcelain"):
        warnings.append("you have uncommitted changes")
    if _git("log", "--oneline", "origin/main..HEAD"):
        warnings.append("you have commits not pushed to origin/main")
    return warnings


def _is_ignored(path: str) -> bool:
    return path in IGNORED_FILES or path.startswith(IGNORED_PREFIXES)


def classify(changed: list[str]) -> tuple[list[str], list[str]]:
    """Split changed paths into (appdaemon-app changes, HA-config changes)."""
    app_changes = [f for f in changed if f.startswith(APPDAEMON_APPS_PREFIX)]
    config_changes = [f for f in changed
                      if not _is_ignored(f) and not f.startswith("appdaemon/")]
    return app_changes, config_changes


def _remote_pull_script(path: Optional[str]) -> str:
    candidates = f'"{path}"' if path else " ".join(REPO_CANDIDATES)
    return f"""
set -e
# git runs as root (the checkout is root-owned; the SSH user has passwordless
# sudo). safe.directory='*' avoids the "dubious ownership" guard; GitHub auth
# uses the repo-local deploy key via core.sshCommand (set once during setup).
git() {{ sudo git -c safe.directory='*' "$@"; }}
repo=""
for d in {candidates}; do
  if git -C "$d" remote get-url origin 2>/dev/null | grep -qi homeassistant-config; then repo="$d"; break; fi
done
[ -z "$repo" ] && {{ echo "REPO_NOT_FOUND"; exit 3; }}
before=$(git -C "$repo" rev-parse HEAD)
git -C "$repo" pull --ff-only
after=$(git -C "$repo" rev-parse HEAD)
echo "REPO=$repo"
echo "---CHANGED---"
git -C "$repo" diff --name-only "$before" "$after"
"""


def pull_on_box(host: str, path: Optional[str]) -> list[str]:
    """Run `git pull` on the box over SSH; return the list of changed paths."""
    result = subprocess.run(
        ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=15", host,
         "bash", "-s"],
        input=_remote_pull_script(path), capture_output=True, text=True,
    )
    out = result.stdout
    if result.returncode != 0 or "REPO_NOT_FOUND" in out:
        detail = (out + result.stderr).strip()
        if "REPO_NOT_FOUND" in out:
            raise SystemExit("Could not find the repo checkout on the box. "
                             "Pass --path <dir>.")
        unreachable = any(s in detail for s in (
            "Could not resolve", "No route to host", "timed out", "Connection refused"))
        hint = ("\n\nThe box's SSH is only reachable on the local network — connect "
                "to the LAN (or a VPN into it) and retry. (The public domain exposes "
                "only 443/HA, not SSH.)") if unreachable else ""
        raise SystemExit(f"Pull over SSH failed (host {host}):\n{detail}{hint}")
    marker = "---CHANGED---"
    changed_block = out.split(marker, 1)[1] if marker in out else ""
    return [line.strip() for line in changed_block.splitlines() if line.strip()]


def _show_group(label: str, files: list[str]) -> None:
    if not files:
        return
    print(f"  {label} ({len(files)}):")
    for f in files:
        print(f"    - {f}")


def _confirm_dashboard_push(assume_yes: bool) -> bool:
    if assume_yes:
        return True
    print(f"  {DASHBOARD_FILE} changed. Pushing overwrites the live dashboard, "
          "including any UI edits since your last `ha dashboard pull`.")
    return input("  Push dashboard to live? [y/N] ").strip().lower() in ("y", "yes")


def run(host: str = DEFAULT_SSH_HOST, path: Optional[str] = None,
        core: bool = False, assume_yes: bool = False) -> None:
    warnings = local_push_warnings()
    if warnings and not assume_yes:
        print("The box deploys origin/main, but:")
        for w in warnings:
            print(f"  - {w}")
        if input("Deploy whatever is on origin/main anyway? [y/N] ").strip().lower() not in ("y", "yes"):
            print("Aborted.")
            return

    print(f"Pulling on {host}...")
    changed = pull_on_box(host, path)
    if not changed:
        print("Already up to date — nothing to deploy.")
        return

    app_changes, config_changes = classify(changed)
    dashboard_changed = DASHBOARD_FILE in changed
    other = [f for f in changed
             if f not in app_changes and f not in config_changes and f != DASHBOARD_FILE]

    print(f"Pulled {len(changed)} changed file(s):")
    _show_group("AppDaemon apps", app_changes)
    _show_group("HA config", config_changes)
    _show_group("Dashboard", [DASHBOARD_FILE] if dashboard_changed else [])
    _show_group("Other (not deployed)", other)

    client = HaClient()
    done: list[str] = []

    if config_changes:
        if core:
            print("→ Restarting Home Assistant core (homeassistant.restart)...", end=" ", flush=True)
            client.call_service("homeassistant", "restart")
            print("done.")
            done.append("HA core restart")
        else:
            print("→ Validating HA config...", end=" ", flush=True)
            verdict = client.check_config()
            if verdict.get("result") != "valid":
                print("INVALID.")
                raise SystemExit(f"Config invalid, not reloading:\n{verdict.get('errors')}")
            print("valid.")
            print("→ Reloading all HA YAML (homeassistant.reload_all)...", end=" ", flush=True)
            client.call_service("homeassistant", "reload_all")
            print("done.")
            done.append("HA config reload")

    if app_changes:
        print(f"→ Restarting AppDaemon add-on ({APPDAEMON_ADDON})...", end=" ", flush=True)
        client.call_service("hassio", "addon_restart", {"addon": APPDAEMON_ADDON})
        print("done.")
        done.append("AppDaemon restart")

    if dashboard_changed and _confirm_dashboard_push(assume_yes):
        # push prints its own "Pushed ... (N views)" confirmation.
        print("→ Pushing dashboard to live...")
        dashboard.push(dashboard.DEFAULT_URL_PATH, dashboard.DEFAULT_FILE, assume_yes=True)
        done.append("dashboard push")

    if done:
        print(f"✅  Deployed: {', '.join(done)}.")
    elif dashboard_changed:
        print("Dashboard change not pushed; nothing else to deploy.")
    else:
        print("Changes were dev-only (not deployed to HA) — no restart needed.")
