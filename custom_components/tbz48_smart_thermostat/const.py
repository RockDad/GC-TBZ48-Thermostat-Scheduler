"""Constant definitions for tbz48_smart_thermostat."""

DOMAIN = "tbz48_smart_thermostat"
PLATFORMS = [
    "number",
    "select",
    "time",
]

INTEGRATION_OPTIONS = [
    "enable_multi_room_strategy",
    "enable_eco_temperatures",
    "enable_external_sensor_strategy",
]

# Device
DEVICE_NAME = "GC-TBZ48 Smart Thermostat"
DEVICE_MANUFACTURER = "Custom"
DEVICE_MODEL = "Smart Thermostat Scheduler"
DEVICE_ENTRY_TYPE = "service"

# Temperature and Tolerance
STEP_MINOR = 0.01
STEP_MAJOR = 0.5
STEP_WHOLE = 1.0
DEFAULT_TOLERANCE = 1.0
DEFAULT_TOLERANCE_MIN = 0.5
DEFAULT_TOLERANCE_MAX_C = 5.0
DEFAULT_TOLERANCE_MAX_F = 10
SETPOINT_RANGE_MIN = 3
SETPOINT_RANGE_MAX = 15
ECO_RANGE_MIN = 55
ECO_RANGE_MAX = 85
DEFAULT_ECO_MIN = ECO_RANGE_MIN + 5
DEFAULT_ECO_MAX = ECO_RANGE_MAX - 5
DEFAULT_EXTERNAL_MIN = 68
DEFAULT_EXTERNAL_MAX = 78

# Time Settings
DEFAULT_TIME_STRING = "06:00"

# Sensor Setting
DEFAULT_SENSOR = "sensor.none_found"
SENSOR_TYPE_TEMPERATURE = "temperature"
UNIT_CELSIUS = "°C"
UNIT_FARENHEIT = "°F"

# Thermostat state
STATE_OPTIONS = ["idle", "heat", "cool", "eco"]
STATE_DEFAULT = "idle"

# HBZ48  Thermostat State
TBZ48_STATE_OPTIONS = [
    "idle",
    "heating",
    "cooling",
    "off",
    "preheating",
    "drying",
    "fan",
    "defrosting",
]
TBZ48_STATE_DEFAULT = "idle"
