"""Constants for the Immich Jobs Control integration."""

from datetime import timedelta

DOMAIN = "immich_jobs_control"

# Configuration Keys
CONF_HOST = "host"
CONF_API_KEY = "api_key"

# Default values
DEFAULT_NAME = "Immich"
SCAN_INTERVAL = timedelta(seconds=30)  # Frecuencia de actualización de estado

# Data Keys (used in the coordinator data store)
IMMICH_COORDINATOR = "coordinator"
IMMICH_CLIENT = "client"

# Job Status Attributes
ATTR_QUEUE_SIZE = "queue_size"
ATTR_MAX_CONCURRENCY = "max_concurrency"

