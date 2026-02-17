"""Operation helpers for V2."""

from __future__ import annotations

from typing import Any, Dict

from blurtbase.objects import Operation


def transfer(
    from_account: str,
    to_account: str,
    amount: str,
    memo: str = "",
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "from": from_account,
        "to": to_account,
        "amount": amount,
        "memo": memo,
    }
    return Operation("transfer", payload, prefix=prefix)


def vote(
    voter: str,
    author: str,
    permlink: str,
    weight: int,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "voter": voter,
        "author": author,
        "permlink": permlink,
        "weight": int(weight),
    }
    return Operation("vote", payload, prefix=prefix)
