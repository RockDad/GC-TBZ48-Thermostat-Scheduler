import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import PLATFORMS, DOMAIN
from .helper import create_platform, get_platform
from .input_boolean import async_setup_entry_ib
from .input_boolean import async_unload_ib_entries

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Smart Thermostat component!"""
    hass.states.async_set(DOMAIN + ".world", "Paulus")
    setup_platform(hass, "input_boolean")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Smart Thermostat from a config entry."""
    await async_setup_entry_ib(hass, entry, None)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload Smart Thermostat entry."""
    unload_options = await async_unload_ib_entries(hass, entry)
    unload_select = await hass.config_entries.async_forward_entry_unload(
        entry, "select"
    )
    unload_number = await hass.config_entries.async_forward_entry_unload(
        entry, "number"
    )
    unload_time = await hass.config_entries.async_forward_entry_unload(entry, "time")

    return unload_select and unload_number and unload_time and unload_options


def setup_platform(hass: HomeAssistant, name):
    platform = get_platform(hass, name)

    if platform is None:
        create_platform(hass, name)
