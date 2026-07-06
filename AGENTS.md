# Context
This repo contains Home Assistant (HA) configuration. It includes:
- A bunch of YAML as per the official HA configuration docs
- Some YAML that is generated code via `ha gen` typically (but not always) contains generated in the filename
- Appdaemon python apps. These are all my automations, and are tested in ./appdaemon/tests
- NEVER modify generated files, instead use `ha gen`

# Rules for agents to follow
- Do not make assumptions, always check with me. Ask clarifying questions if 
there's ambiguity in the task at hand.
- Comments are good, but do not add superfluous or overly verbose comments for the sake of it
- When you make changes, ALWAYS make sure ALL tests are passing, you can execute tests by running `pipenv run pytest appdaemon/tests/ -v`

# This repo is PUBLIC
- It is hosted on a public GitHub remote. NEVER commit secrets (tokens, passwords,
  API keys, coordinates, addresses). Real secrets live in `secrets/secrets.yaml`,
  which is gitignored; reference them with `!secret <name>` in YAML, or load them
  via `load_token()` in Python (see `ops/client.py`). When adding config, use a
  `!secret` reference rather than the literal value.

# Logging for diagnosability
Production is diagnosed after the fact via the `ops/` toolkit (see below), so the
logs are the primary evidence. When writing automations, prefer logs that make a
future `/ha-diagnose` quick:
- The worst failures are SILENT ones — an action calls a service, returns normally,
  but the real-world effect never happens (e.g. a `media_player.play_media` whose
  provider fails, leaving the speaker idle). For actions whose effect is observable,
  follow the verify-after pattern in `MusicHandler._verify_playback`
  (`appdaemon/apps/utils/music.py`): schedule a short read-only `run_in` that checks
  the outcome and logs `INFO` on success / `WARNING` when the intended effect didn't
  happen. Keep it read-only and exception-safe so it can never affect behaviour.
- Never `except: pass` / `except: return None` silently — log at `WARNING` with the
  exception before swallowing it.
- Log at `WARNING`/`ERROR` for anything actionable (it surfaces in `ha logs --level
  ERROR`); use `DEBUG` for routine "why nothing happened" breadcrumbs (locked rooms,
  unmapped scenes) that are noisy in normal operation but invaluable when grepping.

# The `ha` CLI
All supporting tooling lives in the `ops/` package behind one Typer CLI, `ha`
(repo-root `./ha` launcher, aliased in `~/.zshrc`; `pipenv run ha` also works).
`--help` works on any command, `ha --install-completion` sets up shell
completion. It uses the token in `secrets/secrets.yaml` and talks to the live
instance (`https://calamarbicefalo.uk`).

Live diagnostics (read-only):
- `ha logs [--level ERROR] [--grep x] [--tail N]` — HA core warnings/errors
  (via the `system_log` WebSocket API; `/api/error_log` returns 404 on this
  instance because file logging is disabled).
- `ha appderrors [--since 24h]` — AppDaemon app errors, surfaced into HA by the
  `error_reporter` app as `sensor.appdaemon_last_error` + `appdaemon.error` events.
- `ha state <entity_id>` — current state + attributes.
- `ha history <entity_id> [--since 2h]` / `ha logbook [--entity x] [--since 2h]`.
- `ha template "<jinja>"` — render a template against live state (debug conditions).

Codegen: `ha gen` regenerates the AppDaemon type stubs (from local config +
live HA state) into `appdaemon/apps/generated/`.

Deploy: `ha install` pushes `origin/main` to the box (`git pull --ff-only` over
SSH with agent forwarding), then restarts the AppDaemon add-on and/or reloads HA
config based on what the pull touched (reporting each action), and prompts to
`ha dashboard push` if dashboard.yaml changed. Needs the box on the LAN/VPN (the
public domain exposes only 443/HA, not SSH); restart/reload/push is HA-API/443. Its
file classification in `ops/install.py` is COUPLED TO THE REPO LAYOUT — if you
move/rename deployed dirs (esp. `appdaemon/apps/`) or add dev-only dirs, update
the constants there; `test_install.py` guards the AppDaemon path.

Dashboard as code: `dashboard.yaml` is a git-tracked mirror of the storage-mode
`dashboard-playground` dashboard (edited by clicking in the HA UI). Keep them in
sync with:
- `ha dashboard pull` — snapshot the live dashboard into `dashboard.yaml` (run
  this before committing after editing in the UI).
- `ha dashboard push [-y]` — write `dashboard.yaml` back to the live dashboard
  (mutates live; prompts unless `-y`). Use after hand-editing the YAML.
Both go over the `lovelace/config` WebSocket API. Keys are sorted and multiline
templates render as `|` block scalars for stable diffs.

Triage loop when diagnosing a problem:
1. `ha appderrors` and `ha logs --level ERROR` to find the failure.
2. `ha state` / `ha history` / `ha logbook` / `ha template` to find the root
   cause against live state.
3. Reproduce it as a failing test under `appdaemon/tests/`.
4. Fix, then make ALL tests pass (`pipenv run pytest appdaemon/tests/ -v`).
5. Propose the change on a branch — do NOT deploy (I merge; HA pulls).