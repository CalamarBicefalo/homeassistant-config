from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ops.dashboard import dump_yaml, load_yaml


def test_dump_yaml_sorts_keys_for_stable_diffs() -> None:
    out = dump_yaml({"views": [{"type": "grid", "badges": [], "cards": []}]})
    # Keys within a view come out alphabetically regardless of input order.
    assert out.index("badges:") < out.index("cards:") < out.index("type:")


def test_dump_yaml_uses_block_scalars_for_multiline() -> None:
    out = dump_yaml({"views": [{"content": "line one\nline two\n"}]})
    assert "content: |" in out
    assert "\\n" not in out


def test_dump_yaml_round_trips_through_yaml_load() -> None:
    config = {"views": [{"title": "Home", "cards": [{"type": "markdown", "content": "a\nb\n"}]}]}
    assert yaml.safe_load(dump_yaml(config)) == config


def test_load_yaml_rejects_non_lovelace_config(tmp_path: Path) -> None:
    path = tmp_path / "not-a-dashboard.yaml"
    path.write_text("foo: bar\n")
    with pytest.raises(SystemExit):
        load_yaml(str(path))


def test_load_yaml_accepts_views(tmp_path: Path) -> None:
    path = tmp_path / "dashboard.yaml"
    path.write_text("views:\n- title: Home\n")
    assert load_yaml(str(path)) == {"views": [{"title": "Home"}]}
