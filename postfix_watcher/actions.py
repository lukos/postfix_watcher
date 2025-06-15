import requests
from .logging import get_logger
logger = get_logger()

def send_notification(endpoint, message):
    try:
        requests.post(endpoint, json={"message": message})
    except Exception as e:
        logger.error("Failed to call API endpoint: {e}", exc_info=True)
        print(f"Failed to send notification: {e}")
