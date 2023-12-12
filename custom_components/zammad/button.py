"""Platform for button integration."""
from homeassistant.exceptions import HomeAssistantError
from homeassistant.components.button import ButtonEntity, ButtonEntityDescription

import logging
from typing import Final

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime
from zammad_py.api import OnlineNotification

from .const import DOMAIN, INITIAL_USER_ID
from .coordinator import ZammadUpdateCoordinator
from .entity import ZammadEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Zammad buttons."""
    coordinator: ZammadUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([ZammadButton(coordinator, entry, button) for button in BUTTONS])


@dataclass
class ZammadButtonEntityDescription(ButtonEntityDescription):
    """Describes Zammad button entity."""

    value_fn: Callable[
        [str | int | float], str | int | float | datetime
    ] = lambda value: value


BUTTONS: Final[list[ZammadButtonEntityDescription]] = [
    ZammadButtonEntityDescription(
        key="mark_all_read",
        translation_key="zammad_self_mark_notifications_read",
    )
]


class ZammadButton(ZammadEntity, ButtonEntity):
    """Represents a Zammad button."""

    entity_description: ZammadButtonEntityDescription

    async def _clear_notifications(self, zammad_client, zammad_user_id) -> None:
        # Get available notifications
        zammad_notifications = await self.hass.async_add_executor_job(
            OnlineNotification(connection=zammad_client).all
        )

        for notification in zammad_notifications:
            if not notification["seen"]:
                # Update 'seen' field to be True
                await self.hass.async_add_executor_job(
                    OnlineNotification(connection=zammad_client).update,
                    notification["id"],
                    {"seen": True},
                )

    async def async_press(self) -> None:
        """Handle the button press."""
        # Get connection details
        zammad_client = self.coordinator.client
        zammad_user_id = self.coordinator.zammad_user_id
        if zammad_user_id == INITIAL_USER_ID:
            raise HomeAssistantError("User ID not available")

        match self.entity_description.key:
            case "mark_all_read":
                await self._clear_notifications(zammad_client, zammad_user_id)
