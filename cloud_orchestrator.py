"""
Platinum Tier - Cloud Agent Orchestrator
Handles non-sensitive operations 24/7 on cloud infrastructure
"""
import os
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime

class CloudAgentOrchestrator:
    def __init__(self, vault_path):
        self.vault = Path(vault_path)
        self.agent_name = "cloud"
        self.setup_directories()
        self.load_config()
        self.iteration_count = 0
        self.max_iterations = 100  # Higher for continuous operation

    def setup_directories(self):
        """Ensure all required directories exist"""
        dirs = [
            'Needs_Action', 'Plans', 'Approved', 'Rejected',
            'Pending_Approval', 'Done', 'Logs', 'Briefings', 
            'Accounting', 'In_Progress', 'Updates', 'Signals'
        ]
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
                "max_iterations": 100,
                "tier": "platinum_cloud",
                "agent_role": "cloud",
                "dry_run": True
            }

    def check_all_watchers(self):
        """Check all watcher directories for new items (non-sensitive operations)"""
        watcher_dirs = [
            self.vault / 'Watchers' / 'Gmail',
            self.vault / 'Watchers' / 'LinkedIn', 
            self.vault / 'Watchers' / 'Facebook',
            self.vault / 'Watchers' / 'Instagram',
            self.vault / 'Watchers' / 'Twitter',
            self.vault / 'Watchers' / 'File_System',
            self.vault / 'Drop_Folder'
        ]
        
        all_items = []
        for watcher_dir in watcher_dirs:
            if watcher_dir.exists():
                items = list(watcher_dir.glob('*.md'))
                all_items.extend(items)
        
        # Also check domain-specific Needs_Action folders for cloud operations
        cloud_domains = ['email', 'social', 'accounting']  # Cloud handles these
        for domain in cloud_domains:
            domain_dir = self.vault / 'Needs_Action' / domain
            if domain_dir.exists():
                items = list(domain_dir.glob('*.md'))
                all_items.extend(items)
        
        return all_items

    def claim_task(self, task_file):
        """Claim a task using the claim-by-move rule"""
        in_progress_dir = self.vault / 'In_Progress' / self.agent_name
        in_progress_dir.mkdir(exist_ok=True)
        
        # Move task to in-progress with agent prefix
        claimed_name = f"{self.agent_name}_{task_file.name}"
        claimed_file = in_progress_dir / claimed_name
        task_file.rename(claimed_file)
        
        print(f"[CLOUD_AGENT] Claimed task: {claimed_name}")
        return claimed_file

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
                "--output", str(self.vault / 'Plans' / task_file.parent.name / f'plan_{task_file.stem}.md')
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            # Log the result
            self.log_action({
                'timestamp': datetime.now().isoformat(),
                'action_type': 'claude_processing',
                'actor': f'claude-cloud-{self.agent_name}',
                'target': task_file.name,
                'parameters': {'task_type': task_file.parent.name},
                'approval_status': 'not_required_yet',
                'result': 'success' if result.returncode == 0 else 'fail',
                'error': result.stderr if result.returncode != 0 else None
            })

            return result.returncode == 0

        except Exception as e:
            self.log_error(f"Claude processing failed: {e}")
            return False

    def create_claude_prompt(self, task_file):
        """Create prompt for Claude based on task file"""
        content = task_file.read_text()

        prompt = f"""You are my AI Employee (Platinum Tier - Cloud Agent). Process this task from {task_file.parent.name}:

{content}

## Instructions:
1. Read the task carefully
2. Cross-reference with Business_Goals.md and past tasks
3. Create a step-by-step plan in /Plans/{task_file.parent.name}/ folder
4. If action is needed, create approval request in /Pending_Approval/{task_file.parent.name}/
5. For social media (FB, IG, X/Twitter): Draft content → approval → MCP posting
6. For email: Draft response → approval → MCP sending
7. For accounting: Draft entries → approval → MCP execution in Odoo
8. Update Updates/ folder with status (Dashboard.md is for Local Agent only)
9. Use appropriate skills if needed

## Available Skills (from C:\\Users\\manal\\OneDrive\\Desktop\\Hacakthon 0\\.claude\\skills):
- file_processor: Read/write files
- text_analyzer: Analyze text content
- task_planner: Create task plans
- email_drafter: Draft email responses
- data_extractor: Extract data from files
- linkedin-poster: Create LinkedIn posts
- gmail-watcher: Monitor Gmail
- odoo-invoice-creator: Create invoices in Odoo (draft only)
- social-poster-meta: Post to Facebook/Instagram
- social-poster-x: Post to Twitter/X
- social-summarizer: Generate social media summaries
- audit-logger: Log all actions

## Rules from Company_Handbook.md:
- You are the CLOUD AGENT - handle non-sensitive operations only
- Draft all responses/posts but do not execute final actions
- All actions require approval by Local Agent
- Do not handle WhatsApp, payments, or sensitive credentials
- For social media, create drafts but do not post without approval
- For emails, draft but do not send without approval
- For accounting, create draft entries but do not post without approval

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
            f.write(f"[{timestamp}] CLOUD_AGENT ERROR: {message}\n")

    def update_signals(self):
        """Update signals for Local Agent (since Dashboard.md is Local Agent's responsibility)"""
        signals_dir = self.vault / 'Signals'
        signals_dir.mkdir(exist_ok=True)
        
        # Count tasks
        needs_action = len(list((self.vault / 'Needs_Action' / 'email').glob('*.md'))) + \
                      len(list((self.vault / 'Needs_Action' / 'social').glob('*.md'))) + \
                      len(list((self.vault / 'Needs_Action' / 'accounting').glob('*.md')))
        
        pending = len(list((self.vault / 'Pending_Approval' / 'email').glob('*.md'))) + \
                 len(list((self.vault / 'Pending_Approval' / 'social').glob('*.md'))) + \
                 len(list((self.vault / 'Pending_Approval' / 'accounting').glob('*.md')))
        
        done = len(list((self.vault / 'Done').glob('*.md')))

        signal_content = f"""---
type: system_signal
generated_by: cloud_agent
timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

# Cloud Agent Signal

## Task Summary (Cloud Agent Operations)
- **Needs Action**: {needs_action}
- **Pending Approval**: {pending}
- **Completed Tasks**: {done}

## Cloud Agent Status
- Active and monitoring non-sensitive operations
- Processing email, social media, and accounting drafts
- Awaiting local agent approval for final execution

## Recent Cloud Activities
{self.get_recent_cloud_activities()}

---
*Signal generated by Cloud Agent*
"""
        
        signal_file = signals_dir / f'cloud_signal_{int(datetime.now().timestamp())}.md'
        signal_file.write_text(signal_content)

    def get_recent_cloud_activities(self):
        """Get recent activities from cloud logs"""
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            log_file = self.vault / 'Logs' / f'{today}.json'

            if log_file.exists():
                with open(log_file, 'r') as f:
                    logs = json.load(f)

                # Get last 5 cloud activities
                recent = logs[-5:] if len(logs) > 5 else logs
                activities = []

                for log in recent:
                    timestamp = log.get('timestamp', '').split('T')[-1][:8]  # Get time portion
                    action = log.get('action_type', '')
                    target = log.get('target', '')[:30]  # Shorten target name
                    activities.append(f"- {timestamp}: {action} ({target})")

                return '\n'.join(activities)
        except:
            pass

        return "- No activities logged yet"

    def health_monitor(self):
        """Perform health checks and monitoring"""
        # Log health status
        health_log = self.vault / 'Logs' / 'health_monitor.log'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(health_log, 'a') as f:
            f.write(f"[{timestamp}] CLOUD_AGENT HEALTH: Running normally\n")
        
        # In a real implementation, this would check:
        # - API connectivity
        # - Resource usage
        # - Error rates
        # - Task processing rates
        print(f"[HEALTH_MONITOR] Cloud Agent running normally at {timestamp}")

    def run(self):
        """Main orchestration loop for cloud agent"""
        print("[ROCKET] Starting Platinum Tier Cloud Agent Orchestrator")
        print(f"[CLOUD] Agent: {self.agent_name}")
        print(f"[FOLDER] Vault: {self.vault}")
        print("[CLOCK] Check interval: 30 seconds")
        print("[ITERATION] Designed for continuous operation")
        print("=" * 50)

        self._start_time = datetime.now()

        try:
            while True:  # Continuous operation for cloud agent
                # Perform health monitoring
                self.health_monitor()
                
                # Check for new tasks from all watchers
                tasks = self.check_all_watchers()

                if tasks:
                    print(f"[CLIPBOARD] Cloud Agent found {len(tasks)} task(s) to process")

                    for task in tasks:
                        print(f"  Cloud Agent processing: {task.name}")
                        
                        # Claim the task using claim-by-move rule
                        claimed_task = self.claim_task(task)
                        
                        success = self.process_with_claude(claimed_task)

                        if success:
                            print(f"  [CHECK] Cloud Agent processed: {claimed_task.name}")

                # Update signals for Local Agent
                self.update_signals()
                
                # Increment iteration counter
                self.iteration_count += 1
                
                # Wait before next check
                time.sleep(self.config['check_interval'])

        except KeyboardInterrupt:
            print("\n[STOP SIGN] Cloud Agent Orchestrator stopped by user")
        except Exception as e:
            print(f"[CROSS MARK] Error in Cloud Agent orchestrator: {e}")
            self.log_error(f"Cloud Agent Orchestrator crashed: {e}")

if __name__ == "__main__":
    VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Platinum"
    orchestrator = CloudAgentOrchestrator(VAULT_PATH)
    orchestrator.run()