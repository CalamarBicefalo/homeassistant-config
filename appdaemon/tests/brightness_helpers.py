"""Helpers for setting up the generated `sensor.<room>_brightness` wrappers.

The AppDaemon BrightnessHandler reads these wrapper sensors (state = category,
attributes = illuminance + hysteresis thresholds). These mirror the calibration
profiles in windows.yaml so scene tests can express a lux reading and get a
correctly-populated wrapper sensor.
"""

# Keep in sync with windows.yaml.
WINDOW = dict(cloudy=1000, bright=10000, direct_sunlight=50000,
              lights_on_below=1500, lights_off_above=4000, blinds_shade_above=5000)
AMBIANCE = dict(cloudy=60, bright=200, direct_sunlight=1000,
                lights_on_below=60, lights_off_above=200)


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
    attributes = {
        "illuminance": illuminance,
        "sensor_type": "window" if cal is WINDOW else "ambiance",
        "lights_on_below": cal["lights_on_below"],
        "lights_off_above": cal["lights_off_above"],
    }
    if "blinds_shade_above" in cal:
        attributes["blinds_shade_above"] = cal["blinds_shade_above"]
    given_that.state_of(sensor).is_set_to(category(illuminance, cal), attributes)
