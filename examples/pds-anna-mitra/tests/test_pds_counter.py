#!/usr/bin/env python3
"""End-to-end integration tests for PDS Anna-Mitra Counter Prototype.

Covers:
- Database initialization and deterministic card seeding.
- Statutory NFSA PMGKAY quota calculation (AAY 35 kg / PHH 5 kg per member) vs Karnataka 2026-27 state add-ons.
- Two-tap dispense latency and transaction persistence across database disconnects/restarts.
- Tamper detection via SHA-256 hash chaining and HMAC signature verification.
- Clock rollback prevention.
- Multi-terminal split-brain duplicate card drawal detection.
- Zero-PII regional audio dialogue generation in Kannada and Hindi.
"""
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP_DIR = HERE.parent / "app"
sys.path.insert(0, str(APP_DIR))

from pds_counter import (  # noqa: E402
    calculate_entitlements,
    format_receipt_slip,
    generate_ivr_dialog,
    get_db,
    init_database,
    record_transaction,
    run_verify,
)
from crypto_core import reconcile_batch_logs  # noqa: E402


class TestPDSCounterIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_fps.db"
        self.conn = get_db(self.db_path)
        init_database(self.conn, dealer_id="FPS-TEST-TALUK-01")

    def tearDown(self):
        self.conn.close()
        self.temp_dir.cleanup()

    def test_database_seeding(self):
        cur = self.conn.execute("SELECT COUNT(*) as c FROM beneficiary_cards")
        count = cur.fetchone()["c"]
        self.assertEqual(count, 6)

        cur = self.conn.execute("SELECT * FROM shop_metadata WHERE key = 'dealer_id'")
        self.assertEqual(cur.fetchone()["value"], "FPS-TEST-TALUK-01")

    def test_quota_calculation_aay(self):
        cur = self.conn.execute("SELECT * FROM beneficiary_cards WHERE card_id = 'KA-BLR-AAY-1001'")
        card_row = cur.fetchone()
        ent = calculate_entitlements(card_row)

        self.assertEqual(ent["scheme"], "AAY")
        self.assertEqual(ent["central_nfsa"]["rice_kg"], 35.0)
        self.assertEqual(ent["central_nfsa"]["cost_inr"], 0.0)
        self.assertEqual(ent["state_addon"]["subsidized_dal_kg"], 1.0)
        self.assertEqual(ent["total_cash_payable_inr"], 25.0)

    def test_quota_calculation_phh(self):
        # 4 members: 4 * 5 = 20 kg free rice
        cur = self.conn.execute("SELECT * FROM beneficiary_cards WHERE card_id = 'KA-BLR-PHH-1002'")
        card_row = cur.fetchone()
        ent = calculate_entitlements(card_row)

        self.assertEqual(ent["scheme"], "PHH")
        self.assertEqual(ent["member_count"], 4)
        self.assertEqual(ent["central_nfsa"]["rice_kg"], 20.0)
        self.assertEqual(ent["central_nfsa"]["cost_inr"], 0.0)
        self.assertEqual(ent["state_addon"]["dbt_cash_inr"], 680.0)  # 4 * 170 INR
        self.assertEqual(ent["state_addon"]["subsidized_dal_kg"], 1.0)
        self.assertEqual(ent["total_cash_payable_inr"], 25.0)

    def test_quota_calculation_nphh(self):
        cur = self.conn.execute("SELECT * FROM beneficiary_cards WHERE card_id = 'KA-BLR-NPHH-2001'")
        card_row = cur.fetchone()
        ent = calculate_entitlements(card_row)

        self.assertEqual(ent["scheme"], "NPHH")
        self.assertEqual(ent["central_nfsa"]["rice_kg"], 0.0)
        self.assertEqual(ent["central_nfsa"]["cost_inr"], 0.0)
        self.assertEqual(ent["total_cash_payable_inr"], 0.0)

    def test_two_tap_dispense_and_persistence_across_restart(self):
        # Tap 1 & 2: Dispense transaction
        tx1 = record_transaction(self.conn, "KA-BLR-PHH-1002", timestamp_override="2026-11-03T10:00:00Z")
        self.assertEqual(tx1["seq"], 1)
        self.assertEqual(tx1["items"]["rice_kg"], 20.0)

        tx2 = record_transaction(self.conn, "KA-BLR-PHH-1003", timestamp_override="2026-11-03T10:01:00Z")
        self.assertEqual(tx2["seq"], 2)
        self.assertEqual(tx2["prev_hash"], tx1["hash"])

        receipt_text = format_receipt_slip(tx1)
        self.assertIn("COMMODITY DISPENSATION SUMMARY", receipt_text)
        self.assertIn("Central Rice (PMGKAY):  20.0 kg  [100% FREE]", receipt_text)

        # Simulate system shutdown / restart: close connection and open brand new one
        self.conn.close()
        new_conn = get_db(self.db_path)

        valid, msg = run_verify(new_conn)
        self.assertTrue(valid, msg)

        cur = new_conn.execute("SELECT COUNT(*) as c FROM offline_transactions")
        self.assertEqual(cur.fetchone()["c"], 2)
        new_conn.close()
        # Re-attach for tearDown
        self.conn = get_db(self.db_path)

    def test_tamper_detection_sql_update(self):
        record_transaction(self.conn, "KA-BLR-PHH-1002", timestamp_override="2026-11-03T10:00:00Z")
        record_transaction(self.conn, "KA-BLR-PHH-1003", timestamp_override="2026-11-03T10:01:00Z")
        record_transaction(self.conn, "KA-BLR-PHH-1004", timestamp_override="2026-11-03T10:02:00Z")

        # Rogue dealer alters row 2 items from 10 kg to 5 kg to divert grain
        tampered_items = json.dumps({"rice_kg": 5.0, "state_dal_kg": 1.0, "wheat_kg": 0.0}, sort_keys=True)
        self.conn.execute("UPDATE offline_transactions SET items_json = ? WHERE seq = 2", (tampered_items,))
        self.conn.commit()

        valid, msg = run_verify(self.conn)
        self.assertFalse(valid)
        self.assertIn("Tampered record payload at row 2", msg)

    def test_clock_rollback_rejection(self):
        record_transaction(self.conn, "KA-BLR-PHH-1002", timestamp_override="2026-11-03T10:15:00Z")

        # Attempt to insert record with rolled-back clock
        with self.assertRaises(ValueError) as ctx:
            record_transaction(self.conn, "KA-BLR-PHH-1003", timestamp_override="2026-11-03T10:10:00Z")
        self.assertIn("Clock rollback violation", str(ctx.exception))

    def test_multi_terminal_reconciliation_conflict(self):
        # Create second database representing Shop B in neighboring village
        db_b_path = Path(self.temp_dir.name) / "shop_b.db"
        conn_b = get_db(db_b_path)
        init_database(conn_b, dealer_id="FPS-TEST-TALUK-02")

        # Beneficiary KA-BLR-PHH-1002 draws quota at Shop A at 10:00
        tx_a = record_transaction(self.conn, "KA-BLR-PHH-1002", timestamp_override="2026-11-03T10:00:00Z")

        # Same beneficiary travels to Shop B and draws quota again while Shop B is offline at 11:30
        tx_b = record_transaction(conn_b, "KA-BLR-PHH-1002", timestamp_override="2026-11-03T11:30:00Z")

        conn_b.close()

        # Central sync reconciliation
        batches = [
            [{
                "seq": tx_a["seq"],
                "prev_hash": tx_a["prev_hash"],
                "timestamp": tx_a["timestamp"],
                "card_id": tx_a["card_id"],
                "items": tx_a["items"],
                "dealer_id": tx_a["dealer_id"],
                "hash": tx_a["hash"],
                "signature": tx_a["signature"],
                "key_version": tx_a["key_version"]
            }],
            [{
                "seq": tx_b["seq"],
                "prev_hash": tx_b["prev_hash"],
                "timestamp": tx_b["timestamp"],
                "card_id": tx_b["card_id"],
                "items": tx_b["items"],
                "dealer_id": tx_b["dealer_id"],
                "hash": tx_b["hash"],
                "signature": tx_b["signature"],
                "key_version": tx_b["key_version"]
            }]
        ]

        accepted, conflicts = reconcile_batch_logs(batches)
        self.assertEqual(len(accepted), 1)
        self.assertEqual(len(conflicts), 1)
        self.assertEqual(conflicts[0]["type"], "CONFLICT_DUPLICATE_OFFLINE_DRAWAL")
        self.assertEqual(conflicts[0]["card_id"], "KA-BLR-PHH-1002")
        self.assertEqual(conflicts[0]["original_tx"]["dealer_id"], "FPS-TEST-TALUK-01")
        self.assertEqual(conflicts[0]["conflicting_tx"]["dealer_id"], "FPS-TEST-TALUK-02")

    def test_zero_pii_voice_dialogue(self):
        cur = self.conn.execute("SELECT * FROM beneficiary_cards WHERE card_id = 'KA-BLR-PHH-1002'")
        card_row = cur.fetchone()

        kn_dialog = generate_ivr_dialog(card_row, lang="kn")
        hi_dialog = generate_ivr_dialog(card_row, lang="hi")

        # Zero PII check: no citizen names, no Aadhaar numbers
        self.assertNotIn("Kenchaiah", kn_dialog["spoken_audio_script"])
        self.assertNotIn("Ratnamma", kn_dialog["spoken_audio_script"])
        self.assertNotIn("Aadhaar", kn_dialog["spoken_audio_script"])
        self.assertNotIn("Kenchaiah", hi_dialog["spoken_audio_script"])

        # Quota numbers check
        self.assertIn("ಇಪ್ಪತ್ತು ಕಿಲೋಗ್ರಾಂ — ಉಚಿತ", kn_dialog["spoken_audio_script"])
        self.assertIn("बीस किलोग्राम — बिल्कुल मुफ़्त", hi_dialog["spoken_audio_script"])

    def test_negative_commodity_quantity_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            record_transaction(self.conn, "KA-BLR-PHH-1002", custom_items={"rice_kg": -10.0, "wheat_kg": 0.0, "state_dal_kg": 1.0})
        self.assertIn("Quantities must be non-negative", str(ctx.exception))

    def test_future_timestamp_beyond_horizon_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            record_transaction(self.conn, "KA-BLR-PHH-1002", timestamp_override="2099-01-01T00:00:00Z")
        self.assertIn("exceeds operational horizon", str(ctx.exception))

    def test_invalid_iso_timestamp_format_rejected(self):
        with self.assertRaises(ValueError) as ctx:
            record_transaction(self.conn, "KA-BLR-PHH-1002", timestamp_override="INVALID_TIMESTAMP")
        self.assertIn("Invalid ISO-8601 timestamp format", str(ctx.exception))

    def test_sql_injection_attempt_in_card_id(self):
        malicious_input = "KA-BLR-PHH-1002' OR '1'='1"
        with self.assertRaises(ValueError) as ctx:
            record_transaction(self.conn, malicious_input)
        self.assertIn("not found in local offline database", str(ctx.exception))

    def test_interrupted_transaction_atomicity(self):
        # Verify that if an exception occurs mid-transaction, no partial record is committed
        cur = self.conn.execute("SELECT COUNT(*) as c FROM offline_transactions")
        initial_count = cur.fetchone()["c"]

        try:
            # Trigger failure with invalid custom items
            record_transaction(self.conn, "KA-BLR-PHH-1002", custom_items={"rice_kg": -50.0})
        except ValueError:
            pass

        cur = self.conn.execute("SELECT COUNT(*) as c FROM offline_transactions")
        self.assertEqual(cur.fetchone()["c"], initial_count)


