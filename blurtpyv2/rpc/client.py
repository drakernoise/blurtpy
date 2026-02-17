"""Minimal RPC client wrapper for V2."""

from __future__ import annotations

from typing import Any, Iterable, List, Optional

from blurtapi.graphenerpc import GrapheneRPC


class RpcClient:
    """Lightweight wrapper around GrapheneRPC with a stable V2 surface."""

    def __init__(self, urls, user: Optional[str] = None, password: Optional[str] = None, **kwargs):
        self._rpc = GrapheneRPC(urls, user, password, **kwargs)

    def close(self) -> None:
        self._rpc.rpcclose()

    def call(self, method: str, *args, **kwargs) -> Any:
        """Call an arbitrary RPC method."""
        return getattr(self._rpc, method)(*args, **kwargs)

    def get_account(self, name: str) -> Optional[dict]:
        """Get a single account by name (or None)."""
        accounts = self.get_accounts([name])
        return accounts[0] if accounts else None

    def get_accounts(self, names: Iterable[str]) -> List[dict]:
        """Get multiple accounts by name."""
        return self._rpc.get_accounts(list(names), api="database")

    def get_dynamic_global_properties(self) -> dict:
        return self._rpc.get_dynamic_global_properties(api="database")

    def broadcast_transaction(self, tx: dict) -> Any:
        return self._rpc.broadcast_transaction(tx, api="network_broadcast")

    def broadcast_transaction_synchronous(self, tx: dict) -> Any:
        return self._rpc.broadcast_transaction_synchronous(tx, api="network_broadcast")
