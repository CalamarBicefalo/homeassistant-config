from __future__ import annotations

from typing import Any


def generate_services(root_dir: str, services: list[dict[str, Any]]) -> None:
    services = sorted(services, key=lambda d: d["domain"])
    with open(f"{root_dir}/services.py", "w") as out:
        out.write("from typing import NewType\n"
                  "Service  = NewType('UserId', str)\n")
        for domain in services:
            for name in sorted(domain["services"].keys()):
                symbol = f'{domain["domain"].replace(".", "_").upper()}_{name.replace(".", "_").upper()}'
                out.write(f'{symbol}: Service = Service("{domain["domain"]}/{name}")\n')
