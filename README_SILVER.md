# Personal AI Employee - Silver Tier

## Overview
This is the Silver Tier implementation of the Autonomous AI Employee system. It provides enhanced automation capabilities with multiple watchers, Claude Code integration, and cross-platform task management.

## Features
- ✅ Multi-channel watchers (Gmail, WhatsApp, LinkedIn, File System)
- ✅ Claude Code integration for task processing
- ✅ Obsidian vault as knowledge base and dashboard
- ✅ Advanced human-in-the-loop approval system
- ✅ Automated logging and monitoring across channels
- ✅ Skill-based task execution across platforms
- ✅ MCP server integration for cross-platform actions

## Directory Structure
```
C:/Users/manal/OneDrive/Desktop/Hacakthon 0/
├── AI_Employee_Vault_Silver/ # Silver Tier Obsidian vault
│   ├── Dashboard.md          # Live status dashboard
│   ├── Company_Handbook.md   # Rules and guidelines
│   ├── Needs_Action/         # New tasks from all channels
│   ├── Plans/                # Task plans created by Claude
│   ├── Pending_Approval/     # Actions needing approval
│   ├── Approved/             # Approved actions
│   ├── Rejected/             # Rejected actions
│   ├── Done/                 # Completed tasks
│   ├── Logs/                 # System logs
│   ├── Skills/               # Agent skills
│   ├── Watchers/             # Channel-specific watchers
│   │   ├── Gmail/            # Gmail watcher files
│   │   ├── WhatsApp/         # WhatsApp watcher files
│   │   ├── LinkedIn/         # LinkedIn watcher files
│   │   └── File_System/      # File system watcher files
│   └── Config/               # System configuration
├── .claude/skills/           # Claude skills directory
├── orchestrator_silver.py    # Silver Tier coordination script
└── filesystem_watcher.py     # File watcher (enhanced)
```

## Setup Instructions

1. **Configure environment variables:**
   - Edit C:/Users/manal/OneDrive/Desktop/Hacakthon 0/.env
   - Add your Claude API key and other credentials
   - Configure API keys for Gmail, WhatsApp, and LinkedIn

2. **Start the system:**
   ```bash
   # Terminal 1 - Start Silver Tier orchestrator
   python orchestrator_silver.py
   ```

3. **Test the system:**
   - Place files in AI_Employee_Vault_Silver/Drop_Folder/
   - Simulate messages in watcher directories
   - Watch Claude process them automatically
   - Check Dashboard.md for updates

## Available Skills:
The system can use skills from C:\Users\manal\OneDrive\Desktop\Hacakthon 0\.claude\skills:
- file_processor: Read and write files
- text_analyzer: Analyze text content
- task_planner: Create detailed task plans
- email_drafter: Draft email responses
- data_extractor: Extract structured data
- linkedin_poster: Create LinkedIn posts
- gmail_reader: Process Gmail messages
- whatsapp_handler: Handle WhatsApp messages
- approval_handler: Manage approval workflow

## How It Works:
1. **Detection**: Multiple watchers monitor Gmail, WhatsApp, LinkedIn, and file system
2. **Task Creation**: Creates .md file in Needs_Action from any channel
3. **Processing**: Orchestrator triggers Claude to process
4. **Planning**: Claude creates plan in /Plans/
5. **Approval**: If needed, creates approval request
6. **Execution**: After approval, actions are taken via MCP servers
7. **Completion**: Files moved to /Done/, dashboard updated

## Silver Tier Requirements Met:
- Multiple watchers (Gmail, WhatsApp, LinkedIn, File System)
- Advanced task processing with Claude Code
- Multiple MCP servers for cross-platform actions
- Dashboard.md updates automatically
- All AI functionality as Agent Skills
- Enhanced human-in-the-loop for approvals

## Next Steps (Gold Tier):
- Add calendar integration
- Implement advanced analytics
- Create custom reporting
- Add more MCP servers
- Enhance security with encryption
- Add machine learning for pattern recognition