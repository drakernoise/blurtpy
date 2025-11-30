# blurtstorage Module

This module handles the persistent storage of data for `blurtpy`, specifically the secure local wallet and configuration settings.

## Key Components

*   **`SQLiteStore` (`sqlite.py`):** Implements the storage backend using SQLite. It stores encrypted private keys and configuration key-value pairs.
*   **`MasterPassword` (`masterpassword.py`):** Handles the encryption and decryption of the wallet using a user-provided password. It ensures that private keys are never stored in plain text.
*   **`DataDir`:** Manages the directory where the wallet file (`blurtpy.sqlite`) is stored (usually in the user's application data folder).

## Security Note

While this module encrypts your keys, the security of your wallet ultimately depends on the strength of your **Master Password**. Always choose a strong, unique password and keep your `blurtpy.sqlite` file safe.
