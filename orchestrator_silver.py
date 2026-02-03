"""
Silver Tier - Main Orchestrator
Coordinates between multiple watchers, Claude, and MCP servers
"""
import os
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime

class SilverOrchestrator:
    def __init__(self, vault_path):
        self.vault = Path(vault_path)
        self.setup_directories()
        self.load_config()

    def setup_directories(self):
        """Ensure all required directories exist"""
        dirs = ['Needs_Action', 'Plans', 'Approved', 'Rejected',
                'Pending_Approval', 'Done', 'Logs']
        for dir_name in dirs:
            (self.vault / dir_name).mkdir(exist_ok=True)

    def load_config(self):
        """Load configuration"""
        config_file = self.vault / 'Config' / 'system_config.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "claude_path": "claude",
                "check_interval": 30,
                "max_iterations": 10,
                "tier": "silver",
                "dry_run": True
            }

    def check_all_watchers(self):
        """Check all watcher directories for new items"""
        watcher_dirs = [
            self.vault / 'Watchers' / 'Gmail',
            self.vault / 'Watchers' / 'WhatsApp', 
            self.vault / 'Watchers' / 'LinkedIn',
            self.vault / 'Watchers' / 'File_System',
            self.vault / 'Drop_Folder'
        ]
        
        all_items = []
        for watcher_dir in watcher_dirs:
            if watcher_dir.exists():
                items = list(watcher_dir.glob('*.md'))
                all_items.extend(items)
        
        # Also check Needs_Action for any items that need processing
        needs_action_items = list((self.vault / 'Needs_Action').glob('*.md'))
        all_items.extend(needs_action_items)
        
        return all_items

    def process_with_claude(self, task_file):
        """Process a task using Claude Code"""
        try:
            # Create a prompt for Claude
            prompt = self.create_claude_prompt(task_file)

            # Run Claude Code
            cmd = [
                self.config['claude_path'],
                "process-task",
                "--prompt", prompt,
                "--vault", str(self.vault),
                "--output", str(self.vault / 'Plans' / f'plan_{task_file.stem}.md')
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            # Log the result
            self.log_action({
                'timestamp': datetime.now().isoformat(),
                'action': 'claude_processing',
                'task': task_file.name,
                'success': result.returncode == 0,
                'output': result.stdout[:500]  # First 500 chars
            })

            return result.returncode == 0

        except Exception as e:
            self.log_error(f"Claude processing failed: {e}")
            return False

    def create_claude_prompt(self, task_file):
        """Create prompt for Claude based on task file"""
        content = task_file.read_text()

        prompt = f"""You are my AI Employee (Silver Tier). Process this task from {task_file.parent.name}:

{content}

## Instructions:
1. Read the task carefully
2. Create a step-by-step plan in /Plans/ folder
3. If action is needed, create approval request in /Pending_Approval/
4. Update Dashboard.md with status
5. Use appropriate skills if needed

## Available Skills (from C:\\Users\\manal\\OneDrive\\Desktop\\Hacakthon 0\\.claude\\skills):
- file_processor: Read/write files
- text_analyzer: Analyze text content
- task_planner: Create task plans
- email_drafter: Draft email responses
- data_extractor: Extract data from files
- linkedin_poster: Create LinkedIn posts
- gmail_reader: Process Gmail messages
- whatsapp_handler: Handle WhatsApp messages
- approval_handler: Manage approval workflow

## Rules from Company_Handbook.md:
- Always be professional
- Flag payments over $500
- Get approval for external communications
- Follow multi-channel processing guidelines

Create a detailed plan now."""
        return prompt

    def log_action(self, data):
        """Log actions to JSON log file"""
        log_dir = self.vault / 'Logs'
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = log_dir / f'{today}.json'

        # Read existing logs or create new
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(data)

        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

    def log_error(self, message):
        """Log error messages"""
        error_log = self.vault / 'Logs' / 'errors.log'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(error_log, 'a') as f:
            f.write(f"[{timestamp}] ERROR: {message}\n")

    def update_dashboard(self):
        """Update the main dashboard"""
        dashboard = self.vault / 'Dashboard.md'

        # Count tasks
        needs_action = len(list((self.vault / 'Needs_Action').glob('*.md')))
        pending = len(list((self.vault / 'Pending_Approval').glob('*.md')))
        done = len(list((self.vault / 'Done').glob('*.md')))

        # Check watcher statuses
        gmail_count = len(list((self.vault / 'Watchers' / 'Gmail').glob('*.md'))) if (self.vault / 'Watchers' / 'Gmail').exists() else 0
        whatsapp_count = len(list((self.vault / 'Watchers' / 'WhatsApp').glob('*.md'))) if (self.vault / 'Watchers' / 'WhatsApp').exists() else 0
        linkedin_count = len(list((self.vault / 'Watchers' / 'LinkedIn').glob('*.md'))) if (self.vault / 'Watchers' / 'LinkedIn').exists() else 0
        file_count = len(list((self.vault / 'Watchers' / 'File_System').glob('*.md'))) if (self.vault / 'Watchers' / 'File_System').exists() else 0

        content = f"""---
type: dashboard
last_updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
status: active
---

# AI Employee Dashboard (Silver Tier)

## System Status
- [CHECK] Claude Code: Running
- [CHECK] Obsidian Vault: Active
- [RECYCLE] File Watcher: Monitoring
- [CHART] Orchestrator: Active
- [LINK] LinkedIn Watcher: Active
- [EMAIL] Email Watcher: Active
- [CHAT] WhatsApp Watcher: Active

## Task Summary
- **Needs Action**: {needs_action}
- **Pending Approval**: {pending}
- **Completed Tasks**: {done}

## Channel Activity
- **Gmail Messages**: {gmail_count}
- **WhatsApp Messages**: {whatsapp_count}
- **LinkedIn Activities**: {linkedin_count}
- **File Drops**: {file_count}

## Recent Activities
{self.get_recent_activities()}

## Pending Items
- {pending} item(s) in Pending Approval
- {needs_action} item(s) in Needs Action

## Status
Silver Tier active – watchers monitoring Gmail + WhatsApp + LinkedIn + File System

## Daily Briefing
- Processed multi-channel inputs
- All watchers active and monitoring
- Ready to process new inputs

---
*Last updated automatically by AI Employee*
"""
        dashboard.write_text(content)

    def get_recent_activities(self):
        """Get recent activities from logs"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            log_file = self.vault / 'Logs' / f'{today}.json'

            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)

                # Get last 5 activities
                recent = logs[-5:] if len(logs) > 5 else logs
                activities = []

                for log in recent:
                    timestamp = log.get('timestamp', '').split('T')[-1][:8]  # Get time portion
                    action = log.get('action', '')
                    activities.append(f"- {timestamp}: {action}")

                return '\n'.join(activities)
        except:
            pass

        return "- No activities logged yet"

    def run(self):
        """Main orchestration loop"""
        print("[ROCKET] Starting Silver Tier Orchestrator")
        print(f"[FOLDER] Vault: {self.vault}")
        print("[CLOCK] Check interval: 30 seconds")
        print("=" * 50)

        self._start_time = datetime.now()

        try:
            while True:
                # Check for new tasks from all watchers
                tasks = self.check_all_watchers()

                if tasks:
                    print(f"[CLIPBOARD] Found {len(tasks)} task(s) to process")

                    for task in tasks:
                        print(f"  Processing: {task.name}")
                        success = self.process_with_claude(task)

                        if success:
                            # Move to Needs_Action folder for further processing
                            needs_action_file = self.vault / 'Needs_Action' / task.name
                            
                            # Only move if it's not already in Needs_Action
                            if task.parent != self.vault / 'Needs_Action':
                                task.rename(needs_action_file)
                                print(f"  [CHECK] Moved to Needs_Action: {task.name}")

                # Update dashboard
                self.update_dashboard()

                # Wait before next check
                time.sleep(self.config['check_interval'])

        except KeyboardInterrupt:
            print("\n[STOP SIGN] Orchestrator stopped by user")
        except Exception as e:
            print(f"[CROSS MARK] Error in orchestrator: {e}")
            self.log_error(f"Orchestrator crashed: {e}")

if __name__ == "__main__":
    VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Silver"
    orchestrator = SilverOrchestrator(VAULT_PATH)
    orchestrator.run()