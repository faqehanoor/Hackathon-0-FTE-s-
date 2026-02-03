# Welcome to Your Personal AI Employee System

## Overview
This is your Bronze Tier autonomous AI employee system. It's designed to handle routine tasks, process documents, and assist with daily operations.

## Current Status
- System: Active
- Tier: Bronze
- Last Update: February 3, 2026
- Capabilities: File processing, task management, basic decision making

## How It Works
1. **Detection**: File watcher monitors the Drop_Folder for new files
2. **Processing**: Tasks are created and processed by Claude AI
3. **Decision Making**: Following rules in Company_Handbook.md
4. **Action**: Executing approved tasks automatically
5. **Reporting**: Updating Dashboard.md with status

## Directory Structure
- `Drop_Folder/` - Place files here to trigger processing
- `Needs_Action/` - New tasks detected by system
- `Plans/` - Detailed plans created by Claude
- `Pending_Approval/` - Actions requiring human approval
- `Approved/` - Tasks approved for execution
- `Rejected/` - Tasks that were rejected
- `Done/` - Successfully completed tasks
- `Logs/` - System activity logs
- `Skills/` - Available AI capabilities
- `Config/` - System configuration

## Getting Started
1. Place a document in `Drop_Folder/` to begin processing
2. Monitor `Dashboard.md` for system status
3. Review and approve/reject tasks in `Pending_Approval/` as needed
4. Check `Done/` folder for completed tasks

## Support
For questions or issues, refer to the system documentation or contact your system administrator.