# Context
This repo contains Home Assistant (HA) configuration. It includes:
- A bunch of YAML as per the official HA configuration docs
- Some YAML that is generated code via ./generate.py typically (but not always) contains generated in the filename
- Appdaemon python apps. These are all my automations, and are tested in ./appdaemon/tests
- NEVER modify generated files, instead use generate.py
- A dashboard using minimalist UI in ./ui_lovelace_minimalist/dashboard

# Rules for agents to follow
- Do not make assumptions, always check with me. Ask clarifying questions if 
there's ambiguity in the task at hand.
- Comments are good, but do not add superfluous or overly verbose comments for the sake of it
- When you make changes, ALWAYS make sure ALL tests are passing, you can execute tests by running `pipenv run pytest appdaemon/tests/ -v`

# Production diagnostics
The `ops/` package is a read-only toolkit for inspecting the live HA instance
(`https://calamarbicefalo.uk`). It reuses the token in `secrets/secrets.yaml`.
Run commands from the repo root with `pipenv run python -m ops.<cmd>`:
- `ops.logs [--level ERROR] [--grep x] [--tail N]` — HA core warnings/errors
  (via the `system_log` WebSocket API; `/api/error_log` returns 404 on this
  instance because file logging is disabled).
- `ops.appderrors [--since 24h]` — AppDaemon app errors, surfaced into HA by the
  `error_reporter` app as `sensor.appdaemon_last_error` + `appdaemon.error` events.
- `ops.state <entity_id>` — current state + attributes.
- `ops.history <entity_id> [--since 2h]` / `ops.logbook [--entity x] [--since 2h]`.
- `ops.template "<jinja>"` — render a template against live state (debug conditions).

Triage loop when diagnosing a problem:
1. `ops.appderrors` and `ops.logs --level ERROR` to find the failure.
2. `ops.state` / `ops.history` / `ops.logbook` / `ops.template` to find the root
   cause against live state.
3. Reproduce it as a failing test under `appdaemon/tests/`.
4. Fix, then make ALL tests pass (`pipenv run pytest appdaemon/tests/ -v`).
5. Propose the change on a branch — do NOT deploy (I merge; HA pulls).