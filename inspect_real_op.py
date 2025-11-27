from blurtpy import Blurt
import json

# Connect to Blurt
b = Blurt(node=["https://rpc.blurt.world"])

import sys

# ... (connection setup)

if len(sys.argv) > 1:
    # Check specific block
    block_num = int(sys.argv[1])
    print(f"Inspecting specific block {block_num}...")
    blocks_to_check = [block_num]
else:
    # Search back 20000 blocks
    print("Searching for recent account_update operations...")
    props = b.get_dynamic_global_properties()
    head_block = props['head_block_number']
    blocks_to_check = range(head_block, head_block - 20000, -1)

found = False
for block_num in blocks_to_check:
    if found and len(sys.argv) == 1: break # Stop after first find in search mode
    
    if len(sys.argv) == 1 and block_num % 100 == 0:
        print(f"Checking block {block_num}...")
    
    try:
        block = b.rpc.get_block(block_num)
    except Exception as e:
        print(f"Error fetching block {block_num}: {e}")
        continue

    if not block or 'transactions' not in block:
        if len(sys.argv) > 1: print("Block has no transactions.")
        continue
        
    for tx in block['transactions']:
        for op in tx['operations']:
            op_type = op[0]
            op_data = op[1]
            
            if op_type in ['account_update', 'account_update2']:
                print(f"\n[FOUND] {op_type} in block {block_num}")
                print(json.dumps(op, indent=2))
                
                # Check if 'extensions' is present in the dictionary
                if 'extensions' in op_data:
                    print(f"EXTENSIONS FIELD FOUND: {op_data['extensions']}")
                else:
                    print("EXTENSIONS FIELD NOT FOUND in JSON")
                
                found = True
                
if not found:
    print("No account_update or account_update2 found.")
