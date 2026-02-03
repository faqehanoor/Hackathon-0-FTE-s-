---
name: file_processor
description: Reads, writes, and manipulates files in the vault system. Use when processing documents or creating new files.
---

## Overview
This skill handles file operations within the AI Employee vault.

## When to Use
- Reading documents from Drop_Folder
- Creating task files in Needs_Action
- Moving files between folders
- Writing plan files to Plans directory

## Core Operations
1. **Read**: Access file content for processing
2. **Write**: Create new files with structured content
3. **Move**: Transfer files between vault directories
4. **Validate**: Check file types and content

## Example Usage
When a new file arrives:
1. Read the original file content
2. Create a task file in Needs_Action with metadata
3. Extract key information for processing
4. Log the action to the appropriate log file

## File Naming Convention
- Tasks: TASK_timestamp_original_filename.md
- Plans: PLAN_task_id_description.md
- Logs: YYYY-MM-DD.json

## Security Guidelines
- Only operate on files within the vault directory
- Don't overwrite existing files without confirmation
- Maintain audit trail of all file operations
- Respect file permissions and access controls

## Error Handling
- Log file access errors
- Retry failed operations once
- Escalate persistent errors to human operator