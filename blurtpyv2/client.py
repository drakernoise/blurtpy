"""High-level V2 client."""

from __future__ import annotations

from typing import Any, Iterable, Optional
from datetime import datetime, timezone

from blurtpyv2.rpc import RpcClient
from blurtpyv2.tx import (
    TxBuilder,
    transfer as op_transfer,
    vote as op_vote,
    power_up as op_power_up,
    power_down as op_power_down,
    delegate_vesting_shares as op_delegate_vesting_shares,
    undelegate_vesting_shares as op_undelegate_vesting_shares,
    witness_vote as op_witness_vote,
    witness_proxy as op_witness_proxy,
    transfer_to_savings as op_transfer_to_savings,
    transfer_from_savings as op_transfer_from_savings,
    cancel_transfer_from_savings as op_cancel_transfer_from_savings,
    comment as op_comment,
    delete_comment as op_delete_comment,
    custom_json as op_custom_json,
    account_update as op_account_update,
    claim_reward_balance as op_claim_reward_balance,
    create_proposal as op_create_proposal,
    update_proposal_votes as op_update_proposal_votes,
    remove_proposal as op_remove_proposal,
    update_proposal as op_update_proposal,
    escrow_transfer as op_escrow_transfer,
    escrow_dispute as op_escrow_dispute,
    escrow_release as op_escrow_release,
    escrow_approve as op_escrow_approve,
    witness_set_properties as op_witness_set_properties,
    witness_update as op_witness_update,
    change_recovery_account as op_change_recovery_account,
    request_account_recovery as op_request_account_recovery,
    recover_account as op_recover_account,
    decline_voting_rights as op_decline_voting_rights,
    account_create as op_account_create,
    account_create_with_delegation as op_account_create_with_delegation,
    claim_account as op_claim_account,
    create_claimed_account as op_create_claimed_account,
    convert as op_convert,
    set_withdraw_vesting_route as op_set_withdraw_vesting_route,
    custom_binary as op_custom_binary,
    op_wrapper as op_op_wrapper,
    account_update2 as op_account_update2,
)
from blurtpyv2.wallet import Wallet


