# blurtgraphenebase Module

This module contains the low-level cryptographic primitives, encoding utilities, and data types that form the foundation of the Blurt protocol. It handles the "nuts and bolts" of blockchain interaction.

## Key Components

*   **`ecdsasig.py`:** Implements Elliptic Curve Digital Signature Algorithm (ECDSA) for signing transactions.
*   **`base58.py`:** Utilities for Base58 encoding and decoding (used for addresses and keys).
*   **`types.py`:** Defines low-level serialization types (e.g., `Int64`, `String`, `Array`) to ensure data matches the binary format expected by the blockchain.
*   **`chains.py`:** Contains configuration for known chains (Chain IDs, address prefixes).
*   **`bip32.py` / `bip38.py`:** Implements Bitcoin Improvement Proposals for hierarchical deterministic keys and password-protected keys.

## Usage

This module is used extensively by `blurtbase` to serialize operations and by `blurtpy` to sign transactions. It is rarely used directly by end-users.
