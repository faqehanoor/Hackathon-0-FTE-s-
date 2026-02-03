---
name: social-poster-meta
description: Posts content to Facebook and Instagram via Meta Business API.
---

## Overview
This skill handles posting to Facebook and Instagram with approval workflow.

## When to Use
- When creating business promotion content
- When engaging with followers
- When sharing company updates

## Parameters
- platform: facebook or instagram
- content: Post content/caption
- media_url: Optional image/video URL
- target_audience: Who to target with the post

## Process
1. Format content appropriately for the platform
2. Create approval request in /Pending_Approval/
3. After approval, call Meta Business API to post
4. Track engagement metrics
5. Log the posting action