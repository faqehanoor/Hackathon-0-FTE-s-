---
type: skill_definition
skill_id: file_processor
version: 1.0
author: System
category: file_operations
---

# File Processor Skill

This skill enables the AI Employee to read, write, and manipulate files.

## Capabilities
- Read text files (TXT, MD, CSV)
- Write new files
- Parse structured data
- Convert file formats
- Validate file contents

## Usage
```
skill: file_processor
action: read
target: path/to/file.txt
output_format: text
```

## Parameters
- `action`: read, write, parse, validate
- `target`: file path
- `content`: for write operations
- `output_format`: text, json, csv

## Permissions
- Read: All vault directories
- Write: Needs_Action, Plans, Done
- Modify: With approval only