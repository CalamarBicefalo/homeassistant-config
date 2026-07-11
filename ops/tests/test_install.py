from __future__ import annotations

import types
from pathlib import Path

import pytest

from ops import install
from ops.install import APPDAEMON_APPS_PREFIX, classify


def test_appdaemon_apps_prefix_matches_a_real_dir() -> None:
    # Guards against silent drift: if appdaemon apps are moved/renamed, this
    # fails so APPDAEMON_APPS_PREFIX gets updated — otherwise app changes would
    # be misclassified as config and the AppDaemon add-on would never restart.
    repo_root = Path(__file__).resolve().parents[2]
    assert (repo_root / APPDAEMON_APPS_PREFIX).is_dir(), (
        f"{APPDAEMON_APPS_PREFIX!r} in ops/install.py no longer exists — "
        "update it to the new AppDaemon apps location.")


def test_classify_splits_appdaemon_and_config() -> None:
    app, config = classify([
        "appdaemon/apps/src/living_room.py",
        "configuration.yaml",
        "config/automations/lights.yaml",
    ])
    assert app == ["appdaemon/apps/src/living_room.py"]
    assert config == ["configuration.yaml", "config/automations/lights.yaml"]


def test_classify_ignores_dev_only_and_dashboard() -> None:
    app, config = classify([
        "ops/install.py",
        "dashboard.yaml",
        "README.md",
        "appdaemon/tests/test_x.py",
        "docs/img/foo.png",
    ])
    assert app == []
    assert config == []


def test_classify_generated_yaml_counts_as_config() -> None:
    app, config = classify(["helpers/input_boolean/input_boolean_generated.yaml"])
    assert app == []
    assert config == ["helpers/input_boolean/input_boolean_generated.yaml"]


def _ok(*_a, **_k):
    return types.SimpleNamespace(returncode=0, stdout="", stderr="")


def test_regenerate_runs_gen_and_returns_changed_files(monkeypatch) -> None:
    ran = {}
    monkeypatch.setattr(install, "generate", lambda: ran.setdefault("gen", True))
    monkeypatch.setattr(install.subprocess, "run", _ok)
    monkeypatch.setattr(install, "_git",
                        lambda *a: "devices/templates/brightness_generated.yaml\n")

    changed = install.regenerate()

    assert ran["gen"] is True
    assert changed == ["devices/templates/brightness_generated.yaml"]


def test_regenerate_returns_empty_when_nothing_changed(monkeypatch) -> None:
    monkeypatch.setattr(install, "generate", lambda: None)
    monkeypatch.setattr(install.subprocess, "run", _ok)
    monkeypatch.setattr(install, "_git", lambda *a: "")

    assert install.regenerate() == []


def test_commit_and_push_raises_on_push_failure(monkeypatch) -> None:
    def run(cmd, **_k):
        if cmd[:2] == ["git", "push"]:
            return types.SimpleNamespace(returncode=1, stdout="", stderr="rejected")
        return _ok()

    monkeypatch.setattr(install.subprocess, "run", run)
    with pytest.raises(SystemExit):
        install.commit_and_push_generated(["devices/templates/brightness_generated.yaml"])
