import requests
from .logging import get_logger
logger = get_logger()

def send_notification(endpoint, message, username, password):
    try:
        auth = (username, password) if username and password else None
        response = requests.post(endpoint, 
                      json=message,
                      auth=auth)
        response.raise_for_status()
    except Exception as e:
        logger.error("Failed to call API endpoint: {e}", exc_info=True)
        print(f"Failed to send notification: {e}")
