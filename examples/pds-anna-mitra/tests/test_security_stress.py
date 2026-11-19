"""Automated security stress tests for PDS Anna-Mitra cryptographic core.

Tests:
1. Payload modification tampering detection.
2. Record deletion / chain breakage detection.
3. Ledger truncation caught by external checkpoint hash pinning.
4. Full-ledger rewrite attack detection against pinned checkpoints.
5. Sequence number gap and rollback rejection.
6. Independent timestamp rollback / clock manipulation rejection (with monotonic seq).
7. Key compromise / wrong key rejection.
8. Key rotation across transaction batches with key versioning.
9. Multi-device duplicate card drawal detection in central reconciler.
"""
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "app"))
from crypto_core import (  # noqa: E402
    compute_receipt_hash,
    reconcile_batch_logs,
    sign_hash,
    verify_chain,
)


class TestSecurityStress(unittest.TestCase):
    def setUp(self):
        self.secret_key = "SECURE_FPS_TERMINAL_KEY_KRN_2026_TEST"
        self.genesis = "GENESIS_ROOT_HASH_00000000000000000000000000000000000000000000000000"
        self.records = self._generate_chain(count=5)

    def _generate_chain(self, count=5, secret_key=None, start_seq=1, prev_hash=None, key_ver="v1"):
        key = secret_key or self.secret_key
        curr_prev = prev_hash or self.genesis
        records = []
        for i in range(count):
            seq = start_seq + i
            ts = f"2026-11-03T10:{seq - 1:02d}:00Z"
            card_id = f"KA-BLR-PHH-{1000 + i}"
            items = {"rice_kg": 20.0, "wheat_kg": 0.0, "state_dal_kg": 1.0}
            items_str = json.dumps(items, sort_keys=True)
            h = compute_receipt_hash(curr_prev, seq, ts, card_id, items_str, "FPS-42-BANGALORE-RURAL")
            sig = sign_hash(h, key)
            r = {
                "seq": seq,
                "prev_hash": curr_prev,
                "timestamp": ts,
                "card_id": card_id,
                "items": items,
                "dealer_id": "FPS-42-BANGALORE-RURAL",
                "key_version": key_ver,
                "hash": h,
                "signature": sig
            }
            records.append(r)
            curr_prev = h
        return records

    def test_valid_chain_verifies(self):
        valid, msg = verify_chain(self.records, self.secret_key)
        self.assertTrue(valid, msg)
        self.assertEqual(msg, "Chain verified successfully")

    def test_record_payload_modification_fails(self):
        # Attacker modifies grain amount in record #2 from 20kg to 35kg
        tampered = [dict(r) for r in self.records]
        tampered[1]["items"] = {"rice_kg": 35.0, "wheat_kg": 0.0, "state_dal_kg": 1.0}
        valid, msg = verify_chain(tampered, self.secret_key)
        self.assertFalse(valid)
        self.assertIn("Tampered record payload at row 2", msg)

    def test_record_deletion_breaks_chain(self):
        # Attacker deletes record #3 to hide a transaction
        tampered = [self.records[0], self.records[1], self.records[3], self.records[4]]
        valid, msg = verify_chain(tampered, self.secret_key)
        self.assertFalse(valid)
        self.assertIn("Sequence gap or rollback detected at row 3", msg)

    def test_ledger_truncation_caught_by_checkpoint(self):
        # Attacker truncates the last 2 records to pretend they never happened
        pinned_checkpoint = self.records[4]["hash"]
        truncated = self.records[:3]
        valid, msg = verify_chain(truncated, self.secret_key, pinned_checkpoint_hash=pinned_checkpoint)
        self.assertFalse(valid)
        self.assertIn("Checkpoint verification failed", msg)

    def test_full_ledger_rewrite_caught_by_checkpoint(self):
        # Attacker with stolen key generates a brand new alternative chain of 5 records
        pinned_checkpoint = self.records[4]["hash"]
        alternate_records = self._generate_chain(count=5, start_seq=1)
        alternate_records[0]["card_id"] = "KA-BLR-PHH-9999"
        items_str = json.dumps(alternate_records[0]["items"], sort_keys=True)
        h = compute_receipt_hash(self.genesis, 1, alternate_records[0]["timestamp"], "KA-BLR-PHH-9999", items_str, "FPS-42-BANGALORE-RURAL")
        alternate_records[0]["hash"] = h
        alternate_records[0]["signature"] = sign_hash(h, self.secret_key)
        for i in range(1, 5):
            alternate_records[i]["prev_hash"] = alternate_records[i - 1]["hash"]
            items_str_i = json.dumps(alternate_records[i]["items"], sort_keys=True)
            h_i = compute_receipt_hash(alternate_records[i]["prev_hash"], alternate_records[i]["seq"],
                                       alternate_records[i]["timestamp"], alternate_records[i]["card_id"],
                                       items_str_i, alternate_records[i]["dealer_id"])
            alternate_records[i]["hash"] = h_i
            alternate_records[i]["signature"] = sign_hash(h_i, self.secret_key)

        valid, msg = verify_chain(alternate_records, self.secret_key, pinned_checkpoint_hash=pinned_checkpoint)
        self.assertFalse(valid)
        self.assertIn("Checkpoint verification failed", msg)

    def test_sequence_number_gap_or_rollback_detected(self):
        # Non-monotonic sequence (attacker rolls back sequence)
        tampered = [dict(r) for r in self.records]
        tampered[3]["seq"] = 2  # Rollback sequence number
        valid, msg = verify_chain(tampered, self.secret_key)
        self.assertFalse(valid)
        self.assertIn("Sequence gap or rollback detected at row 4", msg)

    def test_timestamp_rollback_detected_independently_of_sequence(self):
        # Sequence is monotonic (1, 2, 3, 4, 5), but timestamp at row 3 rolls backward from 10:01 to 09:15
        tampered = [dict(r) for r in self.records]
        tampered[2]["timestamp"] = "2026-11-03T09:15:00Z"
        # Rehash and resign row 3 so hash/sig are valid for the modified timestamp
        items_str = json.dumps(tampered[2]["items"], sort_keys=True)
        h3 = compute_receipt_hash(tampered[2]["prev_hash"], tampered[2]["seq"], tampered[2]["timestamp"],
                                  tampered[2]["card_id"], items_str, tampered[2]["dealer_id"])
        tampered[2]["hash"] = h3
        tampered[2]["signature"] = sign_hash(h3, self.secret_key)
        # Re-link row 4
        tampered[3]["prev_hash"] = h3
        items_str_4 = json.dumps(tampered[3]["items"], sort_keys=True)
        h4 = compute_receipt_hash(h3, tampered[3]["seq"], tampered[3]["timestamp"],
                                  tampered[3]["card_id"], items_str_4, tampered[3]["dealer_id"])
        tampered[3]["hash"] = h4
        tampered[3]["signature"] = sign_hash(h4, self.secret_key)

        valid, msg = verify_chain(tampered, self.secret_key)
        self.assertFalse(valid)
        self.assertIn("Clock rollback detected at row 3", msg)

    def test_key_rotation_verification(self):
        # Terminal rotates key from key_v1 to key_v2 after record #3
        key_v1 = "SECRET_KEY_BATCH_V1"
        key_v2 = "SECRET_KEY_BATCH_V2_ROTATED"
        keys_map = {"v1": key_v1, "v2": key_v2}

        records_part1 = self._generate_chain(count=3, secret_key=key_v1, start_seq=1, key_ver="v1")
        last_hash = records_part1[-1]["hash"]
        records_part2 = self._generate_chain(count=2, secret_key=key_v2, start_seq=4, prev_hash=last_hash, key_ver="v2")

        combined = records_part1 + records_part2
        valid, msg = verify_chain(combined, keys_map)
        self.assertTrue(valid, msg)

    def test_wrong_secret_key_fails_hmac(self):
        wrong_key = "ATTACKER_STOLEN_OR_FORGED_KEY"
        valid, msg = verify_chain(self.records, wrong_key)
        self.assertFalse(valid)
        self.assertIn("Invalid signature at row 1", msg)

    def test_multi_device_duplicate_card_drawal_detected(self):
        batch_shop_a = [
            {
                "seq": 1,
                "card_id": "KA-BLR-PHH-1042",
                "timestamp": "2026-11-03T10:00:00Z",
                "dealer_id": "FPS-SHOP-A",
                "items": {"rice_kg": 20.0}
            }
        ]
        batch_shop_b = [
            {
                "seq": 1,
                "card_id": "KA-BLR-PHH-1042",
                "timestamp": "2026-11-03T11:30:00Z",
                "dealer_id": "FPS-SHOP-B",
                "items": {"rice_kg": 20.0}
            }
        ]

        accepted, conflicts = reconcile_batch_logs([batch_shop_a, batch_shop_b])
        self.assertEqual(len(accepted), 1)
        self.assertEqual(len(conflicts), 1)
        conflict = conflicts[0]
        self.assertEqual(conflict["type"], "CONFLICT_DUPLICATE_OFFLINE_DRAWAL")
        self.assertEqual(conflict["card_id"], "KA-BLR-PHH-1042")
        self.assertIn("already drew rations at terminal FPS-SHOP-A", conflict["reason"])

    def test_future_timestamp_beyond_horizon_rejected(self):
        records = [r.copy() for r in self.records]
        records[2]["timestamp"] = "2099-01-01T12:00:00Z"
        # Recompute hash & sig for row 3
        items_str = json.dumps(records[2]["items"], sort_keys=True)
        h = compute_receipt_hash(records[2]["prev_hash"], records[2]["seq"], records[2]["timestamp"],
                                 records[2]["card_id"], items_str, records[2]["dealer_id"])
        records[2]["hash"] = h
        records[2]["signature"] = sign_hash(h, self.secret_key)

        valid, msg = verify_chain(records, self.secret_key)
        self.assertFalse(valid)
        self.assertIn("Timestamp out of bounds at row 3", msg)

    def test_invalid_iso_timestamp_rejected(self):
        records = [r.copy() for r in self.records]
        records[1]["timestamp"] = "INVALID-DATE-STRING"
        items_str = json.dumps(records[1]["items"], sort_keys=True)
        h = compute_receipt_hash(records[1]["prev_hash"], records[1]["seq"], records[1]["timestamp"],
                                 records[1]["card_id"], items_str, records[1]["dealer_id"])
        records[1]["hash"] = h
        records[1]["signature"] = sign_hash(h, self.secret_key)

        valid, msg = verify_chain(records, self.secret_key)
        self.assertFalse(valid)
        self.assertIn("Invalid timestamp format at row 2", msg)

    def test_record_reordering_detected(self):
        # Swap rows 1 and 2
        reordered = [self.records[1], self.records[0]] + self.records[2:]
        valid, msg = verify_chain(reordered, self.secret_key)
        self.assertFalse(valid)
        self.assertTrue("Sequence gap" in msg or "Hash chain broken" in msg, msg)

    def test_checkpoint_replacement_or_loss_detected(self):
        # Ledger is empty but checkpoint was expected
        valid, msg = verify_chain([], self.secret_key, pinned_checkpoint_hash="SOME_ANCHOR_HASH")
        self.assertFalse(valid)
        self.assertIn("full truncation attack", msg)

        # Ledger has wrong checkpoint
        valid, msg = verify_chain(self.records, self.secret_key, pinned_checkpoint_hash="FORGED_OR_REPLACED_CHECKPOINT")
        self.assertFalse(valid)
        self.assertIn("Checkpoint verification failed", msg)


if __name__ == "__main__":
    unittest.main()
