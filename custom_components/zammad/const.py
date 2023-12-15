"""Constants for Zammad Integration"""
from datetime import timedelta

DOMAIN = "zammad"
PROPER_NAME = "Zammad"

PLATFORMS = ["sensor", "binary_sensor", "button"]
DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)

STARTUP_MESSAGE = f"Starting setup for {DOMAIN}"
INITIAL_USER_ID = -1

API_URL_PATH = "/api/v1"

HUMAN_ERR_MSG_FIELD = "error_human"
