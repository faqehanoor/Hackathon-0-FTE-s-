---
name: task-planner
description: Creates a Plan.md file with steps and checkboxes for tasks. Use for processing items from /Needs_Action.
---

## Overview
Generate structured plans for tasks like emails or files.

## When to Use
- After reading a task file.
- When planning multi-step actions (e.g., reply email, send invoice).

## Core Steps
1. Read the task file content.
2. Identify objective (e.g., "Send invoice").
3. Break into 3-5 steps with checkboxes: - [ ] Step 1
4. Add approval if sensitive (e.g., payment).
5. Write to /Plans/PLAN_task_id.md.

## Example
Input: WhatsApp message - "Send January invoice."

Output Plan.md:
---
created: 2026-02-02
status: pending
---
## Objective
Send invoice to client.

## Steps
- [ ] Calculate amount from rates.
- [ ] Generate PDF.
- [ ] Draft email (requires approval).
- [ ] Log transaction.

## Approval
Move to /Pending_Approval if needed.

## Success Criteria
- Plan has clear steps.
- File moved to /In_Progress after planning.