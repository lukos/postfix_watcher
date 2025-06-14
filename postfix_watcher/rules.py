import re
from .actions import send_notification

def apply_rules(line, config):
    for rule in config['rules']:
        if re.search(rule['pattern'], line):
            endpoint = rule.get('endpoint', config['default']['endpoint'])
            send_notification(endpoint, line)
