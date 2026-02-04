# Personal AI Employee - Platinum Tier

## Overview
This is the Platinum Tier implementation of the Autonomous AI Employee system. It provides production-level hybrid operation with cloud and local agents, ensuring 24/7 availability while maintaining privacy and security.

## Features
- ✅ All Gold Tier features (cross-domain integration, Odoo accounting, etc.)
- ✅ Hybrid Cloud + Local Agent Architecture
- ✅ 24/7 Cloud Agent for non-sensitive operations
- ✅ Local Agent for sensitive operations and approvals
- ✅ Proper domain specialization (Cloud vs Local responsibilities)
- ✅ Delegation via synced vault with claim-by-move rule
- ✅ Single-writer rule for Dashboard.md
- ✅ Health monitoring and crash recovery
- ✅ Git-based vault synchronization
- ✅ Privacy-first design (sensitive data stays local)
- ✅ Production-ready architecture

## Architecture

### Cloud Agent (Non-Sensitive Operations)
- Email triage and draft replies
- Social post drafts and scheduling (LinkedIn, Facebook, Instagram, Twitter/X)
- General monitoring (public API watchers)
- Initial processing of all incoming tasks
- Draft creation for all operations
- Preliminary analysis and planning

### Local Agent (Sensitive Operations)
- Final approval of all actions
- WhatsApp session management
- Payments and banking operations
- Final "send/post" actions
- Access to sensitive credentials
- Human-in-the-loop decision making

## Directory Structure
```
C:/Users/manal/OneDrive/Desktop/Hacakthon 0/
├── AI_Employee_Vault_Platinum/ # Platinum Tier Obsidian vault
│   ├── Dashboard.md              # Live status dashboard (Local Agent only)
│   ├── Company_Handbook.md      # Rules and guidelines
│   ├── Business_Goals.md        # Business objectives
│   ├── Needs_Action/            # New tasks from all channels
│   │   ├── email/               # Email-related tasks
│   │   ├── social/              # Social media tasks
│   │   ├── whatsapp/            # WhatsApp tasks
│   │   └── accounting/          # Accounting tasks
│   ├── Plans/                   # Task plans created by Claude
│   │   ├── email/
│   │   ├── social/
│   │   ├── whatsapp/
│   │   └── accounting/
│   ├── Pending_Approval/        # Actions needing approval
│   │   ├── email/
│   │   ├── social/
│   │   ├── whatsapp/
│   │   └── accounting/
│   ├── Approved/                # Approved actions
│   ├── Rejected/                # Rejected actions
│   ├── Done/                    # Completed tasks
│   ├── Logs/                    # System logs
│   ├── Skills/                  # Agent skills
│   ├── Briefings/               # Weekly CEO briefings
│   ├── Accounting/              # Accounting-related files
│   ├── In_Progress/             # Tasks claimed by agents
│   │   ├── cloud/               # Tasks claimed by Cloud Agent
│   │   └── local/               # Tasks claimed by Local Agent
│   ├── Updates/                 # Cloud Agent updates for Local Agent
│   ├── Signals/                 # Cloud Agent signals for Local Agent
│   ├── Watchers/                # Channel-specific watchers
│   │   ├── Gmail/               # Gmail watcher files
│   │   ├── LinkedIn/            # LinkedIn watcher files
│   │   ├── Facebook/            # Facebook watcher files
│   │   ├── Instagram/           # Instagram watcher files
│   │   ├── Twitter/             # Twitter/X watcher files
│   │   └── File_System/         # File system watcher files
│   └── Config/                  # System configuration
├── .claude/skills/              # Claude skills directory
├── cloud_orchestrator.py        # Cloud Agent orchestrator
├── local_orchestrator.py        # Local Agent orchestrator
├── health_monitor.py            # Health monitoring for Cloud Agent
├── vault_sync.py                # Git-based vault synchronization
├── platinum_demo.py             # End-to-end demo script
└── start_platinum_tier.py       # Startup script
```

## Setup Instructions

### 1. Cloud Agent Setup (Oracle Cloud Free Tier Recommended)
1. Sign up for Oracle Cloud Free Tier at oracle.com/cloud/free
2. Create an AMD/ARM-based VM instance
3. Install Python and required dependencies
4. Clone this repository to the cloud instance
5. Configure the remote Git repository for vault synchronization

### 2. Local Agent Setup
1. Ensure .env file with sensitive credentials is NOT synced to cloud
2. Configure local environment with sensitive credentials
3. Set up local Git repository with proper .gitignore

### 3. Configure Environment Variables
- Edit C:/Users/manal/OneDrive/Desktop/Hacakthon 0/.env
- Add your Claude API key and other credentials
- Configure API keys for all services
- Ensure sensitive credentials are NOT synced to cloud

### 4. Start the System
```bash
# On Cloud Instance - Start Cloud Agent and Health Monitor
python cloud_orchestrator.py
python health_monitor.py

# Locally - Start Local Agent when needed
python local_orchestrator.py
```

### 5. Test the System
1. Simulate email received while Local Agent is offline
2. Verify Cloud Agent creates draft and approval request
3. Bring Local Agent online and approve request
4. Verify Local Agent executes the action
5. Check Dashboard.md updates

## Delegation and Sync Protocols

### Claim-by-Move Rule
- When an agent finds a task in Needs_Action, it moves the file to In_Progress/<agent-name>/
- This prevents duplicate work
- Other agents ignore tasks already claimed

### Single-Writer Rule
- Dashboard.md is only updated by Local Agent
- Cloud Agent writes updates to Updates/ or Signals/ folder
- Local Agent merges cloud updates into Dashboard.md

### Vault Sync
- Use Git for synchronization between Cloud and Local agents
- Push/pull via cron jobs
- Only markdown/state files are synced
- Sensitive files (.env, tokens, session files) are excluded via .gitignore

## How It Works:
1. **Cloud Agent Operation**: Runs 24/7 on cloud infrastructure, handling non-sensitive operations
2. **Local Agent Operation**: Runs on local device, handling sensitive operations and approvals
3. **Task Delegation**: Cloud Agent drafts, Local Agent approves and executes
4. **Sync Mechanism**: Git-based synchronization with proper security boundaries
5. **Health Monitoring**: Automatic restart and alerting for cloud agent
6. **Privacy Protection**: Sensitive data remains local at all times

## Platinum Tier Requirements Met:
- All Gold requirements completed
- Cloud Agent running 24/7 for non-sensitive operations
- Local Agent for sensitive operations and approvals
- Proper work-zone specialization (domain ownership)
- Delegation via synced vault with claim-by-move rule
- Single-writer rule for dashboard updates
- Health monitoring and crash recovery
- Privacy-first design with sensitive data staying local
- Production-ready architecture with proper security boundaries

## End-to-End Demo:
The system demonstrates the complete Platinum Tier workflow:
1. Email received while Local Agent offline → Cloud Agent drafts response
2. Cloud Agent creates approval request in Pending_Approval/
3. Local Agent comes online → discovers and approves request
4. Local Agent executes sensitive action (send email, create invoice)
5. Dashboard updated with completion status

This proves the hybrid always-on + safe delegation concept.