import re
import subprocess
from .actions import send_notification
from .logging import get_logger
logger = get_logger()
import os
from string import Template
import json

_FLAG_MAP = {
    "IGNORECASE": re.IGNORECASE, "MULTILINE": re.MULTILINE,
    "DOTALL": re.DOTALL, "VERBOSE": re.VERBOSE
}

def _compile_flags(flag_names):
    flags = 0
    for n in (flag_names or []):
        flags |= _FLAG_MAP.get(n.upper(), 0)
    return flags

def apply_rules(line, config):
    for rule in config['rules']:
        flags = _compile_flags(rule.get('flags'))
        m = re.search(rule['pattern'], line, flags)
        if not m:
            continue

        logger.info("Matched rule '%s'", rule['name'])

        endpoint = rule.get('endpoint', config['default']['endpoint'])
        username = rule.get('endpoint_username') or config.get('default', {}).get('endpoint_username')
        password = rule.get('endpoint_password') or config.get('default', {}).get('endpoint_password')
        token    = rule.get('endpoint_token')    or config.get('default', {}).get('endpoint_token')

        # Context = env vars + named capture groups from THIS ONE regex
        context = {}
        context.update(os.environ)
        context.update({k: v for k, v in m.groupdict().items() if v is not None})

        # Render endpoint message using ${group_name}
        template_src = rule.get('endpoint_message', config['default']['endpoint_message'])
        try:
            # Use substitute() to fail fast on missing vars; swap to safe_substitute() if you prefer
            message_str = Template(template_src).substitute(context)
        except KeyError as e:
            missing = e.args[0]
            logger.error(f"endpoint_message references '${{{missing}}}' but that named group/env var wasn't provided.")
            raise

        try:
            message = json.loads(message_str)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON after substitution: {message_str}", exc_info=True)
            raise

        send_notification(endpoint, message, username, password, token)

        if rule.get('delete-message', config.get('default', {}).get('delete-message', False)):
            mid_match = re.search(config['default']['messageid-pattern'], line)
            if not mid_match:
                logger.warning("Could not find message id in line: %s", line)
                return
            message_id = mid_match.group(1)
            try:
                subprocess.run(['sudo', 'postsuper', '-d', message_id], check=True)
                logger.info(f"Deleted message {message_id} via postsuper")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to delete message {message_id}: {e}")
        else:
            logger.info("No matched rule for %s", line[:60])    # Don't log entire line which will be really long