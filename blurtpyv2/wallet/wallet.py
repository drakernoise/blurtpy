"""High-level wallet facade for V2 (skeleton)."""

from __future__ import annotations

from typing import Iterable, Any, Optional

from blurtpyv2.tx import TxBuilder
from .keystore import KeyStore


class Wallet:
    """Simple wallet facade that delegates to a KeyStore."""

    def __init__(self, keystore: Optional[KeyStore] = None) -> None:
        self.keystore = keystore or KeyStore()

    def add_private_key(self, private_key: Any):
        return self.keystore.add_private_key(private_key)

    def sign_transaction(
        self,
        builder: TxBuilder,
        public_keys: Iterable[Any],
        chain: str = "BLURT",
    ):
        return builder.sign_with_keystore(self.keystore, public_keys, chain=chain)
