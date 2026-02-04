"""
Platinum Tier - Demo Script
Demonstrates the end-to-end flow: Cloud offline detection → draft → approval → local execution
"""
import os
import time
from pathlib import Path
from datetime import datetime

def create_demo_scenario():
    """Create a scenario demonstrating the Platinum Tier workflow"""
    print("=" * 60)
    print("PLATINUM TIER DEMO: Hybrid Cloud + Local Workflow")
    print("=" * 60)
    print()

    # Define vault path
    vault_path = Path("C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Platinum")

    print("SCENARIO: Email received while Local Agent is offline")
    print("-" * 50)

    # Step 1: Simulate email received while local is offline
    print("1. [EMAIL] Email received at Cloud Agent while Local Agent offline")
    email_task = vault_path / "Needs_Action" / "email" / f"email_task_{int(datetime.now().timestamp())}.md"
    email_content = f"""---
type: email_received
sender: client@example.com
received: {datetime.now().isoformat()}
priority: medium
---

# Email from client@example.com

## Message
Can you please send me the invoice for the project we discussed last week? I need it for our accounting department.

## Action Required
- [ ] Draft invoice in Odoo
- [ ] Create approval request
- [ ] Wait for Local Agent approval
"""
    email_task.write_text(email_content)
    print(f"   -> Created task: {email_task.name}")

    # Step 2: Cloud Agent processes the email
    print("\n2. [CLOUD] Cloud Agent processes email (while Local Agent offline)")
    print("   -> Cloud Agent claims task using claim-by-move rule")

    # Move to in-progress
    in_progress_dir = vault_path / "In_Progress" / "cloud"
    in_progress_dir.mkdir(exist_ok=True)
    claimed_task = in_progress_dir / f"cloud_{email_task.name}"
    email_task.rename(claimed_task)
    print(f"   -> Claimed task: {claimed_task.name}")

    # Create draft plan
    plan_file = vault_path / "Plans" / "email" / f"plan_{email_task.stem}.md"
    plan_content = f"""---
type: task_plan
plan_id: plan_{int(datetime.now().timestamp())}
created: {datetime.now().isoformat()}
status: pending_execution
author: cloud_agent
related_to: {claimed_task.name}
---

# Task Execution Plan: Email Response & Invoice Request

## Original Task
Process email requesting invoice from client@example.com

## Plan Overview
1. Analyze email content
2. Check if invoice exists in Odoo
3. If not, draft new invoice
4. Create approval request for Local Agent
5. Wait for approval before execution

## Detailed Steps

### Step 1: Email Analysis
- [x] Read email content
- [x] Identify request (invoice needed)
- [x] Extract client information

### Step 2: Invoice Check
- [ ] Check Odoo for existing invoice
- [ ] If none exists, prepare draft invoice

### Step 3: Approval Process
- [ ] Create approval request in /Pending_Approval/
- [ ] Wait for Local Agent to approve
- [ ] After approval, execute invoice creation and email response

## Dependencies
- Access to Odoo accounting system
- Local Agent approval

## Approval Required
YES - Creating invoice in Odoo and sending email response

## Risk Level
MEDIUM - Financial transaction requiring approval
"""
    plan_file.write_text(plan_content)
    print(f"   -> Created plan: {plan_file.name}")

    # Step 3: Cloud Agent creates approval request
    print("\n3. [CLOUD] Cloud Agent creates approval request")
    approval_dir = vault_path / "Pending_Approval" / "accounting"
    approval_dir.mkdir(exist_ok=True)
    approval_file = approval_dir / f"req_inv_{int(datetime.now().timestamp())}_approval.md"
    approval_content = f"""---
type: approval_request
action: create_odoo_invoice_and_email
request_id: req_inv_{int(datetime.now().timestamp())}
related_to: {claimed_task.name}
reason: client_requested_invoice
financial_threshold: true
amount_estimate: medium
---

# Invoice Creation and Email Approval Request

## Request Details
- **Action**: Create invoice in Odoo and send email response
- **Client**: client@example.com
- **Request**: Invoice for project discussed last week
- **Urgency**: Needed for client's accounting department

## Invoice Information
- Customer: client@example.com (to be verified in Odoo)
- Service: Project from last week
- Due Date: As requested by client

## Email Response Draft
Subject: Invoice for Our Recent Project

Dear Valued Client,

Thank you for your request. I'm preparing the invoice for the project we discussed last week. I'll have it ready for you shortly.

I'll follow up with you once it's completed and sent.

Best regards,
AI Employee System

## Action Required
Please review and approve the creation of this invoice in Odoo and the email response. The client has requested this for their accounting department.

## Next Steps
- If approved: Invoice will be created in Odoo and email sent to client
- If rejected: Alternative solution will be proposed to client

## Approval Options
- Move this file to /Approved/ to proceed
- Move this file to /Rejected/ with reason to cancel
"""
    approval_file.write_text(approval_content)
    print(f"   -> Created approval request: {approval_file.name}")

    print("\n4. [SLEEP] Local Agent remains offline - Cloud Agent continues monitoring")
    print("   -> Cloud Agent has completed draft work and awaits approval")
    print("   -> System remains operational despite Local Agent being offline")

    print("\n5. [SYNC] Local Agent comes online - discovers approval request")
    print("   -> Local Agent scans Pending_Approval/accounting/ directory")
    print(f"   -> Discovers: {approval_file.name}")

    print("\n6. [APPROVE] Local Agent approves the request")
    approved_dir = vault_path / "Approved"
    approved_dir.mkdir(exist_ok=True)
    approved_file = approved_dir / f"approved_{approval_file.name}"
    approval_file.rename(approved_file)
    print(f"   -> Moved to Approved: {approved_file.name}")

    print("\n7. [EXECUTE] Local Agent executes the approved action")
    print("   -> Local Agent calls Odoo MCP to create invoice")
    print("   -> Local Agent calls Email MCP to send response")

    # Simulate execution
    done_dir = vault_path / "Done"
    done_dir.mkdir(exist_ok=True)
    executed_file = done_dir / f"executed_{approved_file.name}"
    approved_file.rename(executed_file)
    print(f"   -> Action executed and moved to Done: {executed_file.name}")

    print("\n8. [UPDATE] Dashboard updated by Local Agent")
    print("   -> Local Agent updates Dashboard.md with completion status")

    # Update dashboard
    dashboard_file = vault_path / "Dashboard.md"
    dashboard_content = f"""---
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
- **Needs Action**: 0
- **Pending Approval**: 0
- **Completed Tasks**: 1

## Cloud Agent Status
- Last signal: Cloud agent processed email from client@example.com
- Processing non-sensitive operations 24/7
- Successfully handed off approval request to Local Agent

## Recent Activities
- {datetime.now().strftime('%H:%M:%S')}: Invoice created and email sent to client@example.com
- {datetime.now().strftime('%H:%M:%S')}: Approval request processed successfully

## Pending Items
- 0 item(s) in Pending Approval (Local Agent)
- Cloud agent may have additional items in its queues

## Status
Platinum Tier active - Hybrid operation with Cloud (drafts) + Local (execution)

## Financial Summary
- Recent Invoice Created: $XXX.XX for client@example.com
- Pending Invoices: 0
- MTD Revenue: Updated

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
    dashboard_file.write_text(dashboard_content)

    print("\nDEMONSTRATION COMPLETE!")
    print("=" * 60)
    print("[SUCCESS] Cloud Agent operated 24/7 while Local Agent was offline")
    print("[SUCCESS] Draft work completed by Cloud Agent")
    print("[SUCCESS] Approval request created and processed by Local Agent")
    print("[SUCCESS] Sensitive execution handled by Local Agent")
    print("[SUCCESS] Hybrid system maintained operational continuity")
    print("[SUCCESS] Proper separation of duties maintained (privacy/security)")
    print("=" * 60)

if __name__ == "__main__":
    create_demo_scenario()