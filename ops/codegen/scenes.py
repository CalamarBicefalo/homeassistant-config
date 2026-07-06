from __future__ import annotations

from typing import Any


def generate_scenes(root_dir: str, states: list[dict[str, Any]]) -> None:
    states = sorted(states, key=lambda s: s["entity_id"])
    with open(f"{root_dir}/scenes.py", "w") as out:
        out.write("from scene_controllers import scene\n"
                  "from entities import Entity\n"
                  "from scene_controllers.scene import Scene\n")
        for s in states:
            if s["entity_id"].startswith("scene."):
                name = s["entity_id"].replace("scene.", "").replace(".", "_").upper()
                out.write(f'{name}: Scene = scene.from_entity(Entity("{s["entity_id"]}"))\n')
