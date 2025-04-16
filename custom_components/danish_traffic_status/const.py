"""Constants for the Danish Traffic Status integration."""

DOMAIN = "danish_traffic_status"
DEFAULT_NAME = "Danish Traffic Status"
DEFAULT_SCAN_INTERVAL = 15  # minutes

CONF_TRAIN_LINES = "train_lines"
CONF_METRO_LINES = "metro_lines"

DEFAULT_TRAIN_LINES = ["C"]
DEFAULT_METRO_LINES = ["M1/M2"]

ATTR_LINE = "line"
ATTR_STATUS = "status"
ATTR_LAST_UPDATED = "last_updated"
ATTR_MESSAGE = "message"
ATTR_URL = "url"
