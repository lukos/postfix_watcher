import requests

def send_notification(endpoint, message):
    try:
        requests.post(endpoint, json={"message": message})
    except Exception as e:
        print(f"Failed to send notification: {e}")
