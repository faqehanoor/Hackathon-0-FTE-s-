---
name: ceo-briefing-generator
description: Generates weekly CEO briefings with financial summary and business insights.
---

## Overview
This skill creates comprehensive weekly briefings for CEO with financial data pulled from Odoo and task completion metrics.

## When to Use
- During scheduled weekly review (typically Sunday/Monday)
- When requested to summarize business performance
- When generating executive reports

## Parameters
- period: Week or month to summarize
- include_financials: Whether to pull revenue/expense data from Odoo
- include_tasks: Whether to summarize completed tasks
- include_insights: Whether to provide proactive suggestions

## Process
1. Pull revenue data from Odoo (account.move filtered by date)
2. Read completed tasks from /Done/ folder
3. Compare against Business_Goals.md targets
4. Identify bottlenecks and delays
5. Generate proactive suggestions (cancel unused subs, follow up on late payments)
6. Format as executive summary with tables and metrics
7. Save to /Briefings/ folder