class Client:
    """V2 client combining RPC, TX builder and wallet."""

    def __init__(self, urls, wallet: Optional[Wallet] = None, chain: str = "BLURT", **kwargs):
        self.rpc = RpcClient(urls, **kwargs)
        self.wallet = wallet or Wallet()
        self.chain = chain

    def close(self) -> None:
        self.rpc.close()

    def get_account(self, name: str) -> Optional[dict]:
        return self.rpc.get_account(name)

    def estimate_voting_power(
        self,
        account: dict,
        now: Optional[datetime] = None,
        regen_seconds: int = 432000,
    ) -> int:
        """Estimate current voting power (0-10000) based on last_vote_time."""
        if account is None:
            raise ValueError("account is required")
        current = int(account.get("voting_power", 10000))
        last_vote_time = account.get("last_vote_time")
        if not last_vote_time:
            return min(10000, current)
        if now is None:
            now = datetime.now(timezone.utc)
        if isinstance(last_vote_time, str):
            try:
                last_vote_time = datetime.strptime(last_vote_time, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
            except ValueError:
                return min(10000, current)
        elif last_vote_time.tzinfo is None:
            last_vote_time = last_vote_time.replace(tzinfo=timezone.utc)
        delta = max(0, (now - last_vote_time).total_seconds())
        regenerated = int(delta * 10000 / regen_seconds)
        return min(10000, current + regenerated)

    def get_account_voting_power(self, name: str) -> int:
        account = self.get_account(name)
        return self.estimate_voting_power(account)

    def get_voting_power_info(self, name: str) -> dict:
        account = self.get_account(name)
        now = datetime.now(timezone.utc)
        current = int(account.get("voting_power", 10000))
        last_vote_time = account.get("last_vote_time")
        estimated = self.estimate_voting_power(account, now=now)
        return {
            "account": name,
            "current_voting_power": current,
            "estimated_voting_power": estimated,
            "last_vote_time": last_vote_time,
            "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S"),
            "regen_seconds": 432000,
        }

    def build_transfer(self, from_account: str, to_account: str, amount: str, memo: str = "") -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_transfer(from_account, to_account, amount, memo, prefix=self.chain))
        return builder

    def build_vote(self, voter: str, author: str, permlink: str, weight: int) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_vote(voter, author, permlink, weight, prefix=self.chain))
        return builder

    def build_power_up(self, from_account: str, to_account: str, amount: str) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_power_up(from_account, to_account, amount, prefix=self.chain))
        return builder

    def build_power_down(self, account: str, vesting_shares: str) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_power_down(account, vesting_shares, prefix=self.chain))
        return builder

    def build_delegate(self, delegator: str, delegatee: str, vesting_shares: str) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_delegate_vesting_shares(delegator, delegatee, vesting_shares, prefix=self.chain)
        )
        return builder

    def build_undelegate(self, delegator: str, delegatee: str) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_undelegate_vesting_shares(delegator, delegatee, prefix=self.chain))
        return builder

    def build_witness_vote(self, account: str, witness: str, approve: bool) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_witness_vote(account, witness, approve, prefix=self.chain))
        return builder

    def build_witness_proxy(self, account: str, proxy: str) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_witness_proxy(account, proxy, prefix=self.chain))
        return builder

    def build_transfer_to_savings(self, from_account: str, to_account: str, amount: str, memo: str = "") -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_transfer_to_savings(from_account, to_account, amount, memo, prefix=self.chain))
        return builder

    def build_transfer_from_savings(
        self,
        from_account: str,
        request_id: int,
        to_account: str,
        amount: str,
        memo: str = "",
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_transfer_from_savings(from_account, request_id, to_account, amount, memo, prefix=self.chain)
        )
        return builder

    def build_cancel_transfer_from_savings(self, from_account: str, request_id: int) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_cancel_transfer_from_savings(from_account, request_id, prefix=self.chain))
        return builder

    def build_comment(
        self,
        parent_author: str,
        parent_permlink: str,
        author: str,
        permlink: str,
        title: str,
        body: str,
        json_metadata: Any = "",
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_comment(parent_author, parent_permlink, author, permlink, title, body, json_metadata)
        )
        return builder

    def build_delete_comment(self, author: str, permlink: str) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_delete_comment(author, permlink))
        return builder

    def build_custom_json(
        self,
        id: str,
        json_data: Any,
        required_auths: Optional[Iterable[str]] = None,
        required_posting_auths: Optional[Iterable[str]] = None,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_custom_json(
                id,
                json_data,
                required_auths=list(required_auths or []),
                required_posting_auths=list(required_posting_auths or []),
            )
        )
        return builder

    def build_account_update(
        self,
        account: str,
        memo_key: str,
        owner: Optional[dict] = None,
        active: Optional[dict] = None,
        posting: Optional[dict] = None,
        json_metadata: Any = "",
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_account_update(
                account,
                memo_key,
                owner=owner,
                active=active,
                posting=posting,
                json_metadata=json_metadata,
                prefix=self.chain,
            )
        )
        return builder

    def build_claim_reward_balance(
        self,
        account: str,
        reward_blurt: str,
        reward_vests: str,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_claim_reward_balance(
                account,
                reward_blurt,
                reward_vests,
                prefix=self.chain,
            )
        )
        return builder

    def build_create_proposal(
        self,
        creator: str,
        receiver: str,
        start_date: str,
        end_date: str,
        daily_pay: str,
        subject: str,
        permlink: str,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_create_proposal(
                creator,
                receiver,
                start_date,
                end_date,
                daily_pay,
                subject,
                permlink,
                prefix=self.chain,
            )
        )
        return builder

    def build_update_proposal_votes(
        self,
        voter: str,
        proposal_ids: Iterable[int],
        approve: bool,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_update_proposal_votes(voter, list(proposal_ids), approve)
        )
        return builder

    def build_remove_proposal(self, proposal_owner: str, proposal_ids: Iterable[int]) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_remove_proposal(proposal_owner, list(proposal_ids), prefix=self.chain))
        return builder

    def build_update_proposal(
        self,
        proposal_id: int,
        creator: str,
        daily_pay: str,
        subject: str,
        permlink: str,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_update_proposal(proposal_id, creator, daily_pay, subject, permlink, prefix=self.chain)
        )
        return builder

    def build_escrow_transfer(
        self,
        from_account: str,
        to_account: str,
        agent: str,
        escrow_id: int,
        blurt_amount: str,
        fee: str,
        ratification_deadline: str,
        escrow_expiration: str,
        json_meta: Any = "",
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_escrow_transfer(
                from_account,
                to_account,
                agent,
                escrow_id,
                blurt_amount,
                fee,
                ratification_deadline,
                escrow_expiration,
                json_meta=json_meta,
                prefix=self.chain,
            )
        )
        return builder

    def build_escrow_dispute(
        self,
        from_account: str,
        to_account: str,
        who: str,
        escrow_id: int,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_escrow_dispute(from_account, to_account, who, escrow_id))
        return builder

    def build_escrow_release(
        self,
        from_account: str,
        to_account: str,
        who: str,
        escrow_id: int,
        blurt_amount: str,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_escrow_release(
                from_account,
                to_account,
                who,
                escrow_id,
                blurt_amount,
                prefix=self.chain,
            )
        )
        return builder

    def build_escrow_approve(
        self,
        from_account: str,
        to_account: str,
        agent: str,
        who: str,
        escrow_id: int,
        approve: bool,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_escrow_approve(from_account, to_account, agent, who, escrow_id, approve))
        return builder

    def build_witness_set_properties(self, owner: str, props: list) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_witness_set_properties(owner, props, prefix=self.chain))
        return builder

    def build_witness_update(
        self,
        owner: str,
        url: str,
        block_signing_key: str,
        props: dict,
        fee: str,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_witness_update(owner, url, block_signing_key, props, fee, prefix=self.chain))
        return builder


    def build_change_recovery_account(self, account_to_recover: str, new_recovery_account: str) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_change_recovery_account(account_to_recover, new_recovery_account))
        return builder

    def build_request_account_recovery(
        self,
        recovery_account: str,
        account_to_recover: str,
        new_owner_authority: dict,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_request_account_recovery(recovery_account, account_to_recover, new_owner_authority, prefix=self.chain)
        )
        return builder

    def build_recover_account(
        self,
        account_to_recover: str,
        new_owner_authority: dict,
        recent_owner_authority: dict,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_recover_account(
                account_to_recover,
                new_owner_authority,
                recent_owner_authority,
                prefix=self.chain,
            )
        )
        return builder

    def build_decline_voting_rights(self, account: str, decline: bool) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_decline_voting_rights(account, decline))
        return builder

    def build_account_create(
        self,
        fee: str,
        creator: str,
        new_account_name: str,
        owner: dict,
        active: dict,
        posting: dict,
        memo_key: str,
        json_metadata: Any = "",
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_account_create(
                fee,
                creator,
                new_account_name,
                owner,
                active,
                posting,
                memo_key,
                json_metadata=json_metadata,
                prefix=self.chain,
            )
        )
        return builder

    def build_account_create_with_delegation(
        self,
        fee: str,
        delegation: str,
        creator: str,
        new_account_name: str,
        owner: dict,
        active: dict,
        posting: dict,
        memo_key: str,
        json_metadata: Any = "",
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_account_create_with_delegation(
                fee,
                delegation,
                creator,
                new_account_name,
                owner,
                active,
                posting,
                memo_key,
                json_metadata=json_metadata,
                prefix=self.chain,
            )
        )
        return builder

    def build_claim_account(self, creator: str, fee: str) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_claim_account(creator, fee, prefix=self.chain))
        return builder

    def build_create_claimed_account(
        self,
        creator: str,
        new_account_name: str,
        owner: dict,
        active: dict,
        posting: dict,
        memo_key: str,
        json_metadata: Any = "",
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_create_claimed_account(
                creator,
                new_account_name,
                owner,
                active,
                posting,
                memo_key,
                json_metadata=json_metadata,
                prefix=self.chain,
            )
        )
        return builder

    def build_convert(self, owner: str, requestid: int, amount: str) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_convert(owner, requestid, amount, prefix=self.chain))
        return builder

    def build_set_withdraw_vesting_route(
        self,
        from_account: str,
        to_account: str,
        percent: int,
        auto_vest: bool,
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_set_withdraw_vesting_route(from_account, to_account, percent, auto_vest))
        return builder

    def build_custom_binary(self, id: int, data: str) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_custom_binary(id, data))
        return builder

    def build_op_wrapper(self, op: dict) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(op_op_wrapper(op, prefix=self.chain))
        return builder

    def build_account_update2(
        self,
        account: str,
        owner: Optional[dict] = None,
        active: Optional[dict] = None,
        posting: Optional[dict] = None,
        memo_key: Optional[str] = None,
        json_metadata: Any = "",
        posting_json_metadata: Any = "",
    ) -> TxBuilder:
        builder = TxBuilder(rpc=self.rpc)
        builder.add_operation(
            op_account_update2(
                account,
                owner=owner,
                active=active,
                posting=posting,
                memo_key=memo_key,
                json_metadata=json_metadata,
                posting_json_metadata=posting_json_metadata,
                prefix=self.chain,
            )
        )
        return builder

    def _sign_builder(
        self,
        builder: TxBuilder,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
    ) -> dict:
        if wif_keys:
            return builder.sign_with_wifs(wif_keys, chain=self.chain)
        if public_keys:
            return self.wallet.sign_transaction(builder, public_keys, chain=self.chain)
        return builder.build()

    def transfer(
        self,
        from_account: str,
        to_account: str,
        amount: str,
        memo: str = "",
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_transfer(from_account, to_account, amount, memo)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def vote(
        self,
        voter: str,
        author: str,
        permlink: str,
        weight: int,
        min_voting_power: Optional[int] = None,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        if min_voting_power is not None:
            current = self.get_account_voting_power(voter)
            if current < int(min_voting_power):
                raise ValueError("Insufficient voting power for vote")
        builder = self.build_vote(voter, author, permlink, weight)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def power_up(
        self,
        from_account: str,
        to_account: str,
        amount: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_power_up(from_account, to_account, amount)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def power_down(
        self,
        account: str,
        vesting_shares: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_power_down(account, vesting_shares)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def delegate(
        self,
        delegator: str,
        delegatee: str,
        vesting_shares: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_delegate(delegator, delegatee, vesting_shares)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def undelegate(
        self,
        delegator: str,
        delegatee: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_undelegate(delegator, delegatee)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def witness_vote(
        self,
        account: str,
        witness: str,
        approve: bool,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_witness_vote(account, witness, approve)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def witness_proxy(
        self,
        account: str,
        proxy: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_witness_proxy(account, proxy)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def transfer_to_savings(
        self,
        from_account: str,
        to_account: str,
        amount: str,
        memo: str = "",
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_transfer_to_savings(from_account, to_account, amount, memo)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def transfer_from_savings(
        self,
        from_account: str,
        request_id: int,
        to_account: str,
        amount: str,
        memo: str = "",
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_transfer_from_savings(from_account, request_id, to_account, amount, memo)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def cancel_transfer_from_savings(
        self,
        from_account: str,
        request_id: int,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_cancel_transfer_from_savings(from_account, request_id)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def comment(
        self,
        parent_author: str,
        parent_permlink: str,
        author: str,
        permlink: str,
        title: str,
        body: str,
        json_metadata: Any = "",
        min_voting_power: Optional[int] = None,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        if min_voting_power is not None:
            current = self.get_account_voting_power(author)
            if current < int(min_voting_power):
                raise ValueError("Insufficient voting power for comment")
        builder = self.build_comment(
            parent_author,
            parent_permlink,
            author,
            permlink,
            title,
            body,
            json_metadata,
        )
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def delete_comment(
        self,
        author: str,
        permlink: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_delete_comment(author, permlink)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def custom_json(
        self,
        id: str,
        json_data: Any,
        required_auths: Optional[Iterable[str]] = None,
        required_posting_auths: Optional[Iterable[str]] = None,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_custom_json(id, json_data, required_auths, required_posting_auths)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def account_update(
        self,
        account: str,
        memo_key: str,
        owner: Optional[dict] = None,
        active: Optional[dict] = None,
        posting: Optional[dict] = None,
        json_metadata: Any = "",
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_account_update(
            account,
            memo_key,
            owner=owner,
            active=active,
            posting=posting,
            json_metadata=json_metadata,
        )
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def claim_reward_balance(
        self,
        account: str,
        reward_blurt: str,
        reward_vests: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_claim_reward_balance(account, reward_blurt, reward_vests)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def create_proposal(
        self,
        creator: str,
        receiver: str,
        start_date: str,
        end_date: str,
        daily_pay: str,
        subject: str,
        permlink: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_create_proposal(
            creator,
            receiver,
            start_date,
            end_date,
            daily_pay,
            subject,
            permlink,
        )
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def update_proposal_votes(
        self,
        voter: str,
        proposal_ids: Iterable[int],
        approve: bool,
        min_voting_power: Optional[int] = None,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        if min_voting_power is not None:
            current = self.get_account_voting_power(voter)
            if current < int(min_voting_power):
                raise ValueError("Insufficient voting power for proposal vote")
        builder = self.build_update_proposal_votes(voter, proposal_ids, approve)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def remove_proposal(
        self,
        proposal_owner: str,
        proposal_ids: Iterable[int],
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_remove_proposal(proposal_owner, proposal_ids)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def update_proposal(
        self,
        proposal_id: int,
        creator: str,
        daily_pay: str,
        subject: str,
        permlink: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_update_proposal(proposal_id, creator, daily_pay, subject, permlink)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def escrow_transfer(
        self,
        from_account: str,
        to_account: str,
        agent: str,
        escrow_id: int,
        blurt_amount: str,
        fee: str,
        ratification_deadline: str,
        escrow_expiration: str,
        json_meta: Any = "",
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_escrow_transfer(
            from_account,
            to_account,
            agent,
            escrow_id,
            blurt_amount,
            fee,
            ratification_deadline,
            escrow_expiration,
            json_meta=json_meta,
        )
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def escrow_dispute(
        self,
        from_account: str,
        to_account: str,
        who: str,
        escrow_id: int,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_escrow_dispute(from_account, to_account, who, escrow_id)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def escrow_release(
        self,
        from_account: str,
        to_account: str,
        who: str,
        escrow_id: int,
        blurt_amount: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_escrow_release(
            from_account,
            to_account,
            who,
            escrow_id,
            blurt_amount,
        )
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def escrow_approve(
        self,
        from_account: str,
        to_account: str,
        agent: str,
        who: str,
        escrow_id: int,
        approve: bool,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_escrow_approve(from_account, to_account, agent, who, escrow_id, approve)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def witness_set_properties(
        self,
        owner: str,
        props: list,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_witness_set_properties(owner, props)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def witness_update(
        self,
        owner: str,
        url: str,
        block_signing_key: str,
        props: dict,
        fee: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_witness_update(owner, url, block_signing_key, props, fee)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx


    def change_recovery_account(
        self,
        account_to_recover: str,
        new_recovery_account: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_change_recovery_account(account_to_recover, new_recovery_account)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def request_account_recovery(
        self,
        recovery_account: str,
        account_to_recover: str,
        new_owner_authority: dict,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_request_account_recovery(recovery_account, account_to_recover, new_owner_authority)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def recover_account(
        self,
        account_to_recover: str,
        new_owner_authority: dict,
        recent_owner_authority: dict,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_recover_account(account_to_recover, new_owner_authority, recent_owner_authority)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def decline_voting_rights(
        self,
        account: str,
        decline: bool,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_decline_voting_rights(account, decline)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def account_create(
        self,
        fee: str,
        creator: str,
        new_account_name: str,
        owner: dict,
        active: dict,
        posting: dict,
        memo_key: str,
        json_metadata: Any = "",
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_account_create(
            fee,
            creator,
            new_account_name,
            owner,
            active,
            posting,
            memo_key,
            json_metadata=json_metadata,
        )
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def account_create_with_delegation(
        self,
        fee: str,
        delegation: str,
        creator: str,
        new_account_name: str,
        owner: dict,
        active: dict,
        posting: dict,
        memo_key: str,
        json_metadata: Any = "",
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_account_create_with_delegation(
            fee,
            delegation,
            creator,
            new_account_name,
            owner,
            active,
            posting,
            memo_key,
            json_metadata=json_metadata,
        )
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def claim_account(
        self,
        creator: str,
        fee: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_claim_account(creator, fee)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def create_claimed_account(
        self,
        creator: str,
        new_account_name: str,
        owner: dict,
        active: dict,
        posting: dict,
        memo_key: str,
        json_metadata: Any = "",
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_create_claimed_account(
            creator,
            new_account_name,
            owner,
            active,
            posting,
            memo_key,
            json_metadata=json_metadata,
        )
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def convert(
        self,
        owner: str,
        requestid: int,
        amount: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_convert(owner, requestid, amount)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def set_withdraw_vesting_route(
        self,
        from_account: str,
        to_account: str,
        percent: int,
        auto_vest: bool,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_set_withdraw_vesting_route(from_account, to_account, percent, auto_vest)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def custom_binary(
        self,
        id: int,
        data: str,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_custom_binary(id, data)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def op_wrapper(
        self,
        op: dict,
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_op_wrapper(op)
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx

    def account_update2(
        self,
        account: str,
        owner: Optional[dict] = None,
        active: Optional[dict] = None,
        posting: Optional[dict] = None,
        memo_key: Optional[str] = None,
        json_metadata: Any = "",
        posting_json_metadata: Any = "",
        wif_keys: Optional[Iterable[str]] = None,
        public_keys: Optional[Iterable[Any]] = None,
        broadcast: bool = True,
    ) -> Any:
        builder = self.build_account_update2(
            account,
            owner=owner,
            active=active,
            posting=posting,
            memo_key=memo_key,
            json_metadata=json_metadata,
            posting_json_metadata=posting_json_metadata,
        )
        tx = self._sign_builder(builder, wif_keys=wif_keys, public_keys=public_keys)
        return self.rpc.broadcast_transaction(tx) if broadcast else tx
