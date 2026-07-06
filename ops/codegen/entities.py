from __future__ import annotations

from typing import Any


def generate_entities(root_dir: str, states: list[dict[str, Any]]) -> None:
    states = sorted(states, key=lambda s: s["entity_id"])
    with open(f"{root_dir}/entities.py", "w") as out:
        out.write("from typing import NewType\n"
                  "Entity = NewType('Entity', str)\n")
        for s in states:
            out.write(f'{s["entity_id"].replace(".", "_").upper()}: Entity = Entity("{s["entity_id"]}")\n')
