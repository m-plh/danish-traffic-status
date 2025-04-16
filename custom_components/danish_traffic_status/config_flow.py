"""Config flow for Danish Traffic Status integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
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


class DanishTrafficStatusConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Danish Traffic Status."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input.get(CONF_NAME, DEFAULT_NAME),
                data=user_input,
            )

        # Provide default values
        data_schema = vol.Schema(
            {
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Optional(
                    CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL
                ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
                vol.Optional(
                    CONF_TRAIN_LINES, default=", ".join(DEFAULT_TRAIN_LINES)
                ): str,
                vol.Optional(
                    CONF_METRO_LINES, default=", ".join(DEFAULT_METRO_LINES)
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return DanishTrafficStatusOptionsFlowHandler(config_entry)


class DanishTrafficStatusOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Danish Traffic Status."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # Process train and metro lines from comma-separated strings to lists
            train_lines = [line.strip() for line in user_input.get(CONF_TRAIN_LINES, "").split(",") if line.strip()]
            metro_lines = [line.strip() for line in user_input.get(CONF_METRO_LINES, "").split(",") if line.strip()]
            
            return self.async_create_entry(
                title="",
                data={
                    CONF_SCAN_INTERVAL: user_input.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
                    CONF_TRAIN_LINES: train_lines,
                    CONF_METRO_LINES: metro_lines,
                },
            )

        options = {
            vol.Optional(
                CONF_SCAN_INTERVAL,
                default=self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            ): vol.All(vol.Coerce(int), vol.Range(min=5, max=60)),
            vol.Optional(
                CONF_TRAIN_LINES,
                default=", ".join(self.config_entry.options.get(CONF_TRAIN_LINES, DEFAULT_TRAIN_LINES)),
            ): str,
            vol.Optional(
                CONF_METRO_LINES,
                default=", ".join(self.config_entry.options.get(CONF_METRO_LINES, DEFAULT_METRO_LINES)),
            ): str,
        }

        return self.async_show_form(step_id="init", data_schema=vol.Schema(options))
