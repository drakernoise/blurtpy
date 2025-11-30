# blurtbase Module

This module defines the fundamental data structures and operations of the Blurt blockchain protocol. It maps Python objects to the binary structures required by the blockchain.

## Key Components

*   **`operations.py`:** Contains class definitions for all blockchain operations (e.g., `Transfer`, `Vote`, `AccountUpdate`). These classes handle the serialization of data for signing.
*   **`objects.py`:** Defines basic blockchain objects like `Amount`, `Asset`, `PublicKey`, etc.
*   **`signedtransactions.py`:** Logic for creating and signing transactions.
*   **`memo.py`:** Implements encryption and decryption of transaction memos.

## Usage

This module is the "grammar" of the library. When you call `b.transfer()` in `blurtpy`, it uses `blurtbase.operations.Transfer` to create the operation object that will be signed and broadcast.
