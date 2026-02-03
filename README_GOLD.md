# Personal AI Employee - Gold Tier

## Overview
This is the Gold Tier implementation of the Autonomous AI Employee system. It provides full autonomous business operations with cross-domain integration, Odoo accounting, and comprehensive business intelligence.

## Features
- ✅ All Silver Tier features (multi-channel watchers, MCP servers, etc.)
- ✅ Full cross-domain integration (Personal + Business)
- ✅ Odoo Community accounting integration via JSON-RPC API
- ✅ Facebook and Instagram integration
- ✅ Twitter (X) integration
- ✅ Multiple MCP servers (Odoo, Facebook, Instagram, Twitter/X)
- ✅ Weekly Business and Accounting Audit with CEO Briefing
- ✅ Error recovery and graceful degradation
- ✅ Comprehensive audit logging
- ✅ Ralph Wiggum loop for autonomous multi-step tasks
- ✅ All AI functionality as Agent Skills

## Directory Structure
```
C:/Users/manal/OneDrive/Desktop/Hacakthon 0/
├── AI_Employee_Vault_Gold/ # Gold Tier Obsidian vault
│   ├── Dashboard.md          # Live status dashboard
│   ├── Company_Handbook.md   # Rules and guidelines
│   ├── Business_Goals.md     # Business objectives
│   ├── Needs_Action/         # New tasks from all channels
│   ├── Plans/                # Task plans created by Claude
│   ├── Pending_Approval/     # Actions needing approval
│   ├── Approved/             # Approved actions
│   ├── Rejected/             # Rejected actions
│   ├── Done/                 # Completed tasks
│   ├── Logs/                 # System logs
│   ├── Skills/               # Agent skills
│   ├── Briefings/            # Weekly CEO briefings
│   ├── Accounting/           # Accounting-related files
│   ├── Watchers/             # Channel-specific watchers
│   │   ├── Gmail/            # Gmail watcher files
│   │   ├── WhatsApp/         # WhatsApp watcher files
│   │   ├── LinkedIn/         # LinkedIn watcher files
│   │   ├── Facebook/         # Facebook watcher files
│   │   ├── Instagram/        # Instagram watcher files
│   │   ├── Twitter/          # Twitter/X watcher files
│   │   └── File_System/      # File system watcher files
│   └── Config/               # System configuration
├── .claude/skills/           # Claude skills directory
├── orchestrator_gold.py      # Gold Tier coordination script
├── odoo_mcp.py               # Odoo MCP server
├── facebook_mcp.py           # Facebook MCP server
├── instagram_mcp.py          # Instagram MCP server
├── twitter_mcp.py            # Twitter/X MCP server
└── start_gold_tier.py        # Startup script
```

## Setup Instructions

1. **Install Odoo Community Edition (v19+) locally**
   - Download from odoo.com
   - Set up database and user account
   - Enable required modules: Accounting, Invoicing, CRM

2. **Configure environment variables:**
   - Edit C:/Users/manal/OneDrive/Desktop/Hacakthon 0/.env
   - Add your Claude API key and other credentials
   - Configure API keys for Gmail, WhatsApp, LinkedIn, Facebook, Instagram, Twitter/X, and Odoo

3. **Start the system:**
   ```bash
   # Terminal 1 - Start Gold Tier orchestrator and all components
   python start_gold_tier.py
   ```

4. **Test the system:**
   - Place files in AI_Employee_Vault_Gold/Drop_Folder/
   - Simulate messages in watcher directories
   - Watch Claude process them automatically
   - Check Dashboard.md for updates
   - Monitor weekly briefings in Briefings folder

## Available Skills:
The system can use skills from C:\Users\manal\OneDrive\Desktop\Hacakthon 0\.claude\skills:
- All Silver Tier skills
- odoo-invoice-creator: Create invoices in Odoo
- ceo-briefing-generator: Generate CEO briefings
- social-poster-meta: Post to Facebook/Instagram
- social-poster-x: Post to Twitter/X
- social-summarizer: Generate social media summaries
- error-handler: Handle errors gracefully
- audit-logger: Log all actions comprehensively

## How It Works:
1. **Detection**: Multiple watchers monitor all channels
2. **Processing**: Tasks are created and processed by Claude AI
3. **Decision Making**: Following rules in Company_Handbook.md
4. **Odoo Integration**: Invoices, payments, and accounting entries
5. **Social Media**: Posts and engagement across platforms
6. **Action**: Executing approved tasks via MCP servers
7. **Reporting**: Updating Dashboard.md and generating CEO briefings

## Gold Tier Requirements Met:
- All Silver requirements completed
- Full cross-domain integration (Personal + Business)
- Odoo accounting system integration via JSON-RPC API
- Facebook and Instagram integration
- Twitter (X) integration
- Multiple MCP servers for different action types
- Weekly Business and Accounting Audit with CEO Briefing
- Error recovery and graceful degradation
- Comprehensive audit logging
- Ralph Wiggum loop for autonomous multi-step tasks
- All AI functionality as Agent Skills

## Example Workflow:
Client WhatsApp message "invoice bhejo" → AI plan → Odoo invoice draft → approval → invoice posted → email notification → log → briefing reflection.