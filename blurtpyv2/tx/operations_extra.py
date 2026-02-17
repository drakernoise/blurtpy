"""Additional operation helpers for V2 (second batch)."""

from __future__ import annotations

from typing import Any, Dict, Optional

from blurtbase.objects import Operation


def power_up(
    from_account: str,
    to_account: str,
    amount: str,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "from": from_account,
        "to": to_account,
        "amount": amount,
    }
    return Operation("transfer_to_vesting", payload, prefix=prefix)


def power_down(
    account: str,
    vesting_shares: str,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "account": account,
        "vesting_shares": vesting_shares,
    }
    return Operation("withdraw_vesting", payload, prefix=prefix)


def delegate_vesting_shares(
    delegator: str,
    delegatee: str,
    vesting_shares: str,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "delegator": delegator,
        "delegatee": delegatee,
        "vesting_shares": vesting_shares,
    }
    return Operation("delegate_vesting_shares", payload, prefix=prefix)


def undelegate_vesting_shares(
    delegator: str,
    delegatee: str,
    prefix: str = "BLURT",
) -> Operation:
    return delegate_vesting_shares(delegator, delegatee, "0.000000 VESTS", prefix=prefix)


def witness_vote(
    account: str,
    witness: str,
    approve: bool,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "account": account,
        "witness": witness,
        "approve": bool(approve),
    }
    return Operation("account_witness_vote", payload, prefix=prefix)


def witness_proxy(
    account: str,
    proxy: str,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "account": account,
        "proxy": proxy,
    }
    return Operation("account_witness_proxy", payload, prefix=prefix)


