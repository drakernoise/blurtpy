# blurtpy: Python Library for Blurt

`blurtpy` is a modern, robust, and secure Python library for interacting with the **Blurt** blockchain.
It is a direct fork of the popular `beem` library, optimized and cleaned specifically for the Blurt ecosystem.

## Key Features

*   **Native to Blurt:** No dead code from Steem or Hive. Optimized for Blurt's consensus rules.
*   **Secure:** Security audit performed. Hardened private key handling to prevent accidental leaks.
*   **Complete:** Supports account operations, transfers, voting, witnesses, and more.
*   **High Performance:** Support for WebSocket and HTTP nodes. Fast transaction signing (optional support for `secp256k1`).

## Installation

### Prerequisites
*   Python 3.8 or higher.
*   `pip` and `setuptools`.

### Installation from Source
```bash
git clone https://gitlab.com/your-username/blurtpy.git
cd blurtpy
pip install -e .
```

### Optional Dependencies (Recommended)
For faster transaction signing:
```bash
pip install secp256k1prp
```
or
```bash
pip install cryptography
```

## Quick Start

### Connecting to Blurt
```python
from blurtpy import Blurt

# Connect to a public node
b = Blurt(node=["https://rpc.blurt.world"])

print(b.info())
```

### Account Management
```python
from blurtpy.account import Account

# Read account information
acc = Account("tekraze", blockchain_instance=b)
print(f"Balance: {acc.balances['available']}")
print(f"Voting Power: {acc.vp:.2f}%")
```

### Sending a Transfer
```python
from blurtpy import Blurt

# You need the active key to transfer
wif = "5YourActivePrivateKey..." 
b = Blurt(keys=[wif], node=["https://rpc.blurt.world"])

b.transfer("recipient", 10, "BLURT", "test memo", account="your-username")
```

### Voting on a Post
```python
from blurtpy import Blurt

# You need the posting key
wif = "5YourPostingPrivateKey..."
b = Blurt(keys=[wif], node=["https://rpc.blurt.world"])

# Vote at 100%
b.vote("@author/permlink", 100, account="your-username")
```

## Security

`blurtpy` has been audited to ensure responsible handling of private keys.
*   **Log Protection:** `PrivateKey` objects do not show the WIF (private key) when printed or converted to string, preventing leaks in logs.
*   **Deterministic Signing:** Support for robust ECDSA signatures.

> **Note:** Never share your private keys. If you use the local wallet (`blurtpy.sqlite`), make sure to protect it with a strong password.

## Additional Documentation

In the `docs/` folder you will find:
*   [Migration Guide and Walkthrough](docs/walkthrough.md)
*   [Security Audit Report](docs/security_audit_report.md)

## Credits

`blurtpy` is a fork of the library modified by Samuel Alphée Richard (Saboin), which is a fork of [beem](https://github.com/holgern/beem) created by Holger Hattendorf, who in turn based it on `python-bitshares` by Fabian Schuh.
We thank the open source community for laying the foundations of this project.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
