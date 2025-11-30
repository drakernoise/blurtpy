# blurtstorage Module

This module handles the persistent storage of data for `blurtpy`, specifically the secure local wallet and configuration settings.

## File Descriptions

| File | Description |
| :--- | :--- |
| `__init__.py` | Module initialization. |
| `base.py` | Base class for storage implementations. |
| `exceptions.py` | Storage-specific exceptions (e.g., `WrongMasterPasswordException`). |
| `interfaces.py` | Defines the abstract interfaces for Store, ConfigStore, and KeyStore. |
| `masterpassword.py` | **`MasterPassword` class**: Handles the encryption and decryption of the wallet using a user-provided password. |
| `ram.py` | **`RamStore` class**: An in-memory storage implementation (non-persistent), useful for testing. |
| `sqlite.py` | **`SQLiteStore` class**: The default persistent storage backend using SQLite. Stores encrypted keys and config. |

## Security Note

While this module encrypts your keys, the security of your wallet ultimately depends on the strength of your **Master Password**. Always choose a strong, unique password and keep your `blurtpy.sqlite` file safe.
