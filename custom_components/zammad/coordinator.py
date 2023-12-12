"""Data update coordinator for the Nextcloud integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

import logging
from typing import Any
from zammad_py import ZammadAPI
from zammad_py.api import OnlineNotification

from .const import DEFAULT_SCAN_INTERVAL, INITIAL_USER_ID

_LOGGER = logging.getLogger(__name__)


class ZammadUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Zammad data update coordinator."""

    def __init__(
        self, hass: HomeAssistant, client: ZammadAPI, entry: ConfigEntry
    ) -> None:
        """Initialize the Zammad coordinator."""
        self.client = client
        self.url = entry.data[CONF_URL]
        self.zammad_user_id = INITIAL_USER_ID

        super().__init__(
            hass,
            _LOGGER,
            name=self.url,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch all Zammad data."""

        zammad_data = await self.hass.async_add_executor_job(self.client.user.me)
        self.zammad_user_id = zammad_data["id"]
        zammad_notifications = await self.hass.async_add_executor_job(
            OnlineNotification(connection=self.client).all
        )

        unread_notifs = 0
        for notification in zammad_notifications:
            if (
                not notification["seen"]
                and notification["user_id"] == self.zammad_user_id
            ):
                unread_notifs += 1

        zammad_data["notifications"] = unread_notifs

        return zammad_data
