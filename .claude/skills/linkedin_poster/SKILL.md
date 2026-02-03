---
name: linkedin_poster
description: Creates and posts content to LinkedIn. Use when generating business/sales content or engaging with professional community.
---

## Overview
This skill handles LinkedIn posting functionality for business development.

## When to Use
- Creating promotional content for services/products
- Sharing industry insights or tips
- Engaging with professional community
- Following up on business opportunities

## Posting Process
1. **Content Creation**: Draft engaging post with hook + value + CTA + hashtags
2. **Approval Request**: Create approval file in /Pending_Approval/ before posting
3. **MCP Execution**: After approval, call LinkedIn MCP server to post
4. **Confirmation**: Update dashboard with posting status

## Post Structure
```
Hook: Attention-grabbing opening line
Value: Insight, tip, or valuable information
CTA: Clear call-to-action
Hashtags: #Industry #Business #Networking
```

## Example
Input: "Share insight about AI automation benefits"

Output:
"🤖 Did you know that businesses using AI automation see an average 40% increase in productivity?

Small changes, big results. At [Company], we help businesses leverage AI to streamline operations and boost efficiency.

Want to explore how AI can transform your business? Let's connect!

#AI #Automation #BusinessEfficiency #Innovation #Productivity"