"""Platform for sensor integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.util.dt import parse_datetime
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
)

import logging
from typing import Final

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from .const import DOMAIN
from .coordinator import ZammadUpdateCoordinator
from .entity import ZammadEntity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Zammad sensors."""
    coordinator: ZammadUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(
        [
            ZammadSensor(coordinator, entry, sensor)
            for sensor in SENSORS
            if sensor.key in coordinator.data
        ]
    )

@dataclass
class ZammadSensorEntityDescription(SensorEntityDescription):
    """Describes Zammad sensor entity."""

    value_fn: Callable[[str | int | float], str | int | float | datetime] = (
        lambda value: value
    )

SENSORS: Final[list[ZammadSensorEntityDescription]] = [
    ZammadSensorEntityDescription(
        key="id",
        translation_key="zammad_self_user_id",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    ZammadSensorEntityDescription(
        key="organization_id",
        translation_key="zammad_self_user_org_id",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    ZammadSensorEntityDescription(
        key="login_failed",
        translation_key="zammad_self_login_failed",
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ZammadSensorEntityDescription(
        key="last_login",
        translation_key="zammad_self_last_login",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=parse_datetime
    ),
    ZammadSensorEntityDescription(
        key="updated_at",
        translation_key="zammad_self_updated_at",
        device_class=SensorDeviceClass.TIMESTAMP,
        value_fn=parse_datetime
    ),
    ZammadSensorEntityDescription(
        key="notifications",
        translation_key="zammad_self_notifications",
        state_class=SensorStateClass.MEASUREMENT,
    )
]

class ZammadSensor(ZammadEntity, SensorEntity):
    """Represents a Zammad sensor."""

    entity_description: ZammadSensorEntityDescription

    @property
    def native_value(self) -> str | int | float | datetime:
        """Return the state for this sensor."""
        val = self.coordinator.data.get(self.entity_description.key)
        return self.entity_description.value_fn(val)