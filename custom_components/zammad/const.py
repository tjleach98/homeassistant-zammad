"""Constants for Zammad Integration"""
from datetime import timedelta

DOMAIN = "zammad"
PROPER_NAME = "Zammad"

PLATFORMS = ["sensor", "binary_sensor"]
DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)

STARTUP_MESSAGE = f"Starting setup for {DOMAIN}"