# `blurtpyv2` Usage Examples (Experimental)

This folder contains example scripts for the **V2 experimental API**. The V2 layer is under active development and focuses on a minimal, modular API.

## Requirements
Install the package locally (editable mode recommended while developing):

```bash
pip install -e .
```

## Quick Start

```python
from blurtpyv2 import Client

client = Client("https://<tu-nodo>")

# Read-only example
account = client.get_account("your_username")
print(account)
```

## Transfers (unsigned or signed)

```python
from blurtpyv2 import Client

client = Client("https://<tu-nodo>")

# Build-only (no signing, no broadcast)
tx = client.transfer(
    from_account="alice",
    to_account="bob",
    amount="1.000 BLURT",
    memo="hi",
    broadcast=False,
)
print(tx)
```

```python
from blurtpyv2 import Client

client = Client("https://<tu-nodo>")

# Signed + broadcast
client.transfer(
    from_account="alice",
    to_account="bob",
    amount="1.000 BLURT",
    memo="hi",
    wif_keys=["<wif_private_key>"],
    broadcast=True,
)
```

## Votes

```python
from blurtpyv2 import Client

client = Client("https://<tu-nodo>")

# Build-only vote
vote_tx = client.vote(
    voter="alice",
    author="bob",
    permlink="my-post",
    weight=10000,
    broadcast=False,
)
print(vote_tx)
```

## Propuestas (DHF)

```python
from blurtpyv2 import Client

client = Client("https://<tu-nodo>")

tx = client.create_proposal(
    creator="alice",
    receiver="bob",
    start_date="2025-01-01T00:00:00",
    end_date="2025-01-02T00:00:00",
    daily_pay="1.000 BLURT",
    subject="my proposal",
    permlink="proposal-permlink",
    broadcast=False,
)
print(tx)
```

## Escrow

```python
from blurtpyv2 import Client

client = Client("https://<tu-nodo>")

tx = client.escrow_transfer(
    from_account="alice",
    to_account="bob",
    agent="agent",
    escrow_id=1,
    blurt_amount="1.000 BLURT",
    fee="0.010 BLURT",
    ratification_deadline="2025-01-01T00:00:00",
    escrow_expiration="2025-01-02T00:00:00",
    json_meta={"note": "example"},
    broadcast=False,
)
print(tx)
```

## Cuenta / Recovery

```python
from blurtpyv2 import Client

client = Client("https://<tu-nodo>")

# Update2
tx = client.account_update2(
    account="alice",
    memo_key="BLURT1111111111111111111111111111111114T1Anm",
    broadcast=False,
)
print(tx)
```

## Voting power (UI metrics)

```python
from blurtpyv2 import Client

client = Client("https://<tu-nodo>")

info = client.get_voting_power_info("alice")
print(info)
```

## Wallet (KeyStore)

```python
from blurtpyv2.wallet import KeyStore

keystore = KeyStore()
keystore.add_private_key("<wif_private_key>")

pubkeys = keystore.list_public_keys()
print(pubkeys)
```

## Notes
- V2 is experimental. APIs may change.
- Use read-only calls or broadcast with care.
