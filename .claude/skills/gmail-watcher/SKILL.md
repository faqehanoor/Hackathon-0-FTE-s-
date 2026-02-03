---
name: gmail-watcher
description: Monitors Gmail inbox for new emails and creates tasks in the system.
---

## Overview
This skill connects to Gmail via IMAP to check for new emails and creates task files for processing.

## When to Use
- When user wants to monitor Gmail inbox
- When email processing is needed
- When checking for new customer communications

## Parameters
- username: Gmail address
- password: App password for authentication
- check_interval: How often to check for new emails

## Process
1. Connect to Gmail via IMAP
2. Search for unread emails since last check
3. Extract email details (sender, subject, body)
4. Create task file in Watchers/Gmail directory
5. Assign priority based on content keywords