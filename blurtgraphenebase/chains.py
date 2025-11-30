# -*- coding: utf-8 -*-
default_prefix = "BLURT"
known_chains = {
    "BLURT": {
        "chain_id": "cd8d90f29f399dd4b78908d4422042531c353326660f97d9f96669084a973210",
        "prefix": "BLURT",
        "chain_assets": [
            {"asset": "BLURT", "symbol": "BLURT", "precision": 3, "id": 1},
            {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
        ],
    },
    "TESTNET": {
        "chain_id": "885242db8d9f49742c14df62b869d7930976b64d23d513483db7b17253510c2c",
        "prefix": "BLURT",
        "chain_assets": [
            {"asset": "TESTS", "symbol": "TESTS", "precision": 3, "id": 1},
            {"asset": "VESTS", "symbol": "VESTS", "precision": 6, "id": 2}
        ],
    }
}
