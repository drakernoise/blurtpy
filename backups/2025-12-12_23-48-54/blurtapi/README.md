# blurtapi Module

This module is responsible for the low-level RPC (Remote Procedure Call) communication with the Blurt blockchain nodes.

## File Descriptions

| File | Description |
| :--- | :--- |
| `__init__.py` | Module initialization. |
| `exceptions.py` | RPC-specific exception classes (e.g., `RPCError`, `NumRetriesReached`). |
| `graphenerpc.py` | **`GrapheneRPC` class**: Handles the JSON-RPC protocol to send requests and receive responses. Manages connection lifecycle and error handling. |
| `node.py` | **`Node` class**: Represents a connection to a specific blockchain node URL. |
| `noderpc.py` | **`NodeRPC` class**: A wrapper for specific node interactions, often used to group related API calls. |
| `rpcutils.py` | Utility functions for RPC communication (e.g., sleeping between retries). |
| `version.py` | Module version information. |

## Usage

This module is primarily used internally by the `Blurt` class in `blurtpy/blurt.py`. Developers rarely need to interact with `blurtapi` directly unless they are building custom RPC connectors or low-level tools.
