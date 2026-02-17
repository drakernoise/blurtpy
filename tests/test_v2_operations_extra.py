import unittest

from blurtpyv2.tx import (
    power_up,
    power_down,
    delegate_vesting_shares,
    undelegate_vesting_shares,
    witness_vote,
    witness_proxy,
    transfer_to_savings,
    transfer_from_savings,
    cancel_transfer_from_savings,
    comment,
    delete_comment,
    custom_json,
    account_update,
    claim_reward_balance,
    create_proposal,
    update_proposal_votes,
    remove_proposal,
    update_proposal,
    escrow_transfer,
    escrow_dispute,
    escrow_release,
    escrow_approve,
    witness_set_properties,
    witness_update,
    change_recovery_account,
    request_account_recovery,
    recover_account,
    decline_voting_rights,
    account_create,
    account_create_with_delegation,
    claim_account,
    create_claimed_account,
    convert,
    set_withdraw_vesting_route,
    custom_binary,
    op_wrapper,
    account_update2,
)


class TestV2OperationsExtra(unittest.TestCase):
    def test_power_up(self):
        op = power_up("alice", "bob", "1.000 BLURT")
        self.assertEqual(op[0], "transfer_to_vesting")

    def test_power_down(self):
        op = power_down("alice", "1.000000 VESTS")
        self.assertEqual(op[0], "withdraw_vesting")

    def test_delegate(self):
        op = delegate_vesting_shares("alice", "bob", "1.000000 VESTS")
        self.assertEqual(op[0], "delegate_vesting_shares")

    def test_undelegate(self):
        op = undelegate_vesting_shares("alice", "bob")
        self.assertEqual(op[0], "delegate_vesting_shares")

    def test_witness_vote(self):
        op = witness_vote("alice", "w1", True)
        self.assertEqual(op[0], "account_witness_vote")

    def test_witness_proxy(self):
        op = witness_proxy("alice", "proxy")
        self.assertEqual(op[0], "account_witness_proxy")

    def test_transfer_to_savings(self):
        op = transfer_to_savings("alice", "bob", "1.000 BLURT", memo="hi")
        self.assertEqual(op[0], "transfer_to_savings")

    def test_transfer_from_savings(self):
        op = transfer_from_savings("alice", 1, "bob", "1.000 BLURT", memo="hi")
        self.assertEqual(op[0], "transfer_from_savings")

    def test_cancel_transfer_from_savings(self):
        op = cancel_transfer_from_savings("alice", 1)
        self.assertEqual(op[0], "cancel_transfer_from_savings")

    def test_comment(self):
        op = comment("", "test", "alice", "p1", "t", "body", {"tags": ["x"]})
        self.assertEqual(op[0], "comment")

    def test_delete_comment(self):
        op = delete_comment("alice", "p1")
        self.assertEqual(op[0], "delete_comment")

    def test_custom_json(self):
        op = custom_json("id", {"k": "v"}, required_posting_auths=["alice"])
        self.assertEqual(op[0], "custom_json")

    def test_account_update(self):
        op = account_update("alice", "BLURT1111111111111111111111111111111114T1Anm")
        self.assertEqual(op[0], "account_update")

    def test_claim_reward_balance(self):
        op = claim_reward_balance("alice", "1.000 BLURT", "1.000000 VESTS")
        self.assertEqual(op[0], "claim_reward_balance")

    def test_create_proposal(self):
        op = create_proposal(
            "alice",
            "bob",
            "2025-01-01T00:00:00",
            "2025-01-02T00:00:00",
            "1.000 BLURT",
            "subject",
            "permlink",
        )
        self.assertEqual(op[0], "create_proposal")

    def test_update_proposal_votes(self):
        op = update_proposal_votes("alice", [1, 2], True)
        self.assertEqual(op[0], "update_proposal_votes")

    def test_remove_proposal(self):
        op = remove_proposal("alice", [1])
        self.assertEqual(op[0], "remove_proposal")

    def test_update_proposal(self):
        op = update_proposal(1, "alice", "1.000 BLURT", "subject", "permlink")
        self.assertEqual(op[0], "update_proposal")

    def test_escrow_transfer(self):
        op = escrow_transfer(
            "alice",
            "bob",
            "agent",
            1,
            "1.000 BLURT",
            "0.010 BLURT",
            "2025-01-01T00:00:00",
            "2025-01-02T00:00:00",
            json_meta={"k": "v"},
        )
        self.assertEqual(op[0], "escrow_transfer")

    def test_escrow_dispute(self):
        op = escrow_dispute("alice", "bob", "alice", 1)
        self.assertEqual(op[0], "escrow_dispute")

    def test_escrow_release(self):
        op = escrow_release("alice", "bob", "alice", 1, "1.000 BLURT")
        self.assertEqual(op[0], "escrow_release")

    def test_escrow_approve(self):
        op = escrow_approve("alice", "bob", "agent", "alice", 1, True)
        self.assertEqual(op[0], "escrow_approve")

    def test_witness_set_properties(self):
        op = witness_set_properties("alice", [["key", "BLURT1111111111111111111111111111111114T1Anm"]])
        self.assertEqual(op[0], "witness_set_properties")

    def test_witness_update(self):
        op = witness_update(
            "alice",
            "https://example.com",
            "BLURT1111111111111111111111111111111114T1Anm",
            {"account_creation_fee": "1.000 BLURT", "maximum_block_size": 65536},
            "0.000 BLURT",
        )
        self.assertEqual(op[0], "witness_update")


    def test_change_recovery_account(self):
        op = change_recovery_account("alice", "bob")
        self.assertEqual(op[0], "change_recovery_account")

    def test_request_account_recovery(self):
        op = request_account_recovery(
            "recovery",
            "alice",
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
        )
        self.assertEqual(op[0], "request_account_recovery")

    def test_recover_account(self):
        op = recover_account(
            "alice",
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
        )
        self.assertEqual(op[0], "recover_account")

    def test_decline_voting_rights(self):
        op = decline_voting_rights("alice", True)
        self.assertEqual(op[0], "decline_voting_rights")

    def test_account_create(self):
        op = account_create(
            "1.000 BLURT",
            "creator",
            "newaccount",
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            "BLURT1111111111111111111111111111111114T1Anm",
            {"profile": {"name": "x"}},
        )
        self.assertEqual(op[0], "account_create")

    def test_account_create_with_delegation(self):
        op = account_create_with_delegation(
            "1.000 BLURT",
            "1.000000 VESTS",
            "creator",
            "newaccount",
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            "BLURT1111111111111111111111111111111114T1Anm",
            {"profile": {"name": "x"}},
        )
        self.assertEqual(op[0], "account_create_with_delegation")

    def test_claim_account(self):
        op = claim_account("creator", "1.000 BLURT")
        self.assertEqual(op[0], "claim_account")

    def test_create_claimed_account(self):
        op = create_claimed_account(
            "creator",
            "newaccount",
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            "BLURT1111111111111111111111111111111114T1Anm",
            {"profile": {"name": "x"}},
        )
        self.assertEqual(op[0], "create_claimed_account")

    def test_convert(self):
        op = convert("alice", 1, "1.000 BLURT")
        self.assertEqual(op[0], "convert")

    def test_set_withdraw_vesting_route(self):
        op = set_withdraw_vesting_route("alice", "bob", 10000, True)
        self.assertEqual(op[0], "set_withdraw_vesting_route")

    def test_custom_binary(self):
        op = custom_binary(1, "deadbeef")
        self.assertEqual(op[0], "custom_binary")

    def test_op_wrapper(self):
        op = op_wrapper({"type": "transfer"})
        self.assertEqual(op[0], "op_wrapper")

    def test_account_update2(self):
        op = account_update2("alice", memo_key="BLURT1111111111111111111111111111111114T1Anm")
        self.assertEqual(op[0], "account_update2")


if __name__ == "__main__":
    unittest.main()