def transfer_to_savings(
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
    return Operation("transfer_to_savings", payload, prefix=prefix)


def transfer_from_savings(
    from_account: str,
    request_id: int,
    to_account: str,
    amount: str,
    memo: str = "",
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "from": from_account,
        "request_id": int(request_id),
        "to": to_account,
        "amount": amount,
        "memo": memo,
    }
    return Operation("transfer_from_savings", payload, prefix=prefix)


def cancel_transfer_from_savings(
    from_account: str,
    request_id: int,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "from": from_account,
        "request_id": int(request_id),
    }
    return Operation("cancel_transfer_from_savings", payload, prefix=prefix)


def comment(
    parent_author: str,
    parent_permlink: str,
    author: str,
    permlink: str,
    title: str,
    body: str,
    json_metadata: Any = "",
) -> Operation:
    payload: Dict[str, Any] = {
        "parent_author": parent_author,
        "parent_permlink": parent_permlink,
        "author": author,
        "permlink": permlink,
        "title": title,
        "body": body,
        "json_metadata": json_metadata,
    }
    return Operation("comment", payload)


def delete_comment(author: str, permlink: str) -> Operation:
    payload: Dict[str, Any] = {
        "author": author,
        "permlink": permlink,
    }
    return Operation("delete_comment", payload)


def custom_json(
    id: str,
    json_data: Any,
    required_auths: Optional[list] = None,
    required_posting_auths: Optional[list] = None,
) -> Operation:
    payload: Dict[str, Any] = {
        "id": id,
        "json": json_data,
        "required_auths": required_auths or [],
        "required_posting_auths": required_posting_auths or [],
    }
    return Operation("custom_json", payload)


def account_update(
    account: str,
    memo_key: str,
    owner: Optional[dict] = None,
    active: Optional[dict] = None,
    posting: Optional[dict] = None,
    json_metadata: Any = "",
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "account": account,
        "memo_key": memo_key,
        "json_metadata": json_metadata,
        "prefix": prefix,
    }
    if owner is not None:
        payload["owner"] = owner
    if active is not None:
        payload["active"] = active
    if posting is not None:
        payload["posting"] = posting
    return Operation("account_update", payload, prefix=prefix)


def claim_reward_balance(
    account: str,
    reward_blurt: str,
    reward_vests: str,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "account": account,
        "reward_blurt": reward_blurt,
        "reward_vests": reward_vests,
    }
    return Operation("claim_reward_balance", payload, prefix=prefix)


def create_proposal(
    creator: str,
    receiver: str,
    start_date: str,
    end_date: str,
    daily_pay: str,
    subject: str,
    permlink: str,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "creator": creator,
        "receiver": receiver,
        "start_date": start_date,
        "end_date": end_date,
        "daily_pay": daily_pay,
        "subject": subject,
        "permlink": permlink,
    }
    return Operation("create_proposal", payload, prefix=prefix)


def update_proposal_votes(
    voter: str,
    proposal_ids: list,
    approve: bool,
) -> Operation:
    payload: Dict[str, Any] = {
        "voter": voter,
        "proposal_ids": proposal_ids,
        "approve": bool(approve),
    }
    return Operation("update_proposal_votes", payload)


def remove_proposal(
    proposal_owner: str,
    proposal_ids: list,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "proposal_owner": proposal_owner,
        "proposal_ids": proposal_ids,
    }
    return Operation("remove_proposal", payload, prefix=prefix)


def update_proposal(
    proposal_id: int,
    creator: str,
    daily_pay: str,
    subject: str,
    permlink: str,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "proposal_id": int(proposal_id),
        "creator": creator,
        "daily_pay": daily_pay,
        "subject": subject,
        "permlink": permlink,
    }
    return Operation("update_proposal", payload, prefix=prefix)


def escrow_transfer(
    from_account: str,
    to_account: str,
    agent: str,
    escrow_id: int,
    blurt_amount: str,
    fee: str,
    ratification_deadline: str,
    escrow_expiration: str,
    json_meta: Any = "",
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "from": from_account,
        "to": to_account,
        "agent": agent,
        "escrow_id": int(escrow_id),
        "blurt_amount": blurt_amount,
        "fee": fee,
        "ratification_deadline": ratification_deadline,
        "escrow_expiration": escrow_expiration,
        "json_meta": json_meta,
    }
    return Operation("escrow_transfer", payload, prefix=prefix)


def escrow_dispute(
    from_account: str,
    to_account: str,
    who: str,
    escrow_id: int,
) -> Operation:
    payload: Dict[str, Any] = {
        "from": from_account,
        "to": to_account,
        "who": who,
        "escrow_id": int(escrow_id),
    }
    return Operation("escrow_dispute", payload)


def escrow_release(
    from_account: str,
    to_account: str,
    who: str,
    escrow_id: int,
    blurt_amount: str,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "from": from_account,
        "to": to_account,
        "who": who,
        "escrow_id": int(escrow_id),
        "blurt_amount": blurt_amount,
    }
    return Operation("escrow_release", payload, prefix=prefix)


def escrow_approve(
    from_account: str,
    to_account: str,
    agent: str,
    who: str,
    escrow_id: int,
    approve: bool,
) -> Operation:
    payload: Dict[str, Any] = {
        "from": from_account,
        "to": to_account,
        "agent": agent,
        "who": who,
        "escrow_id": int(escrow_id),
        "approve": bool(approve),
    }
    return Operation("escrow_approve", payload)


def witness_set_properties(
    owner: str,
    props: list,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "owner": owner,
        "props": props,
        "prefix": prefix,
    }
    return Operation("witness_set_properties", payload, prefix=prefix)


def witness_update(
    owner: str,
    url: str,
    block_signing_key: str,
    props: dict,
    fee: str,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "owner": owner,
        "url": url,
        "block_signing_key": block_signing_key,
        "props": props,
        "fee": fee,
        "prefix": prefix,
    }
    return Operation("witness_update", payload, prefix=prefix)




def change_recovery_account(account_to_recover: str, new_recovery_account: str) -> Operation:
    payload: Dict[str, Any] = {
        "account_to_recover": account_to_recover,
        "new_recovery_account": new_recovery_account,
    }
    return Operation("change_recovery_account", payload)


def request_account_recovery(
    recovery_account: str,
    account_to_recover: str,
    new_owner_authority: dict,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "recovery_account": recovery_account,
        "account_to_recover": account_to_recover,
        "new_owner_authority": new_owner_authority,
        "prefix": prefix,
    }
    return Operation("request_account_recovery", payload, prefix=prefix)


def recover_account(
    account_to_recover: str,
    new_owner_authority: dict,
    recent_owner_authority: dict,
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "account_to_recover": account_to_recover,
        "new_owner_authority": new_owner_authority,
        "recent_owner_authority": recent_owner_authority,
        "prefix": prefix,
    }
    return Operation("recover_account", payload, prefix=prefix)


def decline_voting_rights(account: str, decline: bool) -> Operation:
    payload: Dict[str, Any] = {
        "account": account,
        "decline": bool(decline),
    }
    return Operation("decline_voting_rights", payload)


def account_create(
    fee: str,
    creator: str,
    new_account_name: str,
    owner: dict,
    active: dict,
    posting: dict,
    memo_key: str,
    json_metadata: Any = "",
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "fee": fee,
        "creator": creator,
        "new_account_name": new_account_name,
        "owner": owner,
        "active": active,
        "posting": posting,
        "memo_key": memo_key,
        "json_metadata": json_metadata,
        "prefix": prefix,
    }
    return Operation("account_create", payload, prefix=prefix)


def account_create_with_delegation(
    fee: str,
    delegation: str,
    creator: str,
    new_account_name: str,
    owner: dict,
    active: dict,
    posting: dict,
    memo_key: str,
    json_metadata: Any = "",
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "fee": fee,
        "delegation": delegation,
        "creator": creator,
        "new_account_name": new_account_name,
        "owner": owner,
        "active": active,
        "posting": posting,
        "memo_key": memo_key,
        "json_metadata": json_metadata,
        "prefix": prefix,
    }
    return Operation("account_create_with_delegation", payload, prefix=prefix)


def claim_account(creator: str, fee: str, prefix: str = "BLURT") -> Operation:
    payload: Dict[str, Any] = {
        "creator": creator,
        "fee": fee,
        "prefix": prefix,
    }
    return Operation("claim_account", payload, prefix=prefix)


def create_claimed_account(
    creator: str,
    new_account_name: str,
    owner: dict,
    active: dict,
    posting: dict,
    memo_key: str,
    json_metadata: Any = "",
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "creator": creator,
        "new_account_name": new_account_name,
        "owner": owner,
        "active": active,
        "posting": posting,
        "memo_key": memo_key,
        "json_metadata": json_metadata,
        "prefix": prefix,
    }
    return Operation("create_claimed_account", payload, prefix=prefix)


def convert(owner: str, requestid: int, amount: str, prefix: str = "BLURT") -> Operation:
    payload: Dict[str, Any] = {
        "owner": owner,
        "requestid": int(requestid),
        "amount": amount,
        "prefix": prefix,
    }
    return Operation("convert", payload, prefix=prefix)


def set_withdraw_vesting_route(
    from_account: str,
    to_account: str,
    percent: int,
    auto_vest: bool,
) -> Operation:
    payload: Dict[str, Any] = {
        "from_account": from_account,
        "to_account": to_account,
        "percent": int(percent),
        "auto_vest": bool(auto_vest),
    }
    return Operation("set_withdraw_vesting_route", payload)


def custom_binary(id: int, data: str) -> Operation:
    payload: Dict[str, Any] = {
        "id": int(id),
        "data": data,
    }
    return Operation("custom_binary", payload)


def op_wrapper(op: dict, prefix: str = "BLURT") -> Operation:
    payload: Dict[str, Any] = {
        "op": op,
        "prefix": prefix,
    }
    return Operation("op_wrapper", payload, prefix=prefix)


def account_update2(
    account: str,
    owner: Optional[dict] = None,
    active: Optional[dict] = None,
    posting: Optional[dict] = None,
    memo_key: Optional[str] = None,
    json_metadata: Any = "",
    posting_json_metadata: Any = "",
    prefix: str = "BLURT",
) -> Operation:
    payload: Dict[str, Any] = {
        "account": account,
        "json_metadata": json_metadata,
        "posting_json_metadata": posting_json_metadata,
        "prefix": prefix,
    }
    if owner is not None:
        payload["owner"] = owner
    if active is not None:
        payload["active"] = active
    if posting is not None:
        payload["posting"] = posting
    if memo_key is not None:
        payload["memo_key"] = memo_key
    return Operation("account_update2", payload, prefix=prefix)
