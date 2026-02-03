---
name: approval_handler
description: Manages the approval workflow by monitoring Pending_Approval folder and executing actions when files are moved to Approved folder.
---

## Overview
This skill handles the human-in-the-loop approval process.

## When to Use
- Monitoring /Pending_Approval/ for new requests
- Detecting when files are moved to /Approved/
- Executing approved actions via MCP servers
- Logging results when actions are completed

## Approval Workflow
1. **Monitor**: Watch /Pending_Approval/ for new approval requests
2. **Wait**: Allow human to review and move files to /Approved/ or /Rejected/
3. **Execute**: When moved to /Approved/, execute the requested action
4. **Log**: Record outcome and move to /Done/

## Action Execution
- **Email**: Use email-mcp to send draft/response
- **LinkedIn**: Use linkedin-mcp to post content
- **WhatsApp**: Use whatsapp-mcp to send message
- **Other**: Use appropriate MCP server

## Error Handling
- Log MCP server failures
- Retry failed actions once
- Escalate persistent failures to human operator
- Update dashboard with execution status