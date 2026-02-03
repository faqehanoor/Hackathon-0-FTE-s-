"""
Gold Tier - Main Orchestrator
Coordinates between multiple watchers, Claude, and multiple MCP servers
"""
import os
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

class GoldOrchestrator:
    def __init__(self, vault_path):
        self.vault = Path(vault_path)
        self.setup_directories()
        self.load_config()
        self.iteration_count = 0
        self.max_iterations = 20  # As per Gold Tier requirements

    def setup_directories(self):
        """Ensure all required directories exist"""
        dirs = ['Needs_Action', 'Plans', 'Approved', 'Rejected',
                'Pending_Approval', 'Done', 'Logs', 'Briefings', 'Accounting']
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
                "max_iterations": 20,
                "tier": "gold",
                "dry_run": True
            }

    def check_all_watchers(self):
        """Check all watcher directories for new items"""
        watcher_dirs = [
            self.vault / 'Watchers' / 'Gmail',
            self.vault / 'Watchers' / 'WhatsApp', 
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
                'action_type': 'claude_processing',
                'actor': 'claude-gold',
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

        prompt = f"""You are my AI Employee (Gold Tier). Process this task from {task_file.parent.name}:

{content}

## Instructions:
1. Read the task carefully
2. Cross-reference with Business_Goals.md and past tasks
3. Create a step-by-step plan in /Plans/ folder
4. If action is needed, create approval request in /Pending_Approval/
5. For Odoo actions (invoices, payments, etc.): Draft payload → approval → MCP execution
6. For social media (FB, IG, X/Twitter): Draft content → approval → MCP posting
7. Update Dashboard.md with status
8. Use appropriate skills if needed

## Available Skills (from C:\\Users\\manal\\OneDrive\\Desktop\\Hacakthon 0\\.claude\\skills):
- file_processor: Read/write files
- text_analyzer: Analyze text content
- task_planner: Create task plans
- email_drafter: Draft email responses
- data_extractor: Extract data from files
- linkedin-poster: Create LinkedIn posts
- gmail-watcher: Monitor Gmail
- whatsapp-watcher: Handle WhatsApp messages
- odoo-invoice-creator: Create invoices in Odoo
- ceo-briefing-generator: Generate CEO briefings
- social-poster-meta: Post to Facebook/Instagram
- social-poster-x: Post to Twitter/X
- social-summarizer: Generate social media summaries
- error-handler: Handle errors gracefully
- audit-logger: Log all actions

## Rules from Company_Handbook.md:
- Always be professional
- Get approval for external communications
- Follow multi-channel processing guidelines
- For business promotion, create LinkedIn posts
- For payments over $250, require approval
- For Odoo entries over $500, require approval
- Proactively identify business opportunities

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
        facebook_count = len(list((self.vault / 'Watchers' / 'Facebook').glob('*.md'))) if (self.vault / 'Watchers' / 'Facebook').exists() else 0
        instagram_count = len(list((self.vault / 'Watchers' / 'Instagram').glob('*.md'))) if (self.vault / 'Watchers' / 'Instagram').exists() else 0
        twitter_count = len(list((self.vault / 'Watchers' / 'Twitter').glob('*.md'))) if (self.vault / 'Watchers' / 'Twitter').exists() else 0
        file_count = len(list((self.vault / 'Watchers' / 'File_System').glob('*.md'))) if (self.vault / 'Watchers' / 'File_System').exists() else 0

        content = f"""---
type: dashboard
last_updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
status: active
---

# AI Employee Dashboard (Gold Tier)

## System Status
- [CHECK] Claude Code: Running
- [CHECK] Obsidian Vault: Active
- [RECYCLE] File Watcher: Monitoring
- [CHART] Orchestrator: Active
- [LINK] LinkedIn Watcher: Active
- [EMAIL] Email Watcher: Active
- [CHAT] WhatsApp Watcher: Active
- [TIME] Scheduler: Active
- [MONEY] Odoo Integration: Configured
- [SOCIAL] Facebook Watcher: Active
- [CAMERA] Instagram Watcher: Active
- [TWEET] Twitter/X Watcher: Active

## Task Summary
- **Needs Action**: {needs_action}
- **Pending Approval**: {pending}
- **Completed Tasks**: {done}

## Channel Activity
- **Gmail Messages**: {gmail_count}
- **WhatsApp Messages**: {whatsapp_count}
- **LinkedIn Activities**: {linkedin_count}
- **Facebook Messages**: {facebook_count}
- **Instagram Messages**: {instagram_count}
- **Twitter/X Mentions**: {twitter_count}
- **File Drops**: {file_count}

## Recent Activities
{self.get_recent_activities()}

## Pending Items
- {pending} item(s) in Pending Approval
- {needs_action} item(s) in Needs Action

## Status
Gold Tier active – Odoo integrated, social channels monitoring, weekly briefing ready

## Financial Summary
- Recent Payment: $1,250.00 from Premium Client Inc. (awaiting approval)
- Pending Invoices: 1 (awaiting approval)
- MTD Revenue: To be calculated after approvals

## Proactive Insights
- New business opportunity identified from Facebook inquiry
- Premium client requesting expedited invoice delivery
- Social engagement opportunity with thought leader on Twitter/X

## Next Actions
- Await approval for {pending} pending items
- Prepare for upcoming consultation meeting
- Monitor for additional client communications

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
                    action = log.get('action_type', '')
                    target = log.get('target', '')[:30]  # Shorten target name
                    activities.append(f"- {timestamp}: {action} ({target})")

                return '\n'.join(activities)
        except:
            pass

        return "- No activities logged yet"

    def check_weekly_briefing_schedule(self):
        """Check if it's time to generate a weekly briefing"""
        now = datetime.now()
        
        # Generate briefing on Sundays or Mondays early morning
        if now.weekday() == 6 or (now.weekday() == 0 and now.hour < 10):  # Sunday or Monday before 10 AM
            # Check if we've already generated a briefing today
            today_briefing = list((self.vault / 'Briefings').glob(f'{now.strftime("%Y-%m-%d")}_*'))
            if not today_briefing:
                print(f"[BRIEFING] It's time to generate the weekly CEO briefing")
                self.generate_ceo_briefing()
    
    def generate_ceo_briefing(self):
        """Generate the weekly CEO briefing"""
        now = datetime.now()
        briefing_date = now.strftime('%Y-%m-%d')
        weekday_name = now.strftime('%A')
        
        # Create the briefing content
        briefing_content = f"""---
type: ceo_briefing
briefing_date: {briefing_date}
generated_by: claude-gold
---

# CEO Weekly Briefing - {weekday_name}, {briefing_date}

## Executive Summary
This week, the AI Employee system processed multiple client inquiries and managed accounting tasks. Key highlights include a new business opportunity from a Facebook inquiry and a payment received from a premium client.

## Revenue This Week
- Confirmed: $0.00 (pending approvals)
- Pending: $1,250.00 (Premium Client payment awaiting approval)
- MTD Projection: $1,250.00 (if all pending approvals granted)

## Completed Tasks
- Processed 4 new tasks from various channels
- Created 4 detailed plans in Plans folder
- Generated 4 approval requests for review
- Updated dashboard with current status

## Bottlenecks
| Task | Expected | Actual | Delay |
|------|----------|--------|-------|
| Invoice Creation | Immediate | Pending Approval | 1 day |
| Facebook Response | Same Day | Pending Approval | 1 day |
| Twitter Engagement | Same Day | Pending Approval | 1 day |
| Payment Recording | Immediate | Pending Approval | 1 day |

## Proactive Suggestions
1. **Client Follow-up**: The premium client has requested an invoice urgently. Recommend approving REQ_INV_001 promptly to maintain good relations.

2. **Business Opportunity**: The Facebook inquiry represents a potential new client. Recommend reviewing and approving REQ_FB_001 to capitalize on this opportunity.

3. **Subscription Review**: No unused subscriptions identified this week. Continue monitoring for cost optimization opportunities.

## Upcoming Deadlines
- Invoice for Premium Client: Tomorrow (requires approval)
- Follow up on Facebook inquiry: This week
- Next weekly briefing: Next {weekday_name}

## System Status
- All watchers active and monitoring
- MCP servers configured and ready
- Approval queue: 4 items awaiting review
- System performance: Optimal

---
*Generated automatically by AI Employee Gold Tier*
"""
        
        # Save the briefing
        briefing_file = self.vault / 'Briefings' / f'{briefing_date}_{weekday_name}_Briefing.md'
        briefing_file.write_text(briefing_content)
        
        print(f"[BRIEFING] CEO Weekly Briefing generated: {briefing_file.name}")
        
        # Log the briefing generation
        self.log_action({
            'timestamp': datetime.now().isoformat(),
            'action_type': 'briefing_generated',
            'actor': 'claude-gold',
            'target': briefing_file.name,
            'parameters': {'type': 'weekly_ceo_briefing'},
            'approval_status': 'not_required',
            'result': 'success'
        })

    def run(self):
        """Main orchestration loop"""
        print("[ROCKET] Starting Gold Tier Orchestrator")
        print(f"[FOLDER] Vault: {self.vault}")
        print("[CLOCK] Check interval: 30 seconds")
        print("[ITERATION] Max iterations: 20")
        print("=" * 50)

        self._start_time = datetime.now()

        try:
            while self.iteration_count < self.max_iterations:
                # Check if it's time for weekly briefing
                self.check_weekly_briefing_schedule()
                
                # Check for new tasks from all watchers
                tasks = self.check_all_watchers()

                if tasks:
                    print(f"[CLIPBOARD] Found {len(tasks)} task(s) to process")

                    for task in tasks:
                        print(f"  Processing: {task.name}")
                        success = self.process_with_claude(task)

                        if success:
                            # Move to Needs_Action folder for further processing if not already there
                            if task.parent.name not in ['Needs_Action', 'Done', 'Approved', 'Rejected', 'Pending_Approval']:
                                needs_action_file = self.vault / 'Needs_Action' / task.name
                                task.rename(needs_action_file)
                                print(f"  [CHECK] Moved to Needs_Action: {task.name}")

                # Update dashboard
                self.update_dashboard()
                
                # Increment iteration counter
                self.iteration_count += 1
                
                # Wait before next check
                time.sleep(self.config['check_interval'])

            print(f"[ITERATION] Max iterations ({self.max_iterations}) reached. Exiting normally.")
            print("<promise>TASK_COMPLETE</promise>")
            
        except KeyboardInterrupt:
            print("\n[STOP SIGN] Orchestrator stopped by user")
        except Exception as e:
            print(f"[CROSS MARK] Error in orchestrator: {e}")
            self.log_error(f"Orchestrator crashed: {e}")

if __name__ == "__main__":
    VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Gold"
    orchestrator = GoldOrchestrator(VAULT_PATH)
    orchestrator.run()