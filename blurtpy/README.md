# blurtpy Core Module

This directory contains the core logic and main classes of the `blurtpy` library. It is the high-level interface that developers interact with most frequently.

## Key Classes

*   **`Blurt` (`blurt.py`):** The main entry point. Connects to the blockchain, manages the wallet, and handles transactions.
*   **`Account` (`account.py`):** Represents a Blurt account. Used to fetch balances, history, and perform account-specific actions.
*   **`Wallet` (`wallet.py`):** Manages local private keys and locking/unlocking of the database.
*   **`TransactionBuilder` (`transactionbuilder.py`):** Constructs and signs transactions.
*   **`NodeList` (`nodelist.py`):** Manages the list of RPC nodes and benchmarking.

## Usage Example

```python
from blurtpy import Blurt
from blurtpy.account import Account

# Initialize Blurt instance
b = Blurt(node="best")

# Access Wallet
if b.wallet.created():
    b.wallet.unlock("your-password")

# Access Account
acc = Account("tekraze", blockchain_instance=b)
print(acc.balances)
```
