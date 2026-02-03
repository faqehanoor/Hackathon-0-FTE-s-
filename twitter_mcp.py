"""
Gold Tier - Twitter/X MCP Server
Handles Twitter/X operations via API v2
"""
import os
import json
import requests
import time
from pathlib import Path
from datetime import datetime

class TwitterMCP:
    def __init__(self, config):
        self.config = config
        self.bearer_token = config['bearer_token']
        self.base_url = "https://api.twitter.com/2"
        self.headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json'
        }
        self.running = True
        
    def post_tweet(self, text, reply_to_id=None):
        """Post a tweet to Twitter/X"""
        url = f"{self.base_url}/tweets"
        
        data = {
            'text': text
        }
        
        if reply_to_id:
            data['reply'] = {'in_reply_to_tweet_id': reply_to_id}
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            result = response.json()
            
            if 'data' in result and 'id' in result['data']:
                print(f"[TWITTER_MCP] Tweet posted with ID: {result['data']['id']}")
                return result['data']['id']
            else:
                print(f"[TWITTER_MCP] Error posting tweet: {result}")
                return None
        except Exception as e:
            print(f"[TWITTER_MCP] Error posting tweet: {e}")
            return None
    
    def get_user_info(self, username):
        """Get user information by username"""
        url = f"{self.base_url}/users/by/username/{username}"
        
        try:
            response = requests.get(url, headers=self.headers)
            result = response.json()
            
            if 'data' in result:
                print(f"[TWITTER_MCP] Retrieved info for user: {result['data']['username']}")
                return result['data']
            else:
                print(f"[TWITTER_MCP] Error getting user info: {result}")
                return None
        except Exception as e:
            print(f"[TWITTER_MCP] Error getting user info: {e}")
            return None
    
    def monitor_approvals(self, vault_path):
        """Monitor the Approved folder for Twitter/X tasks"""
        vault = Path(vault_path)
        approved_dir = vault / 'Approved'
        
        if not approved_dir.exists():
            approved_dir.mkdir(parents=True, exist_ok=True)
            return []
        
        # Find Twitter/X approval files
        twitter_approvals = []
        for file in approved_dir.glob('*twitter*'):
            if file.suffix == '.md':
                twitter_approvals.append(file)
        
        for file in approved_dir.glob('*x*'):
            if file.suffix == '.md':
                twitter_approvals.append(file)
        
        return twitter_approvals
    
    def process_twitter_approvals(self, vault_path):
        """Process approved Twitter/X tasks"""
        approvals = self.monitor_approvals(vault_path)
        
        for approval_file in approvals:
            # Read the approval file to extract details
            content = approval_file.read_text()
            
            print(f"[TWITTER_MCP] Processing Twitter/X approval: {approval_file.name}")
            
            # Extract tweet content from the approval file (simplified parsing)
            lines = content.split('\n')
            tweet_text = ""
            collecting_tweet = False
            
            for line in lines:
                if 'Post Draft' in line:
                    collecting_tweet = True
                elif collecting_tweet and line.startswith('"Thanks for the great question!'):
                    tweet_text = line
                    break
                elif collecting_tweet and line.startswith('##'):
                    collecting_tweet = False
                elif collecting_tweet and not line.startswith('##'):
                    tweet_text += line + " "
            
            if tweet_text.strip():
                # Clean up the tweet text
                tweet_text = tweet_text.strip().strip('"')
                
                # Post the tweet to Twitter/X
                tweet_id = self.post_tweet(tweet_text)
                
                if tweet_id:
                    result = {
                        'status': 'success',
                        'operation': 'tweet_posted',
                        'tweet_id': tweet_id,
                        'file_processed': approval_file.name
                    }
                    
                    # Log the result
                    self.log_operation(result, vault_path)
                    
                    # Move processed file to Done
                    done_dir = Path(vault_path) / 'Done'
                    done_dir.mkdir(exist_ok=True)
                    approval_file.rename(done_dir / approval_file.name)
                    
                    print(f"[TWITTER_MCP] Posted tweet: {tweet_id}")
                else:
                    print(f"[TWITTER_MCP] Failed to post tweet")
            else:
                print(f"[TWITTER_MCP] No tweet content found in approval file: {approval_file.name}")
    
    def log_operation(self, result, vault_path):
        """Log the operation to the appropriate log file"""
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(exist_ok=True)
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = logs_dir / f'{today}_twitter.json'
        
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
        print(f"[TWITTER_MCP] Twitter/X MCP Server started.")
        print(f"[TWITTER_MCP] Monitoring for approved Twitter/X tasks...")
        
        try:
            while self.running:
                self.process_twitter_approvals(vault_path)
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("[TWITTER_MCP] Twitter/X MCP Server stopped by user")

if __name__ == "__main__":
    # Load Twitter/X configuration from environment
    import dotenv
    dotenv.load_dotenv()
    
    config = {
        'bearer_token': os.getenv('TWITTER_BEARER_TOKEN', 'your_bearer_token_here'),
    }
    
    if not config['bearer_token'] or config['bearer_token'] == 'your_bearer_token_here':
        print("[WARNING] Twitter/X bearer token not found in .env file. Please configure TWITTER_BEARER_TOKEN.")
        print("[INFO] This is a simulation - Twitter/X operations will be logged but not executed.")
    else:
        VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Gold"
        mcp_server = TwitterMCP(config)
        mcp_server.run(VAULT_PATH)