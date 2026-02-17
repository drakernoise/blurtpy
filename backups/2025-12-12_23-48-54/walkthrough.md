# Walkthrough: Blurtpy Hardfork & Cleanup

## Overview
This document summarizes the changes made to `blurtpy` to create a dedicated Blurt blockchain library, removing legacy Steem/Hive references and the internal market logic which is not applicable to Blurt.

## Changes

### 1. Removal of Internal Market Logic
- **Deleted `blurtpy/market.py`**: The internal DEX logic was removed as Blurt is a single-asset chain.
- **Cleaned `blurtpy/cli.py`**: Removed the following commands:
    - `ticker`
    - `orderbook`
    - `buy`
    - `sell`
    - `cancel`
    - `openorders`
    - `tradehistory`
- **Refactored CLI Commands**: Updated `witnessfeed` and `info` commands to remove dependencies on `Market` class.

### 2. Removal of TBD (Legacy SBD/HBD)
- **Updated `blurtgraphenebase/chains.py`**: Removed the asset with ID 0 (SBD/TBD) from the chain definition.
- **Cleaned `blurtpy/amount.py`**: Removed TBD references from docstrings.
- **Refactored `blurtpy/blurt.py`**:
    - Renamed functions:
        - `rshares_to_tbd` -> `rshares_to_value`
        - `get_tbd_per_rshares` -> `get_value_per_rshares`
        - `tbd_to_rshares` -> `value_to_rshares`
        - `sp_to_tbd` -> `sp_to_value`
        - `vests_to_tbd` -> `vests_to_value`
    - Removed `tbd_symbol` property.
    - Updated logic to treat "Value" as a float (USD/Peg) instead of an on-chain asset.

### 3. Verification
- **Compilation**: The codebase compiles successfully (`python -m compileall .`).
- **Syntax Check**: Verified that no syntax errors were introduced during the refactoring.

## Next Steps
- **Testing**: Run unit tests (though many might need updates due to API changes).
- **New Repository**: Push this code to a new GitLab repository.
- **Price Oracle**: Implement a new `PriceOracle` class to fetch external prices for `witnessfeed` and other valuation needs.
