"""Summary binary data from Zammad."""
from typing import Final

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import ZammadUpdateCoordinator
from .entity import ZammadEntity

BINARY_SENSORS: Final[list[BinarySensorEntityDescription]] = [
    BinarySensorEntityDescription(
        key="out_of_office",
        translation_key="zammad_self_out_of_office",
    ),
    BinarySensorEntityDescription(
        key="verified",
        translation_key="zammad_self_verified",
    ),
    BinarySensorEntityDescription(
        key="active",
        translation_key="zammad_self_active",
    ),
    BinarySensorEntityDescription(
        key="vip",
        translation_key="zammad_self_vip",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Zammad binary sensors."""
    coordinator: ZammadUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            ZammadBinarySensor(coordinator, entry, sensor)
            for sensor in BINARY_SENSORS
            if sensor.key in coordinator.data
        ]
    )


class ZammadBinarySensor(ZammadEntity, BinarySensorEntity):
    """Represents a Nextcloud binary sensor."""

    @property
    def is_on(self) -> bool:
        """Return true if the binary sensor is on."""
        val = self.coordinator.data.get(self.entity_description.key)
        return val is True or val == "yes"
