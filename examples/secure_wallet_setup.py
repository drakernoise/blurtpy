import getpass
from blurtpy import Blurt
from blurtpy.wallet import Wallet
from blurtpy.exceptions import WalletExists
from blurtpy.account import Account

def setup_wallet():
    """
    Interactive script to setup a secure wallet and add keys.
    """
    print("=== Blurtpy Secure Wallet Setup ===")
    print("This script will create a local encrypted database file to store your keys.")
    
    b = Blurt()
    
    # 1. Create Wallet if it doesn't exist
    if b.wallet.created():
        print("\nA wallet already exists!")
        print("If you want to delete it and start over, delete the 'blurtpy.sqlite' file or use b.wallet.wipe(True)")
    else:
        print("\nLet's create a new wallet.")
        password = getpass.getpass("Choose a master password for the wallet: ")
        confirm = getpass.getpass("Confirm password: ")
        
        if password != confirm:
            print("Error: Passwords do not match.")
            return
            
        try:
            b.wallet.create(password)
            print("Wallet created successfully.")
        except WalletExists:
            print("The wallet already existed.")

    # 2. Unlock Wallet
    if b.wallet.locked():
        password = getpass.getpass("\nEnter wallet password to unlock: ")
        try:
            b.wallet.unlock(password)
            print("Wallet unlocked.")
        except Exception as e:
            print(f"Error unlocking: {e}")
            return

    # 3. Add Keys
    while True:
        print("\n--- Key Management ---")
        print("You can add as many keys as you want (Owner, Active, Posting, Memo).")
        print("1. Add a new private key (WIF)")
        print("2. List saved public keys")
        print("3. Exit")
        
        option = input("Choose an option: ")
        
        if option == "1":
            print("\nEnter one of your private WIF keys.")
            print("Valid types: Posting, Active, Owner, Memo.")
            print("(Note: The Master Password is NOT a WIF key, use the keys derived from it).")
            wif = getpass.getpass("WIF Key (starts with 5...): ")
            try:
                b.wallet.addPrivateKey(wif)
                print("Key added successfully!")
                
                # Try to identify which account it belongs to
                pub = b.wallet.publickey_from_wif(wif)
                account = b.wallet.getAccountFromPublicKey(pub)
                if account:
                    print(f"This key belongs to account: {account}")
                else:
                    print("Key saved. (Note: Could not automatically identify the account,")
                    print("this is normal for Memo keys or if there are connection issues).")
                    
            except Exception as e:
                if "Key already in the store" in str(e):
                    print(f"\n[INFO] This key is ALREADY in your wallet.")
                    try:
                        pub = b.wallet.publickey_from_wif(wif)
                        print(f"Public Key: {pub}")
                        account = b.wallet.getAccountFromPublicKey(pub)
                        if account:
                            print(f"It belongs to account: {account}")
                            # Check authority
                            acc = Account(account, blockchain_instance=b)
                            print(f"Checking permissions for {account}...")
                            found_roles = []
                            for role in ['owner', 'active', 'posting', 'memo']:
                                if role == 'memo':
                                    if acc['memo_key'] == str(pub):
                                        found_roles.append(role)
                                else:
                                    for auth in acc[role]['key_auths']:
                                        if auth[0] == str(pub):
                                            found_roles.append(role)
                            
                            if found_roles:
                                print(f"This key has permissions: {', '.join(found_roles).upper()}")
                            else:
                                print("This key does NOT match any current permissions on the blockchain for this account.")
                                print("It might be an old key.")
                    except Exception as inner_e:
                        print(f"Could not analyze key details: {inner_e}")
                else:
                    print(f"Error adding key: {e}")
                
        elif option == "2":
            keys = b.wallet.getPublicKeys()
            print(f"\nThere are {len(keys)} saved keys:")
            for k in keys:
                print(f"- {k}")
                
        elif option == "3":
            break

if __name__ == "__main__":
    setup_wallet()
