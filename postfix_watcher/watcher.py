from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
import json
from .rules import apply_rules
from .config import load_config

class MailLogHandler(FileSystemEventHandler):
    def __init__(self, config, mail_file, state_file="/var/lib/postfix-watcher/state.json"):
        self.config = config
        self.mail_file = mail_file
        self.state_file = state_file

        # Load saved state if exists
        self._file_pos = 0
        self._inode = None
        self._load_state()

    def _load_state(self):
        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)
            if state.get('mail_file') == self.mail_file:
                self._file_pos = state.get('offset', 0)
                self._inode = state.get('inode')
        except Exception:
            # State file missing or corrupted, start fresh
            self._file_pos = 0
            self._inode = None

    def _save_state(self):
        state = {
            'mail_file': self.mail_file,
            'offset': self._file_pos,
            'inode': self._inode
        }
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(state, f)

    def on_modified(self, event):
        if not event.is_directory and event.src_path == self.mail_file:
            try:
                st = os.stat(self.mail_file)
                current_inode = st.st_ino
                current_size = st.st_size

                # Detect rotation or truncation: inode changed or file smaller than last offset
                if self._inode != current_inode or current_size < self._file_pos:
                    self._file_pos = 0
                    self._inode = current_inode

                with open(self.mail_file, 'r') as f:
                    f.seek(self._file_pos)
                    new_lines = f.readlines()
                    self._file_pos = f.tell()
                
                for line in new_lines:
                    apply_rules(line, self.config)

                self._save_state()
            except Exception as e:
                print(f"Error processing mail file: {e}")

def start_watcher():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--mail-file", default="/var/log/mail.log", help="Path to the mail log file to watch")
    args = parser.parse_args()

    config = load_config(args.config)
    observer = Observer()
    handler = MailLogHandler(config, args.mail_file)
    observer.schedule(handler, path=args.mail_file.rsplit("/", 1)[0], recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
