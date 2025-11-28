import getpass
from blurtpy import Blurt
from blurtpy.account import Account

def diagnose():
    print("=== Blurtpy Key Diagnostic Tool ===")
    username = input("Enter your username (e.g. draktest): ")
    
    b = Blurt()
    
    # 1. Check if wallet exists
    if not b.wallet.created():
        print("Error: No wallet found. Please run wallet_manager.py first.")
        return

    # 2. Unlock wallet
    if b.wallet.locked():
        pwd = getpass.getpass("Enter wallet password: ")
        try:
            b.wallet.unlock(pwd)
            print("Wallet unlocked.")
        except Exception as e:
            print(f"Error unlocking wallet: {e}")
            return

    # 3. Get Account Data from Blockchain
    print(f"\nFetching account data for '{username}' from blockchain...")
    try:
        acc = Account(username, blockchain_instance=b)
        print("Account found.")
    except Exception as e:
        print(f"Error fetching account: {e}")
        return

    # 4. Get Public Keys from Account
    owner_key = acc['owner']['key_auths'][0][0]
    active_key = acc['active']['key_auths'][0][0]
    posting_key = acc['posting']['key_auths'][0][0]
    memo_key = acc['memo_key']

    print(f"\n--- Blockchain Keys for {username} ---")
    print(f"Owner:   {owner_key}")
    print(f"Active:  {active_key}")
    print(f"Posting: {posting_key}")
    print(f"Memo:    {memo_key}")

    # 5. Check Wallet
    print(f"\n--- Wallet Check ---")
    wallet_keys = b.wallet.getPublicKeys()
    
    missing = []
    
    if owner_key in wallet_keys:
        print(f"[OK] Owner Key found in wallet.")
    else:
        print(f"[MISSING] Owner Key NOT found in wallet.")
        missing.append("Owner")

    if active_key in wallet_keys:
        print(f"[OK] Active Key found in wallet.")
    else:
        print(f"[MISSING] Active Key NOT found in wallet.")
        missing.append("Active")

    if posting_key in wallet_keys:
        print(f"[OK] Posting Key found in wallet.")
    else:
        print(f"[MISSING] Posting Key NOT found in wallet.")
        missing.append("Posting")
        
    if memo_key in wallet_keys:
        print(f"[OK] Memo Key found in wallet.")
    else:
        print(f"[MISSING] Memo Key NOT found in wallet.")
        missing.append("Memo")

    print("\n--- Diagnosis ---")
    if not missing:
        print("All keys are present! You should be able to perform any operation.")
    else:
        print(f"You are missing the following keys: {', '.join(missing)}")
        print("To fix this:")
        print("1. Run 'python examples/wallet_manager.py'")
        print("2. Choose Option 1 (Add key)")
        print("3. Enter the Private WIF for the missing keys.")
        if "Owner" in missing:
            print("NOTE: To change keys (account_management.py), you MUST have the Owner Key.")

if __name__ == "__main__":
    diagnose()
