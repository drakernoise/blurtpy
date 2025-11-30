# blurtapi Module

This module is responsible for the low-level RPC (Remote Procedure Call) communication with the Blurt blockchain nodes.

## Key Components

*   **`GrapheneRPC` (`graphenerpc.py`):** Handles the JSON-RPC protocol to send requests and receive responses from the blockchain.
*   **`NodeRPC` (`noderpc.py`):** A wrapper for specific node interactions.
*   **`Node` (`node.py`):** Represents a connection to a specific blockchain node.

## Usage

This module is primarily used internally by the `Blurt` class in `blurtpy/blurt.py`. Developers rarely need to interact with `blurtapi` directly unless they are building custom RPC connectors or low-level tools.
