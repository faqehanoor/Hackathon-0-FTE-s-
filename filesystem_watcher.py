"""
Bronze Tier - File System Watcher
Watches a folder for new files and creates tasks
"""
import os
import time
import shutil
import logging
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileDropHandler(FileSystemEventHandler):
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.needs_action.mkdir(exist_ok=True)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('FileWatcher')

    def on_created(self, event):
        if not event.is_directory:
            source = Path(event.src_path)
            if source.suffix in ['.txt', '.pdf', '.doc', '.docx', '.md']:
                # Create task file
                task_id = f"FILE_{int(time.time())}_{source.name}"
                task_file = self.needs_action / f"{task_id}.md"

                content = f"""---
type: file_drop
original_name: {source.name}
source_path: {str(source)}
size: {source.stat().st_size} bytes
detected: {time.strftime('%Y-%m-%d %H:%M:%S')}
priority: medium
status: pending
---

# New File Detected: {source.name}

## File Information
- **Name**: {source.name}
- **Type**: {source.suffix}
- **Size**: {source.stat().st_size} bytes
- **Location**: {str(source)}

## Suggested Actions
- [ ] Review file content
- [ ] Categorize file
- [ ] Move to appropriate folder
- [ ] Notify user about file

## Processing Instructions
1. Read the file content
2. Determine what type of file it is
3. Decide appropriate action
4. Create a plan in /Plans/ folder
"""
                task_file.write_text(content)
                self.logger.info(f"Created task for new file: {source.name}")

                # Copy file to vault for processing
                vault_copy = self.needs_action / source.name
                shutil.copy2(source, vault_copy)

def start_file_watcher(vault_path, watch_folder):
    """Start watching a folder for new files"""
    event_handler = FileDropHandler(vault_path)
    observer = Observer()
    observer.schedule(event_handler, watch_folder, recursive=False)
    observer.start()

    try:
        print(f"[FOLDER] File Watcher started. Monitoring: {watch_folder}")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Configure these paths
    VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault"
    WATCH_FOLDER = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault/Drop_Folder"

    # Create watch folder if it doesn't exist
    os.makedirs(WATCH_FOLDER, exist_ok=True)

    print("[INFO] Starting File System Watcher...")
    print(f"[INFO] Vault: {VAULT_PATH}")
    print(f"[INFO] Watch Folder: {WATCH_FOLDER}")
    print("[INFO] Drop files in the watch folder to trigger tasks.")

    start_file_watcher(VAULT_PATH, WATCH_FOLDER)