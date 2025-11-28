import os
import shutil
import datetime
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

def update_memo_key(blurt_instance, account_name, new_memo_key):
    """
    Updates the memo key for the given account.
    Requires Active or Owner key to be present in the wallet.
    """
    try:
        acc = Account(account_name, blockchain_instance=blurt_instance)
        
        # Construct Account_update operation
        # We must preserve existing authorities (owner, active, posting)
        # and only change the memo_key.
        
        op = operations.Account_update(
            account=account_name,
            owner=acc["owner"],
            active=acc["active"],
            posting=acc["posting"],
            memo_key=new_memo_key,
            json_metadata=acc["json_metadata"],
            posting_json_metadata=acc.get("posting_json_metadata", ""),
            extensions=acc.get("extensions", []),
            prefix=blurt_instance.chain_params["prefix"]
        )
        
        # Sign and Broadcast
        # The library automatically selects the required key from the wallet
        blurt_instance.txbuffer.clear()
        blurt_instance.txbuffer.appendOps([op])
        blurt_instance.wallet.sign_transaction(blurt_instance.txbuffer)
        resp = blurt_instance.txbuffer.broadcast()
        return resp
        
    except Exception as e:
        raise Exception(f"Failed to update memo key: {e}")


def print_banner():
    clear_screen()
    print(r"""
  ____  _durt  _              
 |  _ \| |_   | |    _ __  _   _ 
 | |_) | | |  | |   | '_ \| | | |
 |  _ <| | |_ | |___| |_) | |_| |
 |_| \_\_|\__||_____| .__/ \__, |
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
        print("6. Account Operations (Blockchain)")
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
                else:
                    print("Key saved. (Note: Could not automatically identify the account,")
                    print("this is normal for Memo keys or if there are connection issues).")
                    
            except Exception as e:
                print(f"Error adding key: {e}")
            
            input("\nPress Enter to continue...")
                
        elif option == "2":
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

            # Inline Cleanup for Orphans
            if orphans:
                print(f"\n[NOTICE] Found {len(orphans)} orphan key(s) that are not used by any account.")
                cleanup = input("Do you want to DELETE these orphan keys? (y/N): ")
                if cleanup.lower() == 'y':
                    if backup_wallet():
                        deleted_count = 0
                        for k in orphans:
                            try:
                                b.wallet.removePrivateKeyFromPublicKey(k)
                                deleted_count += 1
                            except Exception as e:
                                print(f"Error deleting {k}: {e}")
                        print(f"Successfully deleted {deleted_count} orphan keys.")
                        # Remove from analyzed_keys list for display
                        analyzed_keys = [x for x in analyzed_keys if x['pub'] not in orphans]
                    else:
                        print("Backup failed. Aborting deletion.")

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
                    continue
            else:
                print("\nNo keys remaining in wallet.")
            
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

        elif option == "6":
            print("\n--- Account Operations (Blockchain) ---")
            print("1. Update Memo Key (Promote Orphan Key)")
            print("2. Back to Main Menu")
            
            sub_op = input("Choose an option: ")
            
            if sub_op == "1":
                print("\n--- Update Memo Key ---")
                print("This will set an 'Orphan' key from your wallet as your official Memo Key on the blockchain.")
                print("Requires Active or Owner key for the account to be present in the wallet.")
                
                # 1. Find potential accounts in wallet
                keys = b.wallet.getPublicKeys()
                accounts_found = set()
                orphans = []
                
                print("Analyzing wallet keys...")
                for k in keys:
                    try:
                        accs = list(b.wallet.getAccountsFromPublicKey(k))
                        if accs:
                            for a in accs:
                                accounts_found.add(a)
                        else:
                            orphans.append(k)
                    except:
                        pass
                
                if not accounts_found:
                    print("[!] No accounts identified in wallet. Cannot proceed.")
                    print("Please import your Active or Owner key first.")
                    input("\nPress Enter to continue...")
                    continue
                    
                if not orphans:
                    print("[!] No orphan keys found to promote.")
                    input("\nPress Enter to continue...")
                    continue
                
                # 2. Select Account
                target_account = ""
                if len(accounts_found) == 1:
                    target_account = list(accounts_found)[0]
                    print(f"Target Account: {target_account}")
                else:
                    print("\nSelect Account:")
                    sorted_accs = sorted(list(accounts_found))
                    for idx, acc in enumerate(sorted_accs):
                        print(f"{idx+1}. {acc}")
                    
                    try:
                        sel = int(input("Enter number: "))
                        target_account = sorted_accs[sel-1]
                    except:
                        print("Invalid selection.")
                        input("\nPress Enter to continue...")
                        continue

                # 3. Select Orphan Key
                print(f"\nSelect Orphan Key to set as MEMO key for '{target_account}':")
                t = PrettyTable()
                t.field_names = ["#", "Public Key"]
                t.align = "l"
                
                for idx, k in enumerate(orphans):
                    t.add_row([idx+1, k])
                print(t)
                
                try:
                    sel = int(input("Enter number: "))
                    new_memo_key = orphans[sel-1]
                except:
                    print("Invalid selection.")
                    input("\nPress Enter to continue...")
                    continue
                
                # 4. Confirm and Execute
                print(f"\n[CONFIRM] You are about to update the MEMO key for '{target_account}'.")
                print(f"New Memo Key: {new_memo_key}")
                confirm = input("Type 'YES' to confirm transaction: ")
                
                if confirm == "YES":
                    if not backup_wallet():
                        print("Backup failed. Aborting.")
                        input("\nPress Enter to continue...")
                        continue
                        
                    print("Broadcasting transaction...")
                    try:
                        resp = update_memo_key(b, target_account, new_memo_key)
                        print("\n[SUCCESS] Transaction broadcasted!")
                        print(f"Ref Block Num: {resp.get('ref_block_num')}")
                        print("Your Memo Key has been updated.")
                    except Exception as e:
                        print(f"\n[ERROR] Transaction failed: {e}")
                else:
                    print("Operation cancelled.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    setup_wallet()
