"""
Silver Tier - Email MCP Server
Handles external email actions via SMTP
"""
import os
import smtplib
import time
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json

class EmailMCP:
    def __init__(self, config):
        self.config = config
        self.running = True
        
    def send_email(self, to_email, subject, body, cc=None, bcc=None):
        """Send an email via SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.config['username']
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = cc
                
            # Add body to email
            msg.attach(MIMEText(body, 'plain'))
            
            # Create SMTP session
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()  # Enable security
            server.login(self.config['username'], self.config['password'])
            
            # Get all recipients
            recipients = [to_email]
            if cc:
                recipients.extend(cc.split(','))
            if bcc:
                recipients.extend(bcc.split(','))
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.config['username'], recipients, text)
            server.quit()
            
            print(f"[EMAIL_MCP] Email sent successfully to {to_email}")
            
            # Log the action
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'email_sent',
                'to': to_email,
                'subject': subject,
                'status': 'success'
            }
            
            return True, log_entry
            
        except Exception as e:
            print(f"[EMAIL_MCP] Failed to send email: {e}")
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': 'email_failed',
                'to': to_email,
                'subject': subject,
                'error': str(e),
                'status': 'failed'
            }
            
            return False, log_entry
    
    def monitor_approvals(self, vault_path):
        """Monitor the Approved folder for email tasks"""
        vault = Path(vault_path)
        approved_dir = vault / 'Approved'
        
        if not approved_dir.exists():
            approved_dir.mkdir(parents=True, exist_ok=True)
            return []
        
        # Find email approval files
        email_approvals = []
        for file in approved_dir.glob('*email*'):
            if file.suffix == '.md':
                email_approvals.append(file)
        
        return email_approvals
    
    def process_email_approvals(self, vault_path):
        """Process approved email tasks"""
        approvals = self.monitor_approvals(vault_path)
        
        for approval_file in approvals:
            # Read the approval file to extract email details
            content = approval_file.read_text()
            
            # Extract email details (this is simplified parsing)
            lines = content.split('\n')
            to_email = None
            subject = None
            body = []
            collecting_body = False
            
            for line in lines:
                if line.startswith('- To:'):
                    to_email = line.replace('- To:', '').strip()
                elif line.startswith('- Subject:'):
                    subject = line.replace('- Subject:', '').strip()
                elif line.startswith('## Email Body'):
                    collecting_body = True
                elif collecting_body and line.startswith('- '):
                    body.append(line.replace('- ', ''))
                elif collecting_body and line.strip() == '':
                    collecting_body = False
            
            body_text = '\n'.join(body)
            
            if to_email and subject and body_text:
                # Send the email
                success, log_entry = self.send_email(to_email, subject, body_text)
                
                # Log the result
                logs_dir = Path(vault_path) / 'Logs'
                logs_dir.mkdir(exist_ok=True)
                today = datetime.now().strftime('%Y-%m-%d')
                log_file = logs_dir / f'{today}_mcp.json'
                
                # Read existing logs or create new
                if log_file.exists():
                    with open(log_file, 'r') as f:
                        logs = json.load(f)
                else:
                    logs = []
                
                logs.append(log_entry)
                
                with open(log_file, 'w') as f:
                    json.dump(logs, f, indent=2)
                
                # Move processed file to Done
                done_dir = Path(vault_path) / 'Done'
                done_dir.mkdir(exist_ok=True)
                approval_file.rename(done_dir / approval_file.name)
                
                print(f"[EMAIL_MCP] Processed email approval: {approval_file.name}")
    
    def run(self, vault_path):
        """Main MCP server loop"""
        print(f"[EMAIL_MCP] Email MCP Server started.")
        print(f"[EMAIL_MCP] Monitoring for approved email tasks...")
        
        try:
            while self.running:
                self.process_email_approvals(vault_path)
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("[EMAIL_MCP] Email MCP Server stopped by user")

if __name__ == "__main__":
    # Load email configuration from environment
    import dotenv
    dotenv.load_dotenv()
    
    config = {
        'username': os.getenv('GMAIL_USERNAME', ''),
        'password': os.getenv('GMAIL_PASSWORD', ''),  # Use app password
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587
    }
    
    if not config['username'] or not config['password']:
        print("[WARNING] Gmail credentials not found in .env file. Please configure GMAIL_USERNAME and GMAIL_PASSWORD.")
        exit(1)
    
    VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Silver"
    mcp_server = EmailMCP(config)
    mcp_server.run(VAULT_PATH)