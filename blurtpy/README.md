# blurtpy Core Module

This directory contains the core logic and main classes of the `blurtpy` library. It is the high-level interface that developers interact with most frequently.

## File Descriptions

| File | Description |
| :--- | :--- |
| `__init__.py` | Module initialization and exports. |
| `account.py` | **`Account` class**: Represents a Blurt account. Used to fetch balances, history, and perform account-specific actions. |
| `amount.py` | **`Amount` class**: Handles currency amounts (e.g., "10.000 BLURT") and arithmetic operations. |
| `asciichart.py` | Utilities for generating ASCII charts, primarily for the CLI. |
| `asset.py` | **`Asset` class**: Represents blockchain assets (BLURT, VESTS) and their properties. |
| `block.py` | **`Block` class**: Represents a block on the blockchain, containing transactions. |
| `blockchain.py` | **`Blockchain` class**: General blockchain information, current block, chain parameters. |
| `blockchaininstance.py` | Manages the shared `Blurt` instance to ensure a single connection is used across objects. |
| `blockchainobject.py` | Base class for all blockchain objects, handling caching and lazy loading. |
| `blurt.py` | **`Blurt` class**: The main entry point. Connects to the blockchain, manages the wallet, and handles transactions. |
| `blurtsigner.py` | Logic for signing transactions using available keys. |
| `cli.py` | Command Line Interface (CLI) implementation for the `blurtpy` command. |
| `comment.py` | **`Comment` class**: Represents posts and comments. Used to read content, reply, and vote. |
| `constants.py` | System constants and configuration defaults. |
| `conveyor.py` | Efficiently processes blocks and operations in a stream. |
| `discussions.py` | **`Discussions` class**: Fetches discussion lists (trending, hot, created, etc.). |
| `exceptions.py` | Custom exception classes for `blurtpy`. |
| `imageuploader.py` | Utilities for uploading images to IPFS or other hosting services. |
| `instance.py` | Helper functions for instance management. |
| `market.py` | **`Market` class**: Interface for the Decentralized Exchange (DEX). |
| `memo.py` | Utilities for encrypting and decrypting transaction memos. |
| `message.py` | Tools for signing and verifying arbitrary text messages with private keys. |
| `nodelist.py` | **`NodeList` class**: Manages the list of RPC nodes and performs latency benchmarking. |
| `price.py` | **`Price` class**: Represents an exchange rate between two assets. |
| `profile.py` | Utilities for parsing and handling user profile metadata. |
| `snapshot.py` | Tools for taking snapshots of account balances or other state. |
| `storage.py` | Interface for the local storage backend. |
| `transactionbuilder.py` | **`TransactionBuilder` class**: Constructs, signs, and broadcasts transactions. |
| `utils.py` | General utility functions (date parsing, formatting, etc.). |
| `version.py` | Library version information. |
| `vote.py` | **`Vote` class**: Represents a vote on a post or comment. |
| `wallet.py` | **`Wallet` class**: Manages local private keys and locking/unlocking of the database. |
| `witness.py` | **`Witness` class**: Represents a block producer (witness) and related operations. |

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
acc = Account("<YOUR_USERNAME>", blockchain_instance=b)
print(acc.balances)
```
