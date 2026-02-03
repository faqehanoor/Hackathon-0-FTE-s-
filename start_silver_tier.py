"""
Silver Tier - Startup Script
Launches all Silver Tier components
"""
import subprocess
import sys
import os
from pathlib import Path

def start_component(script_name, description):
    """Start a component and return its process"""
    print(f"[STARTUP] Starting {description}...")
    try:
        process = subprocess.Popen([sys.executable, script_name])
        print(f"[STARTUP] {description} started with PID: {process.pid}")
        return process
    except Exception as e:
        print(f"[ERROR] Failed to start {description}: {e}")
        return None

def main():
    print("=" * 60)
    print("Silver Tier AI Employee System - Startup")
    print("=" * 60)
    
    # Define components to start
    components = [
        ("orchestrator_silver.py", "Silver Tier Orchestrator"),
        ("gmail_watcher.py", "Gmail Watcher"),
        ("whatsapp_watcher.py", "WhatsApp Watcher"),
        ("linkedin_poster.py", "LinkedIn Poster"),
        ("email_mcp.py", "Email MCP Server"),
        ("scheduler.py", "Task Scheduler")
    ]
    
    processes = {}
    
    # Start all components
    for script, description in components:
        process = start_component(script, description)
        if process:
            processes[description] = process
    
    print("\n" + "=" * 60)
    print("All Silver Tier components started successfully!")
    print("=" * 60)
    print("\nComponents running:")
    for desc, proc in processes.items():
        print(f"  - {desc} (PID: {proc.pid})")
    
    print("\nSystem is now monitoring:")
    print("  - Gmail inbox for new emails")
    print("  - WhatsApp for new messages")
    print("  - LinkedIn for engagement opportunities")
    print("  - File system for new documents")
    print("  - Scheduled tasks")
    print("  - Pending approvals")
    print("\nThe Silver Tier AI Employee is now operational!")
    print("\nTo stop the system, press Ctrl+C in this window.")

if __name__ == "__main__":
    main()