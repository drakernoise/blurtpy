# `blurtpy` Usage Examples

This folder contains example scripts to perform common tasks with the `blurtpy` library.

## Requirements
Make sure you have installed the library and configured your private key (WIF) in environment variables or in the script itself (carefully!).

```bash
pip install blurtpy
```

## Initial Setup (IMPORTANT!)

Before running the examples, you must configure your **Secure Wallet**. This will create an encrypted local database (`blurtpy.sqlite`) to store your private keys, avoiding the need to write them in the code.

1.  Run the setup script:
    ```bash
    python examples/secure_wallet_setup.py
    ```
2.  Follow the instructions to create a master password and add your keys (WIF).

## Examples Index

### 1. Social Interaction (`social_actions.py`)
-   Comment on a post.
-   Count comments and list authors.
-   Vote on comments.
-   Find a user's latest post.
-   Search recent posts by criteria (tags).

### 2. Fund Management (`wallet_actions.py`)
-   Power Up (Transfer to Vesting).
-   Delegate Blurt Power (BP).
-   Multiple transfer (batch).
-   Recurring transfer (logic example).
-   Transfer to Savings.

### 3. Account Management (`account_management.py`)
-   Set recovery account.
-   Change account keys.

## Execution
To run any of the scripts (it will ask for the wallet password):

```bash
python examples/social_actions.py
```

## Node Optimization
The library includes a function to automatically find the fastest node. You can use it in your own scripts like this:

```python
from blurtpy import Blurt
# It will automatically connect to the node with the lowest latency
b = Blurt(node="best")
```
