import requests
from .logging import get_logger
logger = get_logger()

def send_notification(endpoint, message, username, password, token):
    logger.info(f"Calling API to handle rule trigger")
    try:
        auth = (username, password) if username and password else None
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.post(endpoint, 
                      json=message,
                      auth=auth,
                      headers=headers)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to call API endpoint: {e}", exc_info=True)
        print(f"Failed to send notification: {e}")
