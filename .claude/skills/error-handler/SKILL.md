---
name: error-handler
description: Handles errors gracefully with recovery mechanisms.
---

## Overview
This skill manages error handling and recovery for the AI Employee system.

## When to Use
- When encountering API timeouts or rate limits
- When authentication fails
- When tasks are misinterpreted
- When processes fail unexpectedly

## Parameters
- error_type: Type of error encountered
- severity: Critical, high, medium, or low
- affected_system: Which system/component is affected

## Process
1. Identify error type and severity
2. For transient errors: Implement exponential backoff retry (3 attempts)
3. For auth failures: Create alert file in /Needs_Action/, pause affected component
4. For logic failures: Queue for human review
5. Log error details for debugging
6. Resume operations when possible