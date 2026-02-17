# blurtbase Module

This module defines the fundamental data structures and operations of the Blurt blockchain protocol. It maps Python objects to the binary structures required by the blockchain.

## File Descriptions

| File | Description |
| :--- | :--- |
| `__init__.py` | Module initialization. |
| `ledgertransactions.py` | Support for signing transactions with Ledger hardware wallets. |
| `memo.py` | **`Memo` class**: Implements encryption and decryption of transaction memos using shared secrets. |
| `objects.py` | Defines basic blockchain objects like `Amount`, `Asset`, `PublicKey`, `Permission`, etc. |
| `objecttypes.py` | Enumeration of object types used in the Graphene protocol (e.g., `account_object`, `asset_object`). |
| `operationids.py` | Constants mapping operation names to their numeric IDs (e.g., `TRANSFER`, `VOTE`). |
| `operations.py` | **Operation Classes**: Definitions for all blockchain operations (e.g., `Transfer`, `Vote`, `AccountUpdate`). Handles serialization. |
| `signedtransactions.py` | **`SignedTransaction` class**: Logic for creating, signing, and verifying transactions. |
| `transactions.py` | Base transaction definitions. |
| `version.py` | Module version information. |

## Usage

This module is the "grammar" of the library. When you call `b.transfer()` in `blurtpy`, it uses `blurtbase.operations.Transfer` to create the operation object that will be signed and broadcast.
