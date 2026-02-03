"""
Gold Tier - Facebook MCP Server
Handles Facebook operations via Meta Business API
"""
import os
import json
import requests
import time
from pathlib import Path
from datetime import datetime

class FacebookMCP:
    def __init__(self, config):
        self.config = config
        self.access_token = config['access_token']
        self.page_id = config['page_id']
        self.base_url = f"https://graph.facebook.com/v17.0/{self.page_id}"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        self.running = True
        
    def post_message(self, message, attachment_url=None):
        """Post a message to Facebook page"""
        url = f"{self.base_url}/feed"
        data = {
            'message': message
        }
        
        if attachment_url:
            data['link'] = attachment_url
        
        try:
            response = requests.post(url, headers=self.headers, data=data)
            result = response.json()
            
            if 'id' in result:
                print(f"[FACEBOOK_MCP] Post created with ID: {result['id']}")
                return result['id']
            else:
                print(f"[FACEBOOK_MCP] Error posting message: {result}")
                return None
        except Exception as e:
            print(f"[FACEBOOK_MCP] Error posting message: {e}")
            return None
    
    def send_private_reply(self, comment_id, message):
        """Send a private reply to a comment"""
        url = f"{self.base_url}/comments"
        data = {
            'comment_id': comment_id,
            'message': message
        }
        
        try:
            response = requests.post(url, headers=self.headers, data=data)
            result = response.json()
            
            if 'success' in result and result['success']:
                print(f"[FACEBOOK_MCP] Private reply sent to comment {comment_id}")
                return True
            else:
                print(f"[FACEBOOK_MCP] Error sending private reply: {result}")
                return False
        except Exception as e:
            print(f"[FACEBOOK_MCP] Error sending private reply: {e}")
            return False
    
    def get_page_info(self):
        """Get basic page information"""
        url = f"{self.base_url}?fields=name,fan_count,overall_star_rating"
        
        try:
            response = requests.get(url, headers=self.headers)
            result = response.json()
            
            if 'name' in result:
                print(f"[FACEBOOK_MCP] Connected to page: {result['name']}")
                return result
            else:
                print(f"[FACEBOOK_MCP] Error getting page info: {result}")
                return None
        except Exception as e:
            print(f"[FACEBOOK_MCP] Error getting page info: {e}")
            return None
    
    def monitor_approvals(self, vault_path):
        """Monitor the Approved folder for Facebook tasks"""
        vault = Path(vault_path)
        approved_dir = vault / 'Approved'
        
        if not approved_dir.exists():
            approved_dir.mkdir(parents=True, exist_ok=True)
            return []
        
        # Find Facebook approval files
        facebook_approvals = []
        for file in approved_dir.glob('*facebook*'):
            if file.suffix == '.md':
                facebook_approvals.append(file)
        
        for file in approved_dir.glob('*fb*'):
            if file.suffix == '.md':
                facebook_approvals.append(file)
        
        return facebook_approvals
    
    def process_facebook_approvals(self, vault_path):
        """Process approved Facebook tasks"""
        approvals = self.monitor_approvals(vault_path)
        
        for approval_file in approvals:
            # Read the approval file to extract details
            content = approval_file.read_text()
            
            print(f"[FACEBOOK_MCP] Processing Facebook approval: {approval_file.name}")
            
            # Extract message from the approval file (simplified parsing)
            lines = content.split('\n')
            message = ""
            collecting_message = False
            
            for line in lines:
                if 'Post Draft' in line:
                    collecting_message = True
                elif collecting_message and line.startswith('#'):
                    collecting_message = False
                elif collecting_message and not line.startswith('##'):
                    message += line + "\n"
            
            if message.strip():
                # Post the message to Facebook
                post_id = self.post_message(message.strip())
                
                if post_id:
                    result = {
                        'status': 'success',
                        'operation': 'post_created',
                        'post_id': post_id,
                        'file_processed': approval_file.name
                    }
                    
                    # Log the result
                    self.log_operation(result, vault_path)
                    
                    # Move processed file to Done
                    done_dir = Path(vault_path) / 'Done'
                    done_dir.mkdir(exist_ok=True)
                    approval_file.rename(done_dir / approval_file.name)
                    
                    print(f"[FACEBOOK_MCP] Posted to Facebook: {post_id}")
                else:
                    print(f"[FACEBOOK_MCP] Failed to post to Facebook")
            else:
                print(f"[FACEBOOK_MCP] No message found in approval file: {approval_file.name}")
    
    def log_operation(self, result, vault_path):
        """Log the operation to the appropriate log file"""
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(exist_ok=True)
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = logs_dir / f'{today}_facebook.json'
        
        # Read existing logs or create new
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append({
            'timestamp': datetime.now().isoformat(),
            'action': result['operation'],
            'file': result['file_processed'],
            'status': result['status'],
            'details': result
        })
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def run(self, vault_path):
        """Main MCP server loop"""
        print(f"[FACEBOOK_MCP] Facebook MCP Server started.")
        print(f"[FACEBOOK_MCP] Page ID: {self.page_id}")
        print(f"[FACEBOOK_MCP] Monitoring for approved Facebook tasks...")
        
        page_info = self.get_page_info()
        if not page_info:
            print("[FACEBOOK_MCP] Cannot proceed without valid page connection")
            return
        
        try:
            while self.running:
                self.process_facebook_approvals(vault_path)
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("[FACEBOOK_MCP] Facebook MCP Server stopped by user")

if __name__ == "__main__":
    # Load Facebook configuration from environment
    import dotenv
    dotenv.load_dotenv()
    
    config = {
        'access_token': os.getenv('FACEBOOK_ACCESS_TOKEN', 'your_access_token_here'),
        'page_id': os.getenv('FACEBOOK_PAGE_ID', 'your_page_id_here'),
    }
    
    if not config['access_token'] or config['access_token'] == 'your_access_token_here':
        print("[WARNING] Facebook access token not found in .env file. Please configure FACEBOOK_ACCESS_TOKEN.")
        print("[INFO] This is a simulation - Facebook operations will be logged but not executed.")
    else:
        VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Gold"
        mcp_server = FacebookMCP(config)
        mcp_server.run(VAULT_PATH)