"""
Gold Tier - Startup Script
Launches all Gold Tier components
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
    print("Gold Tier AI Employee System - Startup")
    print("=" * 60)
    
    # Define components to start
    components = [
        ("orchestrator_gold.py", "Gold Tier Orchestrator"),
        ("gmail_watcher.py", "Gmail Watcher"),
        ("whatsapp_watcher.py", "WhatsApp Watcher"),
        ("linkedin_poster.py", "LinkedIn Poster"),
        ("email_mcp.py", "Email MCP Server"),
        ("odoo_mcp.py", "Odoo MCP Server"),
        ("facebook_mcp.py", "Facebook MCP Server"),
        ("instagram_mcp.py", "Instagram MCP Server"),
        ("twitter_mcp.py", "Twitter/X MCP Server"),
        ("scheduler.py", "Task Scheduler")
    ]
    
    processes = {}
    
    # Start all components
    for script, description in components:
        # Check if the script exists before starting
        if Path(script).exists():
            process = start_component(script, description)
            if process:
                processes[description] = process
        else:
            print(f"[WARNING] {script} not found, skipping...")
    
    print("\n" + "=" * 60)
    print("Gold Tier components started successfully!")
    print("=" * 60)
    print("\nComponents running:")
    for desc, proc in processes.items():
        print(f"  - {desc} (PID: {proc.pid})")
    
    print("\nSystem is now monitoring:")
    print("  - Gmail inbox for new emails")
    print("  - WhatsApp for new messages")
    print("  - LinkedIn for engagement opportunities")
    print("  - Facebook for messages and comments")
    print("  - Instagram for DMs and comments")
    print("  - Twitter/X for mentions and DMs")
    print("  - File system for new documents")
    print("  - Scheduled tasks")
    print("  - Pending approvals")
    print("  - Odoo accounting system")
    print("\nThe Gold Tier AI Employee is now operational!")
    print("\nTo stop the system, press Ctrl+C in this window.")

if __name__ == "__main__":
    main()