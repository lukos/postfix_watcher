import re
import subprocess
from .actions import send_notification
from .logging import get_logger
logger = get_logger()
import os
from string import Template
import json

def apply_rules(line, config):
    for rule in config['rules']:
        if re.search(rule['pattern'], line):
            logger.info("Matched rule '%s'", rule['name'])
            endpoint = rule.get('endpoint', config['default']['endpoint'])
            username = rule.get('endpoint_username') or config.get('default', {}).get('endpoint_username')
            password = rule.get('endpoint_password') or config.get('default', {}).get('endpoint_password')
            token = rule.get('endpoint_token') or config.get('default', {}).get('endpoint_token')
            template = Template(rule.get('endpoint_message', config['default']['endpoint_message']))
            message_str = template.safe_substitute(os.environ)
            try:
                message = json.loads(message_str)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON in endpoint_message template: {message_str}", exc_info=True)
                raise

            send_notification(endpoint, message, username, password, token)
            if rule.get('delete-message', config.get('default', {}).get('delete-message', False)):
                match = re.search(config['default']['messageid-pattern'], line)
                if not match:
                    logger.warning("Could not find message id in line: %s", line)
                    return

                message_id = match.group(1)
                try:
                    subprocess.run(['sudo', 'postsuper', '-d', message_id], check=True)
                    logger.info(f"Deleted message {message_id} via postsuper")
                except subprocess.CalledProcessError as e:
                    logger.error(f"Failed to delete message {message_id}: {e}")
        else:
            logger.info("No matched rule for %s", line[:60])    # Don't log entire line which will be really long