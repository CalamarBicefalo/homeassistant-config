from typing import NewType
Service  = NewType('UserId', str)
ALARM_CONTROL_PANEL_ALARM_ARM_AWAY: Service = Service("alarm_control_panel/alarm_arm_away")
ALARM_CONTROL_PANEL_ALARM_ARM_CUSTOM_BYPASS: Service = Service("alarm_control_panel/alarm_arm_custom_bypass")
ALARM_CONTROL_PANEL_ALARM_ARM_HOME: Service = Service("alarm_control_panel/alarm_arm_home")
ALARM_CONTROL_PANEL_ALARM_ARM_NIGHT: Service = Service("alarm_control_panel/alarm_arm_night")
ALARM_CONTROL_PANEL_ALARM_ARM_VACATION: Service = Service("alarm_control_panel/alarm_arm_vacation")
ALARM_CONTROL_PANEL_ALARM_DISARM: Service = Service("alarm_control_panel/alarm_disarm")
ALARM_CONTROL_PANEL_ALARM_TRIGGER: Service = Service("alarm_control_panel/alarm_trigger")
ASSIST_SATELLITE_ANNOUNCE: Service = Service("assist_satellite/announce")
ASSIST_SATELLITE_START_CONVERSATION: Service = Service("assist_satellite/start_conversation")
AUTOMATION_RELOAD: Service = Service("automation/reload")
AUTOMATION_TOGGLE: Service = Service("automation/toggle")
AUTOMATION_TRIGGER: Service = Service("automation/trigger")
AUTOMATION_TURN_OFF: Service = Service("automation/turn_off")
AUTOMATION_TURN_ON: Service = Service("automation/turn_on")
BACKUP_CREATE_AUTOMATIC: Service = Service("backup/create_automatic")
BUTTON_PRESS: Service = Service("button/press")
CAMERA_DISABLE_MOTION_DETECTION: Service = Service("camera/disable_motion_detection")
CAMERA_ENABLE_MOTION_DETECTION: Service = Service("camera/enable_motion_detection")
CAMERA_PLAY_STREAM: Service = Service("camera/play_stream")
CAMERA_RECORD: Service = Service("camera/record")
CAMERA_SNAPSHOT: Service = Service("camera/snapshot")
CAMERA_TURN_OFF: Service = Service("camera/turn_off")
CAMERA_TURN_ON: Service = Service("camera/turn_on")
CAST_SHOW_LOVELACE_VIEW: Service = Service("cast/show_lovelace_view")
CLIMATE_SET_AUX_HEAT: Service = Service("climate/set_aux_heat")
CLIMATE_SET_FAN_MODE: Service = Service("climate/set_fan_mode")
CLIMATE_SET_HUMIDITY: Service = Service("climate/set_humidity")
CLIMATE_SET_HVAC_MODE: Service = Service("climate/set_hvac_mode")
CLIMATE_SET_PRESET_MODE: Service = Service("climate/set_preset_mode")
CLIMATE_SET_SWING_HORIZONTAL_MODE: Service = Service("climate/set_swing_horizontal_mode")
CLIMATE_SET_SWING_MODE: Service = Service("climate/set_swing_mode")
CLIMATE_SET_TEMPERATURE: Service = Service("climate/set_temperature")
CLIMATE_TOGGLE: Service = Service("climate/toggle")
CLIMATE_TURN_OFF: Service = Service("climate/turn_off")
CLIMATE_TURN_ON: Service = Service("climate/turn_on")
CLOUD_REMOTE_CONNECT: Service = Service("cloud/remote_connect")
CLOUD_REMOTE_DISCONNECT: Service = Service("cloud/remote_disconnect")
CONVERSATION_PROCESS: Service = Service("conversation/process")
CONVERSATION_RELOAD: Service = Service("conversation/reload")
COUNTER_DECREMENT: Service = Service("counter/decrement")
COUNTER_INCREMENT: Service = Service("counter/increment")
COUNTER_RESET: Service = Service("counter/reset")
COUNTER_SET_VALUE: Service = Service("counter/set_value")
COVER_CLOSE_COVER: Service = Service("cover/close_cover")
COVER_CLOSE_COVER_TILT: Service = Service("cover/close_cover_tilt")
COVER_OPEN_COVER: Service = Service("cover/open_cover")
COVER_OPEN_COVER_TILT: Service = Service("cover/open_cover_tilt")
COVER_SET_COVER_POSITION: Service = Service("cover/set_cover_position")
COVER_SET_COVER_TILT_POSITION: Service = Service("cover/set_cover_tilt_position")
COVER_STOP_COVER: Service = Service("cover/stop_cover")
COVER_STOP_COVER_TILT: Service = Service("cover/stop_cover_tilt")
COVER_TOGGLE: Service = Service("cover/toggle")
COVER_TOGGLE_COVER_TILT: Service = Service("cover/toggle_cover_tilt")
CUSTOM_EVENT_FIRE: Service = Service("custom_event/fire")
DEVICE_TRACKER_SEE: Service = Service("device_tracker/see")
DYSON_LOCAL_SET_ANGLE: Service = Service("dyson_local/set_angle")
DYSON_LOCAL_SET_TIMER: Service = Service("dyson_local/set_timer")
FAN_DECREASE_SPEED: Service = Service("fan/decrease_speed")
FAN_INCREASE_SPEED: Service = Service("fan/increase_speed")
FAN_OSCILLATE: Service = Service("fan/oscillate")
FAN_SET_DIRECTION: Service = Service("fan/set_direction")
FAN_SET_PERCENTAGE: Service = Service("fan/set_percentage")
FAN_SET_PRESET_MODE: Service = Service("fan/set_preset_mode")
FAN_TOGGLE: Service = Service("fan/toggle")
FAN_TURN_OFF: Service = Service("fan/turn_off")
FAN_TURN_ON: Service = Service("fan/turn_on")
FFMPEG_RESTART: Service = Service("ffmpeg/restart")
FFMPEG_START: Service = Service("ffmpeg/start")
FFMPEG_STOP: Service = Service("ffmpeg/stop")
FRONTEND_RELOAD_THEMES: Service = Service("frontend/reload_themes")
FRONTEND_SET_THEME: Service = Service("frontend/set_theme")
GOOGLE_ASSISTANT_REQUEST_SYNC: Service = Service("google_assistant/request_sync")
GROUP_RELOAD: Service = Service("group/reload")
GROUP_REMOVE: Service = Service("group/remove")
GROUP_SET: Service = Service("group/set")
HASSIO_ADDON_RESTART: Service = Service("hassio/addon_restart")
HASSIO_ADDON_START: Service = Service("hassio/addon_start")
HASSIO_ADDON_STDIN: Service = Service("hassio/addon_stdin")
HASSIO_ADDON_STOP: Service = Service("hassio/addon_stop")
HASSIO_ADDON_UPDATE: Service = Service("hassio/addon_update")
HASSIO_BACKUP_FULL: Service = Service("hassio/backup_full")
HASSIO_BACKUP_PARTIAL: Service = Service("hassio/backup_partial")
HASSIO_HOST_REBOOT: Service = Service("hassio/host_reboot")
HASSIO_HOST_SHUTDOWN: Service = Service("hassio/host_shutdown")
HASSIO_RESTORE_FULL: Service = Service("hassio/restore_full")
HASSIO_RESTORE_PARTIAL: Service = Service("hassio/restore_partial")
HOMEASSISTANT_CHECK_CONFIG: Service = Service("homeassistant/check_config")
HOMEASSISTANT_RELOAD_ALL: Service = Service("homeassistant/reload_all")
HOMEASSISTANT_RELOAD_CONFIG_ENTRY: Service = Service("homeassistant/reload_config_entry")
HOMEASSISTANT_RELOAD_CORE_CONFIG: Service = Service("homeassistant/reload_core_config")
HOMEASSISTANT_RELOAD_CUSTOM_TEMPLATES: Service = Service("homeassistant/reload_custom_templates")
HOMEASSISTANT_RESTART: Service = Service("homeassistant/restart")
HOMEASSISTANT_SAVE_PERSISTENT_STATES: Service = Service("homeassistant/save_persistent_states")
HOMEASSISTANT_SET_LOCATION: Service = Service("homeassistant/set_location")
HOMEASSISTANT_STOP: Service = Service("homeassistant/stop")
HOMEASSISTANT_TOGGLE: Service = Service("homeassistant/toggle")
HOMEASSISTANT_TURN_OFF: Service = Service("homeassistant/turn_off")
HOMEASSISTANT_TURN_ON: Service = Service("homeassistant/turn_on")
HOMEASSISTANT_UPDATE_ENTITY: Service = Service("homeassistant/update_entity")
HUE_ACTIVATE_SCENE: Service = Service("hue/activate_scene")
HUE_HUE_ACTIVATE_SCENE: Service = Service("hue/hue_activate_scene")
HUMIDIFIER_SET_HUMIDITY: Service = Service("humidifier/set_humidity")
HUMIDIFIER_SET_MODE: Service = Service("humidifier/set_mode")
HUMIDIFIER_TOGGLE: Service = Service("humidifier/toggle")
HUMIDIFIER_TURN_OFF: Service = Service("humidifier/turn_off")
HUMIDIFIER_TURN_ON: Service = Service("humidifier/turn_on")
IMAGE_SNAPSHOT: Service = Service("image/snapshot")
INPUT_BOOLEAN_RELOAD: Service = Service("input_boolean/reload")
INPUT_BOOLEAN_TOGGLE: Service = Service("input_boolean/toggle")
INPUT_BOOLEAN_TURN_OFF: Service = Service("input_boolean/turn_off")
INPUT_BOOLEAN_TURN_ON: Service = Service("input_boolean/turn_on")
INPUT_BUTTON_PRESS: Service = Service("input_button/press")
INPUT_BUTTON_RELOAD: Service = Service("input_button/reload")
INPUT_DATETIME_RELOAD: Service = Service("input_datetime/reload")
INPUT_DATETIME_SET_DATETIME: Service = Service("input_datetime/set_datetime")
INPUT_NUMBER_DECREMENT: Service = Service("input_number/decrement")
INPUT_NUMBER_INCREMENT: Service = Service("input_number/increment")
INPUT_NUMBER_RELOAD: Service = Service("input_number/reload")
INPUT_NUMBER_SET_VALUE: Service = Service("input_number/set_value")
INPUT_SELECT_RELOAD: Service = Service("input_select/reload")
INPUT_SELECT_SELECT_FIRST: Service = Service("input_select/select_first")
INPUT_SELECT_SELECT_LAST: Service = Service("input_select/select_last")
INPUT_SELECT_SELECT_NEXT: Service = Service("input_select/select_next")
INPUT_SELECT_SELECT_OPTION: Service = Service("input_select/select_option")
INPUT_SELECT_SELECT_PREVIOUS: Service = Service("input_select/select_previous")
INPUT_SELECT_SET_OPTIONS: Service = Service("input_select/set_options")
INPUT_TEXT_RELOAD: Service = Service("input_text/reload")
INPUT_TEXT_SET_VALUE: Service = Service("input_text/set_value")
LIGHT_TOGGLE: Service = Service("light/toggle")
LIGHT_TURN_OFF: Service = Service("light/turn_off")
LIGHT_TURN_ON: Service = Service("light/turn_on")
LOCK_LOCK: Service = Service("lock/lock")
LOCK_OPEN: Service = Service("lock/open")
LOCK_UNLOCK: Service = Service("lock/unlock")
LOGBOOK_LOG: Service = Service("logbook/log")
LOGGER_SET_DEFAULT_LEVEL: Service = Service("logger/set_default_level")
LOGGER_SET_LEVEL: Service = Service("logger/set_level")
MEDIA_PLAYER_BROWSE_MEDIA: Service = Service("media_player/browse_media")
MEDIA_PLAYER_CLEAR_PLAYLIST: Service = Service("media_player/clear_playlist")
MEDIA_PLAYER_JOIN: Service = Service("media_player/join")
MEDIA_PLAYER_MEDIA_NEXT_TRACK: Service = Service("media_player/media_next_track")
MEDIA_PLAYER_MEDIA_PAUSE: Service = Service("media_player/media_pause")
MEDIA_PLAYER_MEDIA_PLAY: Service = Service("media_player/media_play")
MEDIA_PLAYER_MEDIA_PLAY_PAUSE: Service = Service("media_player/media_play_pause")
MEDIA_PLAYER_MEDIA_PREVIOUS_TRACK: Service = Service("media_player/media_previous_track")
MEDIA_PLAYER_MEDIA_SEEK: Service = Service("media_player/media_seek")
MEDIA_PLAYER_MEDIA_STOP: Service = Service("media_player/media_stop")
MEDIA_PLAYER_PLAY_MEDIA: Service = Service("media_player/play_media")
MEDIA_PLAYER_REPEAT_SET: Service = Service("media_player/repeat_set")
MEDIA_PLAYER_SELECT_SOUND_MODE: Service = Service("media_player/select_sound_mode")
MEDIA_PLAYER_SELECT_SOURCE: Service = Service("media_player/select_source")
MEDIA_PLAYER_SHUFFLE_SET: Service = Service("media_player/shuffle_set")
MEDIA_PLAYER_TOGGLE: Service = Service("media_player/toggle")
MEDIA_PLAYER_TURN_OFF: Service = Service("media_player/turn_off")
MEDIA_PLAYER_TURN_ON: Service = Service("media_player/turn_on")
MEDIA_PLAYER_UNJOIN: Service = Service("media_player/unjoin")
MEDIA_PLAYER_VOLUME_DOWN: Service = Service("media_player/volume_down")
MEDIA_PLAYER_VOLUME_MUTE: Service = Service("media_player/volume_mute")
MEDIA_PLAYER_VOLUME_SET: Service = Service("media_player/volume_set")
MEDIA_PLAYER_VOLUME_UP: Service = Service("media_player/volume_up")
MQTT_DUMP: Service = Service("mqtt/dump")
MQTT_PUBLISH: Service = Service("mqtt/publish")
MQTT_RELOAD: Service = Service("mqtt/reload")
MUSIC_ASSISTANT_GET_LIBRARY: Service = Service("music_assistant/get_library")
MUSIC_ASSISTANT_GET_QUEUE: Service = Service("music_assistant/get_queue")
MUSIC_ASSISTANT_PLAY_ANNOUNCEMENT: Service = Service("music_assistant/play_announcement")
MUSIC_ASSISTANT_PLAY_MEDIA: Service = Service("music_assistant/play_media")
MUSIC_ASSISTANT_SEARCH: Service = Service("music_assistant/search")
MUSIC_ASSISTANT_TRANSFER_QUEUE: Service = Service("music_assistant/transfer_queue")
NOTIFY_MOBILE_APP_AMANDA_M1AIR_C02FX084Q6LX: Service = Service("notify/mobile_app_amanda_m1air_c02fx084q6lx")
NOTIFY_MOBILE_APP_GALAXY_S23: Service = Service("notify/mobile_app_galaxy_s23")
NOTIFY_MOBILE_APP_GALAXY_WATCH6: Service = Service("notify/mobile_app_galaxy_watch6")
NOTIFY_MOBILE_APP_JOSE_CARLOSS_IPAD: Service = Service("notify/mobile_app_jose_carloss_ipad")
NOTIFY_MOBILE_APP_MANDIES_IPHONE: Service = Service("notify/mobile_app_mandies_iphone")
NOTIFY_MOBILE_APP_SNYK_LAPTOP: Service = Service("notify/mobile_app_snyk_laptop")
NOTIFY_NOTIFY: Service = Service("notify/notify")
NOTIFY_PERSISTENT_NOTIFICATION: Service = Service("notify/persistent_notification")
NOTIFY_SEND_MESSAGE: Service = Service("notify/send_message")
NUMBER_SET_VALUE: Service = Service("number/set_value")
OCTOPUS_ENERGY_PURGE_INVALID_EXTERNAL_STATISTIC_IDS: Service = Service("octopus_energy/purge_invalid_external_statistic_ids")
PERSISTENT_NOTIFICATION_CREATE: Service = Service("persistent_notification/create")
PERSISTENT_NOTIFICATION_DISMISS: Service = Service("persistent_notification/dismiss")
PERSISTENT_NOTIFICATION_DISMISS_ALL: Service = Service("persistent_notification/dismiss_all")
PERSON_RELOAD: Service = Service("person/reload")
RECORDER_DISABLE: Service = Service("recorder/disable")
RECORDER_ENABLE: Service = Service("recorder/enable")
RECORDER_PURGE: Service = Service("recorder/purge")
RECORDER_PURGE_ENTITIES: Service = Service("recorder/purge_entities")
REMOTE_DELETE_COMMAND: Service = Service("remote/delete_command")
REMOTE_LEARN_COMMAND: Service = Service("remote/learn_command")
REMOTE_SEND_COMMAND: Service = Service("remote/send_command")
REMOTE_TOGGLE: Service = Service("remote/toggle")
REMOTE_TURN_OFF: Service = Service("remote/turn_off")
REMOTE_TURN_ON: Service = Service("remote/turn_on")
ROBOROCK_GET_MAPS: Service = Service("roborock/get_maps")
ROBOROCK_GET_VACUUM_CURRENT_POSITION: Service = Service("roborock/get_vacuum_current_position")
ROBOROCK_SET_VACUUM_GOTO_POSITION: Service = Service("roborock/set_vacuum_goto_position")
SCENE_APPLY: Service = Service("scene/apply")
SCENE_CREATE: Service = Service("scene/create")
SCENE_DELETE: Service = Service("scene/delete")
SCENE_RELOAD: Service = Service("scene/reload")
SCENE_TURN_ON: Service = Service("scene/turn_on")
SCHEDULE_GET_SCHEDULE: Service = Service("schedule/get_schedule")
SCHEDULE_RELOAD: Service = Service("schedule/reload")
SCRIPT_RELOAD: Service = Service("script/reload")
SCRIPT_TOGGLE: Service = Service("script/toggle")
SCRIPT_TURN_OFF: Service = Service("script/turn_off")
SCRIPT_TURN_ON: Service = Service("script/turn_on")
SELECT_SELECT_FIRST: Service = Service("select/select_first")
SELECT_SELECT_LAST: Service = Service("select/select_last")
SELECT_SELECT_NEXT: Service = Service("select/select_next")
SELECT_SELECT_OPTION: Service = Service("select/select_option")
SELECT_SELECT_PREVIOUS: Service = Service("select/select_previous")
SIREN_TOGGLE: Service = Service("siren/toggle")
SIREN_TURN_OFF: Service = Service("siren/turn_off")
SIREN_TURN_ON: Service = Service("siren/turn_on")
SWITCH_TOGGLE: Service = Service("switch/toggle")
SWITCH_TURN_OFF: Service = Service("switch/turn_off")
SWITCH_TURN_ON: Service = Service("switch/turn_on")
SYSTEM_LOG_CLEAR: Service = Service("system_log/clear")
SYSTEM_LOG_WRITE: Service = Service("system_log/write")
TEMPLATE_RELOAD: Service = Service("template/reload")
TIME_SET_VALUE: Service = Service("time/set_value")
TIMER_CANCEL: Service = Service("timer/cancel")
TIMER_CHANGE: Service = Service("timer/change")
TIMER_FINISH: Service = Service("timer/finish")
TIMER_PAUSE: Service = Service("timer/pause")
TIMER_RELOAD: Service = Service("timer/reload")
TIMER_START: Service = Service("timer/start")
TODO_ADD_ITEM: Service = Service("todo/add_item")
TODO_GET_ITEMS: Service = Service("todo/get_items")
TODO_REMOVE_COMPLETED_ITEMS: Service = Service("todo/remove_completed_items")
TODO_REMOVE_ITEM: Service = Service("todo/remove_item")
TODO_UPDATE_ITEM: Service = Service("todo/update_item")
TTS_CLEAR_CACHE: Service = Service("tts/clear_cache")
TTS_CLOUD_SAY: Service = Service("tts/cloud_say")
TTS_GOOGLE_TRANSLATE_SAY: Service = Service("tts/google_translate_say")
TTS_SPEAK: Service = Service("tts/speak")
UI_LOVELACE_MINIMALIST_RELOAD: Service = Service("ui_lovelace_minimalist/reload")
UPDATE_CLEAR_SKIPPED: Service = Service("update/clear_skipped")
UPDATE_INSTALL: Service = Service("update/install")
UPDATE_SKIP: Service = Service("update/skip")
VACUUM_CLEAN_SPOT: Service = Service("vacuum/clean_spot")
VACUUM_LOCATE: Service = Service("vacuum/locate")
VACUUM_PAUSE: Service = Service("vacuum/pause")
VACUUM_RETURN_TO_BASE: Service = Service("vacuum/return_to_base")
VACUUM_SEND_COMMAND: Service = Service("vacuum/send_command")
VACUUM_SET_FAN_SPEED: Service = Service("vacuum/set_fan_speed")
VACUUM_START: Service = Service("vacuum/start")
VACUUM_STOP: Service = Service("vacuum/stop")
WEATHER_GET_FORECASTS: Service = Service("weather/get_forecasts")
ZHA_CLEAR_LOCK_USER_CODE: Service = Service("zha/clear_lock_user_code")
ZHA_DISABLE_LOCK_USER_CODE: Service = Service("zha/disable_lock_user_code")
ZHA_ENABLE_LOCK_USER_CODE: Service = Service("zha/enable_lock_user_code")
ZHA_ISSUE_ZIGBEE_CLUSTER_COMMAND: Service = Service("zha/issue_zigbee_cluster_command")
ZHA_ISSUE_ZIGBEE_GROUP_COMMAND: Service = Service("zha/issue_zigbee_group_command")
ZHA_PERMIT: Service = Service("zha/permit")
ZHA_REMOVE: Service = Service("zha/remove")
ZHA_SET_LOCK_USER_CODE: Service = Service("zha/set_lock_user_code")
ZHA_SET_ZIGBEE_CLUSTER_ATTRIBUTE: Service = Service("zha/set_zigbee_cluster_attribute")
ZHA_WARNING_DEVICE_SQUAWK: Service = Service("zha/warning_device_squawk")
ZHA_WARNING_DEVICE_WARN: Service = Service("zha/warning_device_warn")
ZONE_RELOAD: Service = Service("zone/reload")
