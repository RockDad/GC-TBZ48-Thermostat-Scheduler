"""Options for controlling the behavior of the tbz48_smnart_thermostat integration."""

import logging

from homeassistant.components.input_boolean import InputBoolean
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import homeassistant.helpers.entity_registry as er

from .const import DOMAIN, INTEGRATION_OPTIONS
from .helper import get_platform

_LOGGER = logging.getLogger(__name__)


async def async_unload_ib_entries(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload a input_boolean entry."""
    exit_result = True

    for entity_id in hass.states.async_entity_ids("input_boolean"):
        _LOGGER.info("Unloading: %s", entity_id)
        if entity_id.startswith(f"input_boolean.{DOMAIN}_"):
            hass.add_job(remove_entity, hass, entity_id)
    return exit_result


async def remove_entity(hass, entity_id):
    """Local remove_entity."""
    entity_registry = er.async_get(hass)
    entity_registry.async_remove(entity_id)


async def async_setup_entry_ib(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Local ayync_setup_entry() definition."""
    entities = []

    input_boolean_name = "input_boolean"

    for key in INTEGRATION_OPTIONS:
        name = key.replace("_", " ").title()
        name_technical = DOMAIN + "_" + key
        unique_key = "xyzzy"

        _LOGGER.info("Creating input_boolean entity: %s", key)

        input_boolean_instance = InputBoolean(
            {
                "name": name,
                "id": name_technical,
                "unique_id": input_boolean_name + "." + DOMAIN + "_" + key + unique_key,
                "default": False,
                "entry_id": input_boolean_name + "." + DOMAIN + "_" + key,
                "icon": "mdi:toggle-switch-off-outline",
            }
        )
        input_boolean_instance.editable = True
        entities.append(input_boolean_instance)
    # end for
    input_boolean_platform = get_platform(hass, input_boolean_name)

    await input_boolean_platform.async_add_entities(entities, update_before_add=True)
