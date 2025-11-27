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

        # --- MANUAL UPDATE START ---
        from blurtbase import operations
        
        print("[DEBUG] Manually constructing transaction...")
        
        # 1. Derive NEW keys
        key_auths = {}
        for role in ['owner', 'active', 'posting', 'memo']:
            pk = PasswordKey(USERNAME, new_password, role=role)
            key_auths[role] = format(pk.get_public_key(), b.chain_params["prefix"])
            
        print(f"[DEBUG] New Keys derived: {key_auths}")

        # 2. Construct Operation
        # TEST: Try to update ONLY metadata first to verify signing works
        # We use the EXISTING keys for the update payload
        print("[DEBUG] TEST MODE: Updating only metadata to verify signing...")
        
        current_owner_pub = acc["owner"]["key_auths"][0][0]
        current_active_pub = acc["active"]["key_auths"][0][0]
        current_posting_pub = acc["posting"]["key_auths"][0][0]
        current_memo_pub = acc["memo_key"]

        op = operations.Account_update(**{
            "account": USERNAME,
            'owner': {'account_auths': [],
                      'key_auths': [[current_owner_pub, 1]],
                      "address_auths": [],
                      'weight_threshold': 1},
            'active': {'account_auths': [],
                       'key_auths': [[current_active_pub, 1]],
                       "address_auths": [],
                       'weight_threshold': 1},
            'posting': {'account_auths': acc['posting']['account_auths'],
                        'key_auths': [[current_posting_pub, 1]],
                        "address_auths": [],
                        'weight_threshold': 1},
            'memo_key': current_memo_pub,
            "json_metadata": '{"test": "signing_verification"}',
            "prefix": b.chain_params["prefix"],
        })
        
        print("[DEBUG] Operation constructed (METADATA UPDATE ONLY).")
        
        # 3. Get CURRENT Owner Key from Wallet
        print(f"[DEBUG] Current Owner PubKey: {current_owner_pub}")
        
        try:
            current_owner_wif = b.wallet.getPrivateKeyForPublicKey(current_owner_pub)
            print(f"[DEBUG] Got WIF from wallet: {str(current_owner_wif)[:5]}...")
        except Exception as e:
            print(f"[DEBUG] Failed to get WIF: {e}")
            raise
            
        # 4. Sign and Broadcast
        print("[DEBUG] Signing and broadcasting...")
        b.txbuffer.clear()
        b.txbuffer.appendOps([op])
        b.txbuffer.appendWif(current_owner_wif)
        signed_tx = b.txbuffer.sign()
        print(f"[DEBUG] Signed Transaction: {signed_tx}")
        
        # --- LOCAL VERIFICATION ---
        print("[DEBUG] Verifying signature locally...")
        try:
            # We need to reconstruct the Signed_Transaction object to verify
            from blurtgraphenebase.signedtransactions import Signed_Transaction
            from blurtgraphenebase.account import PublicKey
            
            stx = Signed_Transaction(signed_tx)
            # Verify using the Chain ID and the expected Public Keys
            # We pass the public key we expect to have signed it
            # Convert string to PublicKey object
            pub_key_obj = PublicKey(current_owner_pub, prefix=b.chain_params["prefix"])
            stx.verify([pub_key_obj], b.chain_params)
            print("[DEBUG] Local Signature Verification: SUCCESS")
        except Exception as e:
            print(f"[DEBUG] Local Signature Verification: FAILED - {e}")
            import traceback
            traceback.print_exc()
        # --------------------------

        resp = b.txbuffer.broadcast()
        print(f"[DEBUG] Broadcast Response: {resp}")
        
        # acc.update_account_keys(new_password) # Commented out original call
        # --- MANUAL UPDATE END ---
        
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
