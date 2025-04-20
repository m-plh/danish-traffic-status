"""The Danish Traffic Status integration."""
import asyncio
import logging
from datetime import timedelta

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME, CONF_SCAN_INTERVAL

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_SCAN_INTERVAL,
    CONF_TRAIN_LINES,
    CONF_METRO_LINES,
    DEFAULT_TRAIN_LINES,
    DEFAULT_METRO_LINES,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): cv.positive_int,
                vol.Optional(CONF_TRAIN_LINES, default=DEFAULT_TRAIN_LINES): cv.ensure_list,
                vol.Optional(CONF_METRO_LINES, default=DEFAULT_METRO_LINES): cv.ensure_list,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Danish Traffic Status component."""
    if DOMAIN not in config:
        return True

    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Danish Traffic Status from a config entry."""
    coordinator = DanishTrafficStatusDataUpdateCoordinator(hass, entry)
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(
        entry, PLATFORMS)
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok


class DanishTrafficStatusDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Danish Traffic Status data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize the data update coordinator."""
        self.entry = entry
        self.train_lines = entry.options.get(CONF_TRAIN_LINES, DEFAULT_TRAIN_LINES)
        self.metro_lines = entry.options.get(CONF_METRO_LINES, DEFAULT_METRO_LINES)
        self.train_status = {}
        self.metro_status = {}
        
        scan_interval = timedelta(
            minutes=entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=scan_interval,
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            from .traffic_status import TrainStatusService, MetroStatusService
            
            train_service = TrainStatusService()
            metro_service = MetroStatusService()
            
            train_data = {}
            metro_data = {}
            
            # Fetch train status for each configured line
            for line in self.train_lines:
                train_status = await self.hass.async_add_executor_job(
                    train_service.get_status, line
                )
                train_data[line] = train_status
            
            # Fetch metro status for each configured line
            for line in self.metro_lines:
                metro_status = await self.hass.async_add_executor_job(
                    metro_service.get_status, line
                )
                metro_data[line] = metro_status
            
            # Check for changes and send notifications
            for line, status in train_data.items():
                if line in self.train_status and self.train_status[line] != status:
                    if status and status.get("url") != self.train_status[line].get("url"):
                        self._notify_status_change(
                            f"Line {line} changes",
                            status.get("body", "No changes"),
                            status.get("url", "")
                        )
            
            for line, status in metro_data.items():
                if line in self.metro_status and self.metro_status[line] != status:
                    if status and status.get("name") != self.metro_status[line].get("name"):
                        self._notify_status_change(
                            status.get("type", "Metro status"),
                            status.get("name", ""),
                            ""
                        )
            
            # Update stored status
            self.train_status = train_data
            self.metro_status = metro_data
            
            return {
                "train": train_data,
                "metro": metro_data,
            }
            
        except Exception as err:
            _LOGGER.error("Error fetching traffic status data: %s", err)
            raise UpdateFailed(f"Error fetching traffic status data: {err}")
    
    def _notify_status_change(self, title, message, url=""):
        """Send notification through Home Assistant."""
        self.hass.services.call(
            "notify",
            "notify",  # This will use the default notification service
            {
                "title": title,
                "message": message,
                "data": {"url": url} if url else {},
            },
        )
