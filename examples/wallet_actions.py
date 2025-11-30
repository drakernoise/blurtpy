import getpass
import time
from blurtpy import Blurt
from blurtpy.account import Account
from blurtpy.amount import Amount

from blurtpy.nodelist import NodeList

# Configuration
USERNAME = "your_username"
nl = NodeList()
NODE = [n["url"] for n in nl]

# Initialize Blurt
b = Blurt(node=NODE)

# Unlock Wallet
if b.wallet.created():
    if b.wallet.locked():
        pwd = getpass.getpass(f"Enter wallet password to operate as {USERNAME}: ")
        try:
            b.wallet.unlock(pwd)
            print("Wallet unlocked.")
        except Exception as e:
            print(f"Error unlocking: {e}")
            exit()
else:
    print("No wallet found. Run 'examples/wallet_manager.py' first.")
    exit()

def power_up(amount, to_user=None):
    """Converts liquid BLURT to Blurt Power (Vesting)."""
    print(f"Powering Up {amount} BLURT...")
    try:
        acc = Account(USERNAME, blockchain_instance=b)
        # If to_user is None, power up to self
        acc.transfer_to_vesting(amount, to=to_user)
        print("Power Up successful.")
    except Exception as e:
        print(f"Error in Power Up: {e}")

def delegate_bp(amount_vests, to_user):
    """Delegates Blurt Power to another user."""
    print(f"Delegating {amount_vests} VESTS to {to_user}...")
    try:
        acc = Account(USERNAME, blockchain_instance=b)
        acc.delegate_vesting_shares(to_user, amount_vests)
        print("Delegation successful.")
    except Exception as e:
        print(f"Error in Delegation: {e}")

def multiple_transfer(recipients, amount, asset="BLURT", memo=""):
    """Sends the same amount to multiple users."""
    print(f"Starting multiple transfer to {len(recipients)} users...")
    acc = Account(USERNAME, blockchain_instance=b)
    
    for recipient in recipients:
        try:
            print(f"Sending {amount} {asset} to {recipient}...")
            acc.transfer(recipient, amount, asset, memo)
            print("Sent.")
        except Exception as e:
            print(f"Error sending to {recipient}: {e}")

def recurring_transfer(recipient, amount, asset="BLURT", memo="", repetitions=3, interval_seconds=60):
    """Simulates a recurring transfer (run script in background)."""
    print(f"Starting recurring transfer to {recipient}: {repetitions} times every {interval_seconds}s.")
    acc = Account(USERNAME, blockchain_instance=b)
    
    for i in range(repetitions):
        try:
            print(f"Execution {i+1}/{repetitions}...")
            acc.transfer(recipient, amount, asset, memo)
            print("Transfer successful.")
        except Exception as e:
            print(f"Error in recurring transfer: {e}")
        
        if i < repetitions - 1:
            print(f"Waiting {interval_seconds} seconds...")
            time.sleep(interval_seconds)

def transfer_to_savings(amount, asset="BLURT", memo="Savings"):
    """Transfers funds to the Savings account."""
    print(f"Transferring {amount} {asset} to Savings...")
    try:
        acc = Account(USERNAME, blockchain_instance=b)
        acc.transfer_to_savings(amount, asset, memo)
        print("Transfer to Savings successful.")
    except Exception as e:
        print(f"Error in transfer to Savings: {e}")

if __name__ == "__main__":
    # USAGE EXAMPLES (Uncomment to test)
    
    print("Uncomment lines below to test functions.")
    
    # 1. Power Up (1 BLURT)
    # power_up(1)
    
    # 2. Delegate BP (1000 VESTS)
    # delegate_bp("1000 VESTS", "tekraze")
    
    # 3. Multiple Transfer
    # recipients = ["user1", "user2", "user3"]
    # multiple_transfer(recipients, 0.1, "BLURT", "Gift")
    
    # 4. Recurring Transfer (3 times, every 10 seconds)
    # recurring_transfer("draktest", 0.1, "BLURT", "Recurring payment", repetitions=3, interval_seconds=10)
    
    # 5. Savings
    # transfer_to_savings(1, "BLURT", "Saving for the future")
