"""
Silver Tier - Gmail Watcher
Monitors Gmail inbox for new emails and creates tasks
"""
import os
import time
import imaplib
import email
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class GmailWatcher:
    def __init__(self, vault_path, email_config):
        self.vault_path = Path(vault_path)
        self.email_config = email_config
        self.gmail_dir = self.vault_path / 'Watchers' / 'Gmail'
        self.gmail_dir.mkdir(exist_ok=True)
        self.last_check = None
        
    def connect_to_gmail(self):
        """Connect to Gmail using IMAP"""
        try:
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.email_config['username'], self.email_config['password'])
            return mail
        except Exception as e:
            print(f"[ERROR] Could not connect to Gmail: {e}")
            return None
    
    def check_new_emails(self):
        """Check for new emails since last check"""
        mail = self.connect_to_gmail()
        if not mail:
            return []
            
        try:
            mail.select('inbox')
            
            # Search for emails since last check or all emails if first run
            if self.last_check:
                search_criteria = f'(SINCE {self.last_check.strftime("%d-%b-%Y")})'
            else:
                search_criteria = 'ALL'
                
            status, messages = mail.search(None, search_criteria)
            email_ids = messages[0].split()
            
            new_emails = []
            for email_id in email_ids[-10:]:  # Check last 10 emails to avoid overload
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                
                # Extract email information
                subject = msg.get('Subject', 'No Subject')
                sender = msg.get('From', 'Unknown Sender')
                date = msg.get('Date', '')
                
                # Create task file for the email
                task_id = f"gmail_{int(time.time())}_{hash(subject) % 10000}"
                task_file = self.gmail_dir / f"{task_id}.md"
                
                # Get email body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                
                # Determine priority based on keywords
                priority_keywords = ['urgent', 'asap', 'immediate', 'critical', 'important']
                priority = 'low'
                email_lower = f"{subject} {body}".lower()
                for keyword in priority_keywords:
                    if keyword in email_lower:
                        priority = 'high'
                        break
                elif 'meeting' in email_lower or 'schedule' in email_lower:
                    priority = 'medium'
                
                content = f"""---
type: gmail_message
subject: {subject}
sender: {sender}
received: {date}
priority: {priority}
---

# Gmail Message: {subject}

## Message Details
- **From**: {sender}
- **Subject**: {subject}
- **Received**: {date}
- **Priority**: {priority}

## Content
{body}

## Action Required
- [ ] Review message content
- [ ] Determine appropriate response
- [ ] Create plan in /Plans/ folder
- [ ] Draft response if needed (with approval if external communication)
"""
                task_file.write_text(content)
                new_emails.append(task_file)
                
            # Update last check time
            self.last_check = datetime.now()
            mail.close()
            mail.logout()
            
            return new_emails
            
        except Exception as e:
            print(f"[ERROR] Error checking emails: {e}")
            return []

def start_gmail_watcher(vault_path, email_config):
    """Start watching Gmail for new emails"""
    watcher = GmailWatcher(vault_path, email_config)
    
    print(f"[EMAIL] Gmail Watcher started. Monitoring: {email_config['username']}")
    print("[INFO] Checking for new emails every 60 seconds...")
    
    try:
        while True:
            new_emails = watcher.check_new_emails()
            if new_emails:
                print(f"[EMAIL] Found {len(new_emails)} new email(s)")
            
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("[STOP SIGN] Gmail Watcher stopped by user")

if __name__ == "__main__":
    # Load email configuration from environment
    import dotenv
    dotenv.load_dotenv()
    
    email_config = {
        'username': os.getenv('GMAIL_USERNAME', ''),
        'password': os.getenv('GMAIL_PASSWORD', ''),  # Use app password
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587
    }
    
    if not email_config['username'] or not email_config['password']:
        print("[WARNING] Gmail credentials not found in .env file. Please configure GMAIL_USERNAME and GMAIL_PASSWORD.")
        exit(1)
    
    VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Silver"
    start_gmail_watcher(VAULT_PATH, email_config)