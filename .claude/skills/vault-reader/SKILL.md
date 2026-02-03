---
name: vault-reader
description: Reads files from the Obsidian vault folders like /Needs_Action or /Dashboard. Use when checking for new tasks or updating status.
---

## Overview
This skill helps Claude read Markdown files in the vault to process tasks.

## When to Use
- When user says "Check Needs_Action" or similar.
- Automatically when detecting new files via watchers.

## Steps to Follow
1. Use file system tools to list files in /Needs_Action.
2. Read the content of each .md file.
3. Summarize: Extract type, from, subject, content.
4. Write summary to Dashboard.md if needed.

## Example
If file is EMAIL_123.md with content:
---
type: email
from: client@example.com
---
Email Content: Need invoice.

Output: "New email from client about invoice. Action: Generate plan."

## Checklist
- Always check file permissions.
- Don't modify files unless approved.
- Log actions to /Logs.