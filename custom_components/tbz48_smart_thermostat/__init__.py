import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import PLATFORMS
from .helper import create_platform, get_platform
from .input_boolean import async_setup_entry as async_setup_entry_ib

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Smart Thermostat component!"""
    setup_platform(hass, "input_boolean")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Smart Thermostat from a config entry."""
    # Properly await platform setups
    # if entry.domain == "option":
    #    await async_setup_entry_ib(hass, entry)
    # else:
    await async_setup_entry_ib(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload Smart Thermostat entry."""
    unload_select = await hass.config_entries.async_forward_entry_unload(
        entry, "select"
    )
    unload_number = await hass.config_entries.async_forward_entry_unload(
        entry, "number"
    )
    unload_time = await hass.config_entries.async_forward_entry_unload(entry, "time")
    unload_options = await hass.config_entries.async_forward_entry_unload(
        entry, "input_boolean"
    )
    return unload_select and unload_number and unload_time and unload_options


def setup_platform(hass: HomeAssistant, name):
    platform = get_platform(hass, name)

    if platform is None:
        create_platform(hass, name)
