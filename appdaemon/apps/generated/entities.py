from typing import NewType
Entity = NewType('Entity', str)
AUTOMATION_BATTERY_CHECKER: Entity = Entity("automation.battery_checker")
AUTOMATION_TEST: Entity = Entity("automation.test")
BINARY_SENSOR_ACTIVITY_BATHROOM_EMPTY: Entity = Entity("binary_sensor.activity_bathroom_empty")
BINARY_SENSOR_ACTIVITY_BATHROOM_PRESENT: Entity = Entity("binary_sensor.activity_bathroom_present")
BINARY_SENSOR_ACTIVITY_BEDROOM_BEDTIME: Entity = Entity("binary_sensor.activity_bedroom_bedtime")
BINARY_SENSOR_ACTIVITY_BEDROOM_EMPTY: Entity = Entity("binary_sensor.activity_bedroom_empty")
BINARY_SENSOR_ACTIVITY_BEDROOM_PRESENT: Entity = Entity("binary_sensor.activity_bedroom_present")
BINARY_SENSOR_ACTIVITY_BEDROOM_RELAXING: Entity = Entity("binary_sensor.activity_bedroom_relaxing")
BINARY_SENSOR_ACTIVITY_BEDROOM_WAKING_UP: Entity = Entity("binary_sensor.activity_bedroom_waking_up")
BINARY_SENSOR_ACTIVITY_DINING_ROOM_DINING: Entity = Entity("binary_sensor.activity_dining_room_dining")
BINARY_SENSOR_ACTIVITY_DINING_ROOM_EMPTY: Entity = Entity("binary_sensor.activity_dining_room_empty")
BINARY_SENSOR_ACTIVITY_DINING_ROOM_PRESENT: Entity = Entity("binary_sensor.activity_dining_room_present")
BINARY_SENSOR_ACTIVITY_ENSUITE_EMPTY: Entity = Entity("binary_sensor.activity_ensuite_empty")
BINARY_SENSOR_ACTIVITY_ENSUITE_PRESENT: Entity = Entity("binary_sensor.activity_ensuite_present")
BINARY_SENSOR_ACTIVITY_ENSUITE_SHOWERING: Entity = Entity("binary_sensor.activity_ensuite_showering")
BINARY_SENSOR_ACTIVITY_HALLWAY_EMPTY: Entity = Entity("binary_sensor.activity_hallway_empty")
BINARY_SENSOR_ACTIVITY_HALLWAY_PRESENT: Entity = Entity("binary_sensor.activity_hallway_present")
BINARY_SENSOR_ACTIVITY_KITCHEN_COOKING: Entity = Entity("binary_sensor.activity_kitchen_cooking")
BINARY_SENSOR_ACTIVITY_KITCHEN_EMPTY: Entity = Entity("binary_sensor.activity_kitchen_empty")
BINARY_SENSOR_ACTIVITY_KITCHEN_PRESENT: Entity = Entity("binary_sensor.activity_kitchen_present")
BINARY_SENSOR_ACTIVITY_KITCHEN_TV_BREAK: Entity = Entity("binary_sensor.activity_kitchen_tv_break")
BINARY_SENSOR_ACTIVITY_LIVING_ROOM_DINING: Entity = Entity("binary_sensor.activity_living_room_dining")
BINARY_SENSOR_ACTIVITY_LIVING_ROOM_DRUMMING: Entity = Entity("binary_sensor.activity_living_room_drumming")
BINARY_SENSOR_ACTIVITY_LIVING_ROOM_EMPTY: Entity = Entity("binary_sensor.activity_living_room_empty")
BINARY_SENSOR_ACTIVITY_LIVING_ROOM_GAMING: Entity = Entity("binary_sensor.activity_living_room_gaming")
BINARY_SENSOR_ACTIVITY_LIVING_ROOM_PRESENT: Entity = Entity("binary_sensor.activity_living_room_present")
BINARY_SENSOR_ACTIVITY_LIVING_ROOM_RELAXING: Entity = Entity("binary_sensor.activity_living_room_relaxing")
BINARY_SENSOR_ACTIVITY_LIVING_ROOM_WATCHING_TV: Entity = Entity("binary_sensor.activity_living_room_watching_tv")
BINARY_SENSOR_ACTIVITY_OFFICE_EMPTY: Entity = Entity("binary_sensor.activity_office_empty")
BINARY_SENSOR_ACTIVITY_OFFICE_PRESENT: Entity = Entity("binary_sensor.activity_office_present")
BINARY_SENSOR_ACTIVITY_STORAGE_EMPTY: Entity = Entity("binary_sensor.activity_storage_empty")
BINARY_SENSOR_ACTIVITY_STORAGE_PRESENT: Entity = Entity("binary_sensor.activity_storage_present")
BINARY_SENSOR_ACTIVITY_STUDIO_DRUMMING: Entity = Entity("binary_sensor.activity_studio_drumming")
BINARY_SENSOR_ACTIVITY_STUDIO_EMPTY: Entity = Entity("binary_sensor.activity_studio_empty")
BINARY_SENSOR_ACTIVITY_STUDIO_MEETING: Entity = Entity("binary_sensor.activity_studio_meeting")
BINARY_SENSOR_ACTIVITY_STUDIO_PRESENT: Entity = Entity("binary_sensor.activity_studio_present")
BINARY_SENSOR_ACTIVITY_STUDIO_WORKING: Entity = Entity("binary_sensor.activity_studio_working")
BINARY_SENSOR_ACTIVITY_WARDROBE_DRESSING: Entity = Entity("binary_sensor.activity_wardrobe_dressing")
BINARY_SENSOR_ACTIVITY_WARDROBE_EMPTY: Entity = Entity("binary_sensor.activity_wardrobe_empty")
BINARY_SENSOR_ACTIVITY_WARDROBE_PRESENT: Entity = Entity("binary_sensor.activity_wardrobe_present")
BINARY_SENSOR_BEDROOM_INSTANT_MS: Entity = Entity("binary_sensor.bedroom_instant_ms")
BINARY_SENSOR_BEDROOM_MOTION: Entity = Entity("binary_sensor.bedroom_motion")
BINARY_SENSOR_BEDROOM_MS_OCCUPANCY: Entity = Entity("binary_sensor.bedroom_ms_occupancy")
BINARY_SENSOR_DESK: Entity = Entity("binary_sensor.desk")
BINARY_SENSOR_DESK_CHAIR_PS: Entity = Entity("binary_sensor.desk_chair_ps")
BINARY_SENSOR_ENSUITE_DOOR_CS: Entity = Entity("binary_sensor.ensuite_door_cs")
BINARY_SENSOR_ENSUITE_MOTION: Entity = Entity("binary_sensor.ensuite_motion")
BINARY_SENSOR_ENSUITE_MS: Entity = Entity("binary_sensor.ensuite_ms")
BINARY_SENSOR_ESPRESENSE_54B85F_CONNECTIVITY: Entity = Entity("binary_sensor.espresense_54b85f_connectivity")
BINARY_SENSOR_ESPRESENSE_LIVING_ROOM_CONNECTIVITY: Entity = Entity("binary_sensor.espresense_living_room_connectivity")
BINARY_SENSOR_FLAT_DOOR_CS: Entity = Entity("binary_sensor.flat_door_cs")
BINARY_SENSOR_FLICK_CLEANING: Entity = Entity("binary_sensor.flick_cleaning")
BINARY_SENSOR_FLICK_MOP_ATTACHED: Entity = Entity("binary_sensor.flick_mop_attached")
BINARY_SENSOR_FLICK_WATER_BOX_ATTACHED: Entity = Entity("binary_sensor.flick_water_box_attached")
BINARY_SENSOR_FLICK_WATER_SHORTAGE: Entity = Entity("binary_sensor.flick_water_shortage")
BINARY_SENSOR_HALLWAY_MS_MOTION: Entity = Entity("binary_sensor.hallway_ms_motion")
BINARY_SENSOR_JOSE_CARLOSS_IPAD_FOCUS: Entity = Entity("binary_sensor.jose_carloss_ipad_focus")
BINARY_SENSOR_KITCHEN_ALL_MS: Entity = Entity("binary_sensor.kitchen_all_ms")
BINARY_SENSOR_KITCHEN_COOKING_AREA_MS: Entity = Entity("binary_sensor.kitchen_cooking_area_ms")
BINARY_SENSOR_KITCHEN_FRIDGE_MS: Entity = Entity("binary_sensor.kitchen_fridge_ms")
BINARY_SENSOR_KITCHEN_MOTION: Entity = Entity("binary_sensor.kitchen_motion")
BINARY_SENSOR_KITCHEN_MS_MOTION: Entity = Entity("binary_sensor.kitchen_ms_motion")
BINARY_SENSOR_LIVING_ROOM_ALL_MS: Entity = Entity("binary_sensor.living_room_all_ms")
BINARY_SENSOR_LIVING_ROOM_DINING_TABLE_MS: Entity = Entity("binary_sensor.living_room_dining_table_ms")
BINARY_SENSOR_LIVING_ROOM_ENTRANCE_MS: Entity = Entity("binary_sensor.living_room_entrance_ms")
BINARY_SENSOR_LIVING_ROOM_INSTANT_MS: Entity = Entity("binary_sensor.living_room_instant_ms")
BINARY_SENSOR_LIVING_ROOM_MOTION: Entity = Entity("binary_sensor.living_room_motion")
BINARY_SENSOR_LIVING_ROOM_MS_OCCUPANCY: Entity = Entity("binary_sensor.living_room_ms_occupancy")
BINARY_SENSOR_LIVING_ROOM_SOFA_MS: Entity = Entity("binary_sensor.living_room_sofa_ms")
BINARY_SENSOR_LUMI_LUMI_SENSOR_WLEAK_AQ1_MOISTURE: Entity = Entity("binary_sensor.lumi_lumi_sensor_wleak_aq1_moisture")
BINARY_SENSOR_PRESENCE_SENSOR_FP2_C423_PRESENCE_SENSOR_4: Entity = Entity("binary_sensor.presence_sensor_fp2_c423_presence_sensor_4")
BINARY_SENSOR_SNYK_LAPTOP_ACTIVE: Entity = Entity("binary_sensor.snyk_laptop_active")
BINARY_SENSOR_SNYK_LAPTOP_AUDIO_INPUT_IN_USE: Entity = Entity("binary_sensor.snyk_laptop_audio_input_in_use")
BINARY_SENSOR_SNYK_LAPTOP_AUDIO_OUTPUT_IN_USE: Entity = Entity("binary_sensor.snyk_laptop_audio_output_in_use")
BINARY_SENSOR_SNYK_LAPTOP_CAMERA_IN_USE: Entity = Entity("binary_sensor.snyk_laptop_camera_in_use")
BINARY_SENSOR_SNYK_LAPTOP_FOCUS: Entity = Entity("binary_sensor.snyk_laptop_focus")
BINARY_SENSOR_SOFA_PS: Entity = Entity("binary_sensor.sofa_ps")
BINARY_SENSOR_STORAGE_DOOR_CS: Entity = Entity("binary_sensor.storage_door_cs")
BINARY_SENSOR_STUDIO_MOTION: Entity = Entity("binary_sensor.studio_motion")
BINARY_SENSOR_STUDIO_MS_MOTION: Entity = Entity("binary_sensor.studio_ms_motion")
BINARY_SENSOR_VODAFONE_WI_FI_HUB_WAN_STATUS: Entity = Entity("binary_sensor.vodafone_wi_fi_hub_wan_status")
BINARY_SENSOR_WARDROBE_DOOR_LEFT_CS_IASZONE: Entity = Entity("binary_sensor.wardrobe_door_left_cs_iaszone")
BINARY_SENSOR_WARDROBE_DOOR_RIGHT_CS_IASZONE: Entity = Entity("binary_sensor.wardrobe_door_right_cs_iaszone")
BINARY_SENSOR_WARDROBE_MIDDLE_DOOR: Entity = Entity("binary_sensor.wardrobe_middle_door")
BINARY_SENSOR_WARDROBE_MS_MOTION: Entity = Entity("binary_sensor.wardrobe_ms_motion")
BUTTON_AQARA_LUMI_MOTION_AC01_PRESENCE_STATUS_RESET: Entity = Entity("button.aqara_lumi_motion_ac01_presence_status_reset")
BUTTON_BEDROOM_AIR_QUALITY_IDENTIFY: Entity = Entity("button.bedroom_air_quality_identify")
BUTTON_BEDROOM_MS_PRESENCE_STATUS_RESET: Entity = Entity("button.bedroom_ms_presence_status_reset")
BUTTON_COFFEE_TABLE_BUTTON_IDENTIFY: Entity = Entity("button.coffee_table_button_identify")
BUTTON_CS_WARDROBE_RIGHT_IDENTIFY_3: Entity = Entity("button.cs_wardrobe_right_identify_3")
BUTTON_DINING_TABLE_BUTTON_IDENTIFY: Entity = Entity("button.dining_table_button_identify")
BUTTON_ESPRESENSE_54B85F_ENROLL: Entity = Entity("button.espresense_54b85f_enroll")
BUTTON_ESPRESENSE_54B85F_RESTART: Entity = Entity("button.espresense_54b85f_restart")
BUTTON_ESPRESENSE_54B85F_UPDATE: Entity = Entity("button.espresense_54b85f_update")
BUTTON_ESPRESENSE_LIVING_ROOM_ENROLL: Entity = Entity("button.espresense_living_room_enroll")
BUTTON_ESPRESENSE_LIVING_ROOM_RESTART: Entity = Entity("button.espresense_living_room_restart")
BUTTON_ESPRESENSE_LIVING_ROOM_UPDATE: Entity = Entity("button.espresense_living_room_update")
BUTTON_LUMI_LUMI_SENSOR_WLEAK_AQ1_IDENTIFY_2: Entity = Entity("button.lumi_lumi_sensor_wleak_aq1_identify_2")
BUTTON_MEDIA_CONTROLLER_IDENTIFY: Entity = Entity("button.media_controller_identify")
BUTTON_PRESENCE_SENSOR_FP2_C10B_IDENTIFY: Entity = Entity("button.presence_sensor_fp2_c10b_identify")
BUTTON_PRESENCE_SENSOR_FP2_C423_IDENTIFY: Entity = Entity("button.presence_sensor_fp2_c423_identify")
BUTTON_SIGNAL_REPEATER_IDENTIFY: Entity = Entity("button.signal_repeater_identify")
BUTTON_SONY_KD_49XF8096_REBOOT: Entity = Entity("button.sony_kd_49xf8096_reboot")
BUTTON_SONY_KD_49XF8096_TERMINATE_APPS: Entity = Entity("button.sony_kd_49xf8096_terminate_apps")
BUTTON_SYNCHRONIZE_DEVICES: Entity = Entity("button.synchronize_devices")
BUTTON_THERMOMIX_IDENTIFY: Entity = Entity("button.thermomix_identify")
BUTTON_WARDROBE_MIDDLE_DOOR_IDENTIFY: Entity = Entity("button.wardrobe_middle_door_identify")
COVER_BEDROOM_CURTAIN_COVER: Entity = Entity("cover.bedroom_curtain_cover")
COVER_BLINDS_CURTAIN: Entity = Entity("cover.blinds_curtain")
DEVICE_TRACKER_JOSE_CARLOSS_IPAD: Entity = Entity("device_tracker.jose_carloss_ipad")
DEVICE_TRACKER_MANDIES_IPHONE: Entity = Entity("device_tracker.mandies_iphone")
DEVICE_TRACKER_SM_S918B: Entity = Entity("device_tracker.sm_s918b")
DEVICE_TRACKER_SNYK_LAPTOP: Entity = Entity("device_tracker.snyk_laptop")
IMAGE_FLICK_HOME: Entity = Entity("image.flick_home")
INPUT_BOOLEAN_ACTIVITY_LOCK_BATHROOM: Entity = Entity("input_boolean.activity_lock_bathroom")
INPUT_BOOLEAN_ACTIVITY_LOCK_BEDROOM: Entity = Entity("input_boolean.activity_lock_bedroom")
INPUT_BOOLEAN_ACTIVITY_LOCK_DINING_ROOM: Entity = Entity("input_boolean.activity_lock_dining_room")
INPUT_BOOLEAN_ACTIVITY_LOCK_ENSUITE: Entity = Entity("input_boolean.activity_lock_ensuite")
INPUT_BOOLEAN_ACTIVITY_LOCK_HALLWAY: Entity = Entity("input_boolean.activity_lock_hallway")
INPUT_BOOLEAN_ACTIVITY_LOCK_KITCHEN: Entity = Entity("input_boolean.activity_lock_kitchen")
INPUT_BOOLEAN_ACTIVITY_LOCK_LIVING_ROOM: Entity = Entity("input_boolean.activity_lock_living_room")
INPUT_BOOLEAN_ACTIVITY_LOCK_OFFICE: Entity = Entity("input_boolean.activity_lock_office")
INPUT_BOOLEAN_ACTIVITY_LOCK_STORAGE: Entity = Entity("input_boolean.activity_lock_storage")
INPUT_BOOLEAN_ACTIVITY_LOCK_STUDIO: Entity = Entity("input_boolean.activity_lock_studio")
INPUT_BOOLEAN_ACTIVITY_LOCK_WARDROBE: Entity = Entity("input_boolean.activity_lock_wardrobe")
INPUT_BOOLEAN_GUEST_MODE: Entity = Entity("input_boolean.guest_mode")
INPUT_DATETIME_LAST_CLEANED_BATHROOM: Entity = Entity("input_datetime.last_cleaned_bathroom")
INPUT_DATETIME_LAST_CLEANED_BEDROOM: Entity = Entity("input_datetime.last_cleaned_bedroom")
INPUT_DATETIME_LAST_CLEANED_DINING_ROOM: Entity = Entity("input_datetime.last_cleaned_dining_room")
INPUT_DATETIME_LAST_CLEANED_ENSUITE: Entity = Entity("input_datetime.last_cleaned_ensuite")
INPUT_DATETIME_LAST_CLEANED_FLAT: Entity = Entity("input_datetime.last_cleaned_flat")
INPUT_DATETIME_LAST_CLEANED_HALLWAY: Entity = Entity("input_datetime.last_cleaned_hallway")
INPUT_DATETIME_LAST_CLEANED_KITCHEN: Entity = Entity("input_datetime.last_cleaned_kitchen")
INPUT_DATETIME_LAST_CLEANED_LIVING_ROOM: Entity = Entity("input_datetime.last_cleaned_living_room")
INPUT_DATETIME_LAST_CLEANED_OFFICE: Entity = Entity("input_datetime.last_cleaned_office")
INPUT_DATETIME_LAST_CLEANED_STORAGE: Entity = Entity("input_datetime.last_cleaned_storage")
INPUT_DATETIME_LAST_CLEANED_STUDIO: Entity = Entity("input_datetime.last_cleaned_studio")
INPUT_DATETIME_LAST_CLEANED_VACUUM_MOP: Entity = Entity("input_datetime.last_cleaned_vacuum_mop")
INPUT_DATETIME_LAST_CLEANED_WARDROBE: Entity = Entity("input_datetime.last_cleaned_wardrobe")
INPUT_DATETIME_LAST_COOKED: Entity = Entity("input_datetime.last_cooked")
INPUT_DATETIME_LAST_PRESENT_BATHROOM: Entity = Entity("input_datetime.last_present_bathroom")
INPUT_DATETIME_LAST_PRESENT_BEDROOM: Entity = Entity("input_datetime.last_present_bedroom")
INPUT_DATETIME_LAST_PRESENT_DINING_ROOM: Entity = Entity("input_datetime.last_present_dining_room")
INPUT_DATETIME_LAST_PRESENT_ENSUITE: Entity = Entity("input_datetime.last_present_ensuite")
INPUT_DATETIME_LAST_PRESENT_HALLWAY: Entity = Entity("input_datetime.last_present_hallway")
INPUT_DATETIME_LAST_PRESENT_KITCHEN: Entity = Entity("input_datetime.last_present_kitchen")
INPUT_DATETIME_LAST_PRESENT_LIVING_ROOM: Entity = Entity("input_datetime.last_present_living_room")
INPUT_DATETIME_LAST_PRESENT_OFFICE: Entity = Entity("input_datetime.last_present_office")
INPUT_DATETIME_LAST_PRESENT_STORAGE: Entity = Entity("input_datetime.last_present_storage")
INPUT_DATETIME_LAST_PRESENT_STUDIO: Entity = Entity("input_datetime.last_present_studio")
INPUT_DATETIME_LAST_PRESENT_WARDROBE: Entity = Entity("input_datetime.last_present_wardrobe")
INPUT_SELECT_BATHROOM_ACTIVITY: Entity = Entity("input_select.bathroom_activity")
INPUT_SELECT_BEDROOM_ACTIVITY: Entity = Entity("input_select.bedroom_activity")
INPUT_SELECT_DINING_ROOM_ACTIVITY: Entity = Entity("input_select.dining_room_activity")
INPUT_SELECT_ENSUITE_ACTIVITY: Entity = Entity("input_select.ensuite_activity")
INPUT_SELECT_HALLWAY_ACTIVITY: Entity = Entity("input_select.hallway_activity")
INPUT_SELECT_HOMEASSISTANT_MODE: Entity = Entity("input_select.homeassistant_mode")
INPUT_SELECT_KITCHEN_ACTIVITY: Entity = Entity("input_select.kitchen_activity")
INPUT_SELECT_LIVING_ROOM_ACTIVITY: Entity = Entity("input_select.living_room_activity")
INPUT_SELECT_OFFICE_ACTIVITY: Entity = Entity("input_select.office_activity")
INPUT_SELECT_STORAGE_ACTIVITY: Entity = Entity("input_select.storage_activity")
INPUT_SELECT_STUDIO_ACTIVITY: Entity = Entity("input_select.studio_activity")
INPUT_SELECT_WARDROBE_ACTIVITY: Entity = Entity("input_select.wardrobe_activity")
LIGHT_BALCONY: Entity = Entity("light.balcony")
LIGHT_BALCONY_2: Entity = Entity("light.balcony_2")
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
LIGHT_DINING_SOFA_LEFT: Entity = Entity("light.dining_sofa_left")
LIGHT_DRUM_SPOT: Entity = Entity("light.drum_spot")
LIGHT_ENSUITE: Entity = Entity("light.ensuite")
LIGHT_HALLWAY: Entity = Entity("light.hallway")
LIGHT_HALLWAY_2: Entity = Entity("light.hallway_2")
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
LIGHT_STORAGE: Entity = Entity("light.storage")
LIGHT_STORAGE_2: Entity = Entity("light.storage_2")
LIGHT_STUDIO: Entity = Entity("light.studio")
LIGHT_WARDROBE: Entity = Entity("light.wardrobe")
LIGHT_WARDROBE_2: Entity = Entity("light.wardrobe_2")
MEDIA_PLAYER_ALL_SPEAKERS_2: Entity = Entity("media_player.all_speakers_2")
MEDIA_PLAYER_AMANDA_M1AIR_C02FX084Q6LX: Entity = Entity("media_player.amanda_m1air_c02fx084q6lx")
MEDIA_PLAYER_BEDROOM_SPEAKER_R_2: Entity = Entity("media_player.bedroom_speaker_r_2")
MEDIA_PLAYER_BEDROOM_SPEAKERS: Entity = Entity("media_player.bedroom_speakers")
MEDIA_PLAYER_HALLWAY_SPEAKER: Entity = Entity("media_player.hallway_speaker")
MEDIA_PLAYER_KITCHEN_SPEAKER: Entity = Entity("media_player.kitchen_speaker")
MEDIA_PLAYER_LIVING_AREA_2: Entity = Entity("media_player.living_area_2")
MEDIA_PLAYER_LIVING_ROOM_SPEAKER_2: Entity = Entity("media_player.living_room_speaker_2")
MEDIA_PLAYER_LIVING_ROOM_STEREO: Entity = Entity("media_player.living_room_stereo")
MEDIA_PLAYER_SNYK_LAPTOP: Entity = Entity("media_player.snyk_laptop")
MEDIA_PLAYER_SONY_KD_49XF8096: Entity = Entity("media_player.sony_kd_49xf8096")
MEDIA_PLAYER_TV: Entity = Entity("media_player.tv")
MEDIA_PLAYER_TV_2: Entity = Entity("media_player.tv_2")
NUMBER_ESPRESENSE_54B85F_ABSORPTION: Entity = Entity("number.espresense_54b85f_absorption")
NUMBER_ESPRESENSE_54B85F_MAX_DISTANCE: Entity = Entity("number.espresense_54b85f_max_distance")
NUMBER_ESPRESENSE_LIVING_ROOM_ABSORPTION: Entity = Entity("number.espresense_living_room_absorption")
NUMBER_ESPRESENSE_LIVING_ROOM_MAX_DISTANCE: Entity = Entity("number.espresense_living_room_max_distance")
NUMBER_FLICK_VOLUME: Entity = Entity("number.flick_volume")
PERSON_AMANDA: Entity = Entity("person.amanda")
PERSON_JOSE_CARLOS: Entity = Entity("person.jose_carlos")
REMOTE_SONY_KD_49XF8096: Entity = Entity("remote.sony_kd_49xf8096")
REMOTE_TV: Entity = Entity("remote.tv")
SCENE_BEDROOM_BEDTIME: Entity = Entity("scene.bedroom_bedtime")
SCENE_BEDROOM_BRIGHT: Entity = Entity("scene.bedroom_bright")
SCENE_BEDROOM_CONCENTRATE: Entity = Entity("scene.bedroom_concentrate")
SCENE_BEDROOM_DIMMED: Entity = Entity("scene.bedroom_dimmed")
SCENE_BEDROOM_GENTLE_READING: Entity = Entity("scene.bedroom_gentle_reading")
SCENE_BEDROOM_NIGHTLIGHT: Entity = Entity("scene.bedroom_nightlight")
SCENE_BEDROOM_RELAXING: Entity = Entity("scene.bedroom_relaxing")
SCENE_ENSUITE_CONCENTRATE: Entity = Entity("scene.ensuite_concentrate")
SCENE_ENSUITE_NIGHTLIGHT: Entity = Entity("scene.ensuite_nightlight")
SCENE_HALLWAY_BRIGHT: Entity = Entity("scene.hallway_bright")
SCENE_HALLWAY_CONCENTRATE: Entity = Entity("scene.hallway_concentrate")
SCENE_HALLWAY_DIMMED: Entity = Entity("scene.hallway_dimmed")
SCENE_HALLWAY_ENERGISE: Entity = Entity("scene.hallway_energise")
SCENE_HALLWAY_FANCY: Entity = Entity("scene.hallway_fancy")
SCENE_HALLWAY_NATURAL_LIGHT: Entity = Entity("scene.hallway_natural_light")
SCENE_HALLWAY_NIGHTLIGHT: Entity = Entity("scene.hallway_nightlight")
SCENE_HALLWAY_READ: Entity = Entity("scene.hallway_read")
SCENE_HALLWAY_RELAX: Entity = Entity("scene.hallway_relax")
SCENE_HALLWAY_REST: Entity = Entity("scene.hallway_rest")
SCENE_KITCHEN_CONCENTRATE: Entity = Entity("scene.kitchen_concentrate")
SCENE_KITCHEN_COOK: Entity = Entity("scene.kitchen_cook")
SCENE_KITCHEN_COUNTER: Entity = Entity("scene.kitchen_counter")
SCENE_KITCHEN_NIGHTLIGHT: Entity = Entity("scene.kitchen_nightlight")
SCENE_KITCHEN_TV: Entity = Entity("scene.kitchen_tv")
SCENE_LIVING_ROOM_COZY: Entity = Entity("scene.living_room_cozy")
SCENE_LIVING_ROOM_DINING: Entity = Entity("scene.living_room_dining")
SCENE_LIVING_ROOM_DRUMMING: Entity = Entity("scene.living_room_drumming")
SCENE_LIVING_ROOM_GAMING: Entity = Entity("scene.living_room_gaming")
SCENE_LIVING_ROOM_MOVIE: Entity = Entity("scene.living_room_movie")
SCENE_LIVING_ROOM_READING: Entity = Entity("scene.living_room_reading")
SCENE_LIVING_ROOM_WELCOME: Entity = Entity("scene.living_room_welcome")
SCENE_STORAGE_BRIGHT: Entity = Entity("scene.storage_bright")
SCENE_STORAGE_DIMMED: Entity = Entity("scene.storage_dimmed")
SCENE_STUDIO_CONCENTRATE: Entity = Entity("scene.studio_concentrate")
SCENE_STUDIO_DRUMMING: Entity = Entity("scene.studio_drumming")
SCENE_STUDIO_ENERGISE: Entity = Entity("scene.studio_energise")
SCENE_STUDIO_NATURAL_LIGHT: Entity = Entity("scene.studio_natural_light")
SCENE_STUDIO_NIGHTLIGHT: Entity = Entity("scene.studio_nightlight")
SCENE_STUDIO_READ: Entity = Entity("scene.studio_read")
SCENE_STUDIO_RELAX: Entity = Entity("scene.studio_relax")
SCENE_STUDIO_REST: Entity = Entity("scene.studio_rest")
SCENE_STUDIO_SNARING: Entity = Entity("scene.studio_snaring")
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
SENSOR_AQARA_LUMI_MOTION_AC01_DEVICE_TEMPERATURE: Entity = Entity("sensor.aqara_lumi_motion_ac01_device_temperature")
SENSOR_BEDROOM_AIR_QUALITY_HUMIDITY: Entity = Entity("sensor.bedroom_air_quality_humidity")
SENSOR_BEDROOM_AIR_QUALITY_PARTICULATE_MATTER: Entity = Entity("sensor.bedroom_air_quality_particulate_matter")
SENSOR_BEDROOM_AIR_QUALITY_TEMPERATURE: Entity = Entity("sensor.bedroom_air_quality_temperature")
SENSOR_BEDROOM_BUTTON_BATTERY: Entity = Entity("sensor.bedroom_button_battery")
SENSOR_BEDROOM_MS_COMMAND: Entity = Entity("sensor.bedroom_ms_command")
SENSOR_BEDROOM_MS_DEVICE_TEMPERATURE: Entity = Entity("sensor.bedroom_ms_device_temperature")
SENSOR_BLINDS_LAST_OPERATION_DURATION: Entity = Entity("sensor.blinds_last_operation_duration")
SENSOR_COFFEE_TABLE_BUTTON_BATTERY: Entity = Entity("sensor.coffee_table_button_battery")
SENSOR_CS_WARDROBE_RIGHT_BATTERY: Entity = Entity("sensor.cs_wardrobe_right_battery")
SENSOR_CS_WARDROBE_RIGHT_DEVICE_TEMPERATURE: Entity = Entity("sensor.cs_wardrobe_right_device_temperature")
SENSOR_DESK_CHAIR_PS_BATTERY: Entity = Entity("sensor.desk_chair_ps_battery")
SENSOR_DESK_CHAIR_PS_DEVICE_TEMPERATURE: Entity = Entity("sensor.desk_chair_ps_device_temperature")
SENSOR_DINING_TABLE_BUTTON_BATTERY: Entity = Entity("sensor.dining_table_button_battery")
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
SENSOR_ESPRESENSE_54B85F_FREE_MEM: Entity = Entity("sensor.espresense_54b85f_free_mem")
SENSOR_ESPRESENSE_54B85F_UPTIME: Entity = Entity("sensor.espresense_54b85f_uptime")
SENSOR_ESPRESENSE_LIVING_ROOM_FREE_MEM: Entity = Entity("sensor.espresense_living_room_free_mem")
SENSOR_ESPRESENSE_LIVING_ROOM_UPTIME: Entity = Entity("sensor.espresense_living_room_uptime")
SENSOR_FLAT_DOOR_CS_BATTERY: Entity = Entity("sensor.flat_door_cs_battery")
SENSOR_FLAT_DOOR_CS_DEVICE_TEMPERATURE: Entity = Entity("sensor.flat_door_cs_device_temperature")
SENSOR_FLICK_BATTERY: Entity = Entity("sensor.flick_battery")
SENSOR_FLICK_CLEANING_AREA: Entity = Entity("sensor.flick_cleaning_area")
SENSOR_FLICK_CLEANING_TIME: Entity = Entity("sensor.flick_cleaning_time")
SENSOR_FLICK_FILTER_TIME_LEFT: Entity = Entity("sensor.flick_filter_time_left")
SENSOR_FLICK_LAST_CLEAN_BEGIN: Entity = Entity("sensor.flick_last_clean_begin")
SENSOR_FLICK_LAST_CLEAN_END: Entity = Entity("sensor.flick_last_clean_end")
SENSOR_FLICK_MAIN_BRUSH_TIME_LEFT: Entity = Entity("sensor.flick_main_brush_time_left")
SENSOR_FLICK_SENSOR_TIME_LEFT: Entity = Entity("sensor.flick_sensor_time_left")
SENSOR_FLICK_SIDE_BRUSH_TIME_LEFT: Entity = Entity("sensor.flick_side_brush_time_left")
SENSOR_FLICK_STATUS: Entity = Entity("sensor.flick_status")
SENSOR_FLICK_TOTAL_CLEANING_AREA: Entity = Entity("sensor.flick_total_cleaning_area")
SENSOR_FLICK_TOTAL_CLEANING_TIME: Entity = Entity("sensor.flick_total_cleaning_time")
SENSOR_FLICK_VACUUM_ERROR: Entity = Entity("sensor.flick_vacuum_error")
SENSOR_GALAXY_S23_BLE_BEACON: Entity = Entity("sensor.galaxy_s23_ble_beacon")
SENSOR_HACS: Entity = Entity("sensor.hacs")
SENSOR_HALLWAY_MS_BATTERY: Entity = Entity("sensor.hallway_ms_battery")
SENSOR_HALLWAY_MS_ILLUMINANCE: Entity = Entity("sensor.hallway_ms_illuminance")
SENSOR_HALLWAY_MS_TEMPERATURE: Entity = Entity("sensor.hallway_ms_temperature")
SENSOR_JOSE_CARLOSS_IPAD_ACTIVITY: Entity = Entity("sensor.jose_carloss_ipad_activity")
SENSOR_JOSE_CARLOSS_IPAD_BATTERY_LEVEL: Entity = Entity("sensor.jose_carloss_ipad_battery_level")
SENSOR_JOSE_CARLOSS_IPAD_BATTERY_STATE: Entity = Entity("sensor.jose_carloss_ipad_battery_state")
SENSOR_JOSE_CARLOSS_IPAD_BSSID: Entity = Entity("sensor.jose_carloss_ipad_bssid")
SENSOR_JOSE_CARLOSS_IPAD_CONNECTION_TYPE: Entity = Entity("sensor.jose_carloss_ipad_connection_type")
SENSOR_JOSE_CARLOSS_IPAD_GEOCODED_LOCATION: Entity = Entity("sensor.jose_carloss_ipad_geocoded_location")
SENSOR_JOSE_CARLOSS_IPAD_LAST_UPDATE_TRIGGER: Entity = Entity("sensor.jose_carloss_ipad_last_update_trigger")
SENSOR_JOSE_CARLOSS_IPAD_SSID: Entity = Entity("sensor.jose_carloss_ipad_ssid")
SENSOR_JOSE_CARLOSS_IPAD_STORAGE: Entity = Entity("sensor.jose_carloss_ipad_storage")
SENSOR_KITCHEN_ILLUMINANCE_MS: Entity = Entity("sensor.kitchen_illuminance_ms")
SENSOR_KITCHEN_MS_BATTERY: Entity = Entity("sensor.kitchen_ms_battery")
SENSOR_KITCHEN_MS_ILLUMINANCE: Entity = Entity("sensor.kitchen_ms_illuminance")
SENSOR_KITCHEN_MS_TEMPERATURE: Entity = Entity("sensor.kitchen_ms_temperature")
SENSOR_LIVING_ROOM_ILLUMINANCE: Entity = Entity("sensor.living_room_illuminance")
SENSOR_LIVING_ROOM_MS_COMMAND: Entity = Entity("sensor.living_room_ms_command")
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
SENSOR_OUTSIDE_TEMPERATURE: Entity = Entity("sensor.outside_temperature")
SENSOR_SLEEPASANDROID_PHONE: Entity = Entity("sensor.sleepasandroid_phone")
SENSOR_SM_S918B_BATTERY_LEVEL: Entity = Entity("sensor.sm_s918b_battery_level")
SENSOR_SM_S918B_BATTERY_STATE: Entity = Entity("sensor.sm_s918b_battery_state")
SENSOR_SM_S918B_BLE_TRANSMITTER: Entity = Entity("sensor.sm_s918b_ble_transmitter")
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
SENSOR_SOFA_PS_BATTERY: Entity = Entity("sensor.sofa_ps_battery")
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
SENSOR_WARDROBE_MIDDLE_DOOR_BATTERY: Entity = Entity("sensor.wardrobe_middle_door_battery")
SENSOR_WARDROBE_MS_BATTERY: Entity = Entity("sensor.wardrobe_ms_battery")
SUN_SUN: Entity = Entity("sun.sun")
SWITCH_AUTOMATION_LEAVING_HOME: Entity = Entity("switch.automation_leaving_home")
SWITCH_BLINDS_REVERSE: Entity = Entity("switch.blinds_reverse")
SWITCH_DRUMKIT: Entity = Entity("switch.drumkit")
SWITCH_DRUMKIT_CHILD_LOCK: Entity = Entity("switch.drumkit_child_lock")
SWITCH_ESPRESENSE_54B85F_ARDUINO_OTA: Entity = Entity("switch.espresense_54b85f_arduino_ota")
SWITCH_ESPRESENSE_54B85F_AUTO_UPDATE: Entity = Entity("switch.espresense_54b85f_auto_update")
SWITCH_ESPRESENSE_54B85F_PRERELEASE: Entity = Entity("switch.espresense_54b85f_prerelease")
SWITCH_ESPRESENSE_LIVING_ROOM_ARDUINO_OTA: Entity = Entity("switch.espresense_living_room_arduino_ota")
SWITCH_ESPRESENSE_LIVING_ROOM_AUTO_UPDATE: Entity = Entity("switch.espresense_living_room_auto_update")
SWITCH_ESPRESENSE_LIVING_ROOM_PRERELEASE: Entity = Entity("switch.espresense_living_room_prerelease")
SWITCH_FLICK_CHILD_LOCK: Entity = Entity("switch.flick_child_lock")
SWITCH_FLICK_DO_NOT_DISTURB: Entity = Entity("switch.flick_do_not_disturb")
SWITCH_FLICK_STATUS_INDICATOR_LIGHT: Entity = Entity("switch.flick_status_indicator_light")
SWITCH_HALLWAY_MS_LIGHT_SENSOR_ENABLED: Entity = Entity("switch.hallway_ms_light_sensor_enabled")
SWITCH_HALLWAY_MS_MOTION_SENSOR_ENABLED: Entity = Entity("switch.hallway_ms_motion_sensor_enabled")
SWITCH_KITCHEN_MS_LIGHT_SENSOR_ENABLED: Entity = Entity("switch.kitchen_ms_light_sensor_enabled")
SWITCH_KITCHEN_MS_MOTION_SENSOR_ENABLED: Entity = Entity("switch.kitchen_ms_motion_sensor_enabled")
SWITCH_MONITOR: Entity = Entity("switch.monitor")
SWITCH_STUDIO_MS_LIGHT_SENSOR_ENABLED: Entity = Entity("switch.studio_ms_light_sensor_enabled")
SWITCH_STUDIO_MS_MOTION_SENSOR_ENABLED: Entity = Entity("switch.studio_ms_motion_sensor_enabled")
SWITCH_THERMOMIX_SWITCH: Entity = Entity("switch.thermomix_switch")
TIME_FLICK_DO_NOT_DISTURB_BEGIN: Entity = Entity("time.flick_do_not_disturb_begin")
TIME_FLICK_DO_NOT_DISTURB_END: Entity = Entity("time.flick_do_not_disturb_end")
UPDATE_ADVANCED_SSH_WEB_TERMINAL_UPDATE: Entity = Entity("update.advanced_ssh_web_terminal_update")
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
ZONE_GYM: Entity = Entity("zone.gym")
ZONE_HOME: Entity = Entity("zone.home")
