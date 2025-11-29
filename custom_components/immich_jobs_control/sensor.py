"""
Home Assistant Sensor platform for Immich Jobs Control.
Provides a sensor to show the global job status (running/idle).
"""
import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEFAULT_NAME, IMMICH_COORDINATOR, ATTR_QUEUE_SIZE
from .immich_api import ImmichAPIClient

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Immich Jobs Status sensor platform."""
    
    # Retrieve the coordinator instance from Home Assistant data
    coordinator = hass.data[DOMAIN][IMMICH_COORDINATOR]

    async_add_entities([ImmichJobStatusSensor(coordinator)])

class ImmichJobStatusSensor(CoordinatorEntity, SensorEntity):
    """Representation of the global Immich Job Status sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = f"{DEFAULT_NAME} Global Job Status"
        self._attr_unique_id = f"{DOMAIN}_global_status"
        self._attr_icon = "mdi:briefcase-clock"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return "unavailable"

        queue_count = self.coordinator.data.get('queueCount', 0)
        
        # Check if any job is marked as running
        is_any_job_running = any(
            job.get('isRunning', False) or job.get('queueSize', 0) > 0
            for job in self.coordinator.data.get('jobStatus', [])
        )
        
        if queue_count > 0 or is_any_job_running:
            return "running"
        return "idle"

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        if self.coordinator.data is None:
            return {}

        attrs = {}
        attrs[ATTR_QUEUE_SIZE] = self.coordinator.data.get('queueCount', 0)

        # Add status of individual jobs to attributes
        for job in self.coordinator.data.get('jobStatus', []):
            job_name = job.get('jobName', 'unknown').replace('-', '_')
            attrs[f"{job_name}_status"] = "Running" if job.get('isRunning') else "Idle"
            attrs[f"{job_name}_queue"] = job.get('queueSize', 0)
            attrs[f"{job_name}_paused"] = job.get('paused', False)

        return attrs

