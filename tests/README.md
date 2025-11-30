# Blurtpy Native Test Suite

This directory contains the **Native Test Suite** for `blurtpy`, designed to verify the core functionality, security, and stability of the library against the Blurt blockchain.

## 📂 Structure

*   **`test_native_blurt.py`**: The main test file containing all test cases. It uses `unittest` and `pytest`.

## 🧪 What is Tested?

The suite covers 10 critical scenarios to ensure the library works as expected:

### 1. Connectivity & Basics
*   **`test_01_connection_and_props`**: Verifies connection to multiple RPC nodes (failover) and fetches blockchain properties (Head Block).

### 2. Account Data
*   **`test_02_account_fetch_integrity`**: Fetches a real account (`draktest`) and verifies data types (e.g., Balances are `Amount` objects).
*   **`test_03_account_not_found`**: Ensures the library raises the correct `AccountDoesNotExistsException` for non-existent accounts.
*   **`test_06_history_resilience`**: Fetches account history to verify API response handling and pagination.

### 3. Security & Cryptography (Dry-Run)
*   **`test_04_transaction_signing`**: Signs a transfer transaction using the Active Key. **Crucial:** Uses `nobroadcast=True` to verify the signature *without* spending funds.
*   **`test_05_missing_key_protection`**: Confirms that operations requiring a key fail safely (`MissingKeyError` or `WalletLocked`) if the key is not present.
*   **`test_07_memo_encryption`**: Tests AES encryption and decryption of Memos using ephemeral keys (simulating Sender and Receiver).

### 4. Operations (Dry-Run)
These tests construct and sign complex operations to ensure the library generates valid blockchain transactions:
*   **`test_08_power_up_dry_run`**: Transfer to Vesting (Power Up).
*   **`test_09_claim_rewards_dry_run`**: Claim Reward Balance.
*   **`test_10_vote_operation_dry_run`**: Vote on a post.

### 5. Input Validation & Robustness
*   **`test_11_input_validation`**: Verifies that the library rejects invalid or malicious inputs, such as:
    *   Negative transfer amounts (raises `ValueError`).
    *   Invalid asset symbols (raises `AssetDoesNotExistsException`).

> **🛡️ Note on Safety:** All transaction tests are configured as **Dry-Runs** (`nobroadcast=True`). They generate and sign the transaction to prove cryptographic correctness but **DO NOT** broadcast it to the network. No funds are spent.

## ⚙️ Configuration

The tests use a default account (`draktest`) and a public Active Key for verification. **You can (and should) edit these values** in `tests/test_native_blurt.py` to test with your own account or verify different permissions.

Look for these constants at the top of the file:

```python
# User provided key for 'draktest'
ACTIVE_KEY = "5K8sEXDvidZijhKpYDyWxyKSP22T3UdU8276YEsmcDgwbmgRS6K"
ACCOUNT_NAME = "draktest"
```

## 🚀 How to Run Tests

You need `pytest` installed. Run the following command from the root of the project:

```bash
pytest tests/test_native_blurt.py
```

### Verbose Output
To see detailed logs (including connection steps and transaction details):

```bash
pytest tests/test_native_blurt.py -v
```
