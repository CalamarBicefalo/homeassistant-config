"""Helpers for setting up the generated `sensor.<room>_brightness` wrappers.

The AppDaemon BrightnessHandler reads these wrapper sensors (state = category,
attributes = illuminance + hysteresis thresholds). These mirror the calibration
profiles in windows.yaml so scene tests can express a lux reading and get a
correctly-populated wrapper sensor.
"""

# Keep in sync with windows.yaml.
WINDOW = dict(cloudy=1000, bright=10000, direct_sunlight=50000, turn_on_below=1500, allow_off_at=4000)
AMBIANCE = dict(cloudy=60, bright=200, direct_sunlight=1000, turn_on_below=60, allow_off_at=200)


def category(lux, cal):
    if lux >= cal["direct_sunlight"]:
        return "direct_sunlight"
    if lux >= cal["bright"]:
        return "bright"
    if lux >= cal["cloudy"]:
        return "cloudy"
    return "dark"


def set_brightness(given_that, sensor, illuminance, cal=WINDOW):
    """Populate a wrapper sensor from a lux reading, as the template would."""
    given_that.state_of(sensor).is_set_to(category(illuminance, cal), {
        "illuminance": illuminance,
        "sensor_type": "window" if cal is WINDOW else "ambiance",
        "turn_on_below": cal["turn_on_below"],
        "allow_off_at": cal["allow_off_at"],
    })
