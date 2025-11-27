from blurtpy import Blurt
import json

# Connect to Blurt
b = Blurt(node=["https://rpc.blurt.world"])

print("Searching for recent account_update operations...")

# Get current block number
props = b.get_dynamic_global_properties()
head_block = props['head_block_number']

# Search back 100 blocks
found = False
for block_num in range(head_block, head_block - 1000, -1):
    if found: break
    if block_num % 10 == 0:
        print(f"Checking block {block_num}...")
    
    block = b.rpc.get_block(block_num)
    if not block or 'transactions' not in block:
        continue
        
    for tx in block['transactions']:
        for op in tx['operations']:
            op_type = op[0]
            op_data = op[1]
            
            if op_type == 'account_update':
                print(f"\n[FOUND] account_update in block {block_num}")
                print(json.dumps(op, indent=2))
                
                # Check if 'extensions' is present in the dictionary
                if 'extensions' in op_data:
                    print(f"EXTENSIONS FIELD FOUND: {op_data['extensions']}")
                else:
                    print("EXTENSIONS FIELD NOT FOUND in JSON")
                
                found = True
                break
                
if not found:
    print("No account_update found in last 1000 blocks.")
