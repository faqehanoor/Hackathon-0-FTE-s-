---
name: audit-logger
description: Maintains comprehensive audit logs of all system actions.
---

## Overview
This skill ensures all actions are properly logged for audit purposes.

## When to Use
- For every action performed by the system
- When recording approval workflows
- When tracking financial transactions
- When documenting system events

## Parameters
- timestamp: When the action occurred
- action_type: Type of action performed
- actor: Who performed the action (Claude, MCP server, etc.)
- target: What was acted upon
- parameters: Parameters used in the action
- approval_status: Whether approval was required/granted
- result: Success or failure of the action

## Process
1. Capture all relevant information about the action
2. Format as JSON entry
3. Write to daily log file in /Logs/ folder
4. Ensure logs are retained for 90+ days
5. Maintain data integrity and security