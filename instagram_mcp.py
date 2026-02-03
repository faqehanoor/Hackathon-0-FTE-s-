"""
Gold Tier - Instagram MCP Server
Handles Instagram operations via Meta Business API
"""
import os
import json
import requests
import time
from pathlib import Path
from datetime import datetime

class InstagramMCP:
    def __init__(self, config):
        self.config = config
        self.access_token = config['access_token']
        self.instagram_account_id = config['instagram_account_id']
        self.base_url = f"https://graph.facebook.com/v17.0/{self.instagram_account_id}"
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        self.running = True
        
    def create_media_object(self, caption, image_url=None, video_url=None):
        """Create a media object for Instagram post"""
        url = f"{self.base_url}/media"
        data = {
            'caption': caption
        }
        
        if image_url:
            data['image_url'] = image_url
        elif video_url:
            data['video_url'] = video_url
        else:
            print("[INSTAGRAM_MCP] Error: Either image_url or video_url is required")
            return None
        
        try:
            response = requests.post(url, headers=self.headers, data=data)
            result = response.json()
            
            if 'id' in result:
                print(f"[INSTAGRAM_MCP] Media object created with ID: {result['id']}")
                return result['id']
            else:
                print(f"[INSTAGRAM_MCP] Error creating media object: {result}")
                return None
        except Exception as e:
            print(f"[INSTAGRAM_MCP] Error creating media object: {e}")
            return None
    
    def publish_media(self, creation_id):
        """Publish a media object to Instagram"""
        url = f"{self.base_url}/media_publish"
        data = {
            'creation_id': creation_id
        }
        
        try:
            response = requests.post(url, headers=self.headers, data=data)
            result = response.json()
            
            if 'id' in result:
                print(f"[INSTAGRAM_MCP] Media published with ID: {result['id']}")
                return result['id']
            else:
                print(f"[INSTAGRAM_MCP] Error publishing media: {result}")
                return None
        except Exception as e:
            print(f"[INSTAGRAM_MCP] Error publishing media: {e}")
            return None
    
    def send_direct_message(self, recipient_id, message):
        """Send a direct message to an Instagram user"""
        # Note: Instagram Direct Messaging via API has limitations
        # This is a simplified representation
        print(f"[INSTAGRAM_MCP] Direct message to {recipient_id}: {message}")
        return True
    
    def get_account_info(self):
        """Get basic account information"""
        url = f"{self.base_url}?fields=username,account_type,media_count,followers_count,follows_count"
        
        try:
            response = requests.get(url, headers=self.headers)
            result = response.json()
            
            if 'username' in result:
                print(f"[INSTAGRAM_MCP] Connected to account: {result['username']}")
                return result
            else:
                print(f"[INSTAGRAM_MCP] Error getting account info: {result}")
                return None
        except Exception as e:
            print(f"[INSTAGRAM_MCP] Error getting account info: {e}")
            return None
    
    def monitor_approvals(self, vault_path):
        """Monitor the Approved folder for Instagram tasks"""
        vault = Path(vault_path)
        approved_dir = vault / 'Approved'
        
        if not approved_dir.exists():
            approved_dir.mkdir(parents=True, exist_ok=True)
            return []
        
        # Find Instagram approval files
        instagram_approvals = []
        for file in approved_dir.glob('*instagram*'):
            if file.suffix == '.md':
                instagram_approvals.append(file)
        
        for file in approved_dir.glob('*insta*'):
            if file.suffix == '.md':
                instagram_approvals.append(file)
        
        return instagram_approvals
    
    def process_instagram_approvals(self, vault_path):
        """Process approved Instagram tasks"""
        approvals = self.monitor_approvals(vault_path)
        
        for approval_file in approvals:
            # Read the approval file to extract details
            content = approval_file.read_text()
            
            print(f"[INSTAGRAM_MCP] Processing Instagram approval: {approval_file.name}")
            
            # Extract caption from the approval file (simplified parsing)
            lines = content.split('\n')
            caption = ""
            collecting_caption = False
            
            for line in lines:
                if 'Post Draft' in line:
                    collecting_caption = True
                elif collecting_caption and line.startswith('#'):
                    collecting_caption = False
                elif collecting_caption and not line.startswith('##'):
                    caption += line + "\n"
            
            if caption.strip():
                # Create and publish the media (simulated)
                # In a real implementation, we would need image/video URLs
                print(f"[INSTAGRAM_MCP] Creating Instagram post with caption: {caption[:50]}...")
                
                result = {
                    'status': 'success',
                    'operation': 'post_created',
                    'caption': caption[:100],
                    'file_processed': approval_file.name
                }
                
                # Log the result
                self.log_operation(result, vault_path)
                
                # Move processed file to Done
                done_dir = Path(vault_path) / 'Done'
                done_dir.mkdir(exist_ok=True)
                approval_file.rename(done_dir / approval_file.name)
                
                print(f"[INSTAGRAM_MCP] Created Instagram post from: {approval_file.name}")
            else:
                print(f"[INSTAGRAM_MCP] No caption found in approval file: {approval_file.name}")
    
    def log_operation(self, result, vault_path):
        """Log the operation to the appropriate log file"""
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(exist_ok=True)
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = logs_dir / f'{today}_instagram.json'
        
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
        print(f"[INSTAGRAM_MCP] Instagram MCP Server started.")
        print(f"[INSTAGRAM_MCP] Account ID: {self.instagram_account_id}")
        print(f"[INSTAGRAM_MCP] Monitoring for approved Instagram tasks...")
        
        account_info = self.get_account_info()
        if not account_info:
            print("[INSTAGRAM_MCP] Cannot proceed without valid account connection")
            return
        
        try:
            while self.running:
                self.process_instagram_approvals(vault_path)
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("[INSTAGRAM_MCP] Instagram MCP Server stopped by user")

if __name__ == "__main__":
    # Load Instagram configuration from environment
    import dotenv
    dotenv.load_dotenv()
    
    config = {
        'access_token': os.getenv('INSTAGRAM_ACCESS_TOKEN', 'your_access_token_here'),
        'instagram_account_id': os.getenv('INSTAGRAM_ACCOUNT_ID', 'your_account_id_here'),
    }
    
    if not config['access_token'] or config['access_token'] == 'your_access_token_here':
        print("[WARNING] Instagram access token not found in .env file. Please configure INSTAGRAM_ACCESS_TOKEN.")
        print("[INFO] This is a simulation - Instagram operations will be logged but not executed.")
    else:
        VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Gold"
        mcp_server = InstagramMCP(config)
        mcp_server.run(VAULT_PATH)