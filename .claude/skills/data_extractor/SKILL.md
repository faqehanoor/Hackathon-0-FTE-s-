---
name: data_extractor
description: Extracts structured data from documents and files. Use when processing invoices, forms, or other structured documents.
---

## Overview
This skill extracts key information from various document types.

## When to Use
- Processing invoices or receipts
- Extracting contact information
- Reading form submissions
- Parsing structured data from documents

## Extraction Types
1. **Financial Data**: Amounts, dates, account numbers
2. **Contact Info**: Names, emails, phone numbers, addresses
3. **Dates & Times**: Appointments, deadlines, schedules
4. **Identifiers**: Order numbers, invoice IDs, reference codes

## Output Format
Return extracted data as structured JSON:
```json
{
  "type": "invoice|contact|form|other",
  "extracted_data": {
    "amount": 1250.00,
    "date": "2026-02-01",
    "client": "ABC Corp",
    "reference": "INV-2026-001"
  },
  "confidence": 0.95
}
```

## Validation
- Cross-reference extracted data with known patterns
- Flag unusual values for human review
- Verify data consistency across fields

## Error Handling
- Log extraction failures
- Note confidence levels for uncertain extractions
- Fallback to manual review for low-confidence data