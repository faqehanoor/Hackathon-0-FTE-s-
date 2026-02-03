---
type: mcp_server
server_id: MCP_001
status: active
protocol: file_system
---

# MCP Server Definition

This defines a Managed Control Plane server for the AI Employee system.

## Server Details
- Type: File System Monitor
- Protocol: Local file system watching
- Status: Active
- Endpoint: C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault/Drop_Folder

## Capabilities
- Watch for new files
- Trigger task creation
- Support multiple file types
- Real-time notifications

## Configuration
```json
{
  "watch_path": "C:/Users\manal\OneDrive\Desktop\Hacakthon 0\AI_Employee_Vault/Drop_Folder",
  "file_types": [".txt", ".pdf", ".doc", ".docx", ".md"],
  "polling_interval": 5000,
  "notifications": true
}
```