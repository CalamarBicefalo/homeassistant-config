from typing import NewType
Entity = NewType('Entity', str)
BINARY_SENSOR_BEDROOM_INSTANT_MS: Entity = Entity("binary_sensor.bedroom_instant_ms")
BINARY_SENSOR_BEDROOM_MOTION: Entity = Entity("binary_sensor.bedroom_motion")
BINARY_SENSOR_BEDROOM_MS_OCCUPANCY: Entity = Entity("binary_sensor.bedroom_ms_occupancy")
BINARY_SENSOR_DESK_CHAIR_PS: Entity = Entity("binary_sensor.desk_chair_ps")
BINARY_SENSOR_ENSUITE_DOOR_CS: Entity = Entity("binary_sensor.ensuite_door_cs")
BINARY_SENSOR_ENSUITE_MOTION: Entity = Entity("binary_sensor.ensuite_motion")
BINARY_SENSOR_ENSUITE_MS: Entity = Entity("binary_sensor.ensuite_ms")
BINARY_SENSOR_FLAT_DOOR_CS: Entity = Entity("binary_sensor.flat_door_cs")
BINARY_SENSOR_HALLWAY_MS_OCCUPANCY: Entity = Entity("binary_sensor.hallway_ms_occupancy")
BINARY_SENSOR_KITCHEN_MOTION: Entity = Entity("binary_sensor.kitchen_motion")
BINARY_SENSOR_KITCHEN_MS_OCCUPANCY: Entity = Entity("binary_sensor.kitchen_ms_occupancy")
BINARY_SENSOR_LIVING_ROOM_INSTANT_MS: Entity = Entity("binary_sensor.living_room_instant_ms")
BINARY_SENSOR_LIVING_ROOM_MOTION: Entity = Entity("binary_sensor.living_room_motion")
BINARY_SENSOR_LIVING_ROOM_MS_OCCUPANCY: Entity = Entity("binary_sensor.living_room_ms_occupancy")
BINARY_SENSOR_LUMI_LUMI_SENSOR_WLEAK_AQ1_MOISTURE: Entity = Entity("binary_sensor.lumi_lumi_sensor_wleak_aq1_moisture")
BINARY_SENSOR_SNYK_LAPTOP_ACTIVE: Entity = Entity("binary_sensor.snyk_laptop_active")
BINARY_SENSOR_SNYK_LAPTOP_AUDIO_INPUT_IN_USE: Entity = Entity("binary_sensor.snyk_laptop_audio_input_in_use")
BINARY_SENSOR_SNYK_LAPTOP_AUDIO_OUTPUT_IN_USE: Entity = Entity("binary_sensor.snyk_laptop_audio_output_in_use")
BINARY_SENSOR_SNYK_LAPTOP_CAMERA_IN_USE: Entity = Entity("binary_sensor.snyk_laptop_camera_in_use")
BINARY_SENSOR_SNYK_LAPTOP_FOCUS: Entity = Entity("binary_sensor.snyk_laptop_focus")
BINARY_SENSOR_SOFA_PS: Entity = Entity("binary_sensor.sofa_ps")
BINARY_SENSOR_STORAGE_DOOR_CS: Entity = Entity("binary_sensor.storage_door_cs")
BINARY_SENSOR_STUDIO_MOTION: Entity = Entity("binary_sensor.studio_motion")
BINARY_SENSOR_STUDIO_MS_OCCUPANCY: Entity = Entity("binary_sensor.studio_ms_occupancy")
BINARY_SENSOR_VODAFONE_WI_FI_HUB_WAN_STATUS: Entity = Entity("binary_sensor.vodafone_wi_fi_hub_wan_status")
BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE: Entity = Entity("binary_sensor.wardrobe_door_left_cs_iaszone")
BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE: Entity = Entity("binary_sensor.wardrobe_door_right_cs_iaszone")
BINARY_SENSOR_WARDROBE_MIDDLE_DOOR: Entity = Entity("binary_sensor.wardrobe_middle_door")
BINARY_SENSOR_WARDROBE_MS_MOTION: Entity = Entity("binary_sensor.wardrobe_ms_motion")
BUTTON_AIR_QUALITY_IDENTIFY: Entity = Entity("button.air_quality_identify")
BUTTON_AQARA_LUMI_MOTION_AC01_PRESENCE_STATUS_RESET: Entity = Entity("button.aqara_lumi_motion_ac01_presence_status_reset")
BUTTON_BEDROOM_MS_PRESENCE_STATUS_RESET: Entity = Entity("button.bedroom_ms_presence_status_reset")
BUTTON_COFFEE_TABLE_BUTTON_IDENTIFY: Entity = Entity("button.coffee_table_button_identify")
BUTTON_KITCHEN_MS_IDENTIFY: Entity = Entity("button.kitchen_ms_identify")
BUTTON_LUMI_LUMI_SENSOR_WLEAK_AQ1_IDENTIFY_2: Entity = Entity("button.lumi_lumi_sensor_wleak_aq1_identify_2")
BUTTON_MEDIA_CONTROLLER_IDENTIFY: Entity = Entity("button.media_controller_identify")
BUTTON_SIGNAL_REPEATER_IDENTIFY: Entity = Entity("button.signal_repeater_identify")
BUTTON_SONY_KD_49XF8096_REBOOT: Entity = Entity("button.sony_kd_49xf8096_reboot")
BUTTON_SONY_KD_49XF8096_TERMINATE_APPS: Entity = Entity("button.sony_kd_49xf8096_terminate_apps")
BUTTON_SYNCHRONIZE_DEVICES: Entity = Entity("button.synchronize_devices")
BUTTON_THERMOMIX_IDENTIFY: Entity = Entity("button.thermomix_identify")
BUTTON_WARDROBE_MIDDLE_DOOR_IDENTIFY: Entity = Entity("button.wardrobe_middle_door_identify")
COVER_BEDROOM_CURTAIN_COVER: Entity = Entity("cover.bedroom_curtain_cover")
COVER_BLINDS_CURTAIN: Entity = Entity("cover.blinds_curtain")
DEVICE_TRACKER_MANDIES_IPHONE: Entity = Entity("device_tracker.mandies_iphone")
DEVICE_TRACKER_SM_S918B: Entity = Entity("device_tracker.sm_s918b")
DEVICE_TRACKER_SNYK_LAPTOP: Entity = Entity("device_tracker.snyk_laptop")
INPUT_BOOLEAN_GUEST_MODE: Entity = Entity("input_boolean.guest_mode")
INPUT_DATETIME_LAST_CLEANED_BEDROOM: Entity = Entity("input_datetime.last_cleaned_bedroom")
INPUT_DATETIME_LAST_CLEANED_ENSUITE: Entity = Entity("input_datetime.last_cleaned_ensuite")
INPUT_DATETIME_LAST_CLEANED_FLAT: Entity = Entity("input_datetime.last_cleaned_flat")
INPUT_DATETIME_LAST_CLEANED_HALLWAY: Entity = Entity("input_datetime.last_cleaned_hallway")
INPUT_DATETIME_LAST_CLEANED_KITCHEN: Entity = Entity("input_datetime.last_cleaned_kitchen")
INPUT_DATETIME_LAST_CLEANED_LIVING_ROOM: Entity = Entity("input_datetime.last_cleaned_living_room")
INPUT_DATETIME_LAST_CLEANED_STORAGE_ROOM: Entity = Entity("input_datetime.last_cleaned_storage_room")
INPUT_DATETIME_LAST_CLEANED_STUDIO: Entity = Entity("input_datetime.last_cleaned_studio")
INPUT_DATETIME_LAST_CLEANED_VACUUM_MOP: Entity = Entity("input_datetime.last_cleaned_vacuum_mop")
INPUT_DATETIME_LAST_CLEANED_WARDROBE: Entity = Entity("input_datetime.last_cleaned_wardrobe")
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
LIGHT_BALCONY: Entity = Entity("light.balcony")
LIGHT_BATHROOM: Entity = Entity("light.bathroom")
LIGHT_BEDROOM: Entity = Entity("light.bedroom")
LIGHT_DINING_ROOM: Entity = Entity("light.dining_room")
LIGHT_FULL_LIVING_ROOM: Entity = Entity("light.full_living_room")
LIGHT_HALLWAY: Entity = Entity("light.hallway")
LIGHT_HOME: Entity = Entity("light.home")
LIGHT_HUE_WHITE_LAMP_1: Entity = Entity("light.hue_white_lamp_1")
LIGHT_KITCHEN: Entity = Entity("light.kitchen")
LIGHT_LIVING_ROOM: Entity = Entity("light.living_room")
LIGHT_STORAGE: Entity = Entity("light.storage")
LIGHT_STUDIO: Entity = Entity("light.studio")
LIGHT_WARDROBE: Entity = Entity("light.wardrobe")
MEDIA_PLAYER_BEDROOM_SPEAKER_L_2: Entity = Entity("media_player.bedroom_speaker_l_2")
MEDIA_PLAYER_BEDROOM_SPEAKER_R_2: Entity = Entity("media_player.bedroom_speaker_r_2")
MEDIA_PLAYER_BEDROOM_SPEAKERS_2: Entity = Entity("media_player.bedroom_speakers_2")
MEDIA_PLAYER_COOKING_AREA_2: Entity = Entity("media_player.cooking_area_2")
MEDIA_PLAYER_HALLWAY_SPEAKER_2: Entity = Entity("media_player.hallway_speaker_2")
MEDIA_PLAYER_HOME_2: Entity = Entity("media_player.home_2")
MEDIA_PLAYER_KITCHEN_SPEAKER_2: Entity = Entity("media_player.kitchen_speaker_2")
MEDIA_PLAYER_LIVING_ROOM_SPEAKER_2: Entity = Entity("media_player.living_room_speaker_2")
MEDIA_PLAYER_OFFICE_SPEAKER_2: Entity = Entity("media_player.office_speaker_2")
MEDIA_PLAYER_SONY_KD_49XF8096: Entity = Entity("media_player.sony_kd_49xf8096")
MEDIA_PLAYER_TV_2: Entity = Entity("media_player.tv_2")
MEDIA_PLAYER_TV_3: Entity = Entity("media_player.tv_3")
NUMBER_FLICK_VOLUME: Entity = Entity("number.flick_volume")
PERSON_JOSE_CARLOS: Entity = Entity("person.jose_carlos")
REMOTE_SONY_KD_49XF8096: Entity = Entity("remote.sony_kd_49xf8096")
REMOTE_TV: Entity = Entity("remote.tv")
SCENE_BATHROOM_CONCENTRATE: Entity = Entity("scene.bathroom_concentrate")
SCENE_BATHROOM_NIGHTLIGHT: Entity = Entity("scene.bathroom_nightlight")
SCENE_BEDROOM_BRIGHT: Entity = Entity("scene.bedroom_bright")
SCENE_BEDROOM_CONCENTRATE: Entity = Entity("scene.bedroom_concentrate")
SCENE_BEDROOM_DIMMED: Entity = Entity("scene.bedroom_dimmed")
SCENE_BEDROOM_GENTLE_READING: Entity = Entity("scene.bedroom_gentle_reading")
SCENE_BEDROOM_NIGHTLIGHT: Entity = Entity("scene.bedroom_nightlight")
SCENE_BEDROOM_RELAXING: Entity = Entity("scene.bedroom_relaxing")
SCENE_BEDROOM_WARM_EMBRACE: Entity = Entity("scene.bedroom_warm_embrace")
SCENE_DINING_ROOM_DINNER_TIME: Entity = Entity("scene.dining_room_dinner_time")
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
SELECT_DRUMKIT_BACKLIGHT_MODE: Entity = Entity("select.drumkit_backlight_mode")
SELECT_DRUMKIT_POWER_ON_STATE: Entity = Entity("select.drumkit_power_on_state")
SELECT_FLICK_MOP_INTENSITY: Entity = Entity("select.flick_mop_intensity")
SELECT_FLICK_MOP_MODE: Entity = Entity("select.flick_mop_mode")
SELECT_HALLWAY_MS_HUE_MOTION_SENSITIVITY: Entity = Entity("select.hallway_ms_hue_motion_sensitivity")
SELECT_KITCHEN_MS_HUE_MOTION_SENSITIVITY: Entity = Entity("select.kitchen_ms_hue_motion_sensitivity")
SELECT_STUDIO_MS_HUE_MOTION_SENSITIVITY: Entity = Entity("select.studio_ms_hue_motion_sensitivity")
SENSOR_AIR_QUALITY_HUMIDITY: Entity = Entity("sensor.air_quality_humidity")
SENSOR_AIR_QUALITY_PARTICULATE_MATTER: Entity = Entity("sensor.air_quality_particulate_matter")
SENSOR_AIR_QUALITY_TEMPERATURE: Entity = Entity("sensor.air_quality_temperature")
SENSOR_AQARA_LUMI_MOTION_AC01_DEVICE_TEMPERATURE: Entity = Entity("sensor.aqara_lumi_motion_ac01_device_temperature")
SENSOR_BEDROOM_BUTTON_BATTERY: Entity = Entity("sensor.bedroom_button_battery")
SENSOR_BEDROOM_MS_COMMAND: Entity = Entity("sensor.bedroom_ms_command")
SENSOR_BEDROOM_MS_DEVICE_TEMPERATURE: Entity = Entity("sensor.bedroom_ms_device_temperature")
SENSOR_BLINDS_LAST_OPERATION_DURATION: Entity = Entity("sensor.blinds_last_operation_duration")
SENSOR_COFFEE_TABLE_BUTTON_BATTERY: Entity = Entity("sensor.coffee_table_button_battery")
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
SENSOR_ENSUITE_DOOR_CS_DEVICE_TEMERATURE: Entity = Entity("sensor.ensuite_door_cs_device_temerature")
SENSOR_ENSUITE_MS_BATTERY: Entity = Entity("sensor.ensuite_ms_battery")
SENSOR_FLAT_DOOR_CS_BATTERY: Entity = Entity("sensor.flat_door_cs_battery")
SENSOR_FLAT_DOOR_CS_DEVICE_TEMPERATURE: Entity = Entity("sensor.flat_door_cs_device_temperature")
SENSOR_FLICK_BATTERY: Entity = Entity("sensor.flick_battery")
SENSOR_FLICK_CLEANING_AREA: Entity = Entity("sensor.flick_cleaning_area")
SENSOR_FLICK_CLEANING_TIME: Entity = Entity("sensor.flick_cleaning_time")
SENSOR_FLICK_FILTER_TIME_LEFT: Entity = Entity("sensor.flick_filter_time_left")
SENSOR_FLICK_MAIN_BRUSH_TIME_LEFT: Entity = Entity("sensor.flick_main_brush_time_left")
SENSOR_FLICK_SENSOR_TIME_LEFT: Entity = Entity("sensor.flick_sensor_time_left")
SENSOR_FLICK_SIDE_BRUSH_TIME_LEFT: Entity = Entity("sensor.flick_side_brush_time_left")
SENSOR_FLICK_STATUS: Entity = Entity("sensor.flick_status")
SENSOR_FLICK_TOTAL_CLEANING_AREA: Entity = Entity("sensor.flick_total_cleaning_area")
SENSOR_FLICK_TOTAL_CLEANING_TIME: Entity = Entity("sensor.flick_total_cleaning_time")
SENSOR_FLICK_VACUUM_ERROR: Entity = Entity("sensor.flick_vacuum_error")
SENSOR_HACS: Entity = Entity("sensor.hacs")
SENSOR_HALLWAY_MS_BATTERY: Entity = Entity("sensor.hallway_ms_battery")
SENSOR_HALLWAY_MS_ILLUMINANCE: Entity = Entity("sensor.hallway_ms_illuminance")
SENSOR_HALLWAY_MS_TEMPERATURE: Entity = Entity("sensor.hallway_ms_temperature")
SENSOR_KITCHEN_MS_BATTERY: Entity = Entity("sensor.kitchen_ms_battery")
SENSOR_KITCHEN_MS_ILLUMINANCE: Entity = Entity("sensor.kitchen_ms_illuminance")
SENSOR_KITCHEN_MS_TEMPERATURE: Entity = Entity("sensor.kitchen_ms_temperature")
SENSOR_LIVING_ROOM_MS_COMMAND: Entity = Entity("sensor.living_room_ms_command")
SENSOR_LUMI_LUMI_SENSOR_WLEAK_AQ1_BATTERY: Entity = Entity("sensor.lumi_lumi_sensor_wleak_aq1_battery")
SENSOR_LUMI_LUMI_SENSOR_WLEAK_AQ1_BATTERY_2: Entity = Entity("sensor.lumi_lumi_sensor_wleak_aq1_battery_2")
SENSOR_LUMI_LUMI_SENSOR_WLEAK_AQ1_DEVICE_TEMPERATURE: Entity = Entity("sensor.lumi_lumi_sensor_wleak_aq1_device_temperature")
SENSOR_LUMI_LUMI_SENSOR_WLEAK_AQ1_DEVICE_TEMPERATURE_2: Entity = Entity("sensor.lumi_lumi_sensor_wleak_aq1_device_temperature_2")
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
SENSOR_MEDIA_CONTROLLER_BATTERY: Entity = Entity("sensor.media_controller_battery")
SENSOR_SLEEPASANDROID_PHONE: Entity = Entity("sensor.sleepasandroid_phone")
SENSOR_SM_S918B_BATTERY_LEVEL: Entity = Entity("sensor.sm_s918b_battery_level")
SENSOR_SM_S918B_BATTERY_STATE: Entity = Entity("sensor.sm_s918b_battery_state")
SENSOR_SM_S918B_CHARGER_TYPE: Entity = Entity("sensor.sm_s918b_charger_type")
SENSOR_SNYK_LAPTOP_ACTIVE_AUDIO_INPUT: Entity = Entity("sensor.snyk_laptop_active_audio_input")
SENSOR_SNYK_LAPTOP_ACTIVE_AUDIO_OUTPUT: Entity = Entity("sensor.snyk_laptop_active_audio_output")
SENSOR_SNYK_LAPTOP_ACTIVE_CAMERA: Entity = Entity("sensor.snyk_laptop_active_camera")
SENSOR_SNYK_LAPTOP_BSSID: Entity = Entity("sensor.snyk_laptop_bssid")
SENSOR_SNYK_LAPTOP_CONNECTION_TYPE: Entity = Entity("sensor.snyk_laptop_connection_type")
SENSOR_SNYK_LAPTOP_DISPLAYS: Entity = Entity("sensor.snyk_laptop_displays")
SENSOR_SNYK_LAPTOP_FRONTMOST_APP: Entity = Entity("sensor.snyk_laptop_frontmost_app")
SENSOR_SNYK_LAPTOP_GEOCODED_LOCATION: Entity = Entity("sensor.snyk_laptop_geocoded_location")
SENSOR_SNYK_LAPTOP_INTERNAL_BATTERY_LEVEL: Entity = Entity("sensor.snyk_laptop_internal_battery_level")
SENSOR_SNYK_LAPTOP_INTERNAL_BATTERY_STATE: Entity = Entity("sensor.snyk_laptop_internal_battery_state")
SENSOR_SNYK_LAPTOP_LAST_UPDATE_TRIGGER: Entity = Entity("sensor.snyk_laptop_last_update_trigger")
SENSOR_SNYK_LAPTOP_PRIMARY_DISPLAY_ID: Entity = Entity("sensor.snyk_laptop_primary_display_id")
SENSOR_SNYK_LAPTOP_PRIMARY_DISPLAY_NAME: Entity = Entity("sensor.snyk_laptop_primary_display_name")
SENSOR_SNYK_LAPTOP_SSID: Entity = Entity("sensor.snyk_laptop_ssid")
SENSOR_SNYK_LAPTOP_STORAGE: Entity = Entity("sensor.snyk_laptop_storage")
SENSOR_STORAGE_DOOR_CS_BATTERY: Entity = Entity("sensor.storage_door_cs_battery")
SENSOR_STORAGE_DOOR_CS_TEMPERATURE: Entity = Entity("sensor.storage_door_cs_temperature")
SENSOR_STUDIO_MS_BATTERY: Entity = Entity("sensor.studio_ms_battery")
SENSOR_STUDIO_MS_ILLUMINANCE: Entity = Entity("sensor.studio_ms_illuminance")
SENSOR_STUDIO_MS_TEMPERATURE: Entity = Entity("sensor.studio_ms_temperature")
SENSOR_SUN_NEXT_DAWN: Entity = Entity("sensor.sun_next_dawn")
SENSOR_SUN_NEXT_DUSK: Entity = Entity("sensor.sun_next_dusk")
SENSOR_SUN_NEXT_MIDNIGHT: Entity = Entity("sensor.sun_next_midnight")
SENSOR_SUN_NEXT_NOON: Entity = Entity("sensor.sun_next_noon")
SENSOR_SUN_NEXT_RISING: Entity = Entity("sensor.sun_next_rising")
SENSOR_SUN_NEXT_SETTING: Entity = Entity("sensor.sun_next_setting")
SENSOR_THERMOMIX_INSTANTANEOUS_DEMAND: Entity = Entity("sensor.thermomix_instantaneous_demand")
SENSOR_THERMOMIX_SUMMATION_DELIVERED: Entity = Entity("sensor.thermomix_summation_delivered")
SENSOR_THERMOMIX_TEMPERATURE: Entity = Entity("sensor.thermomix_temperature")
SENSOR_VODAFONE_WI_FI_HUB_EXTERNAL_IP: Entity = Entity("sensor.vodafone_wi_fi_hub_external_ip")
SENSOR_VODAFONE_WI_FI_HUB_KIB_S_RECEIVED: Entity = Entity("sensor.vodafone_wi_fi_hub_kib_s_received")
SENSOR_VODAFONE_WI_FI_HUB_KIB_S_SENT: Entity = Entity("sensor.vodafone_wi_fi_hub_kib_s_sent")
SENSOR_WARDROBE_DOOR_LEFT_CS_BATTERY: Entity = Entity("sensor.wardrobe_door_left_cs_battery")
SENSOR_WARDROBE_DOOR_RIGHT_CS_BATTERY: Entity = Entity("sensor.wardrobe_door_right_cs_battery")
SENSOR_WARDROBE_MIDDLE_DOOR_BATTERY: Entity = Entity("sensor.wardrobe_middle_door_battery")
SENSOR_WARDROBE_MS_BATTERY: Entity = Entity("sensor.wardrobe_ms_battery")
SUN_SUN: Entity = Entity("sun.sun")
SWITCH_BLINDS_REVERSE: Entity = Entity("switch.blinds_reverse")
SWITCH_DRUMKIT: Entity = Entity("switch.drumkit")
SWITCH_DRUMKIT_CHILD_LOCK: Entity = Entity("switch.drumkit_child_lock")
SWITCH_FLICK_CHILD_LOCK: Entity = Entity("switch.flick_child_lock")
SWITCH_FLICK_DO_NOT_DISTURB: Entity = Entity("switch.flick_do_not_disturb")
SWITCH_FLICK_STATUS_INDICATOR_LIGHT: Entity = Entity("switch.flick_status_indicator_light")
SWITCH_MONITOR: Entity = Entity("switch.monitor")
SWITCH_THERMOMIX_SWITCH: Entity = Entity("switch.thermomix_switch")
TIME_FLICK_DO_NOT_DISTURB_BEGIN: Entity = Entity("time.flick_do_not_disturb_begin")
TIME_FLICK_DO_NOT_DISTURB_END: Entity = Entity("time.flick_do_not_disturb_end")
UPDATE_APPDAEMON_UPDATE: Entity = Entity("update.appdaemon_update")
UPDATE_CLOUDFLARED_UPDATE: Entity = Entity("update.cloudflared_update")
UPDATE_HOME_ASSISTANT_CORE_UPDATE: Entity = Entity("update.home_assistant_core_update")
UPDATE_HOME_ASSISTANT_OPERATING_SYSTEM_UPDATE: Entity = Entity("update.home_assistant_operating_system_update")
UPDATE_HOME_ASSISTANT_SUPERVISOR_UPDATE: Entity = Entity("update.home_assistant_supervisor_update")
UPDATE_MOSQUITTO_BROKER_UPDATE: Entity = Entity("update.mosquitto_broker_update")
UPDATE_MUSIC_ASSISTANT_BETA_UPDATE: Entity = Entity("update.music_assistant_beta_update")
UPDATE_STUDIO_CODE_SERVER_UPDATE: Entity = Entity("update.studio_code_server_update")
UPDATE_TERMINAL_SSH_UPDATE: Entity = Entity("update.terminal_ssh_update")
VACUUM_FLICK: Entity = Entity("vacuum.flick")
WEATHER_FORECAST_MARSH_COURT: Entity = Entity("weather.forecast_marsh_court")
ZONE_HOME: Entity = Entity("zone.home")
