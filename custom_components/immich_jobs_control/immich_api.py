"""
Immich API client for Home Assistant Custom Component.
Manages communication with the Immich server, specifically for job control and status.
"""
import logging
import requests
from typing import Any, Dict, List, Optional

_LOGGER = logging.getLogger(__name__)

class ImmichAPIClient:
    """Client to interact with the Immich API."""

    def __init__(self, host: str, api_key: str):
        """Initialize the client."""
        self.base_url = host.rstrip('/')
        self.headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json',
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Generic method to make API requests."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.request(method, url, headers=self.headers, json=data, timeout=10)
            response.raise_for_status()
            # Immich status endpoints return JSON, but pause/resume sometimes return 200 with no content.
            return response.json() if response.content else {"status": "ok"}
        except requests.exceptions.Timeout:
            _LOGGER.error("Timeout connecting to Immich server at %s", url)
            return None
        except requests.exceptions.HTTPError as err:
            _LOGGER.error("HTTP Error for %s: %s (Status: %d)", url, err, response.status_code)
            return None
        except requests.exceptions.RequestException as err:
            _LOGGER.error("Error connecting to Immich server at %s: %s", url, err)
            return None

    def get_all_job_status(self) -> Optional[Dict[str, Any]]:
        """
        Get the status of all jobs from Immich.
        Endpoint: GET /api/job/status
        Returns: { 'queueCount': int, 'jobStatus': List[JobStatus] }
        """
        _LOGGER.debug("Fetching all job status from Immich.")
        return self._make_request("GET", "/api/job/status")

    def pause_job(self, job_name: str) -> bool:
        """Send command to pause a specific background job."""
        _LOGGER.info("Attempting to PAUSE job: %s", job_name)
        response = self._make_request("POST", f"/api/job/{job_name}/pause")
        return response is not None

    def resume_job(self, job_name: str) -> bool:
        """Send command to resume a specific background job."""
        _LOGGER.info("Attempting to RESUME job: %s", job_name)
        response = self._make_request("POST", f"/api/job/{job_name}/resume")
        return response is not None

    def check_connection(self) -> bool:
        """Check server connectivity using the ping endpoint."""
        response = self._make_request("GET", "/api/system/ping")
        return response is not None and response.get('res') == 'pong'

