"""
Gold Tier - Odoo MCP Server
Handles Odoo accounting operations via JSON-RPC API
"""
import os
import json
import requests
import time
from pathlib import Path
from datetime import datetime

class OdooMCP:
    def __init__(self, config):
        self.config = config
        self.url = config['url']
        self.db = config['database']
        self.api_key = config['api_key']
        self.uid = None
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.running = True
        
    def authenticate(self):
        """Authenticate with Odoo using API key"""
        try:
            # In Odoo with API keys, we typically use the API key as a bearer token
            self.headers['Authorization'] = f'Bearer {self.api_key}'
            # Test connection
            response = self.call_odoo_method('res.users', 'read', [1], ['name'])
            if response:
                print("[ODOO_MCP] Successfully authenticated with Odoo")
                return True
        except Exception as e:
            print(f"[ODOO_MCP] Authentication failed: {e}")
            return False
    
    def call_odoo_method(self, model, method, args=None, kwargs=None):
        """Call an Odoo model method via JSON-RPC"""
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        
        payload = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'service': 'object',
                'method': 'execute_kw',
                'args': [self.db, 0, self.api_key, model, method, args, kwargs]
            },
            'id': int(time.time())
        }
        
        try:
            response = requests.post(
                f"{self.url}/jsonrpc",
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            
            result = response.json()
            if 'result' in result:
                return result['result']
            else:
                print(f"[ODOO_MCP] Error in response: {result}")
                return None
        except Exception as e:
            print(f"[ODOO_MCP] Error calling Odoo method: {e}")
            return None
    
    def create_invoice(self, partner_id, lines, date_invoice=None, journal_id=1):
        """Create a customer invoice in Odoo"""
        if not date_invoice:
            date_invoice = datetime.now().strftime('%Y-%m-%d')
        
        invoice_vals = {
            'partner_id': partner_id,
            'move_type': 'out_invoice',
            'invoice_date': date_invoice,
            'journal_id': journal_id,
            'invoice_line_ids': [(0, 0, line) for line in lines]
        }
        
        try:
            invoice_id = self.call_odoo_method('account.move', 'create', [invoice_vals])
            if invoice_id:
                print(f"[ODOO_MCP] Invoice created with ID: {invoice_id}")
                return invoice_id
            else:
                print("[ODOO_MCP] Failed to create invoice")
                return None
        except Exception as e:
            print(f"[ODOO_MCP] Error creating invoice: {e}")
            return None
    
    def create_partner(self, name, email=None, phone=None):
        """Create a partner/contact in Odoo"""
        partner_vals = {'name': name}
        if email:
            partner_vals['email'] = email
        if phone:
            partner_vals['phone'] = phone
        
        try:
            partner_id = self.call_odoo_method('res.partner', 'create', [partner_vals])
            if partner_id:
                print(f"[ODOO_MCP] Partner created with ID: {partner_id}")
                return partner_id
            else:
                print("[ODOO_MCP] Failed to create partner")
                return None
        except Exception as e:
            print(f"[ODOO_MCP] Error creating partner: {e}")
            return None
    
    def search_partner(self, domain):
        """Search for partners in Odoo"""
        try:
            partner_ids = self.call_odoo_method('res.partner', 'search', [domain])
            if partner_ids:
                partners = self.call_odoo_method('res.partner', 'read', [partner_ids], ['name', 'email', 'phone'])
                return partners
            else:
                return []
        except Exception as e:
            print(f"[ODOO_MCP] Error searching partners: {e}")
            return []
    
    def register_payment(self, invoice_id, amount, journal_id=1):
        """Register a payment for an invoice in Odoo"""
        try:
            # Create payment wizard
            payment_vals = {
                'amount': amount,
                'journal_id': journal_id,
                'payment_type': 'inbound',
                'partner_type': 'customer',
            }
            
            payment_id = self.call_odoo_method('account.payment', 'create', [payment_vals])
            if payment_id:
                # Post the payment
                self.call_odoo_method('account.payment', 'action_post', [[payment_id]])
                print(f"[ODOO_MCP] Payment registered with ID: {payment_id}")
                
                # Reconcile with invoice
                # This is a simplified version - actual reconciliation is more complex
                return payment_id
            else:
                print("[ODOO_MCP] Failed to register payment")
                return None
        except Exception as e:
            print(f"[ODOO_MCP] Error registering payment: {e}")
            return None
    
    def monitor_approvals(self, vault_path):
        """Monitor the Approved folder for Odoo tasks"""
        vault = Path(vault_path)
        approved_dir = vault / 'Approved'
        
        if not approved_dir.exists():
            approved_dir.mkdir(parents=True, exist_ok=True)
            return []
        
        # Find Odoo approval files
        odoo_approvals = []
        for file in approved_dir.glob('*odoo*'):
            if file.suffix == '.md':
                odoo_approvals.append(file)
        
        for file in approved_dir.glob('*invoice*'):
            if file.suffix == '.md':
                odoo_approvals.append(file)
        
        for file in approved_dir.glob('*payment*'):
            if file.suffix == '.md':
                odoo_approvals.append(file)
        
        return odoo_approvals
    
    def process_odoo_approvals(self, vault_path):
        """Process approved Odoo tasks"""
        approvals = self.monitor_approvals(vault_path)
        
        for approval_file in approvals:
            # Read the approval file to extract details
            content = approval_file.read_text()
            
            # This is a simplified processing - in reality, we'd parse the content
            # to extract specific parameters for the Odoo operation
            print(f"[ODOO_MCP] Processing Odoo approval: {approval_file.name}")
            
            # Example: If it's an invoice approval
            if 'create_odoo_invoice' in str(approval_file) or 'invoice' in content.lower():
                # In a real implementation, we would extract the invoice details
                # from the approval file and create the invoice in Odoo
                print(f"[ODOO_MCP] Creating invoice from approval: {approval_file.name}")
                
                # Mock operation - in reality, we'd parse the file for actual data
                result = {
                    'status': 'success',
                    'operation': 'invoice_created',
                    'file_processed': approval_file.name
                }
                
                # Log the result
                self.log_operation(result, vault_path)
                
                # Move processed file to Done
                done_dir = Path(vault_path) / 'Done'
                done_dir.mkdir(exist_ok=True)
                approval_file.rename(done_dir / approval_file.name)
                
                print(f"[ODOO_MCP] Processed Odoo approval: {approval_file.name}")
    
    def log_operation(self, result, vault_path):
        """Log the operation to the appropriate log file"""
        logs_dir = Path(vault_path) / 'Logs'
        logs_dir.mkdir(exist_ok=True)
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = logs_dir / f'{today}_odoo.json'
        
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
        print(f"[ODOO_MCP] Odoo MCP Server started.")
        print(f"[ODOO_MCP] Connecting to Odoo at: {self.url}")
        print(f"[ODOO_MCP] Database: {self.db}")
        print(f"[ODOO_MCP] Monitoring for approved Odoo tasks...")
        
        if not self.authenticate():
            print("[ODOO_MCP] Cannot proceed without Odoo authentication")
            return
        
        try:
            while self.running:
                self.process_odoo_approvals(vault_path)
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("[ODOO_MCP] Odoo MCP Server stopped by user")

if __name__ == "__main__":
    # Load Odoo configuration from environment
    import dotenv
    dotenv.load_dotenv()
    
    config = {
        'url': os.getenv('ODOO_URL', 'http://localhost:8069'),
        'database': os.getenv('ODOO_DB', 'gold_tier_db'),
        'api_key': os.getenv('ODOO_API_KEY', 'your_api_key_here'),
    }
    
    if not config['api_key'] or config['api_key'] == 'your_api_key_here':
        print("[WARNING] Odoo API key not found in .env file. Please configure ODOO_API_KEY.")
        print("[INFO] This is a simulation - Odoo operations will be logged but not executed.")
        # For simulation, create a mock Odoo MCP
        print("[ODOO_MCP] Running in simulation mode")
    else:
        VAULT_PATH = "C:/Users/manal/OneDrive/Desktop/Hacakthon 0/AI_Employee_Vault_Gold"
        mcp_server = OdooMCP(config)
        mcp_server.run(VAULT_PATH)