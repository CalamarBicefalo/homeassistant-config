---
description: Diagnose a Home Assistant / AppDaemon problem against the live instance and propose a fix
argument-hint: "[symptom, entity_id, or app name — optional]"
allowed-tools: Bash(pipenv run python -m ops.logs:*), Bash(pipenv run python -m ops.appderrors:*), Bash(pipenv run python -m ops.state:*), Bash(pipenv run python -m ops.history:*), Bash(pipenv run python -m ops.logbook:*), Bash(pipenv run python -m ops.template:*), Bash(pipenv run pytest:*), Bash(pipenv run mypy:*)
---

Diagnose a production problem on the live Home Assistant instance and propose a fix.
Focus: $ARGUMENTS

Use the read-only `ops/` toolkit (run from the repo root with `pipenv run python -m ops.<cmd>`).
Do NOT deploy or restart anything — stop at a reviewed branch.

## 1. Gather evidence
- `ops.appderrors` — AppDaemon app errors (backed by `sensor.appdaemon_last_error`).
- `ops.logs --level ERROR` (add `--grep <keyword>` when a focus is given) — HA core errors/warnings.
- If a specific entity/app is in focus, narrow with:
  - `ops.state <entity_id>` — current state + attributes
  - `ops.history <entity_id> --since 6h` — how it changed
  - `ops.logbook --entity <entity_id> --since 6h` — related events
  - `ops.template "<jinja>"` — evaluate a suspect condition against live state

## 2. Root cause
State the root cause in one or two sentences, citing the specific log line / state /
template result that proves it. If the evidence is ambiguous, say so and gather more
rather than guessing.

## 3. Reproduce as a failing test
Add or extend a test under `appdaemon/tests/` that fails for this reason. Reuse the
existing patterns (`automation_fixture`, `given_that`/`assert_that`, fakes).

## 4. Fix
Make the minimal change in `appdaemon/apps/src/` (or the relevant YAML). Never edit
files in `appdaemon/apps/generated/` — run `python generate.py` instead. Then make
ALL tests pass: `pipenv run pytest appdaemon/tests/ -v` (and `pipenv run mypy ops`
if `ops/` changed).

## 5. Propose
Summarize root cause → fix → test evidence. Open the change on a branch and let the
user review/merge — HA pulls on merge. Do not push or deploy unless asked.
