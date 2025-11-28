import os
import shutil
import datetime
from appdirs import user_data_dir
import getpass
from blurtpy import Blurt
from blurtpy.wallet import Wallet
from blurtpy.exceptions import WalletExists
from blurtpy.account import Account

def backup_wallet():
    """Creates a timestamped backup of the wallet file."""
    try:
        appauthor = "blurtpy"
        appname = "blurtpy"
        data_dir = user_data_dir(appname, appauthor)
        db_file = os.path.join(data_dir, "blurtpy.sqlite")
        
        if os.path.exists(db_file):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = os.path.join(data_dir, f"blurtpy_backup_{timestamp}.sqlite")
            shutil.copy2(db_file, backup_name)
            print(f"\n[AUTO-BACKUP] Wallet state saved to: {backup_name}")
            return True
    except Exception as e:
        print(f"\n[AUTO-BACKUP] Warning: Failed to create backup: {e}")
        return False


def setup_wallet():
    """
    Interactive script to setup a secure wallet and add keys.
    """
    print("=== Blurtpy Wallet Manager ===")
    print("This script allows you to create, manage, and inspect your secure local wallet.")
    
    b = Blurt()
    
    # 1. Create Wallet if it doesn't exist
    if not b.wallet.created():
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
            if b.wallet.created():
                 print("(Note: A wallet already exists. If you want to delete it and start over,")
                 print(" delete the 'blurtpy.sqlite' file or use b.wallet.wipe(True))")
        except Exception as e:
            print(f"Error unlocking wallet: {e}")
            exit()
        except Exception as e:
            print(f"Error unlocking: {e}")
            return

    # 3. Add Keys
    while True:
        print("\n--- Key Management ---")
        print("You can add as many keys as you want (Owner, Active, Posting, Memo).")
        print("1. Add a new private key (WIF)")
        print("2. List saved public keys")
        print("3. Import keys from file (account_management output)")
        print("4. Archive current wallet & Start fresh")
        print("5. Cleanup Orphan Keys")
        print("6. Exit")
        
        option = input("Choose an option: ")
        
        if option == "1":
            print("\nEnter one of your private WIF keys.")
            print("Valid types: Posting, Active, Owner, Memo.")
            print("(Note: The Master Password is NOT a WIF key, use the keys derived from it).")
            wif = getpass.getpass("WIF Key (starts with 5...): ")
            try:
                # Check if key already exists
                try:
                    b.wallet.getPrivateKeyForPublicKey(b.wallet.publickey_from_wif(wif))
                    print("Key already in wallet.")
                    replace = input("Do you want to replace it? (y/N): ")
                    if replace.lower() != 'y':
                        print("Skipped.")
                        continue
                except Exception:
                    pass # Key not in wallet

                # Auto-Backup before modification
                if not backup_wallet():
                    print("Backup failed. Aborting operation.")
                    continue

                # If we are replacing, we must remove the old key first
                # (We know it exists if we are here and didn't continue)
                # But wait, the try/except block above handles the "exists" check.
                # If we are here, either it didn't exist, OR it existed and user said 'y'.
                # If it existed, we need to remove it.
                # Re-check existence to be safe or use a flag?
                # Let's just try to remove it if we can, or rely on addPrivateKey raising.
                # But addPrivateKey raises.
                
                pub = b.wallet.publickey_from_wif(wif)
                try:
                    b.wallet.getPrivateKeyForPublicKey(pub)
                    # It exists, so we must be in "replace=y" mode
                    b.wallet.removePrivateKeyFromPublicKey(pub)
                except:
                    pass # Didn't exist

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
                print(f"Error adding key: {e}")
                
        elif option == "2":
            keys = b.wallet.getPublicKeys()
            print(f"\nThere are {len(keys)} saved keys. Analyzing...")
            
            analyzed_keys = []
            for k in keys:
                key_info = {"pub": k, "roles": []}
                try:
                    accounts = list(b.wallet.getAccountsFromPublicKey(k))
                    if accounts:
                        for acc_name in accounts:
                            try:
                                acc = Account(acc_name, blockchain_instance=b)
                                # Check roles
                                found_role = False
                                # Owner
                                for auth in acc["owner"]["key_auths"]:
                                    if auth[0] == k:
                                        key_info["roles"].append(f"[OWNER] {acc_name}")
                                        found_role = True
                                # Active
                                for auth in acc["active"]["key_auths"]:
                                    if auth[0] == k:
                                        key_info["roles"].append(f"[ACTIVE] {acc_name}")
                                        found_role = True
                                # Posting
                                for auth in acc["posting"]["key_auths"]:
                                    if auth[0] == k:
                                        key_info["roles"].append(f"[POSTING] {acc_name}")
                                        found_role = True
                                # Memo
                                if acc["memo_key"] == k:
                                    key_info["roles"].append(f"[MEMO] {acc_name}")
                                    found_role = True
                                
                                if not found_role:
                                     key_info["roles"].append(f"[UNKNOWN-ROLE] {acc_name}")
                            except Exception:
                                key_info["roles"].append(f"[ERROR-CHECKING] {acc_name}")
                    else:
                        key_info["roles"].append("[ORPHAN] (No account found)")
                except Exception as e:
                    key_info["roles"].append(f"[ERROR] {e}")
                
                analyzed_keys.append(key_info)

            # Display Results
            for item in analyzed_keys:
                roles_str = ", ".join(item["roles"])
                print(f"- {item['pub']}  ->  {roles_str}")

            show_priv = input("\nDo you want to reveal the PRIVATE keys? (yes/NO): ")
            if show_priv.lower() == "yes":
                print("\n[WARNING] Displaying Private Keys. Ensure no one is watching!")
                for item in analyzed_keys:
                    try:
                        priv = b.wallet.getPrivateKeyForPublicKey(item["pub"])
                        print(f"- Pub: {item['pub']}")
                        print(f"  Roles: {', '.join(item['roles'])}")
                        print(f"  Priv: {priv}")
                    except Exception as e:
                        print(f"- Pub: {item['pub']} (Error retrieving private key: {e})")

        elif option == "3":
            print("\n--- Import Keys from File ---")
            print("This option reads a text file containing keys in the format generated by account_management.py")
            filepath = input("Enter the path to the key file: ")
            
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                
                import re
                # Regex to find Private keys associated with roles
                # Format expected:
                # ROLE:
                #   Public: ...
                #   Private: 5...
                matches = re.findall(r"(OWNER|ACTIVE|POSTING|MEMO):\s+Public:\s+STM.*\s+Private:\s+(5[HJK][1-9A-Za-z]{48,})", content, re.MULTILINE)
                
                # Try to find account name
                account_match = re.search(r"NEW KEYS for account (.*?):", content)
                account_name = account_match.group(1) if account_match else "Unknown"
                
                if not matches:
                    print("No keys found in the expected format.")
                else:
                    print(f"Found {len(matches)} keys for account '{account_name}'.")
                    
                    if not backup_wallet():
                        print("Backup failed. Aborting import.")
                        continue

                    for role, wif in matches:
                        print(f"Importing {role} key...")
                        try:
                            # Check if key exists
                            try:
                                pub = b.wallet.publickey_from_wif(wif)
                                b.wallet.getPrivateKeyForPublicKey(pub)
                                print(f"  [WARN] Key for {role} is already in the wallet.")
                                replace = input(f"  Do you want to replace the existing {role} key? (y/N): ")
                                if replace.lower() == 'y':
                                    # To replace, we must remove the old one first?
                                    # Actually, addPrivateKey will raise if it exists.
                                    # But since it's the SAME key (same WIF -> same Pub), 
                                    # removing and adding is effectively a no-op but satisfies the "replace" action.
                                    # If the user meant "replace the OLD DIFFERENT key", this logic doesn't catch it 
                                    # because we are checking if THIS WIF is in the wallet.
                                    # But assuming we want to force-add:
                                    try:
                                        b.wallet.removePrivateKeyFromPublicKey(pub)
                                    except:
                                        pass # Ignore if removal fails (shouldn't happen if get succeeded)
                                    
                                    b.wallet.addPrivateKey(wif)
                                    print(f"  Success: {role} key replaced.")
                                else:
                                    print(f"  Skipped.")
                                continue
                            except Exception:
                                pass # Key not in wallet, proceed to add

                            b.wallet.addPrivateKey(wif)
                            print(f"  Success: {role} key added.")
                        except Exception as e:
                            print(f"  Error adding {role} key: {e}")
                                
            except FileNotFoundError:
                print("Error: File not found.")
            except Exception as e:
                print(f"Error reading file: {e}")

        elif option == "4":
            print("\n--- Archive Wallet & Start Fresh ---")
            print("This will rename your current 'blurtpy.sqlite' to a backup file")
            print("and allow you to create a brand new, empty wallet.")
            confirm = input("Are you sure? (type 'YES' to confirm): ")
            
            if confirm == "YES":
                import os
                import datetime
                import shutil
                from appdirs import user_data_dir
                
                # Logic from blurtstorage/sqlite.py
                appauthor = "blurtpy"
                appname = "blurtpy"
                data_dir = user_data_dir(appname, appauthor)
                db_file = os.path.join(data_dir, "blurtpy.sqlite")
                
                print(f"Looking for wallet at: {db_file}")
                
                if os.path.exists(db_file):
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = os.path.join(data_dir, f"blurtpy_backup_{timestamp}.sqlite")
                    try:
                        os.rename(db_file, backup_name)
                        print(f"\nSuccess! Wallet archived as '{backup_name}'.")
                        print("Please restart this script to create a new wallet.")
                        return # Exit script to force restart logic
                    except Exception as e:
                        print(f"Error archiving wallet: {e}")
                else:
                    print(f"Error: No 'blurtpy.sqlite' file found at {db_file}.")
            else:
                print("Operation cancelled.")

        elif option == "5":
            print("\n--- Cleanup Orphan Keys ---")
            print("Analyzing keys to find orphans (keys not associated with any account)...")
            keys = b.wallet.getPublicKeys()
            orphans = []
            
            for k in keys:
                try:
                    accounts = list(b.wallet.getAccountsFromPublicKey(k))
                    if not accounts:
                        orphans.append(k)
                except Exception as e:
                    print(f"Error checking key {k}: {e}")
            
            if not orphans:
                print("No orphan keys found. Your wallet is clean!")
            else:
                print(f"\nFound {len(orphans)} orphan keys:")
                for k in orphans:
                    print(f"- {k}")
                
                confirm = input("\nDo you want to DELETE these keys? (yes/NO): ")
                if confirm.lower() == "yes":
                    if backup_wallet():
                        deleted_count = 0
                        for k in orphans:
                            try:
                                b.wallet.removePrivateKeyFromPublicKey(k)
                                deleted_count += 1
                            except Exception as e:
                                print(f"Error deleting {k}: {e}")
                        print(f"\nSuccessfully deleted {deleted_count} orphan keys.")
                    else:
                        print("Backup failed. Aborting deletion for safety.")
                else:
                    print("Operation cancelled.")

        elif option == "6":
            break

if __name__ == "__main__":
    setup_wallet()
