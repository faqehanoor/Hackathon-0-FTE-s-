"""
Platinum Tier - Vault Sync Script
Synchronizes vault between cloud and local agents using Git
"""
import os
import time
import subprocess
from pathlib import Path
from datetime import datetime

class VaultSync:
    def __init__(self, vault_path, remote_repo_url):
        self.vault = Path(vault_path)
        self.remote_repo = remote_repo_url
        self.sync_interval = 60  # Sync every minute
        self.sync_active = True
        
    def setup_git_repo(self):
        """Initialize git repo in vault if not exists"""
        os.chdir(self.vault)
        
        # Check if git repo exists
        if not (self.vault / '.git').exists():
            print("[SYNC] Initializing new Git repository in vault...")
            subprocess.run(['git', 'init'], check=True)
            subprocess.run(['git', 'remote', 'add', 'origin', self.remote_repo], check=True)
            
            # Create initial commit
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', 'Initial commit - Platinum Tier vault'], check=True)
            subprocess.run(['git', 'branch', '-M', 'main'], check=True)
            subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
            print("[SYNC] Git repository initialized and pushed to remote")
        else:
            print("[SYNC] Git repository already exists")
    
    def configure_gitignore(self):
        """Configure .gitignore to exclude sensitive files"""
        gitignore_path = self.vault / '.gitignore'
        
        # Define sensitive files to exclude
        sensitive_patterns = [
            # Environment files with credentials
            '.env',
            '*.env',
            'env/',
            'venv/',
            'ENV/',
            
            # Session files
            '*.session',
            '*.session-journal',
            'sessions/',
            
            # Token files
            '*.token',
            'tokens/',
            'creds/',
            'credentials/',
            
            # Browser profiles (for WhatsApp, etc.)
            'profiles/',
            'browsers/',
            
            # Local configuration that shouldn't sync
            'local_config/',
            'config_local/',
            
            # Cache files
            '__pycache__/',
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '.pytest_cache/',
            
            # OS-specific files
            '.DS_Store',
            'Thumbs.db',
            '.Spotlight-V100',
            '.Trashes',
            
            # Logs (these should be local)
            'logs/',
            '*.log',
            
            # Temporary files
            'temp/',
            'tmp/',
            '*.tmp',
            '*.temp'
        ]
        
        gitignore_content = '\n'.join(sensitive_patterns) + '\n'
        
        # Write or append to gitignore
        with open(gitignore_path, 'a') as f:
            f.write(gitignore_content)
        
        print("[SYNC] .gitignore configured to exclude sensitive files")
    
    def sync_pull(self):
        """Pull latest changes from remote"""
        try:
            os.chdir(self.vault)
            result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                  capture_output=True, text=True, check=True)
            print(f"[SYNC] Pulled changes: {result.stdout[:100]}...")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[SYNC] Pull failed: {e.stderr}")
            return False
    
    def sync_push(self):
        """Push local changes to remote"""
        try:
            os.chdir(self.vault)
            
            # Check for changes
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True, check=True)
            
            if result.stdout.strip():  # If there are changes
                # Add all changes
                subprocess.run(['git', 'add', '.'], check=True)
                
                # Commit changes
                commit_msg = f"Auto-sync at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                
                # Push to remote
                subprocess.run(['git', 'push', 'origin', 'main'], check=True)
                
                print(f"[SYNC] Changes pushed: {commit_msg}")
                return True
            else:
                print("[SYNC] No changes to push")
                return False
        except subprocess.CalledProcessError as e:
            print(f"[SYNC] Push failed: {e.stderr}")
            return False
    
    def run_sync_cycle(self):
        """Perform one sync cycle (pull then push)"""
        print(f"[SYNC] Starting sync cycle at {datetime.now()}")
        
        # First pull latest changes
        pull_success = self.sync_pull()
        
        # Then push local changes
        push_success = self.sync_push()
        
        if pull_success or push_success:
            print("[SYNC] Sync cycle completed successfully")
            return True
        else:
            print("[SYNC] Sync cycle completed (no changes)")
            return True
    
    def run(self):
        """Main sync loop"""
        print("[SYNC] Starting Vault Sync Service")
        print(f"[SYNC] Vault: {self.vault}")
        print(f"[SYNC] Remote: {self.remote_repo}")
        print(f"[SYNC] Interval: {self.sync_interval}s")
        print("=" * 50)
        
        # Setup git repo and ignore sensitive files
        self.setup_git_repo()
        self.configure_gitignore()
        
        try:
            while self.sync_active:
                self.run_sync_cycle()
                time.sleep(self.sync_interval)
                
        except KeyboardInterrupt:
            print("\n[SYNC] Vault Sync stopped by user")
            self.sync_active = False
        except Exception as e:
            print(f"[SYNC] Error in Vault Sync: {e}")

if __name__ == "__main__":
    # This would be configured with the actual remote repository URL
    VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Platinum"
    REMOTE_REPO = "https://github.com/faqehanoor/platinum-vault-sync.git"  # Placeholder
    
    sync_service = VaultSync(VAULT_PATH, REMOTE_REPO)
    sync_service.run()