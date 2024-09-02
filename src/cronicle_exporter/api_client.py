from typing import Dict, Any, List
import logging
import requests


class ApiClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key}

    def get_schedule(self) -> List[Dict[str, Any]]:
        """
        Fetch schedule events from the Cronicle API.

        Returns:
        List[Dict[str, Any]]: A list of schedule event objects.
        """
        endpoint = f"{self.base_url}/api/app/get_schedule/v1"

        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            return self._parse_schedule_response(response.json())
        except requests.RequestException as e:
            logging.error(f"Error fetching schedule: {e}")
            return []

    def _parse_schedule_response(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        if data.get("code") == 0 and "rows" in data:
            return data["rows"]
        else:
            logging.error(f"Unexpected response format: {data}")
            return []

    def get_last_event(self, event_id: str) -> Dict[str, Any]:
        """
        Fetch the last event history from the Cronicle API.

        Args:
        event_id (str): The ID of the event to fetch history for.

        Returns:
        Dict[str, Any]: The last event history object, or an empty dict if there's an error.
        """
        endpoint = f"{self.base_url}/api/app/get_event_history/v1"
        params = {"id": event_id, "limit": 1}

        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            return self._parse_last_event_response(response.json())
        except requests.RequestException as e:
            logging.error(f"Error fetching last event: {e}")
            return {}

    def _parse_last_event_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if data.get("code") == 0 and "rows" in data and len(data["rows"]) > 0:
            return data["rows"][0]
        else:
            logging.error(f"Unexpected response format or no events: {data}")
            return {}
