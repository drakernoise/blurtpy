# blurtgraphenebase Module

This module contains the low-level cryptographic primitives, encoding utilities, and data types that form the foundation of the Blurt protocol. It handles the "nuts and bolts" of blockchain interaction.

## File Descriptions

| File | Description |
| :--- | :--- |
| `__init__.py` | Module initialization. |
| `account.py` | **`PasswordKey` / `BrainKey`**: Utilities for generating keys from passwords or brain keys (mnemonics). |
| `aes.py` | AES encryption/decryption utilities. |
| `base58.py` | Base58 encoding/decoding implementation (standard for addresses and WIFs). |
| `bip32.py` | BIP32 (Hierarchical Deterministic Wallets) implementation. |
| `bip38.py` | BIP38 (Password-protected private keys) implementation. |
| `chains.py` | Configuration for known blockchain networks (Chain IDs, address prefixes). |
| `dictionary.py` | Word lists for Brain Key generation (English, etc.). |
| `ecdsasig.py` | **ECDSA Signatures**: Core logic for signing data with SECP256k1 curve. |
| `objects.py` | Low-level Graphene objects. |
| `objecttypes.py` | Graphene object type definitions. |
| `operationids.py` | Operation ID constants. |
| `operations.py` | Base operation definitions. |
| `prefix.py` | Address prefix handling. |
| `py23.py` | Python 2/3 compatibility utilities (legacy). |
| `signedtransactions.py` | Low-level signed transaction structure. |
| `types.py` | **Serialization Types**: Defines `Int64`, `String`, `Array`, `PointInTime`, etc., for binary serialization. |
| `unsignedtransactions.py` | Unsigned transaction structure. |
| `version.py` | Module version information. |

## Usage

This module is used extensively by `blurtbase` to serialize operations and by `blurtpy` to sign transactions. It is rarely used directly by end-users.
