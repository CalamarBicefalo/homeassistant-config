from typing import NewType
Entity = NewType('Entity', str)
AUTOMATION_AUTOMATION_3: Entity = Entity("automation.automation_3")
AUTOMATION_BEDSIDE_BUTTON: Entity = Entity("automation.bedside_button")
AUTOMATION_DINNER_BUTTON: Entity = Entity("automation.dinner_button")
AUTOMATION_LIVING_ROOM_BUTTON: Entity = Entity("automation.living_room_button")
BINARY_SENSOR_BEDROOM_MS_OCCUPANCY: Entity = Entity("binary_sensor.bedroom_ms_occupancy")
BINARY_SENSOR_DESK_CHAIR_PS: Entity = Entity("binary_sensor.desk_chair_ps")
BINARY_SENSOR_DESK_ENTERTAINMENT_CONFIGURATION: Entity = Entity("binary_sensor.desk_entertainment_configuration")
BINARY_SENSOR_ENSUITE_DOOR_CS: Entity = Entity("binary_sensor.ensuite_door_cs")
BINARY_SENSOR_ENSUITE_MOTION: Entity = Entity("binary_sensor.ensuite_motion")
BINARY_SENSOR_ENSUITE_MS: Entity = Entity("binary_sensor.ensuite_ms")
BINARY_SENSOR_FLAT_DOOR_CS: Entity = Entity("binary_sensor.flat_door_cs")
BINARY_SENSOR_FLICK_MOP_ATTACHED: Entity = Entity("binary_sensor.flick_mop_attached")
BINARY_SENSOR_FLICK_WATER_BOX_ATTACHED: Entity = Entity("binary_sensor.flick_water_box_attached")
BINARY_SENSOR_FLICK_WATER_SHORTAGE: Entity = Entity("binary_sensor.flick_water_shortage")
BINARY_SENSOR_GALAXY_S9_IS_CHARGING: Entity = Entity("binary_sensor.galaxy_s9_is_charging")
BINARY_SENSOR_GALAXY_S9_WIFI_STATE: Entity = Entity("binary_sensor.galaxy_s9_wifi_state")
BINARY_SENSOR_HALLWAY_MS_OCCUPANCY: Entity = Entity("binary_sensor.hallway_ms_occupancy")
BINARY_SENSOR_KITCHEN_MOTION: Entity = Entity("binary_sensor.kitchen_motion")
BINARY_SENSOR_KITCHEN_MS_OCCUPANCY: Entity = Entity("binary_sensor.kitchen_ms_occupancy")
BINARY_SENSOR_LIVING_ROOM_MOTION: Entity = Entity("binary_sensor.living_room_motion")
BINARY_SENSOR_LIVING_ROOM_MS_OCCUPANCY: Entity = Entity("binary_sensor.living_room_ms_occupancy")
BINARY_SENSOR_SOFA_PS: Entity = Entity("binary_sensor.sofa_ps")
BINARY_SENSOR_STORAGE_DOOR_CS_IASZONE: Entity = Entity("binary_sensor.storage_door_cs_iaszone")
BINARY_SENSOR_STUDIO_MOTION: Entity = Entity("binary_sensor.studio_motion")
BINARY_SENSOR_STUDIO_MS_OCCUPANCY: Entity = Entity("binary_sensor.studio_ms_occupancy")
BINARY_SENSOR_VODAFONE_WI_FI_HUB_WAN_STATUS: Entity = Entity("binary_sensor.vodafone_wi_fi_hub_wan_status")
BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE: Entity = Entity("binary_sensor.wardrobe_door_left_cs_iaszone")
BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE: Entity = Entity("binary_sensor.wardrobe_door_right_cs_iaszone")
BUTTON_AQARA_LUMI_MOTION_AC01_PRESENCE_STATUS_RESET: Entity = Entity("button.aqara_lumi_motion_ac01_presence_status_reset")
BUTTON_BEDROOM_MS_PRESENCE_STATUS_RESET: Entity = Entity("button.bedroom_ms_presence_status_reset")
BUTTON_SONY_KD_49XF8096_REBOOT: Entity = Entity("button.sony_kd_49xf8096_reboot")
BUTTON_SONY_KD_49XF8096_TERMINATE_APPS: Entity = Entity("button.sony_kd_49xf8096_terminate_apps")
BUTTON_SYNCHRONIZE_DEVICES: Entity = Entity("button.synchronize_devices")
CAMERA_FLICK_MAP: Entity = Entity("camera.flick_map")
DEVICE_TRACKER_GALAXY_S9: Entity = Entity("device_tracker.galaxy_s9")
DEVICE_TRACKER_MANDIES_IPHONE: Entity = Entity("device_tracker.mandies_iphone")
HUBITAT_HUB: Entity = Entity("hubitat.hub")
INPUT_DATETIME_LAST_CLEANED_FLAT: Entity = Entity("input_datetime.last_cleaned_flat")
INPUT_DATETIME_LAST_CLEANED_KITCHEN: Entity = Entity("input_datetime.last_cleaned_kitchen")
INPUT_DATETIME_LAST_CLEANED_VACUUM_MOP: Entity = Entity("input_datetime.last_cleaned_vacuum_mop")
INPUT_DATETIME_LAST_COOKED: Entity = Entity("input_datetime.last_cooked")
INPUT_SELECT_BEDROOM_ACTIVITY: Entity = Entity("input_select.bedroom_activity")
INPUT_SELECT_ENSUITE_ACTIVITY: Entity = Entity("input_select.ensuite_activity")
INPUT_SELECT_HALLWAY_ACTIVITY: Entity = Entity("input_select.hallway_activity")
INPUT_SELECT_HOMEASSISTANT_MODE: Entity = Entity("input_select.homeassistant_mode")
INPUT_SELECT_KITCHEN_ACTIVITY: Entity = Entity("input_select.kitchen_activity")
INPUT_SELECT_LIVING_ROOM_ACTIVITY: Entity = Entity("input_select.living_room_activity")
INPUT_SELECT_STORAGE_ROOM_ACTIVITY: Entity = Entity("input_select.storage_room_activity")
INPUT_SELECT_STUDIO_ACTIVITY: Entity = Entity("input_select.studio_activity")
INPUT_SELECT_WARDROBE_ACTIVITY: Entity = Entity("input_select.wardrobe_activity")
LIGHT_BATHROOM: Entity = Entity("light.bathroom")
LIGHT_BATHROOM_1: Entity = Entity("light.bathroom_1")
LIGHT_BATHROOM_2: Entity = Entity("light.bathroom_2")
LIGHT_BATHROOM_3: Entity = Entity("light.bathroom_3")
LIGHT_BEDROOM: Entity = Entity("light.bedroom")
LIGHT_BEDROOM_MAIN: Entity = Entity("light.bedroom_main")
LIGHT_BEDSIDE_1: Entity = Entity("light.bedside_1")
LIGHT_BEDSIDE_2: Entity = Entity("light.bedside_2")
LIGHT_DESK: Entity = Entity("light.desk")
LIGHT_DESK_SPOT: Entity = Entity("light.desk_spot")
LIGHT_DINING_LAMP: Entity = Entity("light.dining_lamp")
LIGHT_DINING_LEFT: Entity = Entity("light.dining_left")
LIGHT_DINING_ROOM: Entity = Entity("light.dining_room")
LIGHT_DINING_SOFA_LEFT: Entity = Entity("light.dining_sofa_left")
LIGHT_DRUM_SPOT: Entity = Entity("light.drum_spot")
LIGHT_FULL_BEDROOM: Entity = Entity("light.full_bedroom")
LIGHT_FULL_LIVING_ROOM: Entity = Entity("light.full_living_room")
LIGHT_HALLWAY: Entity = Entity("light.hallway")
LIGHT_HALLWAY_2: Entity = Entity("light.hallway_2")
LIGHT_HOME: Entity = Entity("light.home")
LIGHT_KITCHEN: Entity = Entity("light.kitchen")
LIGHT_KITCHEN_1: Entity = Entity("light.kitchen_1")
LIGHT_KITCHEN_2: Entity = Entity("light.kitchen_2")
LIGHT_KITCHEN_3: Entity = Entity("light.kitchen_3")
LIGHT_KITCHEN_4: Entity = Entity("light.kitchen_4")
LIGHT_KITCHEN_STRIP: Entity = Entity("light.kitchen_strip")
LIGHT_LAMP_PLANTS: Entity = Entity("light.lamp_plants")
LIGHT_LIVING_DOOR_2: Entity = Entity("light.living_door_2")
LIGHT_LIVING_MIDDLE_LEFT: Entity = Entity("light.living_middle_left")
LIGHT_LIVING_MIDDLE_RIGHT: Entity = Entity("light.living_middle_right")
LIGHT_LIVING_PLANTS: Entity = Entity("light.living_plants")
LIGHT_LIVING_ROOM: Entity = Entity("light.living_room")
LIGHT_LIVING_ROOM_DOOR_1: Entity = Entity("light.living_room_door_1")
LIGHT_LIVING_TV: Entity = Entity("light.living_tv")
LIGHT_ON_OFF_PLUG_1: Entity = Entity("light.on_off_plug_1")
LIGHT_STORAGE: Entity = Entity("light.storage")
LIGHT_STORAGE_2: Entity = Entity("light.storage_2")
LIGHT_STUDIO: Entity = Entity("light.studio")
LIGHT_WARDROBE: Entity = Entity("light.wardrobe")
LIGHT_WARDROBE_2: Entity = Entity("light.wardrobe_2")
MEDIA_PLAYER_BEDROOM_SPEAKERS: Entity = Entity("media_player.bedroom_speakers")
MEDIA_PLAYER_COOKING_AREA: Entity = Entity("media_player.cooking_area")
MEDIA_PLAYER_HALLWAY_SPEAKER: Entity = Entity("media_player.hallway_speaker")
MEDIA_PLAYER_HOME: Entity = Entity("media_player.home")
MEDIA_PLAYER_LIVING_ROOM_SPEAKER: Entity = Entity("media_player.living_room_speaker")
MEDIA_PLAYER_MASS_BEDROOM_SPEAKERS: Entity = Entity("media_player.mass_bedroom_speakers")
MEDIA_PLAYER_MASS_COOKING_AREA: Entity = Entity("media_player.mass_cooking_area")
MEDIA_PLAYER_MASS_HOME: Entity = Entity("media_player.mass_home")
MEDIA_PLAYER_MASS_OFFICE_SPEAKER: Entity = Entity("media_player.mass_office_speaker")
MEDIA_PLAYER_OFFICE_SPEAKER: Entity = Entity("media_player.office_speaker")
MEDIA_PLAYER_SONY_KD_49XF8096: Entity = Entity("media_player.sony_kd_49xf8096")
MEDIA_PLAYER_TV: Entity = Entity("media_player.tv")
MEDIA_PLAYER_TV_2: Entity = Entity("media_player.tv_2")
NUMBER_BEDROOM_SPEAKERS_ANNOUNCEMENTS_VOLUME_INCREASE_RELATIVE: Entity = Entity("number.bedroom_speakers_announcements_volume_increase_relative")
NUMBER_BEDROOM_SPEAKERS_CROSSFADE_DURATION: Entity = Entity("number.bedroom_speakers_crossfade_duration")
NUMBER_COOKING_AREA_ANNOUNCEMENTS_VOLUME_INCREASE_RELATIVE: Entity = Entity("number.cooking_area_announcements_volume_increase_relative")
NUMBER_COOKING_AREA_CROSSFADE_DURATION: Entity = Entity("number.cooking_area_crossfade_duration")
NUMBER_HOME_ANNOUNCEMENTS_VOLUME_INCREASE_RELATIVE: Entity = Entity("number.home_announcements_volume_increase_relative")
NUMBER_HOME_CROSSFADE_DURATION: Entity = Entity("number.home_crossfade_duration")
NUMBER_LIVING_ROOM_SPEAKER_ANNOUNCEMENTS_VOLUME_INCREASE_RELATIVE: Entity = Entity("number.living_room_speaker_announcements_volume_increase_relative")
NUMBER_LIVING_ROOM_SPEAKER_CROSSFADE_DURATION: Entity = Entity("number.living_room_speaker_crossfade_duration")
NUMBER_OFFICE_SPEAKER_ANNOUNCEMENTS_VOLUME_INCREASE_RELATIVE: Entity = Entity("number.office_speaker_announcements_volume_increase_relative")
NUMBER_OFFICE_SPEAKER_CROSSFADE_DURATION: Entity = Entity("number.office_speaker_crossfade_duration")
PERSISTENT_NOTIFICATION_HOMEASSISTANT_CHECK_CONFIG: Entity = Entity("persistent_notification.homeassistant_check_config")
PERSON_AMANDA: Entity = Entity("person.amanda")
PERSON_JOSE_CARLOS: Entity = Entity("person.jose_carlos")
REMOTE_SONY_KD_49XF8096: Entity = Entity("remote.sony_kd_49xf8096")
SCENE_BATHROOM_CONCENTRATE: Entity = Entity("scene.bathroom_concentrate")
SCENE_BATHROOM_NIGHTLIGHT: Entity = Entity("scene.bathroom_nightlight")
SCENE_BEDROOM_BRIGHT: Entity = Entity("scene.bedroom_bright")
SCENE_BEDROOM_CONCENTRATE: Entity = Entity("scene.bedroom_concentrate")
SCENE_BEDROOM_DIMMED: Entity = Entity("scene.bedroom_dimmed")
SCENE_BEDROOM_GENTLE_READING: Entity = Entity("scene.bedroom_gentle_reading")
SCENE_BEDROOM_NIGHTLIGHT: Entity = Entity("scene.bedroom_nightlight")
SCENE_BEDROOM_RELAXING: Entity = Entity("scene.bedroom_relaxing")
SCENE_DINING_ROOM_DINNER_TIME: Entity = Entity("scene.dining_room_dinner_time")
SCENE_FULL_BEDROOM_BRIGHT: Entity = Entity("scene.full_bedroom_bright")
SCENE_FULL_BEDROOM_LOW_LIGHT: Entity = Entity("scene.full_bedroom_low_light")
SCENE_HALLWAY_BRIGHT: Entity = Entity("scene.hallway_bright")
SCENE_HALLWAY_CONCENTRATE: Entity = Entity("scene.hallway_concentrate")
SCENE_HALLWAY_DIMMED: Entity = Entity("scene.hallway_dimmed")
SCENE_HALLWAY_NIGHTLIGHT: Entity = Entity("scene.hallway_nightlight")
SCENE_HALLWAY_TYRELL: Entity = Entity("scene.hallway_tyrell")
SCENE_HOME_CORRIDOR: Entity = Entity("scene.home_corridor")
SCENE_KITCHEN_CONCENTRATE: Entity = Entity("scene.kitchen_concentrate")
SCENE_KITCHEN_COOK: Entity = Entity("scene.kitchen_cook")
SCENE_KITCHEN_COUNTER: Entity = Entity("scene.kitchen_counter")
SCENE_KITCHEN_NIGHTLIGHT: Entity = Entity("scene.kitchen_nightlight")
SCENE_KITCHEN_TV: Entity = Entity("scene.kitchen_tv")
SCENE_LIVING_ROOM_DRUMMING: Entity = Entity("scene.living_room_drumming")
SCENE_LIVING_ROOM_GAMING: Entity = Entity("scene.living_room_gaming")
SCENE_LIVING_ROOM_MOVIE: Entity = Entity("scene.living_room_movie")
SCENE_LIVING_ROOM_READING: Entity = Entity("scene.living_room_reading")
SCENE_LIVING_ROOM_WELCOME: Entity = Entity("scene.living_room_welcome")
SCENE_STORAGE_BRIGHT: Entity = Entity("scene.storage_bright")
SCENE_STORAGE_DIMMED: Entity = Entity("scene.storage_dimmed")
SCENE_STUDIO_CONCENTRATE: Entity = Entity("scene.studio_concentrate")
SCENE_STUDIO_DRUMMING: Entity = Entity("scene.studio_drumming")
SCENE_STUDIO_WORKING: Entity = Entity("scene.studio_working")
SCENE_WARDROBE_BRIGHT: Entity = Entity("scene.wardrobe_bright")
SCENE_WARDROBE_DRESSING: Entity = Entity("scene.wardrobe_dressing")
SCENE_WARDROBE_NIGHTLIGHT: Entity = Entity("scene.wardrobe_nightlight")
SELECT_AQARA_LUMI_MOTION_AC01_APPROACH_DISTANCE: Entity = Entity("select.aqara_lumi_motion_ac01_approach_distance")
SELECT_AQARA_LUMI_MOTION_AC01_MONITORING_MODE: Entity = Entity("select.aqara_lumi_motion_ac01_monitoring_mode")
SELECT_AQARA_LUMI_MOTION_AC01_MOTION_SENSITIVITY: Entity = Entity("select.aqara_lumi_motion_ac01_motion_sensitivity")
SELECT_BEDROOM_MS_APPROACH_DISTANCE: Entity = Entity("select.bedroom_ms_approach_distance")
SELECT_BEDROOM_MS_MONITORING_MODE: Entity = Entity("select.bedroom_ms_monitoring_mode")
SELECT_BEDROOM_MS_MOTION_SENSITIVITY: Entity = Entity("select.bedroom_ms_motion_sensitivity")
SELECT_BEDROOM_SPEAKERS_CROSSFADE_MODE: Entity = Entity("select.bedroom_speakers_crossfade_mode")
SELECT_BEDROOM_SPEAKERS_REPEAT_MODE: Entity = Entity("select.bedroom_speakers_repeat_mode")
SELECT_COOKING_AREA_CROSSFADE_MODE: Entity = Entity("select.cooking_area_crossfade_mode")
SELECT_COOKING_AREA_REPEAT_MODE: Entity = Entity("select.cooking_area_repeat_mode")
SELECT_DRUMKIT_BACKLIGHT_MODE: Entity = Entity("select.drumkit_backlight_mode")
SELECT_DRUMKIT_POWER_ON_STATE: Entity = Entity("select.drumkit_power_on_state")
SELECT_HALLWAY_MS_HUE_MOTION_SENSITIVITY: Entity = Entity("select.hallway_ms_hue_motion_sensitivity")
SELECT_HOME_CROSSFADE_MODE: Entity = Entity("select.home_crossfade_mode")
SELECT_HOME_REPEAT_MODE: Entity = Entity("select.home_repeat_mode")
SELECT_KITCHEN_MS_HUE_MOTION_SENSITIVITY: Entity = Entity("select.kitchen_ms_hue_motion_sensitivity")
SELECT_LIVING_ROOM_SPEAKER_CROSSFADE_MODE: Entity = Entity("select.living_room_speaker_crossfade_mode")
SELECT_LIVING_ROOM_SPEAKER_REPEAT_MODE: Entity = Entity("select.living_room_speaker_repeat_mode")
SELECT_OFFICE_SPEAKER_CROSSFADE_MODE: Entity = Entity("select.office_speaker_crossfade_mode")
SELECT_OFFICE_SPEAKER_REPEAT_MODE: Entity = Entity("select.office_speaker_repeat_mode")
SELECT_STUDIO_MS_HUE_MOTION_SENSITIVITY: Entity = Entity("select.studio_ms_hue_motion_sensitivity")
SENSOR_AQARA_LUMI_MOTION_AC01_DEVICE_TEMPERATURE: Entity = Entity("sensor.aqara_lumi_motion_ac01_device_temperature")
SENSOR_BEDROOM_MS_DEVICE_TEMPERATURE: Entity = Entity("sensor.bedroom_ms_device_temperature")
SENSOR_DESK_CHAIR_PS_BATTERY: Entity = Entity("sensor.desk_chair_ps_battery")
SENSOR_DESK_CHAIR_PS_DEVICE_TEMPERATURE: Entity = Entity("sensor.desk_chair_ps_device_temperature")
SENSOR_DRUMKIT_ACTIVE_POWER: Entity = Entity("sensor.drumkit_active_power")
SENSOR_DRUMKIT_POWER_FACTOR: Entity = Entity("sensor.drumkit_power_factor")
SENSOR_DRUMKIT_RMS_CURRENT: Entity = Entity("sensor.drumkit_rms_current")
SENSOR_DRUMKIT_RMS_VOLTAGE: Entity = Entity("sensor.drumkit_rms_voltage")
SENSOR_DRUMKIT_SUMMATION_DELIVERED: Entity = Entity("sensor.drumkit_summation_delivered")
SENSOR_ELECTRIC_CONSUMPTION_TODAY: Entity = Entity("sensor.electric_consumption_today")
SENSOR_ELECTRIC_CONSUMPTION_YEAR_COST: Entity = Entity("sensor.electric_consumption_year_cost")
SENSOR_ELECTRIC_COST_TODAY: Entity = Entity("sensor.electric_cost_today")
SENSOR_ELECTRIC_TARIFF_RATE: Entity = Entity("sensor.electric_tariff_rate")
SENSOR_ELECTRIC_TARIFF_STANDING: Entity = Entity("sensor.electric_tariff_standing")
SENSOR_ENSUITE_DOOR_CS_BATTERY: Entity = Entity("sensor.ensuite_door_cs_battery")
SENSOR_ENSUITE_MS_BATTERY: Entity = Entity("sensor.ensuite_ms_battery")
SENSOR_FLAT_DOOR_CS_BATTERY: Entity = Entity("sensor.flat_door_cs_battery")
SENSOR_FLAT_DOOR_CS_DEVICE_TEMPERATURE: Entity = Entity("sensor.flat_door_cs_device_temperature")
SENSOR_FLICK_CURRENT_CLEAN_AREA: Entity = Entity("sensor.flick_current_clean_area")
SENSOR_FLICK_CURRENT_CLEAN_DURATION: Entity = Entity("sensor.flick_current_clean_duration")
SENSOR_FLICK_CURRENT_ERROR: Entity = Entity("sensor.flick_current_error")
SENSOR_FLICK_DND_END: Entity = Entity("sensor.flick_dnd_end")
SENSOR_FLICK_DND_START: Entity = Entity("sensor.flick_dnd_start")
SENSOR_FLICK_FILTER_LEFT: Entity = Entity("sensor.flick_filter_left")
SENSOR_FLICK_LAST_CLEAN_AREA: Entity = Entity("sensor.flick_last_clean_area")
SENSOR_FLICK_LAST_CLEAN_DURATION: Entity = Entity("sensor.flick_last_clean_duration")
SENSOR_FLICK_LAST_CLEAN_END: Entity = Entity("sensor.flick_last_clean_end")
SENSOR_FLICK_LAST_CLEAN_START: Entity = Entity("sensor.flick_last_clean_start")
SENSOR_FLICK_MAIN_BRUSH_LEFT: Entity = Entity("sensor.flick_main_brush_left")
SENSOR_FLICK_SENSOR_DIRTY_LEFT: Entity = Entity("sensor.flick_sensor_dirty_left")
SENSOR_FLICK_SIDE_BRUSH_LEFT: Entity = Entity("sensor.flick_side_brush_left")
SENSOR_FLICK_TOTAL_CLEAN_AREA: Entity = Entity("sensor.flick_total_clean_area")
SENSOR_FLICK_TOTAL_CLEAN_COUNT: Entity = Entity("sensor.flick_total_clean_count")
SENSOR_FLICK_TOTAL_DURATION: Entity = Entity("sensor.flick_total_duration")
SENSOR_FLICK_TOTAL_DUST_COLLECTION_COUNT: Entity = Entity("sensor.flick_total_dust_collection_count")
SENSOR_GALAXY_S9_BATTERY_HEALTH: Entity = Entity("sensor.galaxy_s9_battery_health")
SENSOR_GALAXY_S9_BATTERY_LEVEL: Entity = Entity("sensor.galaxy_s9_battery_level")
SENSOR_GALAXY_S9_BATTERY_POWER: Entity = Entity("sensor.galaxy_s9_battery_power")
SENSOR_GALAXY_S9_BATTERY_STATE: Entity = Entity("sensor.galaxy_s9_battery_state")
SENSOR_GALAXY_S9_BATTERY_TEMPERATURE: Entity = Entity("sensor.galaxy_s9_battery_temperature")
SENSOR_GALAXY_S9_CHARGER_TYPE: Entity = Entity("sensor.galaxy_s9_charger_type")
SENSOR_GALAXY_S9_GEOCODED_LOCATION: Entity = Entity("sensor.galaxy_s9_geocoded_location")
SENSOR_GALAXY_S9_WIFI_CONNECTION: Entity = Entity("sensor.galaxy_s9_wifi_connection")
SENSOR_HACS: Entity = Entity("sensor.hacs")
SENSOR_HALLWAY_MS_BATTERY: Entity = Entity("sensor.hallway_ms_battery")
SENSOR_HALLWAY_MS_ILLUMINANCE: Entity = Entity("sensor.hallway_ms_illuminance")
SENSOR_HALLWAY_MS_TEMPERATURE: Entity = Entity("sensor.hallway_ms_temperature")
SENSOR_HUE_DIMMER_SWITCH_1_BATTERY: Entity = Entity("sensor.hue_dimmer_switch_1_battery")
SENSOR_KITCHEN_MS_BATTERY: Entity = Entity("sensor.kitchen_ms_battery")
SENSOR_KITCHEN_MS_ILLUMINANCE: Entity = Entity("sensor.kitchen_ms_illuminance")
SENSOR_KITCHEN_MS_TEMPERATURE: Entity = Entity("sensor.kitchen_ms_temperature")
SENSOR_LUMI_LUMI_SENSOR_WLEAK_AQ1_BATTERY: Entity = Entity("sensor.lumi_lumi_sensor_wleak_aq1_battery")
SENSOR_LUMI_LUMI_SENSOR_WLEAK_AQ1_DEVICE_TEMPERATURE: Entity = Entity("sensor.lumi_lumi_sensor_wleak_aq1_device_temperature")
SENSOR_MANDIES_IPHONE_ACTIVITY: Entity = Entity("sensor.mandies_iphone_activity")
SENSOR_MANDIES_IPHONE_AVERAGE_ACTIVE_PACE: Entity = Entity("sensor.mandies_iphone_average_active_pace")
SENSOR_MANDIES_IPHONE_BATTERY_LEVEL: Entity = Entity("sensor.mandies_iphone_battery_level")
SENSOR_MANDIES_IPHONE_BATTERY_STATE: Entity = Entity("sensor.mandies_iphone_battery_state")
SENSOR_MANDIES_IPHONE_BSSID: Entity = Entity("sensor.mandies_iphone_bssid")
SENSOR_MANDIES_IPHONE_CONNECTION_TYPE: Entity = Entity("sensor.mandies_iphone_connection_type")
SENSOR_MANDIES_IPHONE_DISTANCE: Entity = Entity("sensor.mandies_iphone_distance")
SENSOR_MANDIES_IPHONE_FLOORS_ASCENDED: Entity = Entity("sensor.mandies_iphone_floors_ascended")
SENSOR_MANDIES_IPHONE_FLOORS_DESCENDED: Entity = Entity("sensor.mandies_iphone_floors_descended")
SENSOR_MANDIES_IPHONE_GEOCODED_LOCATION: Entity = Entity("sensor.mandies_iphone_geocoded_location")
SENSOR_MANDIES_IPHONE_LAST_UPDATE_TRIGGER: Entity = Entity("sensor.mandies_iphone_last_update_trigger")
SENSOR_MANDIES_IPHONE_SIM_1: Entity = Entity("sensor.mandies_iphone_sim_1")
SENSOR_MANDIES_IPHONE_SIM_2: Entity = Entity("sensor.mandies_iphone_sim_2")
SENSOR_MANDIES_IPHONE_SSID: Entity = Entity("sensor.mandies_iphone_ssid")
SENSOR_MANDIES_IPHONE_STEPS: Entity = Entity("sensor.mandies_iphone_steps")
SENSOR_MANDIES_IPHONE_STORAGE: Entity = Entity("sensor.mandies_iphone_storage")
SENSOR_SLEEPASANDROID_PHONE: Entity = Entity("sensor.sleepasandroid_phone")
SENSOR_SLEEPASANDROID_S9: Entity = Entity("sensor.sleepasandroid_s9")
SENSOR_STORAGE_DOOR_CS_BATTERY: Entity = Entity("sensor.storage_door_cs_battery")
SENSOR_STUDIO_MS_BATTERY: Entity = Entity("sensor.studio_ms_battery")
SENSOR_STUDIO_MS_ILLUMINANCE: Entity = Entity("sensor.studio_ms_illuminance")
SENSOR_STUDIO_MS_TEMPERATURE: Entity = Entity("sensor.studio_ms_temperature")
SENSOR_VODAFONE_WI_FI_HUB_EXTERNAL_IP: Entity = Entity("sensor.vodafone_wi_fi_hub_external_ip")
SENSOR_VODAFONE_WI_FI_HUB_KIB_S_RECEIVED: Entity = Entity("sensor.vodafone_wi_fi_hub_kib_s_received")
SENSOR_VODAFONE_WI_FI_HUB_KIB_S_SENT: Entity = Entity("sensor.vodafone_wi_fi_hub_kib_s_sent")
SENSOR_WARDROBE_DOOR_LEFT_CS_BATTERY: Entity = Entity("sensor.wardrobe_door_left_cs_battery")
SENSOR_WARDROBE_DOOR_RIGHT_CS_BATTERY: Entity = Entity("sensor.wardrobe_door_right_cs_battery")
SUN_SUN: Entity = Entity("sun.sun")
SWITCH_BEDROOM_SPEAKERS_SHUFFLE_ENABLED: Entity = Entity("switch.bedroom_speakers_shuffle_enabled")
SWITCH_BEDSIDE_2: Entity = Entity("switch.bedside_2")
SWITCH_COOKING_AREA_SHUFFLE_ENABLED: Entity = Entity("switch.cooking_area_shuffle_enabled")
SWITCH_DRUMKIT: Entity = Entity("switch.drumkit")
SWITCH_DRUMKIT_CHILD_LOCK: Entity = Entity("switch.drumkit_child_lock")
SWITCH_DYSON: Entity = Entity("switch.dyson")
SWITCH_HOME_SHUFFLE_ENABLED: Entity = Entity("switch.home_shuffle_enabled")
SWITCH_LIVING_ROOM_SPEAKER_SHUFFLE_ENABLED: Entity = Entity("switch.living_room_speaker_shuffle_enabled")
SWITCH_MONITOR: Entity = Entity("switch.monitor")
SWITCH_OFFICE_SPEAKER_SHUFFLE_ENABLED: Entity = Entity("switch.office_speaker_shuffle_enabled")
UPDATE_APPDAEMON_UPDATE: Entity = Entity("update.appdaemon_update")
UPDATE_CLOUDFLARED_UPDATE: Entity = Entity("update.cloudflared_update")
UPDATE_HOME_ASSISTANT_CORE_UPDATE: Entity = Entity("update.home_assistant_core_update")
UPDATE_HOME_ASSISTANT_OPERATING_SYSTEM_UPDATE: Entity = Entity("update.home_assistant_operating_system_update")
UPDATE_HOME_ASSISTANT_SUPERVISOR_UPDATE: Entity = Entity("update.home_assistant_supervisor_update")
UPDATE_MOSQUITTO_BROKER_UPDATE: Entity = Entity("update.mosquitto_broker_update")
UPDATE_STUDIO_CODE_SERVER_UPDATE: Entity = Entity("update.studio_code_server_update")
UPDATE_TERMINAL_SSH_UPDATE: Entity = Entity("update.terminal_ssh_update")
VACUUM_FLICK: Entity = Entity("vacuum.flick")
WEATHER_FORECAST_MARSH_COURT: Entity = Entity("weather.forecast_marsh_court")
ZONE_HOME: Entity = Entity("zone.home")
