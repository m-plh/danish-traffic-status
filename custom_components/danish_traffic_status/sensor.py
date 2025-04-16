"""Sensor platform for Danish Traffic Status integration."""
import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    ATTR_LINE,
    ATTR_STATUS,
    ATTR_LAST_UPDATED,
    ATTR_MESSAGE,
    ATTR_URL,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Set up Danish Traffic Status sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    # Add train sensors
    for line in coordinator.train_lines:
        entities.append(TrainStatusSensor(coordinator, line))

    # Add metro sensors
    for line in coordinator.metro_lines:
        entities.append(MetroStatusSensor(coordinator, line))

    async_add_entities(entities)


class TrafficStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Traffic Status sensor."""

    def __init__(self, coordinator, line, line_type):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._line = line
        self._line_type = line_type
        self._attr_unique_id = f"{DOMAIN}_{line_type}_{line}"
        self._attr_name = f"{line_type.capitalize()} Line {line} Status"
        self._attr_icon = "mdi:train" if line_type == "train" else "mdi:subway"

    @property
    def available(self):
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def state(self):
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return "unknown"
        
        status_data = self.coordinator.data.get(self._line_type, {}).get(self._line)
        if not status_data:
            return "unknown"
        
        return "normal" if not self._has_disruption(status_data) else "disruption"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {
            ATTR_LINE: self._line,
        }
        
        if self.coordinator.data:
            status_data = self.coordinator.data.get(self._line_type, {}).get(self._line)
            if status_data:
                attrs[ATTR_LAST_UPDATED] = datetime.now().isoformat()
                attrs.update(self._get_attributes(status_data))
        
        return attrs

    def _has_disruption(self, status_data):
        """Check if there is a disruption based on status data."""
        raise NotImplementedError("Subclasses must implement this method")

    def _get_attributes(self, status_data):
        """Get attributes from status data."""
        raise NotImplementedError("Subclasses must implement this method")


class TrainStatusSensor(TrafficStatusSensor):
    """Representation of a Train Status sensor."""

    def __init__(self, coordinator, line):
        """Initialize the sensor."""
        super().__init__(coordinator, line, "train")

    def _has_disruption(self, status_data):
        """Check if there is a disruption based on train status data."""
        return bool(status_data.get("body") and status_data.get("url"))

    def _get_attributes(self, status_data):
        """Get attributes from train status data."""
        attrs = {}
        
        if "body" in status_data:
            attrs[ATTR_MESSAGE] = status_data["body"]
        
        if "url" in status_data:
            attrs[ATTR_URL] = status_data["url"]
            
        if "urgent" in status_data:
            attrs["urgent"] = status_data["urgent"]
            
        return attrs


class MetroStatusSensor(TrafficStatusSensor):
    """Representation of a Metro Status sensor."""

    def __init__(self, coordinator, line):
        """Initialize the sensor."""
        super().__init__(coordinator, line, "metro")

    def _has_disruption(self, status_data):
        """Check if there is a disruption based on metro status data."""
        return bool(status_data.get("name") and not status_data.get("isClearMessage", False))

    def _get_attributes(self, status_data):
        """Get attributes from metro status data."""
        attrs = {}
        
        if "name" in status_data:
            attrs[ATTR_STATUS] = status_data["name"]
            
        if "type" in status_data:
            attrs[ATTR_MESSAGE] = status_data["type"]
            
        if "icon" in status_data:
            attrs["icon"] = status_data["icon"]
            
        return attrs