class TestMonthlyEntitlementGuard(unittest.TestCase):
    """Added after Demo Day Court 1 found repeat and 500 kg dispenses were accepted."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.conn = get_db(Path(self.tmp.name) / "guard.db")
        init_database(self.conn, dealer_id="FPS-TEST-TALUK-01")

    def tearDown(self):
        self.conn.close()
        self.tmp.cleanup()

    def test_second_full_dispense_same_month_is_blocked(self):
        record_transaction(self.conn, "KA-BLR-PHH-1002", timestamp_override="2026-11-05T09:00:00Z")
        with self.assertRaises(ValueError):
            record_transaction(self.conn, "KA-BLR-PHH-1002", timestamp_override="2026-11-06T09:00:00Z")

    def test_next_month_is_allowed(self):
        record_transaction(self.conn, "KA-BLR-PHH-1002", timestamp_override="2026-11-05T09:00:00Z")
        record_transaction(self.conn, "KA-BLR-PHH-1002", timestamp_override="2026-12-02T09:00:00Z")

    def test_quantity_above_entitlement_is_blocked(self):
        with self.assertRaises(ValueError):
            record_transaction(self.conn, "KA-BLR-PHH-1002", custom_items={"rice_kg": 500.0},
                               timestamp_override="2026-11-05T09:00:00Z")

    def test_partial_drawals_up_to_the_limit_are_allowed(self):
        record_transaction(self.conn, "KA-BLR-PHH-1002", custom_items={"rice_kg": 10.0},
                           timestamp_override="2026-11-05T09:00:00Z")
        record_transaction(self.conn, "KA-BLR-PHH-1002", custom_items={"rice_kg": 10.0},
                           timestamp_override="2026-11-06T09:00:00Z")
        with self.assertRaises(ValueError):
            record_transaction(self.conn, "KA-BLR-PHH-1002", custom_items={"rice_kg": 1.0},
                               timestamp_override="2026-11-07T09:00:00Z")


if __name__ == "__main__":
    unittest.main()
