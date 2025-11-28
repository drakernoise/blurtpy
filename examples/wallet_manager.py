import os
import shutil
import datetime
import time
from appdirs import user_data_dir
import getpass
from prettytable import PrettyTable
from blurtpy import Blurt
from blurtpy.wallet import Wallet
from blurtpy.exceptions import WalletExists
from blurtpy.account import Account
from blurtbase import operations

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_account_key(blurt_instance, account_name, new_key, role):
    """
    Updates the key for a specific role (owner, active, posting, memo) on the blockchain.
    Requires a sufficient authority key (Active or Owner) to be present in the wallet.
    """
    try:
        acc = Account(account_name, blockchain_instance=blurt_instance)
        
        # Prepare arguments for Account_update
        update_args = {
            "account": account_name,
            "json_metadata": acc["json_metadata"],
            "posting_json_metadata": acc.get("posting_json_metadata", ""),
            "extensions": acc.get("extensions", []),
            "prefix": blurt_instance.chain_params["prefix"]
        }
        
        # Default: Keep existing memo_key (mandatory field)
        update_args["memo_key"] = acc["memo_key"]
        
        # Update specific role
        if role == "memo":
            update_args["memo_key"] = new_key
        elif role in ["owner", "active", "posting"]:
            # Construct new authority object
            # We assume a simple 1-key authority for this manager
            new_auth = {
                "weight_threshold": 1,
                "account_auths": [],
                "key_auths": [[new_key, 1]]
            }
            update_args[role] = new_auth
        else:
            raise ValueError(f"Invalid role: {role}")

        # Construct Operation
        op = operations.Account_update(**update_args)
        
        # Sign and Broadcast
        blurt_instance.txbuffer.clear()
        blurt_instance.txbuffer.appendOps([op])
        
        # Determine required permission
        # Owner update requires Owner key. Others can use Active.
        signing_perm = "owner" if role == "owner" else "active"
        
        blurt_instance.txbuffer.appendSigner(account_name, signing_perm)
        blurt_instance.txbuffer.sign()
        resp = blurt_instance.txbuffer.broadcast()
        return resp
        
    except Exception as e:
        raise Exception(f"Failed to update {role} key: {e}")


