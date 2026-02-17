"""ECDSA backend for V2 using existing blurtgraphenebase primitives."""

from __future__ import annotations

from typing import Union

from blurtgraphenebase.account import PrivateKey, PublicKey
from blurtgraphenebase.ecdsasig import sign_message, verify_message

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


class EcdsaKeyAdapter:
    """Key adapter for Graphene-compatible WIF/public keys."""

    def to_public(self, private_key: PrivateKeyLike) -> PublicKey:
        return _normalize_private_key(private_key).pubkey

    def parse_public(self, public_key: PublicKeyLike) -> PublicKey:
        return _normalize_public_key(public_key)

    def parse_private(self, private_key: PrivateKeyLike) -> PrivateKey:
        return _normalize_private_key(private_key)


class EcdsaSigner:
    """ECDSA signer using WIF private keys."""

    def __init__(self, private_key: PrivateKeyLike):
        self._private_key = _normalize_private_key(private_key)

    def sign(self, message: bytes) -> bytes:
        """Sign message bytes (hashing is performed internally)."""
        return sign_message(message, str(self._private_key))


class EcdsaVerifier:
    """ECDSA verifier using Graphene public keys."""

    def verify(self, message: bytes, signature: bytes, public_key: PublicKeyLike) -> bool:
        """Verify message bytes (hashing is performed internally)."""
        recovered = verify_message(message, signature)
        expected = bytes(_normalize_public_key(public_key))
        return recovered == expected
