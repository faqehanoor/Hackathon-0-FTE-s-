---
name: social-poster-x
description: Posts content to Twitter/X via API v2.
---

## Overview
This skill handles posting to Twitter/X with approval workflow.

## When to Use
- When sharing industry insights
- When engaging in professional conversations
- When promoting content

## Parameters
- content: Tweet content (max 280 characters)
- thread: Optional thread of tweets
- hashtags: Relevant hashtags to include

## Process
1. Format content appropriately for Twitter/X
2. Create approval request in /Pending_Approval/
3. After approval, call Twitter/X API to post
4. Track engagement metrics
5. Log the posting action