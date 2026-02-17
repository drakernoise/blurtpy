"""In-memory keystore (skeleton) for V2."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Union

from blurtgraphenebase.account import PrivateKey, PublicKey
from blurtpyv2.crypto import EcdsaSigner

PublicKeyLike = Union[str, bytes, PublicKey]
PrivateKeyLike = Union[str, bytes, PrivateKey]


def _normalize_private_key(private_key: PrivateKeyLike) -> PrivateKey:
    if isinstance(private_key, PrivateKey):
        return private_key
    if isinstance(private_key, bytes):
        private_key = private_key.decode("utf-8")
    return PrivateKey(private_key)


def _normalize_public_key(public_key: PublicKeyLike) -> PublicKey:
    if isinstance(public_key, PublicKey):
        return public_key
    if isinstance(public_key, bytes):
        public_key = public_key.decode("utf-8")
    return PublicKey(public_key)


class KeyStore:
    """Simple in-memory key store. No encryption in this skeleton."""

    def __init__(self) -> None:
        self._keys: Dict[str, PrivateKey] = {}

    def add_private_key(self, private_key: PrivateKeyLike) -> PublicKey:
        priv = _normalize_private_key(private_key)
        pub = priv.pubkey
        self._keys[repr(pub)] = priv
        return pub

    def add_private_keys(self, keys: Iterable[PrivateKeyLike]) -> List[PublicKey]:
        return [self.add_private_key(k) for k in keys]

    def remove_public_key(self, public_key: PublicKeyLike) -> None:
        pub = _normalize_public_key(public_key)
        self._keys.pop(repr(pub), None)

    def get_private_key(self, public_key: PublicKeyLike) -> Optional[PrivateKey]:
        pub = _normalize_public_key(public_key)
        return self._keys.get(repr(pub))

    def list_public_keys(self) -> List[PublicKey]:
        return [PublicKey(k) for k in self._keys.keys()]

    def sign(self, message: bytes, public_key: PublicKeyLike) -> bytes:
        priv = self.get_private_key(public_key)
        if priv is None:
            raise KeyError("Private key not found for provided public key")
        return EcdsaSigner(priv).sign(message)
