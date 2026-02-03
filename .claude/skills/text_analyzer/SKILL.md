---
name: text_analyzer
description: Analyzes text content to determine sentiment, topic, urgency, and appropriate response. Use when processing emails, messages, or documents.
---

## Overview
This skill analyzes text content to help classify and prioritize tasks.

## When to Use
- Processing incoming emails or messages
- Analyzing document content for categorization
- Determining urgency level of requests
- Identifying key topics in text

## Analysis Types
1. **Sentiment**: Positive, neutral, negative
2. **Urgency**: Low, medium, high, critical
3. **Category**: Sales, support, finance, HR, general
4. **Entities**: People, organizations, dates, amounts

## Output Format
Return analysis as structured data:
```json
{
  "sentiment": "neutral",
  "urgency": "medium",
  "category": "support",
  "entities": ["client name", "product issue"],
  "keywords": ["refund", "complaint", "urgent"],
  "recommended_action": "create_support_ticket"
}
```

## Classification Guidelines
- **Critical Urgency**: Threats, security issues, legal matters
- **High Urgency**: Financial transactions, deadline approaching
- **Medium Urgency**: Customer inquiries, routine requests
- **Low Urgency**: General information, non-time-sensitive

## Integration
- Pass results to task planner for appropriate action
- Update dashboard with priority indicators
- Route to appropriate team based on category

## Accuracy Considerations
- Flag ambiguous content for human review
- Apply company policies to classification decisions
- Consider context from previous communications