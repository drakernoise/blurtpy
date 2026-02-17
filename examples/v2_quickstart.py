from blurtpyv2 import Client


def main():
    client = Client("https://api.blurtit.com")

    # Read-only
    account = client.get_account("your_username")
    print(account)

    # Build-only transfer (no broadcast)
    tx = client.transfer(
        from_account="alice",
        to_account="bob",
        amount="1.000 BLURT",
        memo="hi",
        broadcast=False,
    )
    print(tx)

    # Build-only witness vote (no broadcast)
    wtx = client.witness_vote(
        account="alice",
        witness="somewitness",
        approve=True,
        broadcast=False,
    )
    print(wtx)


if __name__ == "__main__":
    main()
