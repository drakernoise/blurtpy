import getpass
from blurtpy import Blurt
from blurtpy.account import Account
from blurtgraphenebase.account import PasswordKey

# Configuration
USERNAME = "your_username"  # <--- Change this to your actual Blurt username
NODE = ["https://rpc.blurt.world"]

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
    print("No wallet found. Run 'examples/secure_wallet_setup.py' first.")
    exit()

def set_recovery_account(new_recovery_account):
    """Sets the recovery account for the user."""
    print(f"Setting recovery account to: {new_recovery_account}...")
    try:
        acc = Account(USERNAME, blockchain_instance=b)
        # This operation requires the Owner Key
        acc.change_recovery_account(new_recovery_account)
        print("Recovery account change request sent (will take 30 days).")
    except Exception as e:
        print(f"Error changing recovery account: {e}")

def change_keys(new_password):
    """
    Changes the account keys (Owner, Active, Posting, Memo) derived from a new password.
    WARNING: This is a critical operation. If you lose the new password, you lose the account.
    """
    print("!!! WARNING: YOU ARE ABOUT TO CHANGE YOUR ACCOUNT KEYS !!!")
    print(f"Changing keys for user: {USERNAME}")
    
    confirm = input("Are you sure? (type 'YES' to confirm): ")
    if confirm != "YES":
        print("Operation cancelled.")
        return

    try:
        acc = Account(USERNAME, blockchain_instance=b)
        
        # Generate new keys from the new password
        print("Generating new keys...")
        new_keys = {}
        for role in ["owner", "active", "posting", "memo"]:
            # Derive key from password (username + role + password)
            pk = PasswordKey(USERNAME, new_password, role=role)
            new_keys[role] = str(pk.get_public())
            # Note: In a real app, you should save the new private keys securely here!
            # For this example, we just print them (BE CAREFUL!)
            print(f"New {role} key generated.")

        # Update keys on the blockchain
        # This requires the CURRENT Owner Key (which should be in the wallet)
        print("Sending update transaction to blockchain...")
        
        # --- DEBUG START ---
        print(f"\n[DEBUG] Checking wallet keys for {USERNAME}...")
        print(f"[DEBUG] Chain ID: {b.chain_params['chain_id']}")
        print(f"[DEBUG] Prefix: {b.chain_params['prefix']}")
        try:
            owner_auth = acc["owner"]["key_auths"]
            print(f"[DEBUG] Account Owner Auths: {owner_auth}")
            found = False
            for auth in owner_auth:
                pub = auth[0]
                try:
                    b.wallet.getPrivateKeyForPublicKey(pub)
                    print(f"[DEBUG] FOUND Private Key for {pub} in wallet!")
                    found = True
                except Exception:
                    print(f"[DEBUG] MISSING Private Key for {pub} in wallet.")
            
            if not found:
                print("[DEBUG] CRITICAL - No Owner Key found in wallet!")
            else:
                print("[DEBUG] Owner Key is present. Proceeding...")
        except Exception as e:
            print(f"[DEBUG] Error checking keys: {e}")
        # --- DEBUG END ---

        acc.update_account_keys(new_password)
        print("Keys changed successfully!")
        print("Please update your wallet with the new keys immediately.")
        
        # Show new keys (Security Warning: Do not do this in production logs)
        print("\n--- NEW KEYS (SAVE THEM NOW) ---")
        print(f"Master Password: {new_password}")
        for role in ["owner", "active", "posting", "memo"]:
            pk = PasswordKey(USERNAME, new_password, role=role)
            pub_key = format(pk.get_public(), "STM")
            priv_key = format(pk.get_private(), "WIF")
            print(f"{role.upper()}:")
            print(f"  Public: {pub_key}")
            print(f"  Private: {priv_key}")
            
    except Exception as e:
        print(f"Critical error changing keys: {e}")

if __name__ == "__main__":
    # USAGE EXAMPLES (Uncomment to test)
    
    print("Uncomment lines below to test functions.")
    
    # 1. Set recovery account
    # set_recovery_account("tekraze")
    
    # 2. Change keys (EXTREME CAUTION!)
    # change_keys("MyNewSuperSecurePassword123!")
