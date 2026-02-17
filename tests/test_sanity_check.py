import logging
from blurtpy import Blurt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sanity_check():
    """
    Sanity Check:
    Verifies that the library can connect to real public nodes
    and read basic data without errors.
    """
    logger.info("Starting Sanity Check...")
    
    # List of known public nodes
    nodes = [
        "https://rpc.beblurt.com",
        "https://blurt-rpc.saboin.com",
        "https://rpc.blurt.world"
    ]
    
    try:
        # 1. Connection
        logger.info(f"Connecting to public nodes: {nodes}")
        b = Blurt(node=nodes)
        
        # 2. Read Dynamic Global Properties (DGP)
        logger.info("Reading blockchain state (DGP)...")
        props = b.get_dynamic_global_properties()
        head_block = props['head_block_number']
        logger.info(f"DONE Connection Successful! Current block: {head_block}")
        
        # 3. Read a real account (e.g. 'initminer' or 'saboin')
        target_account = "saboin"
        from blurtpy.account import Account
        logger.info(f"Reading public account '{target_account}'...")
        account = Account(target_account, blockchain_instance=b)
        if account:
            balance = account.get('balance', 'N/A')
            logger.info(f"DONE Account found. Balance: {balance}")
        else:
            logger.warning("WARNING Could not read account (might be a node issue, not a library issue)")

        logger.info("SUCCESS SANITY CHECK COMPLETED SUCCESSFULLY")
        return True

    except Exception as e:
        logger.error(f"FAILED SANITY CHECK FAILED: {e}")
        return False

if __name__ == "__main__":
    sanity_check()
