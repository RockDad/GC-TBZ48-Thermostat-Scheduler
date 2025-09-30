"""Number entity support for tbz48_smart_thermostat."""

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DEFAULT_ECO_MAX,
    DEFAULT_ECO_MIN,
    DEFAULT_TOLERANCE,
    DEFAULT_TOLERANCE_MAX_C,
    DEFAULT_TOLERANCE_MAX_F,
    DEFAULT_TOLERANCE_MIN,
    DEVICE_ENTRY_TYPE,
    DEVICE_MANUFACTURER,
    DEVICE_MODEL,
    DEVICE_NAME,
    DOMAIN,
    ECO_RANGE_MAX,
    ECO_RANGE_MIN,
    SETPOINT_RANGE_MAX,
    SETPOINT_RANGE_MIN,
    STEP_MAJOR,
    STEP_MINOR,
    STEP_WHOLE,
    UNIT_CELSIUS,
    UNIT_FARENHEIT,
)


class TBZ48Number(NumberEntity, RestoreEntity):
    def __init__(
        self,
        name: str,
        unique_id: str,
        default: float,
        min_v: float,
        max_v: float,
        step: float,
        entry_id: str,
        unit: str,
    ):
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = unique_id
        self._attr_native_value = default
        self._default = default
        self._attr_native_unit_of_measurement = unit
        self._attr_native_min_value = min_v
        self._attr_native_max_value = max_v
        self._attr_native_step = step
        self._attr_has_entity_name = True
        self._entry_id = entry_id

    @property
    def native_value(self):
        """Return the native value."""
        return self._attr_native_value

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        if (last_state := await self.async_get_last_state()) is not None:
            try:
                self._attr_native_value = float(last_state.state)
            except ValueError:
                self._attr_native_value = self._default

    @property
    def device_info(self):
        """Define the tbz48_smart_thermostat device."""
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": DEVICE_NAME,
            "manufacturer": DEVICE_MANUFACTURER,
            "model": DEVICE_MODEL,
            "entry_type": DEVICE_ENTRY_TYPE,
        }


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    entities = []

    # User-defined temperature configuration
    temp_min = entry.data["temp_min"]
    temp_max = entry.data["temp_max"]
    temp_default = entry.data["temp_default"]
    unit = entry.data.get("temperature_unit", UNIT_CELSIUS)

    # Scheduled temperature slots
    for i in range(1, 5):
        for prefix in ("m_f", "s_s"):
            key = f"{prefix}_temperature_{i}"
            val = entry.data[key]
            entities.append(
                TBZ48Number(
                    name=key.replace("_", " ").title(),
                    unique_id=key,
                    default=val,
                    min_v=temp_min,
                    max_v=temp_max,
                    step=STEP_MAJOR,
                    entry_id=entry.entry_id,
                    unit=unit,
                )
            )

    tolerance_max = entry.data.get(
        "tolerance_max",
        DEFAULT_TOLERANCE_MAX_F if unit == UNIT_FARENHEIT else DEFAULT_TOLERANCE_MAX_C,
    )

    # Global numeric configuration entities
    fixed_ranges = {
        # Tolerances: hardcoded ranges
        "tolerance_cool": (
            DEFAULT_TOLERANCE,
            DEFAULT_TOLERANCE_MIN,
            tolerance_max,
            STEP_MAJOR,
        ),
        "tolerance_heat": (
            DEFAULT_TOLERANCE,
            DEFAULT_TOLERANCE_MIN,
            tolerance_max,
            STEP_MAJOR,
        ),
        "heat_setpoint_range": (
            entry.data["heat_setpoint_range"],
            SETPOINT_RANGE_MIN,
            SETPOINT_RANGE_MAX,
            STEP_WHOLE,
        ),
        "cool_setpoint_range": (
            entry.data["cool_setpoint_range"],
            SETPOINT_RANGE_MIN,
            SETPOINT_RANGE_MAX,
            STEP_WHOLE,
        ),
        "eco_temperature_min": [
            DEFAULT_ECO_MIN,
            ECO_RANGE_MIN,
            ECO_RANGE_MAX,
            STEP_WHOLE,
        ],
        "eco_temperature_max": [
            DEFAULT_ECO_MAX,
            ECO_RANGE_MIN,
            ECO_RANGE_MAX,
            STEP_WHOLE,
        ],
        # Temperatures: user-defined limits
        "current_temperature": (
            entry.data["current_temperature"],
            temp_min,
            temp_max,
            STEP_MINOR,
        ),
        "current_target_temperature": (
            entry.data["current_target_temperature"],
            temp_min,
            temp_max,
            STEP_MAJOR,
        ),
        "adjusted_target_temperature": (temp_default, temp_min, temp_max, STEP_MAJOR),
        "adjusted_cool_temperature": (
            entry.data["adjusted_cool_temperature"],
            temp_min,
            temp_max,
            STEP_MAJOR,
        ),
        "adjusted_heat_temperature": (
            entry.data["adjusted_heat_temperature"],
            temp_min,
            temp_max,
            STEP_MAJOR,
        ),
    }

    for key, (default, min_v, max_v, step) in fixed_ranges.items():
        name = key.replace("_", " ").title()
        entities.append(
            TBZ48Number(
                name=name,
                unique_id=key,
                default=default,
                min_v=min_v,
                max_v=max_v,
                step=step,
                entry_id=entry.entry_id,
                unit=unit,
            )
        )

    async_add_entities(entities, update_before_add=True)
