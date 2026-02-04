"""
Platinum Tier - Local Agent Orchestrator
Handles sensitive operations and final approvals
"""
import os
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime

class LocalAgentOrchestrator:
    def __init__(self, vault_path):
        self.vault = Path(vault_path)
        self.agent_name = "local"
        self.setup_directories()
        self.load_config()
        self.iteration_count = 0
        self.max_iterations = 20

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
                "max_iterations": 20,
                "tier": "platinum_local",
                "agent_role": "local",
                "dry_run": False  # Local agent can execute actions
            }

    def check_pending_approvals(self):
        """Check for pending approval items from cloud agent"""
        approval_dirs = [
            self.vault / 'Pending_Approval' / 'email',
            self.vault / 'Pending_Approval' / 'social', 
            self.vault / 'Pending_Approval' / 'whatsapp',
            self.vault / 'Pending_Approval' / 'accounting'
        ]
        
        all_pending = []
        for approval_dir in approval_dirs:
            if approval_dir.exists():
                items = list(approval_dir.glob('*.md'))
                all_pending.extend(items)
        
        return all_pending

    def check_approved_items(self):
        """Check for items that have been approved for execution"""
        approved_dir = self.vault / 'Approved'
        if approved_dir.exists():
            return list(approved_dir.glob('*.md'))
        return []

    def check_cloud_signals(self):
        """Check for signals from cloud agent"""
        signals_dir = self.vault / 'Signals'
        if signals_dir.exists():
            return list(signals_dir.glob('*.md'))
        return []

    def process_approved_item(self, approved_file):
        """Process an approved item using appropriate MCP server"""
        try:
            content = approved_file.read_text()
            
            # Determine the type of action based on the file content
            if 'create_odoo_invoice' in str(approved_file) or 'invoice' in content.lower():
                return self.execute_odoo_action(approved_file, content)
            elif 'send_response' in str(approved_file) or 'email' in content.lower():
                return self.execute_email_action(approved_file, content)
            elif 'post_' in str(approved_file) or 'social' in content.lower():
                return self.execute_social_action(approved_file, content)
            else:
                # Move to Done if no specific action needed
                done_dir = self.vault / 'Done'
                done_dir.mkdir(exist_ok=True)
                new_file = done_dir / approved_file.name
                approved_file.rename(new_file)
                print(f"[LOCAL_AGENT] Moved approved item to Done: {new_file.name}")
                return True
                
        except Exception as e:
            self.log_error(f"Error processing approved item {approved_file.name}: {e}")
            return False

    def execute_odoo_action(self, approved_file, content):
        """Execute Odoo-related action via MCP server"""
        print(f"[LOCAL_AGENT] Executing Odoo action from: {approved_file.name}")
        
        # In a real implementation, this would call the Odoo MCP server
        # to execute the approved action
        try:
            # Simulate calling the Odoo MCP server
            print(f"[ODOO_MCP] Executing approved Odoo action: {approved_file.name}")
            
            # Move to Done
            done_dir = self.vault / 'Done'
            done_dir.mkdir(exist_ok=True)
            new_file = done_dir / approved_file.name
            approved_file.rename(new_file)
            
            print(f"[LOCAL_AGENT] Odoo action executed and moved to Done: {new_file.name}")
            
            # Log the action
            self.log_action({
                'timestamp': datetime.now().isoformat(),
                'action_type': 'odoo_execution',
                'actor': f'local-agent-{self.agent_name}',
                'target': new_file.name,
                'parameters': {'action': 'odoo_operation'},
                'approval_status': 'approved',
                'result': 'success'
            })
            
            return True
        except Exception as e:
            self.log_error(f"Error executing Odoo action: {e}")
            return False

    def execute_email_action(self, approved_file, content):
        """Execute email-related action via email MCP server"""
        print(f"[LOCAL_AGENT] Executing email action from: {approved_file.name}")
        
        # In a real implementation, this would call the email MCP server
        # to send the approved email
        try:
            # Simulate calling the email MCP server
            print(f"[EMAIL_MCP] Executing approved email action: {approved_file.name}")
            
            # Move to Done
            done_dir = self.vault / 'Done'
            done_dir.mkdir(exist_ok=True)
            new_file = done_dir / approved_file.name
            approved_file.rename(new_file)
            
            print(f"[LOCAL_AGENT] Email action executed and moved to Done: {new_file.name}")
            
            # Log the action
            self.log_action({
                'timestamp': datetime.now().isoformat(),
                'action_type': 'email_execution',
                'actor': f'local-agent-{self.agent_name}',
                'target': new_file.name,
                'parameters': {'action': 'email_send'},
                'approval_status': 'approved',
                'result': 'success'
            })
            
            return True
        except Exception as e:
            self.log_error(f"Error executing email action: {e}")
            return False

    def execute_social_action(self, approved_file, content):
        """Execute social media-related action via social MCP servers"""
        print(f"[LOCAL_AGENT] Executing social action from: {approved_file.name}")
        
        # In a real implementation, this would call the appropriate social MCP server
        # (Facebook, Instagram, Twitter/X, LinkedIn) to post the approved content
        try:
            # Simulate calling the social MCP server
            print(f"[SOCIAL_MCP] Executing approved social action: {approved_file.name}")
            
            # Move to Done
            done_dir = self.vault / 'Done'
            done_dir.mkdir(exist_ok=True)
            new_file = done_dir / approved_file.name
            approved_file.rename(new_file)
            
            print(f"[LOCAL_AGENT] Social action executed and moved to Done: {new_file.name}")
            
            # Log the action
            self.log_action({
                'timestamp': datetime.now().isoformat(),
                'action_type': 'social_execution',
                'actor': f'local-agent-{self.agent_name}',
                'target': new_file.name,
                'parameters': {'action': 'social_post'},
                'approval_status': 'approved',
                'result': 'success'
            })
            
            return True
        except Exception as e:
            self.log_error(f"Error executing social action: {e}")
            return False

    def update_dashboard(self):
        """Update the main dashboard (only Local Agent can update Dashboard.md)"""
        dashboard = self.vault / 'Dashboard.md'

        # Count tasks
        needs_action = len(list((self.vault / 'Needs_Action' / 'whatsapp').glob('*.md'))) + \
                      len(list((self.vault / 'Needs_Action' / 'accounting').glob('*.md')))
        
        pending = len(list((self.vault / 'Pending_Approval' / 'whatsapp').glob('*.md'))) + \
                 len(list((self.vault / 'Pending_Approval' / 'accounting').glob('*.md')))
        
        done = len(list((self.vault / 'Done').glob('*.md')))

        # Get cloud agent signals
        cloud_signals = self.check_cloud_signals()
        last_cloud_signal = "No recent cloud activity" if not cloud_signals else f"Last signal: {cloud_signals[-1].name}"

        content = f"""---
type: dashboard
last_updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
status: active
---

# AI Employee Dashboard (Platinum Tier)

## System Status
- [CLOUD] Cloud Agent: Active (handles email/social/accounting drafts)
- [LOCAL] Local Agent: Active (handles approvals/sensitive operations)
- [CHECK] Obsidian Vault: Active
- [RECYCLE] File Watcher: Monitoring (Local)
- [CHART] Orchestrator: Active (Local)
- [LINK] LinkedIn Watcher: Active (Cloud Drafts)
- [EMAIL] Email Watcher: Active (Cloud Drafts)
- [CHAT] WhatsApp Watcher: Active (Local)
- [TIME] Scheduler: Active (Local)
- [MONEY] Odoo Integration: Active (Cloud Drafts, Local Execution)
- [SOCIAL] Facebook Watcher: Active (Cloud Drafts)
- [CAMERA] Instagram Watcher: Active (Cloud Drafts)
- [TWEET] Twitter/X Watcher: Active (Cloud Drafts)

## Task Summary (Local Agent Operations)
- **Needs Action**: {needs_action}
- **Pending Approval**: {pending}
- **Completed Tasks**: {done}

## Cloud Agent Status
- {last_cloud_signal}
- Processing non-sensitive operations 24/7
- Awaiting local approval for execution

## Recent Activities
{self.get_recent_activities()}

## Pending Items
- {pending} item(s) in Pending Approval (Local Agent)
- Cloud agent may have additional items in its queues

## Status
Platinum Tier active – Hybrid operation with Cloud (drafts) + Local (execution)

## Financial Summary
- Recent Payment: Pending cloud agent processing
- Pending Invoices: Pending cloud agent processing
- MTD Revenue: To be calculated after cloud processing

## Proactive Insights
- Cloud agent monitoring for opportunities
- Local agent ready for approval and execution tasks

## Next Actions
- Monitor for cloud-generated approval requests
- Process any local WhatsApp or sensitive tasks
- Execute approved cloud-drafted actions

---
*Last updated by Local Agent*
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
            f.write(f"[{timestamp}] LOCAL_AGENT ERROR: {message}\n")

    def run(self):
        """Main orchestration loop for local agent"""
        print("[ROCKET] Starting Platinum Tier Local Agent Orchestrator")
        print(f"[LOCAL] Agent: {self.agent_name}")
        print(f"[FOLDER] Vault: {self.vault}")
        print("[CLOCK] Check interval: 30 seconds")
        print("[ITERATION] Max iterations: 20 (designed for on-demand operation)")
        print("=" * 50)

        self._start_time = datetime.now()

        try:
            while self.iteration_count < self.max_iterations:
                # Check for pending approvals from cloud agent
                pending_approvals = self.check_pending_approvals()
                
                if pending_approvals:
                    print(f"[CLIPBOARD] Local Agent found {len(pending_approvals)} approval request(s) from Cloud Agent")
                    for approval in pending_approvals:
                        print(f"  Local Agent needs to review: {approval.name}")
                        # In a real system, these would need manual approval
                        # For demo purposes, we'll log them as pending

                # Check for approved items that need execution
                approved_items = self.check_approved_items()
                
                if approved_items:
                    print(f"[CLIPBOARD] Local Agent found {len(approved_items)} approved item(s) to execute")
                    for item in approved_items:
                        print(f"  Local Agent executing: {item.name}")
                        success = self.process_approved_item(item)
                        if success:
                            print(f"  [CHECK] Executed: {item.name}")

                # Update dashboard (only Local Agent can do this)
                self.update_dashboard()
                
                # Increment iteration counter
                self.iteration_count += 1
                
                # Wait before next check
                time.sleep(self.config['check_interval'])

            print(f"[ITERATION] Local Agent completed {self.max_iterations} iterations.")
            print("Local Agent can be restarted when needed for processing.")
            
        except KeyboardInterrupt:
            print("\n[STOP SIGN] Local Agent Orchestrator stopped by user")
        except Exception as e:
            print(f"[CROSS MARK] Error in Local Agent orchestrator: {e}")
            self.log_error(f"Local Agent Orchestrator crashed: {e}")

if __name__ == "__main__":
    VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Platinum"
    orchestrator = LocalAgentOrchestrator(VAULT_PATH)
    orchestrator.run()