"""
Custom integration to integrate Zammad with Home Assistant.
"""

from aiohttp.client_exceptions import ClientConnectorError
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.const import CONF_URL, CONF_USERNAME, CONF_PASSWORD

import asyncio
import logging
import json
from requests.exceptions import HTTPError
from zammad_py import ZammadAPI

from .const import (
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
    HUMAN_ERR_MSG_FIELD,
)
from .coordinator import ZammadUpdateCoordinator
from .utils import get_url_from_options

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    url = get_url_from_options(entry.data.get(CONF_URL))
    username = entry.data.get(CONF_USERNAME)
    password = entry.data.get(CONF_PASSWORD)

    try:
        client = ZammadAPI(url=url, username=username, password=password)
        await hass.async_add_executor_job(client.user.me)
    except HTTPError as exc:
        error_json = json.loads(exc.args[0])
        raise ConfigEntryAuthFailed(error_json[HUMAN_ERR_MSG_FIELD])
    except ClientConnectorError as exception:
        raise ConfigEntryNotReady from exception

    coordinator = ZammadUpdateCoordinator(hass, client, entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
