---
name: odoo-invoice-creator
description: Creates invoices in Odoo accounting system with proper approval workflow.
---

## Overview
This skill connects to Odoo via JSON-RPC API to create customer invoices, with required approval workflow.

## When to Use
- When a client requests an invoice
- When converting a quote to invoice
- When recording billable work in accounting system

## Parameters
- customer_id: Odoo customer/partner ID
- invoice_lines: Array of invoice line items
- due_date: Payment due date
- reference: Invoice reference number

## Process
1. Verify customer exists in Odoo or create new partner
2. Prepare invoice lines with descriptions and amounts
3. Create draft invoice in Odoo
4. Submit for approval before posting
5. After approval, post the invoice to finalize
6. Log the action in audit trail