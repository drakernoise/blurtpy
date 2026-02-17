import unittest
from datetime import datetime, timezone, timedelta

from blurtpyv2.client import Client


class DummyRpcClient:
    def __init__(self, urls, **kwargs):
        self.urls = urls
        self.calls = []

    def close(self):
        return None

    def get_account(self, name):
        return {
            "name": name,
            "voting_power": 9000,
            "last_vote_time": "2025-01-01T00:00:00",
        }

    def get_dynamic_global_properties(self):
        return {
            "head_block_number": 1,
            "head_block_id": "00" * 32,
        }

    def broadcast_transaction(self, tx):
        self.calls.append(("broadcast", tx))
        return {"tx": tx}


class TestV2Client(unittest.TestCase):
    def _make_client(self):
        client = Client("https://example.invalid")
        client.rpc = DummyRpcClient("https://example.invalid")
        return client

    def test_transfer_build(self):
        client = self._make_client()
        tx = client.transfer(
            "alice",
            "bob",
            "1.000 BLURT",
            memo="hi",
            broadcast=False,
        )
        self.assertIn("operations", tx)
        self.assertEqual(len(tx["operations"]), 1)

    def test_vote_build(self):
        client = self._make_client()
        tx = client.vote(
            "alice",
            "bob",
            "hello",
            10000,
            broadcast=False,
        )
        self.assertIn("operations", tx)
        self.assertEqual(len(tx["operations"]), 1)

    def test_power_up_build(self):
        client = self._make_client()
        tx = client.power_up("alice", "bob", "1.000 BLURT", broadcast=False)
        self.assertIn("operations", tx)

    def test_power_down_build(self):
        client = self._make_client()
        tx = client.power_down("alice", "1.000000 VESTS", broadcast=False)
        self.assertIn("operations", tx)

    def test_delegate_build(self):
        client = self._make_client()
        tx = client.delegate("alice", "bob", "1.000000 VESTS", broadcast=False)
        self.assertIn("operations", tx)

    def test_undelegate_build(self):
        client = self._make_client()
        tx = client.undelegate("alice", "bob", broadcast=False)
        self.assertIn("operations", tx)

    def test_witness_ops_build(self):
        client = self._make_client()
        tx1 = client.witness_vote("alice", "w1", True, broadcast=False)
        tx2 = client.witness_proxy("alice", "proxy", broadcast=False)
        self.assertIn("operations", tx1)
        self.assertIn("operations", tx2)

    def test_savings_ops_build(self):
        client = self._make_client()
        tx1 = client.transfer_to_savings("alice", "bob", "1.000 BLURT", memo="hi", broadcast=False)
        tx2 = client.transfer_from_savings("alice", 1, "bob", "1.000 BLURT", memo="hi", broadcast=False)
        tx3 = client.cancel_transfer_from_savings("alice", 1, broadcast=False)
        self.assertIn("operations", tx1)
        self.assertIn("operations", tx2)
        self.assertIn("operations", tx3)

    def test_social_ops_build(self):
        client = self._make_client()
        tx1 = client.comment("", "test", "alice", "p1", "t", "body", {"tags": ["x"]}, broadcast=False)
        tx2 = client.delete_comment("alice", "p1", broadcast=False)
        self.assertIn("operations", tx1)
        self.assertIn("operations", tx2)

    def test_custom_json_build(self):
        client = self._make_client()
        tx = client.custom_json("id", {"k": "v"}, required_posting_auths=["alice"], broadcast=False)
        self.assertIn("operations", tx)

    def test_account_ops_build(self):
        client = self._make_client()
        tx1 = client.account_update(
            "alice",
            "BLURT1111111111111111111111111111111114T1Anm",
            broadcast=False,
        )
        tx2 = client.claim_reward_balance(
            "alice",
            "1.000 BLURT",
            "1.000000 VESTS",
            broadcast=False,
        )
        self.assertIn("operations", tx1)
        self.assertIn("operations", tx2)

    def test_proposal_ops_build(self):
        client = self._make_client()
        tx1 = client.create_proposal(
            "alice",
            "bob",
            "2025-01-01T00:00:00",
            "2025-01-02T00:00:00",
            "1.000 BLURT",
            "subject",
            "permlink",
            broadcast=False,
        )
        tx2 = client.update_proposal_votes("alice", [1, 2], True, broadcast=False)
        tx3 = client.remove_proposal("alice", [1], broadcast=False)
        tx4 = client.update_proposal(1, "alice", "1.000 BLURT", "subject", "permlink", broadcast=False)
        self.assertIn("operations", tx1)
        self.assertIn("operations", tx2)
        self.assertIn("operations", tx3)
        self.assertIn("operations", tx4)

    def test_escrow_ops_build(self):
        client = self._make_client()
        tx1 = client.escrow_transfer(
            "alice",
            "bob",
            "agent",
            1,
            "1.000 BLURT",
            "0.010 BLURT",
            "2025-01-01T00:00:00",
            "2025-01-02T00:00:00",
            json_meta={"k": "v"},
            broadcast=False,
        )
        tx2 = client.escrow_dispute("alice", "bob", "alice", 1, broadcast=False)
        tx3 = client.escrow_release("alice", "bob", "alice", 1, "1.000 BLURT", broadcast=False)
        tx4 = client.escrow_approve("alice", "bob", "agent", "alice", 1, True, broadcast=False)
        self.assertIn("operations", tx1)
        self.assertIn("operations", tx2)
        self.assertIn("operations", tx3)
        self.assertIn("operations", tx4)

    def test_witness_ops_build(self):
        client = self._make_client()
        tx1 = client.witness_set_properties(
            "alice",
            [["key", "BLURT1111111111111111111111111111111114T1Anm"]],
            broadcast=False,
        )
        tx2 = client.witness_update(
            "alice",
            "https://example.com",
            "BLURT1111111111111111111111111111111114T1Anm",
            {"account_creation_fee": "1.000 BLURT", "maximum_block_size": 65536},
            "0.000 BLURT",
            broadcast=False,
        )
        self.assertIn("operations", tx1)
        self.assertIn("operations", tx2)

    def test_recovery_ops_build(self):
        client = self._make_client()
        tx1 = client.change_recovery_account("alice", "bob", broadcast=False)
        tx2 = client.request_account_recovery(
            "recovery",
            "alice",
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            broadcast=False,
        )
        tx3 = client.recover_account(
            "alice",
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            {"weight_threshold": 1, "account_auths": [], "key_auths": []},
            broadcast=False,
        )
        tx4 = client.decline_voting_rights("alice", True, broadcast=False)
        self.assertIn("operations", tx1)
        self.assertIn("operations", tx2)
        self.assertIn("operations", tx3)
        self.assertIn("operations", tx4)

    def test_account_create_ops_build(self):
        client = self._make_client()
        auth = {"weight_threshold": 1, "account_auths": [], "key_auths": []}
        tx1 = client.account_create(
            "1.000 BLURT",
            "creator",
            "newaccount",
            auth,
            auth,
            auth,
            "BLURT1111111111111111111111111111111114T1Anm",
            {"profile": {"name": "x"}},
            broadcast=False,
        )
        tx2 = client.account_create_with_delegation(
            "1.000 BLURT",
            "1.000000 VESTS",
            "creator",
            "newaccount",
            auth,
            auth,
            auth,
            "BLURT1111111111111111111111111111111114T1Anm",
            {"profile": {"name": "x"}},
            broadcast=False,
        )
        tx3 = client.claim_account("creator", "1.000 BLURT", broadcast=False)
        tx4 = client.create_claimed_account(
            "creator",
            "newaccount",
            auth,
            auth,
            auth,
            "BLURT1111111111111111111111111111111114T1Anm",
            {"profile": {"name": "x"}},
            broadcast=False,
        )
        tx5 = client.convert("alice", 1, "1.000 BLURT", broadcast=False)
        tx6 = client.set_withdraw_vesting_route("alice", "bob", 10000, True, broadcast=False)
        self.assertIn("operations", tx1)
        self.assertIn("operations", tx2)
        self.assertIn("operations", tx3)
        self.assertIn("operations", tx4)
        self.assertIn("operations", tx5)
        self.assertIn("operations", tx6)

    def test_misc_ops_build(self):
        client = self._make_client()
        tx1 = client.custom_binary(1, "deadbeef", broadcast=False)
        tx2 = client.op_wrapper({"type": "transfer"}, broadcast=False)
        tx3 = client.account_update2(
            "alice",
            memo_key="BLURT1111111111111111111111111111111114T1Anm",
            broadcast=False,
        )
        self.assertIn("operations", tx1)
        self.assertIn("operations", tx2)
        self.assertIn("operations", tx3)

    def test_estimate_voting_power(self):
        client = self._make_client()
        now = datetime(2025, 1, 2, tzinfo=timezone.utc)
        account = {
            "voting_power": 9000,
            "last_vote_time": "2025-01-01T00:00:00",
        }
        vp = client.estimate_voting_power(account, now=now, regen_seconds=432000)
        self.assertTrue(9000 < vp <= 10000)

    def test_get_voting_power_info(self):
        client = self._make_client()
        info = client.get_voting_power_info("alice")
        self.assertEqual(info["account"], "alice")
        self.assertIn("estimated_voting_power", info)

    def test_update_proposal_votes_min_vp(self):
        client = self._make_client()
        with self.assertRaises(ValueError):
            client.update_proposal_votes("alice", [1], True, min_voting_power=9500, broadcast=False)

    def test_vote_min_vp(self):
        client = self._make_client()
        with self.assertRaises(ValueError):
            client.vote("alice", "bob", "hello", 10000, min_voting_power=9500, broadcast=False)

    def test_comment_min_vp(self):
        client = self._make_client()
        with self.assertRaises(ValueError):
            client.comment(
                "",
                "test",
                "alice",
                "p1",
                "t",
                "body",
                {"tags": ["x"]},
                min_voting_power=9500,
                broadcast=False,
            )


if __name__ == "__main__":
    unittest.main()
