"""Options for controlling the behavior of the tbz48_smnart_thermostat integration."""

import logging

from homeassistant.components.input_boolean import InputBoolean
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

# from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DEVICE_ENTRY_TYPE,
    DEVICE_MANUFACTURER,
    DEVICE_MODEL,
    DEVICE_NAME,
    DOMAIN,
    INTEGRATION_OPTIONS,
)
from .helper import get_platform

_LOGGER = logging.getLogger(__name__)


class TBZ48Option(InputBoolean, RestoreEntity):
    """Class definition for tbz48_smart_thermostat options."""

    def __init__(
        self,
        name: str,
        unique_id: str,
        default: bool,
        entry_id: str,
        icon: str,
    ):
        self._attr_name = name.replace("_", " ").title()
        self._attr_unique_id = unique_id
        self._attr_native_value = default
        self._default = default
        self._attr_has_entity_name = True
        self._entry_id = entry_id

    @property
    def native_value(self):
        """Return the native value."""
        return self._attr_native_value

    async def async_set_native_value(self, value: bool) -> None:
        self._attr_native_value = value
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        if (last_state := await self.async_get_last_state()) is not None:
            try:
                self._attr_native_value = bool(last_state.state)
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
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    #    async_add_entities: AddEntitiesCallback,
):
    entities = []

    input_boolean_name = "input_boolean"

    for key in INTEGRATION_OPTIONS:
        name = key.replace("_", " ").title()
        # name = DOMAIN + "_" + name
        name_technical = DOMAIN + "_" + key
        _LOGGER.info("Creating input_boolean entity: %s", key)
        ib_data = {
            "id": name_technical,
            "name": name,
            "icon": "mdi:toggle-switch-off-outline",
        }
        input_boolean_instance = InputBoolean(ib_data)
        input_boolean_instance.editable = True
        input_boolean_instance.entity_id = input_boolean_name + "." + DOMAIN + "_" + key
        entities.append(input_boolean_instance)

        input_boolean_platform = get_platform(hass, input_boolean_name)

    await input_boolean_platform.async_add_entities(entities, update_before_add=True)
