import re
import subprocess
from .actions import send_notification
from .logging import get_logger
logger = get_logger()

def apply_rules(line, config):
    for rule in config['rules']:
        if re.search(rule['pattern'], line):
            endpoint = rule.get('endpoint', config['default']['endpoint'])
            send_notification(endpoint, line)
            if rule.get('delete-message', config.get('default', {}).get('delete-message', False)):
                match = re.search(config['default']['messageid-pattern'], line)
                if not match:
                    logger.warning("Could not find message id in line: %s", line)
                    return

                message_id = match.group(1)
                try:
                    subprocess.run(['postsuper', '-d', message_id], check=True)
                    logger.info(f"Deleted message {message_id} via postsuper")
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to delete message {message_id}: {e}")