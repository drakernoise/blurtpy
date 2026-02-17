"""Algorithm-agnostic crypto interfaces for V2."""

from typing import Protocol


class Signer(Protocol):
    """Signs message bytes (hashing strategy is backend-defined)."""

    def sign(self, message: bytes) -> bytes:
        ...


class Verifier(Protocol):
    """Verifies a signature over message bytes (hashing is backend-defined)."""

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        ...


class KeyAdapter(Protocol):
    """Handles parsing/serialization for key material."""

    def to_public(self, private_key: bytes) -> bytes:
        ...

    def parse_public(self, public_key: bytes) -> bytes:
        ...

    def parse_private(self, private_key: bytes) -> bytes:
        ...
