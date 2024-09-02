import click
import logging

from cronicle_exporter.api_client import ApiClient

# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@click.command()
@click.option("--port", default=8123, help="The port to listen on.")
@click.option("--url", required=True, help="The base URL of the Cronicle API.")
@click.option("--api-key", required=True, help="The API key for authentication.")
def main(port: int, url: str, api_key: str) -> int:
    logging.info(f"Initializing API client with base URL: {url}")
    api_client = ApiClient(url, api_key)

    logging.info("Fetching schedule")
    schedule = api_client.get_schedule()
    logging.info(f"Retrieved {len(schedule)} schedule events")
    logging.info(f"Cronicle-exporter listening on port {port}")
    # TODO: Implement exporter logic here
    return 0


if __name__ == "__main__":
    main()
