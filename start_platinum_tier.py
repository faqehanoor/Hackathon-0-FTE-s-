"""
Platinum Tier - Startup Script
Manages both Cloud and Local Agent operations
"""
import subprocess
import sys
import os
from pathlib import Path
import argparse

def start_component(script_name, description, is_daemon=False):
    """Start a component and return its process"""
    print(f"[STARTUP] Starting {description}...")
    try:
        if is_daemon:
            # For daemon processes, we might want different handling
            process = subprocess.Popen([sys.executable, script_name])
        else:
            process = subprocess.Popen([sys.executable, script_name])
        print(f"[STARTUP] {description} started with PID: {process.pid}")
        return process
    except Exception as e:
        print(f"[ERROR] Failed to start {description}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Platinum Tier AI Employee System')
    parser.add_argument('--mode', choices=['cloud', 'local', 'demo'], 
                       default='local', help='Run mode: cloud, local, or demo')
    parser.add_argument('--skip-monitor', action='store_true', 
                       help='Skip starting health monitor')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Platinum Tier AI Employee System - Startup")
    print("=" * 60)
    print(f"Mode: {args.mode.upper()}")
    print("=" * 60)
    
    processes = {}
    
    if args.mode == 'cloud':
        # Cloud Agent Mode - Start cloud-specific components
        print("Starting Cloud Agent components...")
        
        components = [
            ("cloud_orchestrator.py", "Cloud Agent Orchestrator"),
        ]
        
        if not args.skip_monitor:
            components.append(("health_monitor.py", "Health Monitor"))
        
        for script, description in components:
            if Path(script).exists():
                process = start_component(script, description)
                if process:
                    processes[description] = process
            else:
                print(f"[WARNING] {script} not found, skipping...")
    
    elif args.mode == 'local':
        # Local Agent Mode - Start local-specific components
        print("Starting Local Agent components...")
        
        components = [
            ("local_orchestrator.py", "Local Agent Orchestrator"),
        ]
        
        for script, description in components:
            if Path(script).exists():
                process = start_component(script, description)
                if process:
                    processes[description] = process
            else:
                print(f"[WARNING] {script} not found, skipping...")
    
    elif args.mode == 'demo':
        # Demo Mode - Run the end-to-end demo
        print("Running Platinum Tier Demo...")
        
        if Path("platinum_demo.py").exists():
            demo_result = subprocess.run([sys.executable, "platinum_demo.py"])
            print(f"\nDemo completed with return code: {demo_result.returncode}")
        else:
            print("[ERROR] platinum_demo.py not found")
    
    print("\n" + "=" * 60)
    if processes:
        print("Platinum Tier components started successfully!")
        print("=" * 60)
        print("\nActive processes:")
        for desc, proc in processes.items():
            print(f"  - {desc} (PID: {proc.pid})")
        
        print("\nSystem status:")
        if args.mode == 'cloud':
            print("  - Cloud Agent running 24/7 for non-sensitive operations")
            print("  - Health monitoring active")
            print("  - Processing email, social media, and accounting drafts")
        elif args.mode == 'local':
            print("  - Local Agent running for sensitive operations")
            print("  - Monitoring for approval requests from Cloud Agent")
            print("  - Handling final execution of sensitive actions")
        
        print("\nTo stop the system, press Ctrl+C in this window.")
    else:
        print("No components started. Check that you're in the correct directory.")
    print("=" * 60)

if __name__ == "__main__":
    main()