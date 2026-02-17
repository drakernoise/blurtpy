"""Minimal transaction builder for V2 (skeleton)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, List, Optional
from binascii import unhexlify
import struct

from blurtpyv2.rpc import RpcClient
from blurtpyv2.wallet import KeyStore
from blurtgraphenebase.chains import known_chains
from blurtgraphenebase.signedtransactions import Signed_Transaction


@dataclass
class TxBuilder:
    """Builds a basic unsigned transaction dict."""

    rpc: Optional[RpcClient] = None
    expiration_seconds: int = 30
    ref_block_num: Optional[int] = None
    ref_block_prefix: Optional[int] = None
    operations: List[Any] = field(default_factory=list)
    extensions: List[Any] = field(default_factory=list)

    def add_operation(self, operation: Any) -> None:
        self.operations.append(operation)

    def add_operations(self, ops: Iterable[Any]) -> None:
        self.operations.extend(list(ops))

    def set_expiration(self, seconds: int) -> None:
        self.expiration_seconds = int(seconds)

    def _calc_expiration(self) -> str:
        expiration = datetime.utcnow() + timedelta(seconds=self.expiration_seconds)
        return expiration.replace(microsecond=0).isoformat()

    def _compute_ref_block(self) -> None:
        if self.rpc is None:
            return
        props = self.rpc.get_dynamic_global_properties()
        head_block_number = int(props["head_block_number"])
        head_block_id = props["head_block_id"]
        self.ref_block_num = head_block_number & 0xFFFF
        self.ref_block_prefix = struct.unpack_from("<I", unhexlify(head_block_id), 4)[0]

    def build(self) -> Dict[str, Any]:
        if self.ref_block_num is None or self.ref_block_prefix is None:
            self._compute_ref_block()
        return {
            "ref_block_num": self.ref_block_num,
            "ref_block_prefix": self.ref_block_prefix,
            "expiration": self._calc_expiration(),
            "operations": self.operations,
            "extensions": self.extensions,
        }

    def sign_with_wifs(self, wif_keys: Iterable[str], chain: str = "BLURT") -> Dict[str, Any]:
        """Return a signed transaction dict using provided WIF keys."""
        tx = self.build()
        chain_params = known_chains.get(chain)
        if chain_params is None:
            raise ValueError(f"Unknown chain: {chain}")
        signed = Signed_Transaction({
            **tx,
            "prefix": chain_params.get("prefix", "BLURT"),
        })
        signed.sign(list(wif_keys), chain=chain)
        return signed.json()

    def sign_with_keystore(
        self,
        keystore: KeyStore,
        public_keys: Iterable[Any],
        chain: str = "BLURT",
    ) -> Dict[str, Any]:
        """Sign using a KeyStore and a set of public keys."""
        wifs: List[str] = []
        for pub in public_keys:
            priv = keystore.get_private_key(pub)
            if priv is None:
                raise KeyError("Private key not found for provided public key")
            wifs.append(str(priv))
        return self.sign_with_wifs(wifs, chain=chain)
