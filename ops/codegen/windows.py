"""Generate the brightness template sensors from the windows DSL.

Reads `windows.yaml` (named calibration profiles + one entry per window) and
writes `devices/templates/brightness_generated.yaml`: a `sensor.<room>_brightness`
per window whose state is the light category (dark/cloudy/bright/
direct_sunlight) and whose attributes carry the raw lux, the sensor type and
the lamp-hysteresis thresholds. The AppDaemon BrightnessHandler consumes these
sensors, so the thresholds live in windows.yaml and nowhere else.
"""
from __future__ import annotations

from typing import Any

import yaml

OUTPUT = "devices/templates/brightness_generated.yaml"
ICON = "mdi:white-balance-sunny"


def snake(name: str) -> str:
    return name.lower().replace(" ", "_")


def _classification_template(sensor: str, cal: dict[str, Any]) -> str:
    """Single-line HA template mapping the sensor's lux to a category string."""
    return (
        f"{{% set lux = states('{sensor}') | float(0) %}}"
        f"{{% if lux >= {cal['direct_sunlight']} %}}direct_sunlight"
        f"{{% elif lux >= {cal['bright']} %}}bright"
        f"{{% elif lux >= {cal['cloudy']} %}}cloudy"
        f"{{% else %}}dark{{% endif %}}"
    )


def load_windows(descriptor: dict[str, Any]) -> list[dict[str, Any]]:
    """Resolve each window's named calibration profile into inline thresholds."""
    calibrations = descriptor["calibrations"]
    windows = descriptor["windows"]
    for window in windows:
        profile = window["calibration"]
        if profile not in calibrations:
            raise ValueError(
                f"window '{window['room']}' references unknown calibration '{profile}'")
        window["_cal"] = calibrations[profile]
    return windows


def generate_windows(root_dir: str) -> None:
    with open("windows.yaml", "r") as stream:
        descriptor = yaml.safe_load(stream)
    windows = load_windows(descriptor)

    with open(OUTPUT, "w") as f:
        f.write("# GENERATED from windows.yaml by `ha gen` — do not edit.\n")
        for window in windows:
            room = window["room"]
            sensor = window["illuminance"]
            cal = window["_cal"]
            f.write(f"""
- sensor:
  - name: "{room} Brightness"
    unique_id: {snake(room)}_brightness
    icon: {ICON}
    state: "{_classification_template(sensor, cal)}"
    attributes:
      illuminance: "{{{{ states('{sensor}') | float(0) }}}}"
      sensor_type: {window['type']}
      lights_on_below: {cal['lights_on_below']}
      lights_off_above: {cal['lights_off_above']}
""")
            # Only windows that drive blinds carry a shade threshold.
            if "blinds_shade_above" in cal:
                f.write(f"      blinds_shade_above: {cal['blinds_shade_above']}\n")
