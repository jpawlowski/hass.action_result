"""Constants for service_result."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

# Integration metadata
DOMAIN = "service_result"
ATTRIBUTION = "Data provided by Home Assistant service calls"

# Platform parallel updates - applied to all platforms
PARALLEL_UPDATES = 1

# Config entry data keys
CONF_NAME = "name"
CONF_SERVICE_ACTION = "service_action"  # New: stores the action selector result
CONF_SERVICE_DATA_YAML = "service_data_yaml"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_RESPONSE_DATA_PATH = "response_data_path"  # JSON path into response data
CONF_ATTRIBUTE_NAME = "attribute_name"  # Custom name for the data attribute

# Legacy config entry data keys (for migration)
CONF_SERVICE_DOMAIN = "service_domain"
CONF_SERVICE_NAME = "service_name"

# Default configuration values
DEFAULT_SCAN_INTERVAL_SECONDS = 300  # 5 minutes
DEFAULT_ATTRIBUTE_NAME = "data"

# Entity state values
STATE_OK = "ok"
STATE_ERROR = "error"
