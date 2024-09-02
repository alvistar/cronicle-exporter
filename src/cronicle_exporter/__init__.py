import click
import logging

# Configuring logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


@click.option("--port", default=8123, help="The port to listen on.")
def main() -> int:
    print("Hello from cronicle-exporter!")
    return 0
