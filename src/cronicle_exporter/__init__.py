import click
import logging
import requests
from typing import Dict, Any, List

# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_schedule(url: str, api_key: str) -> List[Dict[str, Any]]:
    """
    Fetch schedule events from the Cronicle API.

    Args:
    url (str): The base URL of the Cronicle API.
    api_key (str): The API key for authentication.

    Returns:
    List[Dict[str, Any]]: A list of schedule event objects.
    """
    endpoint = f"{url}/api/app/get_schedule/v1"
    headers = {"X-API-Key": api_key}

    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return _parse_schedule_response(response.json())
    except requests.RequestException as e:
        logging.error(f"Error fetching schedule: {e}")
        return []


def _parse_schedule_response(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    if data.get("code") == 0 and "rows" in data:
        return data["rows"]
    else:
        logging.error(f"Unexpected response format: {data}")
        return []


@click.command()
@click.option("--port", default=8123, help="The port to listen on.")
@click.option("--url", required=True, help="The base URL of the Cronicle API.")
@click.option("--api-key", required=True, help="The API key for authentication.")
def main(port: int, url: str, api_key: str) -> int:
    print(f"Fetching schedule from {url}")
    schedule = get_schedule(url, api_key)
    print(f"Retrieved {len(schedule)} schedule events")
    print(f"Cronicle-exporter listening on port {port}")
    # TODO: Implement exporter logic here
    return 0


if __name__ == "__main__":
    main()
