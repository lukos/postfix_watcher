import re
import subprocess
from .actions import send_notification
from .logging import get_logger
logger = get_logger()
import os
from string import Template

def apply_rules(line, config):
    for rule in config['rules']:
        if re.search(rule['pattern'], line):
            endpoint = rule.get('endpoint', config['default']['endpoint'])
            username = rule.get('endpoint_username', config['default']['endpoint_username'])
            password = rule.get('endpoint_password', config['default']['endpoint_password'])
            template = Template(rule.get('endpoint_message', config['default']['endpoint_message']))
            message = template.safe_substitute(os.environ)

            send_notification(endpoint, message, username, password)
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