"""
Silver Tier - WhatsApp Watcher
Monitors WhatsApp for new messages and creates tasks
"""
import os
import time
from pathlib import Path
from datetime import datetime
import json

class WhatsAppWatcher:
    def __init__(self, vault_path, whatsapp_config):
        self.vault_path = Path(vault_path)
        self.whatsapp_config = whatsapp_config
        self.whatsapp_dir = self.vault_path / 'Watchers' / 'WhatsApp'
        self.whatsapp_dir.mkdir(exist_ok=True)
        self.last_check = time.time()
        
    def check_new_messages(self):
        """Simulate checking for new WhatsApp messages via API"""
        # In a real implementation, this would connect to WhatsApp Business API
        # For simulation purposes, we'll check for new files in a simulated input directory
        simulated_input_dir = self.vault_path / 'Simulated_Inputs' / 'WhatsApp'
        simulated_input_dir.mkdir(exist_ok=True)
        
        # Look for new message files in the simulated input directory
        new_messages = []
        for msg_file in simulated_input_dir.glob('*.json'):
            if msg_file.stat().st_mtime > self.last_check:
                # Process the message
                with open(msg_file, 'r') as f:
                    msg_data = json.load(f)
                
                # Create task file for the message
                msg_id = f"whatsapp_{int(time.time())}_{hash(str(msg_data)) % 10000}"
                task_file = self.whatsapp_dir / f"{msg_id}.md"
                
                sender = msg_data.get('from', 'Unknown')
                message_body = msg_data.get('body', 'No message body')
                timestamp = msg_data.get('timestamp', datetime.now().isoformat())
                
                # Determine priority
                priority_keywords = ['urgent', 'asap', 'immediately', 'critical']
                priority = 'low'
                msg_lower = message_body.lower()
                for keyword in priority_keywords:
                    if keyword in msg_lower:
                        priority = 'high'
                        break
                elif 'meeting' in msg_lower or 'call' in msg_lower:
                    priority = 'medium'
                
                content = f"""---
type: whatsapp_message
sender: {sender}
received: {timestamp}
priority: {priority}
---

# WhatsApp Message from {sender}

## Message Details
- **From**: {sender}
- **Received**: {timestamp}
- **Priority**: {priority}

## Content
{message_body}

## Action Required
- [ ] Review message content
- [ ] Determine appropriate response
- [ ] Create plan in /Plans/ folder
- [ ] Draft response if needed (with approval if external communication)
"""
                task_file.write_text(content)
                new_messages.append(task_file)
                
                # Move processed file to prevent reprocessing
                processed_dir = self.vault_path / 'Simulated_Inputs' / 'Processed'
                processed_dir.mkdir(exist_ok=True)
                msg_file.rename(processed_dir / msg_file.name)
        
        # Update last check time
        self.last_check = time.time()
        return new_messages

def start_whatsapp_watcher(vault_path, whatsapp_config):
    """Start watching WhatsApp for new messages"""
    watcher = WhatsAppWatcher(vault_path, whatsapp_config)
    
    print(f"[WHATSAPP] WhatsApp Watcher started.")
    print("[INFO] Checking for new messages every 120 seconds...")
    
    try:
        while True:
            new_messages = watcher.check_new_messages()
            if new_messages:
                print(f"[WHATSAPP] Found {len(new_messages)} new message(s)")
            
            time.sleep(120)  # Check every 2 minutes
    except KeyboardInterrupt:
        print("[STOP SIGN] WhatsApp Watcher stopped by user")

if __name__ == "__main__":
    # Load WhatsApp configuration from environment
    import dotenv
    dotenv.load_dotenv()
    
    whatsapp_config = {
        'api_url': os.getenv('WHATSAPP_API_URL', ''),
        'access_token': os.getenv('WHATSAPP_ACCESS_TOKEN', ''),
        'phone_number_id': os.getenv('WHATSAPP_PHONE_NUMBER_ID', '')
    }
    
    if not whatsapp_config['api_url'] or not whatsapp_config['access_token']:
        print("[WARNING] WhatsApp credentials not found in .env file. Please configure WHATSAPP_API_URL and WHATSAPP_ACCESS_TOKEN.")
        print("[INFO] For simulation, place JSON files in AI_Employee_Vault_Silver/Simulated_Inputs/WhatsApp/")
        # Create the simulated input directory
        vault_path = Path("C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Silver")
        sim_dir = vault_path / 'Simulated_Inputs' / 'WhatsApp'
        sim_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a sample message for testing
        sample_msg = {
            "from": "+1234567890",
            "body": "Hi, I'm interested in your services. Can you send me more information?",
            "timestamp": datetime.now().isoformat()
        }
        with open(sim_dir / 'sample_msg.json', 'w') as f:
            json.dump(sample_msg, f)
    
    VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Silver"
    start_whatsapp_watcher(VAULT_PATH, whatsapp_config)