def print_banner():
    clear_screen()
    print(r"""
  ____  _             _              
 | __ )| |_   _ _ __| |_ _ __  _   _ 
 |  _ \| | | | | '__| __| '_ \| | | |
 | |_) | | |_| | |  | |_| |_) | |_| |
 |____/|_|\__,_|_|   \__| .__/ \__, |
                        |_|    |___/ 
      Wallet Manager v1.0
    """)

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
    print_banner()
    
    b = Blurt()
    
    # 1. Create Wallet if it doesn't exist
    if not b.wallet.created():
        print("\n[!] No wallet found.")
        create = input("Do you want to create a new secure wallet? (y/n): ")
        if create.lower() != 'y':
            print("Exiting.")
            return

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
        clear_screen()
        print_banner()
        print("\n" + "="*30)
        print("   KEY MANAGEMENT MENU")
        print("="*30)
        print("1. Add a new private key (WIF)")
        print("2. List Public/Private Keys (Smart Analysis)")
        print("3. Import keys from file")
        print("4. Archive current wallet & Start fresh")
        print("5. Exit")
        print("-" * 30)
        
        option = input("Choose an option: ")
        
        if option == "1":
            print("\n--- Add New Key ---")
            print("Valid types: Posting, Active, Owner, Memo.")
            print("(Note: The Master Password is NOT a WIF key).")
            wif = getpass.getpass("Enter WIF Key (starts with 5...): ")
            try:
                # Check if key already exists
                try:
                    b.wallet.getPrivateKeyForPublicKey(b.wallet.publickey_from_wif(wif))
                    print("\n[!] Key already in wallet.")
                    replace = input("Do you want to replace it? (y/N): ")
                    if replace.lower() != 'y':
                        print("Skipped.")
                        input("\nPress Enter to continue...")
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
                    
                    # Check if this key matches the blockchain state for any role
                    # If not, it might be a new key the user wants to set
                    try:
                        acc_data = Account(account, blockchain_instance=b)
                        
                        # Determine which role this key MIGHT be intended for
                        # This is tricky because we don't know what the user intends.
                        # But if it's NOT in the blockchain, we can ask.
                        
                        is_on_chain = False
                        roles_on_chain = []
                        
                        # Check Owner
                        for auth in acc_data["owner"]["key_auths"]:
                            if auth[0] == pub:
                                is_on_chain = True
                                roles_on_chain.append("OWNER")
                        # Check Active
                        for auth in acc_data["active"]["key_auths"]:
                            if auth[0] == pub:
                                is_on_chain = True
                                roles_on_chain.append("ACTIVE")
                        # Check Posting
                        for auth in acc_data["posting"]["key_auths"]:
                            if auth[0] == pub:
                                is_on_chain = True
                                roles_on_chain.append("POSTING")
                        # Check Memo
                        if acc_data["memo_key"] == pub:
                            is_on_chain = True
                            roles_on_chain.append("MEMO")
                            
                        if is_on_chain:
                            print(f"Blockchain Status: Active as {', '.join(roles_on_chain)} key.")
                        else:
                            print("\n[NOTICE] This key is NOT currently active on the blockchain for account '{}'.".format(account))
                            update = input("Do you want to UPDATE your account to use this key? (y/N): ")
                            if update.lower() == 'y':
                                print("Select role to assign to this key:")
                                print("1. Owner (DANGEROUS)")
                                print("2. Active")
                                print("3. Posting")
                                print("4. Memo")
                                
                                try:
                                    role_sel = int(input("Enter number: "))
                                    role_map = {1: "owner", 2: "active", 3: "posting", 4: "memo"}
                                    target_role = role_map.get(role_sel)
                                    
                                    if target_role:
                                        if target_role == "owner":
                                            print("WARNING: Changing Owner key is critical. Ensure you have a backup!")
                                            confirm = input("Type 'CONFIRM' to proceed: ")
                                            if confirm != "CONFIRM":
                                                print("Aborted.")
                                                raise Exception("Cancelled by user")
                                        
                                        print(f"Updating {target_role} key on blockchain...")
                                        resp = update_account_key(b, account, pub, target_role)
                                        print(f"[SUCCESS] Updated {target_role} key! Block: {resp.get('ref_block_num')}")
                                    else:
                                        print("Invalid role selected.")
                                except Exception as e:
                                    print(f"Update failed: {e}")

                    except Exception as e:
                        print(f"Error checking blockchain state: {e}")

                else:
                    print("Key saved. (Note: Could not automatically identify the account,")
                    print("this is normal for Memo keys or if there are connection issues).")
                    
                    # If we can't identify the account, we can't update it easily without asking for the account name.
                    # For now, let's leave it simple.
                    
            except Exception as e:
                print(f"Error adding key: {e}")
            
            input("\nPress Enter to continue...")
                
        elif option == "2":
            while True: # Analysis Refresh Loop
                keys = b.wallet.getPublicKeys()
                print(f"\nThere are {len(keys)} saved keys. Analyzing on blockchain...")
                
                analyzed_keys = []
                orphans = []
                account_cache = {}
                
                for k in keys:
                    key_info = {"pub": k, "roles": []}
                    try:
                        accounts = list(b.wallet.getAccountsFromPublicKey(k))
                        if accounts:
                            for acc_name in accounts:
                                try:
                                    if acc_name in account_cache:
                                        acc = account_cache[acc_name]
                                    else:
                                        acc = Account(acc_name, blockchain_instance=b)
                                        account_cache[acc_name] = acc
                                    
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
                            orphans.append(k)
                    except Exception as e:
                        key_info["roles"].append(f"[ERROR] {e}")
                    
                    analyzed_keys.append(key_info)

                # Second Pass: Check orphans against found accounts for Memo keys
                if orphans and account_cache:
                     print(f"Performing second pass check for Memo keys on {len(orphans)} orphan(s)...")
                     for orphan_k in list(orphans):
                         for acc_name, acc in account_cache.items():
                             try:
                                 if acc["memo_key"] == orphan_k:
                                     # Update analyzed_keys
                                     for item in analyzed_keys:
                                         if item["pub"] == orphan_k:
                                             item["roles"] = [f"[MEMO] {acc_name}"]
                                     orphans.remove(orphan_k)
                                     break 
                             except:
                                 pass

                # Display Results using PrettyTable
                t = PrettyTable()
                t.field_names = ["Public Key", "Role / Status"]
                t.align = "l"
                
                for item in analyzed_keys:
                    roles_str = ", ".join(item["roles"])
                    t.add_row([item['pub'], roles_str])
                
                print(t)

                # Inline Handling for Orphans
                should_refresh = False
                if orphans:
                    while True:
                        print(f"\n[NOTICE] Found {len(orphans)} orphan key(s) that are not used by any account.")
                        print("What would you like to do?")
                        print("1. Promote an orphan key to be active on the blockchain")
                        print("2. Delete all orphan keys")
                        print("3. Keep them (Do nothing)")
                        print("4. Reveal Private Keys (Inspect before deciding)")
                        
                        choice = input("Choose an option (1-4): ")
                        
                        if choice == "1":
                            # Promote Logic
                            print("\n--- Promote Orphan Key ---")
                            
                            # Select Orphan
                            if len(orphans) == 1:
                                target_key = orphans[0]
                                print(f"Selected Key: {target_key}")
                            else:
                                print("Select key to promote:")
                                for idx, k in enumerate(orphans):
                                    print(f"{idx+1}. {k}")
                                try:
                                    sel = int(input("Enter number: "))
                                    target_key = orphans[sel-1]
                                except:
                                    print("Invalid selection.")
                                    target_key = None
                            
                            if target_key:
                                # Select Account
                                target_account = ""
                                if account_cache:
                                    known_accounts = list(account_cache.keys())
                                    if len(known_accounts) == 1:
                                        target_account = known_accounts[0]
                                        print(f"Target Account: {target_account}")
                                    else:
                                        print("Select Account to update:")
                                        for idx, acc in enumerate(known_accounts):
                                            print(f"{idx+1}. {acc}")
                                        try:
                                            sel = int(input("Enter number: "))
                                            target_account = known_accounts[sel-1]
                                        except:
                                            print("Invalid selection.")
                                
                                if not target_account:
                                    target_account = input("Enter the account name to update: ")
                                
                                if target_account:
                                    print(f"Select role to assign to key {target_key[:10]}...:")
                                    print("1. Owner (DANGEROUS)")
                                    print("2. Active")
                                    print("3. Posting")
                                    print("4. Memo")
                                    
                                    try:
                                        role_sel = int(input("Enter number: "))
                                        role_map = {1: "owner", 2: "active", 3: "posting", 4: "memo"}
                                        target_role = role_map.get(role_sel)
                                        
                                        if target_role:
                                            if target_role == "owner":
                                                print("WARNING: Changing Owner key is critical. Ensure you have a backup!")
                                                confirm = input("Type 'CONFIRM' to proceed: ")
                                                if confirm != "CONFIRM":
                                                    print("Aborted.")
                                                    continue
                                            
                                            if not backup_wallet():
                                                print("Backup failed. Aborting.")
                                        print(f"Update failed: {e}")
                            continue 

                        elif choice == "2":
                            # Delete Logic
                            confirm = input("Are you sure you want to DELETE all orphan keys? (y/N): ")
                            if confirm.lower() == 'y':
                                if backup_wallet():
                                    deleted_count = 0
                                    for k in orphans:
                                        try:
                                            b.wallet.removePrivateKeyFromPublicKey(k)
                                            deleted_count += 1
                                        except Exception as e:
                                            print(f"Error deleting {k}: {e}")
                                    print(f"Successfully deleted {deleted_count} orphan keys.")
                                    should_refresh = True
                                    break
                                else:
                                    print("Backup failed. Aborting deletion.")
                            else:
                                print("Deletion cancelled.")
                            continue

                        elif choice == "3":
                            print("Keeping orphan keys.")
                            break
                        
                        elif choice == "4":
                            print("\n" + "!"*60)
                            print(" [WARNING] DISPLAYING PRIVATE KEYS - ENSURE NO ONE IS WATCHING ")
                            print("!"*60 + "\n")
                            
                            pt = PrettyTable()
                            pt.field_names = ["Public Key", "Role", "Private Key"]
                            pt.align = "l"
                            
                            for item in analyzed_keys:
                                try:
                                    priv = b.wallet.getPrivateKeyForPublicKey(item["pub"])
                                    roles_str = ", ".join(item["roles"])
                                    pt.add_row([item['pub'], roles_str, priv])
                                except Exception as e:
                                    pt.add_row([item['pub'], "Error", str(e)])
                            print(pt)
                            input("\nPress Enter to return to menu...")
                            continue

                        else:
                            print("Invalid option.")
                            continue
                
                if should_refresh:
                    continue

                if analyzed_keys and not orphans: # Only ask if we haven't already dealt with orphans (or if there were none)
                     # But if we just refreshed, we might have orphans again or not.
                     # If we are here, it means we are NOT refreshing.
                     pass

                if analyzed_keys:
                    show_priv = input("\nDo you want to reveal the PRIVATE keys for the remaining keys? (yes/NO): ")
                    if show_priv.lower() == "yes":
                        print("\n" + "!"*60)
                        print(" [WARNING] DISPLAYING PRIVATE KEYS - ENSURE NO ONE IS WATCHING ")
                        print("!"*60 + "\n")
                        
                        pt = PrettyTable()
                        pt.field_names = ["Public Key", "Role", "Private Key"]
                        pt.align = "l"
                        
                        for item in analyzed_keys:
                            try:
                                priv = b.wallet.getPrivateKeyForPublicKey(item["pub"])
                                roles_str = ", ".join(item["roles"])
                                pt.add_row([item['pub'], roles_str, priv])
                            except Exception as e:
                                pt.add_row([item['pub'], "Error", str(e)])
                        print(pt)
                        input("\nPress Enter to clear screen and continue...")
                        clear_screen()
                        # continue # This would restart the analysis loop, effectively refreshing.
                        # But maybe user wants to exit Option 2.
                        # Let's break to go back to Main Menu.
                        break
                    else:
                        break # Go back to Main Menu
                else:
                    print("\nNo keys remaining in wallet.")
                    break
            
            input("\nPress Enter to continue...")

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
                    print("\n[!] No keys found in the expected format.")
                else:
                    print(f"\nFound {len(matches)} keys for account '{account_name}':")
                    
                    t = PrettyTable()
                    t.field_names = ["Role", "Private Key (WIF)"]
                    t.align = "l"
                    for role, wif in matches:
                        t.add_row([role, wif[:10] + "..." + wif[-5:]]) # Mask WIF for preview
                    print(t)
                    
                    confirm_import = input("\nDo you want to import these keys? (y/n): ")
                    if confirm_import.lower() != 'y':
                        print("Import cancelled.")
                        input("\nPress Enter to continue...")
                        continue

                    if not backup_wallet():
                        print("Backup failed. Aborting import.")
                        input("\nPress Enter to continue...")
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
                                    try:
                                        b.wallet.removePrivateKeyFromPublicKey(pub)
                                    except:
                                        pass 
                                    
                                    b.wallet.addPrivateKey(wif)
                                    print(f"  Success: {role} key replaced.")
                                else:
                                    print(f"  Skipped.")
                                continue
                            except Exception:
                                pass # Key not in wallet, proceed to add

                            b.wallet.addPrivateKey(wif)
                            print(f"  Success: {role} key added.")
                            
                            # Blockchain Update Check
                            try:
                                pub = b.wallet.publickey_from_wif(wif)
                                acc_data = Account(account_name, blockchain_instance=b)
                                
                                is_on_chain = False
                                if role == "OWNER":
                                    for auth in acc_data["owner"]["key_auths"]:
                                        if auth[0] == pub: is_on_chain = True
                                elif role == "ACTIVE":
                                    for auth in acc_data["active"]["key_auths"]:
                                        if auth[0] == pub: is_on_chain = True
                                elif role == "POSTING":
                                    for auth in acc_data["posting"]["key_auths"]:
                                        if auth[0] == pub: is_on_chain = True
                                elif role == "MEMO":
                                    if acc_data["memo_key"] == pub: is_on_chain = True
                                
                                if not is_on_chain:
                                    print(f"  [NOTICE] This {role} key is NOT active on the blockchain.")
                                    update = input(f"  Do you want to update your {role} key on the blockchain? (y/N): ")
                                    if update.lower() == 'y':
                                        print(f"  Updating {role} key...")
                                        resp = update_account_key(b, account_name, pub, role.lower())
                                        print(f"  [SUCCESS] Updated {role} key! Block: {resp.get('ref_block_num')}")
                            except Exception as e:
                                print(f"  Warning: Could not verify/update blockchain state: {e}")

                        except Exception as e:
                            print(f"  Error adding {role} key: {e}")
                    
                    input("\nImport complete. Press Enter to continue...")
                    clear_screen()
                    continue
                                
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
            break

if __name__ == "__main__":
    setup_wallet()
