---
name: email-mcp
description: Sends emails via SMTP after approval, handling external communication actions.
---

## Overview
This skill processes approved email tasks and sends them via SMTP protocol.

## When to Use
- When an email needs to be sent after approval
- When handling external communication requests
- When processing items in the Approved folder

## Parameters
- to_email: Recipient email address
- subject: Email subject line
- body: Email body content
- cc: CC recipients (optional)
- bcc: BCC recipients (optional)

## Process
1. Monitor Approved folder for email tasks
2. Extract email details from approval file
3. Connect to SMTP server using credentials
4. Send email to specified recipients
5. Log the action and move processed file to Done