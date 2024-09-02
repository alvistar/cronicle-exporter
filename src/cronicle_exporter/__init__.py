import time

import click
import logging
from prometheus_client import start_http_server, Gauge
from cronicle_exporter.api_client import ApiClient

# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define Prometheus metrics
TIME_START = Gauge("cronicle_event_time_start", "Event start time", ["event_title"])
ELAPSED = Gauge("cronicle_event_elapsed", "Event elapsed time", ["event_title"])
EXIT_CODE = Gauge("cronicle_event_exit_code", "Event exit code", ["event_title"])


@click.command()
@click.option("--port", default=8123, help="The port to listen on.")
@click.option("--url", required=True, help="The base URL of the Cronicle API.")
@click.option("--api-key", required=True, help="The API key for authentication.")
def main(port: int, url: str, api_key: str) -> int:
    logging.info(f"Initializing API client with base URL: {url}")
    api_client = ApiClient(url, api_key)

    # Start up the server to expose the metrics.
    start_http_server(port)
    logging.info(f"Cronicle-exporter listening on port {port}")

    while True:
        logging.info("Fetching schedule")
        schedule = api_client.get_schedule()
        logging.info(f"Retrieved {len(schedule)} schedule events")

        for event in schedule:
            last_event = api_client.get_last_event(event["id"])
            event_title = last_event["event_title"]

            if last_event:
                TIME_START.labels(event_title).set(last_event["time_start"])
                ELAPSED.labels(event_title).set(last_event["elapsed"])
                EXIT_CODE.labels(event_title).set(last_event["code"])

        # Sleep for a while before the next update
        time.sleep(60)  # Update every minute


if __name__ == "__main__":
    main()
