from typing import NewType
Service  = NewType('UserId', str)
HOMEASSISTANT_SAVE_PERSISTENT_STATES: Service = Service("homeassistant/save_persistent_states")
HOMEASSISTANT_TURN_OFF: Service = Service("homeassistant/turn_off")
HOMEASSISTANT_TURN_ON: Service = Service("homeassistant/turn_on")
HOMEASSISTANT_TOGGLE: Service = Service("homeassistant/toggle")
HOMEASSISTANT_STOP: Service = Service("homeassistant/stop")
HOMEASSISTANT_RESTART: Service = Service("homeassistant/restart")
HOMEASSISTANT_CHECK_CONFIG: Service = Service("homeassistant/check_config")
HOMEASSISTANT_UPDATE_ENTITY: Service = Service("homeassistant/update_entity")
HOMEASSISTANT_RELOAD_CORE_CONFIG: Service = Service("homeassistant/reload_core_config")
HOMEASSISTANT_SET_LOCATION: Service = Service("homeassistant/set_location")
HOMEASSISTANT_RELOAD_CONFIG_ENTRY: Service = Service("homeassistant/reload_config_entry")
PERSISTENT_NOTIFICATION_CREATE: Service = Service("persistent_notification/create")
PERSISTENT_NOTIFICATION_DISMISS: Service = Service("persistent_notification/dismiss")
PERSISTENT_NOTIFICATION_MARK_READ: Service = Service("persistent_notification/mark_read")
SYSTEM_LOG_CLEAR: Service = Service("system_log/clear")
SYSTEM_LOG_WRITE: Service = Service("system_log/write")
LOGGER_SET_DEFAULT_LEVEL: Service = Service("logger/set_default_level")
LOGGER_SET_LEVEL: Service = Service("logger/set_level")
PERSON_RELOAD: Service = Service("person/reload")
FRONTEND_SET_THEME: Service = Service("frontend/set_theme")
FRONTEND_RELOAD_THEMES: Service = Service("frontend/reload_themes")
RECORDER_PURGE: Service = Service("recorder/purge")
RECORDER_PURGE_ENTITIES: Service = Service("recorder/purge_entities")
RECORDER_ENABLE: Service = Service("recorder/enable")
RECORDER_DISABLE: Service = Service("recorder/disable")
HASSIO_ADDON_START: Service = Service("hassio/addon_start")
HASSIO_ADDON_STOP: Service = Service("hassio/addon_stop")
HASSIO_ADDON_RESTART: Service = Service("hassio/addon_restart")
HASSIO_ADDON_UPDATE: Service = Service("hassio/addon_update")
HASSIO_ADDON_STDIN: Service = Service("hassio/addon_stdin")
HASSIO_HOST_SHUTDOWN: Service = Service("hassio/host_shutdown")
HASSIO_HOST_REBOOT: Service = Service("hassio/host_reboot")
HASSIO_BACKUP_FULL: Service = Service("hassio/backup_full")
HASSIO_BACKUP_PARTIAL: Service = Service("hassio/backup_partial")
HASSIO_RESTORE_FULL: Service = Service("hassio/restore_full")
HASSIO_RESTORE_PARTIAL: Service = Service("hassio/restore_partial")
CLOUD_REMOTE_CONNECT: Service = Service("cloud/remote_connect")
CLOUD_REMOTE_DISCONNECT: Service = Service("cloud/remote_disconnect")
GROUP_RELOAD: Service = Service("group/reload")
GROUP_SET: Service = Service("group/set")
GROUP_REMOVE: Service = Service("group/remove")
TTS_GOOGLE_TRANSLATE_SAY: Service = Service("tts/google_translate_say")
TTS_CLEAR_CACHE: Service = Service("tts/clear_cache")
TTS_CLOUD_SAY: Service = Service("tts/cloud_say")
UPDATE_INSTALL: Service = Service("update/install")
UPDATE_SKIP: Service = Service("update/skip")
UPDATE_CLEAR_SKIPPED: Service = Service("update/clear_skipped")
SCENE_RELOAD: Service = Service("scene/reload")
SCENE_APPLY: Service = Service("scene/apply")
SCENE_CREATE: Service = Service("scene/create")
SCENE_TURN_ON: Service = Service("scene/turn_on")
LOGBOOK_LOG: Service = Service("logbook/log")
TIMER_RELOAD: Service = Service("timer/reload")
TIMER_START: Service = Service("timer/start")
TIMER_PAUSE: Service = Service("timer/pause")
TIMER_CANCEL: Service = Service("timer/cancel")
TIMER_FINISH: Service = Service("timer/finish")
COUNTER_INCREMENT: Service = Service("counter/increment")
COUNTER_DECREMENT: Service = Service("counter/decrement")
COUNTER_RESET: Service = Service("counter/reset")
COUNTER_CONFIGURE: Service = Service("counter/configure")
ZONE_RELOAD: Service = Service("zone/reload")
SCRIPT_RELOAD: Service = Service("script/reload")
SCRIPT_TURN_ON: Service = Service("script/turn_on")
SCRIPT_TURN_OFF: Service = Service("script/turn_off")
SCRIPT_TOGGLE: Service = Service("script/toggle")
INPUT_TEXT_RELOAD: Service = Service("input_text/reload")
INPUT_TEXT_SET_VALUE: Service = Service("input_text/set_value")
INPUT_NUMBER_RELOAD: Service = Service("input_number/reload")
INPUT_NUMBER_SET_VALUE: Service = Service("input_number/set_value")
INPUT_NUMBER_INCREMENT: Service = Service("input_number/increment")
INPUT_NUMBER_DECREMENT: Service = Service("input_number/decrement")
INPUT_BOOLEAN_RELOAD: Service = Service("input_boolean/reload")
INPUT_BOOLEAN_TURN_ON: Service = Service("input_boolean/turn_on")
INPUT_BOOLEAN_TURN_OFF: Service = Service("input_boolean/turn_off")
INPUT_BOOLEAN_TOGGLE: Service = Service("input_boolean/toggle")
INPUT_BUTTON_RELOAD: Service = Service("input_button/reload")
INPUT_BUTTON_PRESS: Service = Service("input_button/press")
SCHEDULE_RELOAD: Service = Service("schedule/reload")
MEDIA_PLAYER_TURN_ON: Service = Service("media_player/turn_on")
MEDIA_PLAYER_TURN_OFF: Service = Service("media_player/turn_off")
MEDIA_PLAYER_TOGGLE: Service = Service("media_player/toggle")
MEDIA_PLAYER_VOLUME_UP: Service = Service("media_player/volume_up")
MEDIA_PLAYER_VOLUME_DOWN: Service = Service("media_player/volume_down")
MEDIA_PLAYER_MEDIA_PLAY_PAUSE: Service = Service("media_player/media_play_pause")
MEDIA_PLAYER_MEDIA_PLAY: Service = Service("media_player/media_play")
MEDIA_PLAYER_MEDIA_PAUSE: Service = Service("media_player/media_pause")
MEDIA_PLAYER_MEDIA_STOP: Service = Service("media_player/media_stop")
MEDIA_PLAYER_MEDIA_NEXT_TRACK: Service = Service("media_player/media_next_track")
MEDIA_PLAYER_MEDIA_PREVIOUS_TRACK: Service = Service("media_player/media_previous_track")
MEDIA_PLAYER_CLEAR_PLAYLIST: Service = Service("media_player/clear_playlist")
MEDIA_PLAYER_VOLUME_SET: Service = Service("media_player/volume_set")
MEDIA_PLAYER_VOLUME_MUTE: Service = Service("media_player/volume_mute")
MEDIA_PLAYER_MEDIA_SEEK: Service = Service("media_player/media_seek")
MEDIA_PLAYER_JOIN: Service = Service("media_player/join")
MEDIA_PLAYER_SELECT_SOURCE: Service = Service("media_player/select_source")
MEDIA_PLAYER_SELECT_SOUND_MODE: Service = Service("media_player/select_sound_mode")
MEDIA_PLAYER_PLAY_MEDIA: Service = Service("media_player/play_media")
MEDIA_PLAYER_SHUFFLE_SET: Service = Service("media_player/shuffle_set")
MEDIA_PLAYER_UNJOIN: Service = Service("media_player/unjoin")
MEDIA_PLAYER_REPEAT_SET: Service = Service("media_player/repeat_set")
INPUT_SELECT_RELOAD: Service = Service("input_select/reload")
INPUT_SELECT_SELECT_OPTION: Service = Service("input_select/select_option")
INPUT_SELECT_SELECT_NEXT: Service = Service("input_select/select_next")
INPUT_SELECT_SELECT_PREVIOUS: Service = Service("input_select/select_previous")
INPUT_SELECT_SELECT_FIRST: Service = Service("input_select/select_first")
INPUT_SELECT_SELECT_LAST: Service = Service("input_select/select_last")
INPUT_SELECT_SET_OPTIONS: Service = Service("input_select/set_options")
INPUT_DATETIME_RELOAD: Service = Service("input_datetime/reload")
INPUT_DATETIME_SET_DATETIME: Service = Service("input_datetime/set_datetime")
AUTOMATION_TRIGGER: Service = Service("automation/trigger")
AUTOMATION_TOGGLE: Service = Service("automation/toggle")
AUTOMATION_TURN_ON: Service = Service("automation/turn_on")
AUTOMATION_TURN_OFF: Service = Service("automation/turn_off")
AUTOMATION_RELOAD: Service = Service("automation/reload")
NOTIFY_PERSISTENT_NOTIFICATION: Service = Service("notify/persistent_notification")
NOTIFY_MOBILE_APP_GALAXY_S9: Service = Service("notify/mobile_app_galaxy_s9")
NOTIFY_NOTIFY: Service = Service("notify/notify")
CAST_SHOW_LOVELACE_VIEW: Service = Service("cast/show_lovelace_view")
DEVICE_TRACKER_SEE: Service = Service("device_tracker/see")
HUE_ACTIVATE_SCENE: Service = Service("hue/activate_scene")
HUE_HUE_ACTIVATE_SCENE: Service = Service("hue/hue_activate_scene")
SWITCH_TURN_OFF: Service = Service("switch/turn_off")
SWITCH_TURN_ON: Service = Service("switch/turn_on")
SWITCH_TOGGLE: Service = Service("switch/toggle")
BUTTON_PRESS: Service = Service("button/press")
REMOTE_TURN_OFF: Service = Service("remote/turn_off")
REMOTE_TURN_ON: Service = Service("remote/turn_on")
REMOTE_TOGGLE: Service = Service("remote/toggle")
REMOTE_SEND_COMMAND: Service = Service("remote/send_command")
REMOTE_LEARN_COMMAND: Service = Service("remote/learn_command")
REMOTE_DELETE_COMMAND: Service = Service("remote/delete_command")
LIGHT_TURN_ON: Service = Service("light/turn_on")
LIGHT_TURN_OFF: Service = Service("light/turn_off")
LIGHT_TOGGLE: Service = Service("light/toggle")
SPOTCAST_START: Service = Service("spotcast/start")
HUBITAT_CLEAR_CODE: Service = Service("hubitat/clear_code")
HUBITAT_SEND_COMMAND: Service = Service("hubitat/send_command")
HUBITAT_SET_CODE: Service = Service("hubitat/set_code")
HUBITAT_SET_CODE_LENGTH: Service = Service("hubitat/set_code_length")
HUBITAT_SET_ENTRY_DELAY: Service = Service("hubitat/set_entry_delay")
HUBITAT_SET_EXIT_DELAY: Service = Service("hubitat/set_exit_delay")
HUBITAT_SET_HSM: Service = Service("hubitat/set_hsm")
HUBITAT_SET_HUB_MODE: Service = Service("hubitat/set_hub_mode")
CLIMATE_TURN_ON: Service = Service("climate/turn_on")
CLIMATE_TURN_OFF: Service = Service("climate/turn_off")
CLIMATE_SET_HVAC_MODE: Service = Service("climate/set_hvac_mode")
CLIMATE_SET_PRESET_MODE: Service = Service("climate/set_preset_mode")
CLIMATE_SET_AUX_HEAT: Service = Service("climate/set_aux_heat")
CLIMATE_SET_TEMPERATURE: Service = Service("climate/set_temperature")
CLIMATE_SET_HUMIDITY: Service = Service("climate/set_humidity")
CLIMATE_SET_FAN_MODE: Service = Service("climate/set_fan_mode")
CLIMATE_SET_SWING_MODE: Service = Service("climate/set_swing_mode")
ALARM_CONTROL_PANEL_ALARM_DISARM: Service = Service("alarm_control_panel/alarm_disarm")
ALARM_CONTROL_PANEL_ALARM_ARM_HOME: Service = Service("alarm_control_panel/alarm_arm_home")
ALARM_CONTROL_PANEL_ALARM_ARM_AWAY: Service = Service("alarm_control_panel/alarm_arm_away")
ALARM_CONTROL_PANEL_ALARM_ARM_NIGHT: Service = Service("alarm_control_panel/alarm_arm_night")
ALARM_CONTROL_PANEL_ALARM_ARM_VACATION: Service = Service("alarm_control_panel/alarm_arm_vacation")
ALARM_CONTROL_PANEL_ALARM_ARM_CUSTOM_BYPASS: Service = Service("alarm_control_panel/alarm_arm_custom_bypass")
ALARM_CONTROL_PANEL_ALARM_TRIGGER: Service = Service("alarm_control_panel/alarm_trigger")
COVER_OPEN_COVER: Service = Service("cover/open_cover")
COVER_CLOSE_COVER: Service = Service("cover/close_cover")
COVER_SET_COVER_POSITION: Service = Service("cover/set_cover_position")
COVER_STOP_COVER: Service = Service("cover/stop_cover")
COVER_TOGGLE: Service = Service("cover/toggle")
COVER_OPEN_COVER_TILT: Service = Service("cover/open_cover_tilt")
COVER_CLOSE_COVER_TILT: Service = Service("cover/close_cover_tilt")
COVER_STOP_COVER_TILT: Service = Service("cover/stop_cover_tilt")
COVER_SET_COVER_TILT_POSITION: Service = Service("cover/set_cover_tilt_position")
COVER_TOGGLE_COVER_TILT: Service = Service("cover/toggle_cover_tilt")
FAN_TURN_ON: Service = Service("fan/turn_on")
FAN_TURN_OFF: Service = Service("fan/turn_off")
FAN_TOGGLE: Service = Service("fan/toggle")
FAN_INCREASE_SPEED: Service = Service("fan/increase_speed")
FAN_DECREASE_SPEED: Service = Service("fan/decrease_speed")
FAN_OSCILLATE: Service = Service("fan/oscillate")
FAN_SET_DIRECTION: Service = Service("fan/set_direction")
FAN_SET_PERCENTAGE: Service = Service("fan/set_percentage")
FAN_SET_PRESET_MODE: Service = Service("fan/set_preset_mode")
SELECT_SELECT_OPTION: Service = Service("select/select_option")
LOCK_UNLOCK: Service = Service("lock/unlock")
LOCK_LOCK: Service = Service("lock/lock")
LOCK_OPEN: Service = Service("lock/open")
