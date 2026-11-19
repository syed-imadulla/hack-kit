#!/usr/bin/env python3
"""PDS Anna-Mitra — Fair Price Shop Offline Counter & Audit CLI Prototype.

Demonstrates:
- Decoupled Central NFSA (PMGKAY free through 2028) vs Karnataka 2026-27 state add-ons.
- Two-tap fast offline transaction recording in SQLite (< 15 milliseconds).
- SHA-256 hash chaining + HMAC-SHA256 signing with key rotation support.
- Monotonic clock rollback detection and tamper audit via 'verify-chain'.
- Multi-device split-brain conflict detection upon central reconciliation via 'reconcile'.
- Zero-PII regional voice dialogue generation in spoken Kannada and Hindi.
"""
import argparse
import datetime
import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from crypto_core import (  # noqa: E402
    compute_receipt_hash,
    reconcile_batch_logs,
    sign_hash,
    verify_chain,
)

DEFAULT_DB_PATH = HERE.parent / "pds_counter.db"
GENESIS_HASH = "GENESIS_ROOT_HASH_00000000000000000000000000000000000000000000000000"

DEFAULT_KEYS_MAP = {
    "v1": "SECURE_FPS_TERMINAL_KEY_KRN_2026_TEST",
    "v2": "SECURE_FPS_TERMINAL_KEY_KRN_2026_ROTATED_V2",
}

DEFAULT_STATE_CONFIG = {
    "state_code": "KA",
    "effective_date": "2026-11-01",
    "scheme_name": "Karnataka Anna Bhagya & Essential Add-ons 2026-27",
    "rules": {
        "PHH": {
            "dbt_cash_per_member_inr": 170.0,
            "additional_grain_kg": 0.0,
            "subsidized_dal_kg": 1.0,
            "subsidized_dal_price_inr": 25.0,
        },
        "AAY": {
            "dbt_cash_per_household_inr": 0.0,
            "additional_grain_kg": 0.0,
            "subsidized_dal_kg": 1.0,
            "subsidized_dal_price_inr": 25.0,
        },
        "NPHH": {
            "dbt_cash_per_member_inr": 0.0,
            "additional_grain_kg": 0.0,
            "subsidized_dal_kg": 0.0,
            "subsidized_dal_price_inr": 0.0,
        },
    },
}


def get_db(db_path: Optional[Path] = None) -> sqlite3.Connection:
    target = db_path or DEFAULT_DB_PATH
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    return conn


def init_database(conn: sqlite3.Connection, dealer_id: str = "FPS-42-BANGALORE-RURAL"):
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS beneficiary_cards (
                card_id TEXT PRIMARY KEY,
                scheme_type TEXT NOT NULL,
                member_count INTEGER NOT NULL,
                assigned_fps_id TEXT NOT NULL,
                registered_mobile TEXT,
                last_sync_date TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS offline_transactions (
                seq INTEGER PRIMARY KEY,
                prev_hash TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                card_id TEXT NOT NULL,
                items_json TEXT NOT NULL,
                dealer_id TEXT NOT NULL,
                hash TEXT NOT NULL,
                signature TEXT NOT NULL,
                key_version TEXT NOT NULL,
                sync_status TEXT DEFAULT 'PENDING'
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS shop_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
        """)

        # Seed sample beneficiary households if empty
        cur = conn.execute("SELECT COUNT(*) as c FROM beneficiary_cards")
        if cur.fetchone()["c"] == 0:
            sample_cards = [
                ("KA-BLR-AAY-1001", "AAY", 3, dealer_id, "9845011111", "2026-11-01T00:00:00Z"),
                ("KA-BLR-PHH-1002", "PHH", 4, dealer_id, "9845022222", "2026-11-01T00:00:00Z"),
                ("KA-BLR-PHH-1003", "PHH", 2, dealer_id, "9845033333", "2026-11-01T00:00:00Z"),
                ("KA-BLR-PHH-1004", "PHH", 5, dealer_id, "9845044444", "2026-11-01T00:00:00Z"),
                ("KA-BLR-PHH-1005", "PHH", 1, dealer_id, "9845055555", "2026-11-01T00:00:00Z"),
                ("KA-BLR-NPHH-2001", "NPHH", 4, dealer_id, "9845066666", "2026-11-01T00:00:00Z"),
            ]
            conn.executemany(
                "INSERT INTO beneficiary_cards VALUES (?, ?, ?, ?, ?, ?)", sample_cards
            )

        # Seed shop metadata
        conn.execute("INSERT OR REPLACE INTO shop_metadata VALUES ('dealer_id', ?)", (dealer_id,))
        conn.execute("INSERT OR REPLACE INTO shop_metadata VALUES ('stock_arrival_timestamp', '2026-11-03T08:15:00Z')")
        conn.execute("INSERT OR REPLACE INTO shop_metadata VALUES ('active_key_version', 'v1')")


def calculate_entitlements(card_row: sqlite3.Row, state_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    scheme = card_row["scheme_type"].upper()
    members = int(card_row["member_count"])
    cfg = state_config or DEFAULT_STATE_CONFIG
    rules = cfg["rules"].get(scheme, {})

    # 1. Central NFSA PMGKAY Rules (Free foodgrains through 31 Dec 2028)
    if scheme == "AAY":
        central_rice_kg = 35.0
        central_wheat_kg = 0.0
    elif scheme == "PHH":
        central_rice_kg = float(members * 5.0)
        central_wheat_kg = 0.0
    else:  # NPHH / Non-priority
        central_rice_kg = 0.0
        central_wheat_kg = 0.0

    central_grain_total_kg = central_rice_kg + central_wheat_kg
    central_cost_inr = 0.0  # 100% Free under PMGKAY

    # 2. State Add-on Rules (Karnataka 2026-27 Configurable)
    additional_grain_kg = rules.get("additional_grain_kg", 0.0)
    dbt_cash_inr = rules.get("dbt_cash_per_member_inr", 0.0) * members if scheme == "PHH" else rules.get("dbt_cash_per_household_inr", 0.0)
    subsidized_dal_kg = rules.get("subsidized_dal_kg", 0.0)
    subsidized_dal_price_inr = rules.get("subsidized_dal_price_inr", 0.0)

    total_cash_payable_inr = subsidized_dal_price_inr

    return {
        "card_id": card_row["card_id"],
        "scheme": scheme,
        "member_count": members,
        "central_nfsa": {
            "rice_kg": central_rice_kg,
            "wheat_kg": central_wheat_kg,
            "total_grain_kg": central_grain_total_kg,
            "cost_inr": central_cost_inr,
            "statutory_note": "100% Free under NFSA PMGKAY (through 31 Dec 2028)",
        },
        "state_addon": {
            "scheme_name": cfg["scheme_name"],
            "additional_grain_kg": additional_grain_kg,
            "dbt_cash_inr": dbt_cash_inr,
            "subsidized_dal_kg": subsidized_dal_kg,
            "subsidized_dal_cost_inr": subsidized_dal_price_inr,
        },
        "total_cash_payable_inr": total_cash_payable_inr,
    }


def record_transaction(
    conn: sqlite3.Connection,
    card_id: str,
    custom_items: Optional[Dict[str, float]] = None,
    key_ver: str = "v1",
    timestamp_override: Optional[str] = None
) -> Dict[str, Any]:
    with conn:
        cur = conn.execute("SELECT * FROM beneficiary_cards WHERE card_id = ?", (card_id,))
        card_row = cur.fetchone()
        if not card_row:
            raise ValueError(f"Card '{card_id}' not found in local offline database.")

        meta_cur = conn.execute("SELECT value FROM shop_metadata WHERE key = 'dealer_id'")
        dealer_row = meta_cur.fetchone()
        dealer_id = dealer_row["value"] if dealer_row else "FPS-UNKNOWN"

        ent = calculate_entitlements(card_row)

        if custom_items:
            for k, v in custom_items.items():
                if not isinstance(v, (int, float)) or v < 0:
                    raise ValueError(f"Invalid commodity quantity for '{k}': {v}. Quantities must be non-negative numbers.")
            items_payload = custom_items
        else:
            items_payload = {
                "rice_kg": ent["central_nfsa"]["rice_kg"],
                "wheat_kg": ent["central_nfsa"]["wheat_kg"],
                "state_dal_kg": ent["state_addon"]["subsidized_dal_kg"],
            }

        items_json = json.dumps(items_payload, sort_keys=True)

        # Get latest record in chain
        last_cur = conn.execute(
            "SELECT seq, hash, timestamp FROM offline_transactions ORDER BY seq DESC LIMIT 1"
        )
        last_row = last_cur.fetchone()

        if last_row:
            next_seq = last_row["seq"] + 1
            prev_hash = last_row["hash"]
            last_ts = last_row["timestamp"]
        else:
            next_seq = 1
            prev_hash = GENESIS_HASH
            last_ts = ""

        # Validate timestamp format and bounds
        now_ts = timestamp_override or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            parsed_ts = datetime.datetime.fromisoformat(now_ts.replace("Z", "+00:00"))
        except Exception:
            raise ValueError(f"Invalid ISO-8601 timestamp format: {now_ts}")

        if parsed_ts.year > 2030:
            raise ValueError(f"Clock tampering detected: timestamp {now_ts} exceeds operational horizon (year 2030).")

        # Enforce timestamp monotonicity
        if last_ts and now_ts < last_ts:
            raise ValueError(f"Clock rollback violation: proposed timestamp {now_ts} is earlier than previous record timestamp {last_ts}.")

        # Monthly entitlement guard (added after Demo Day Court 1): a card can't draw more
        # than its entitlement in one calendar month at this shop, in one go or across repeats.
        limits = {
            "rice_kg": ent["central_nfsa"]["rice_kg"],
            "wheat_kg": ent["central_nfsa"]["wheat_kg"],
            "state_dal_kg": ent["state_addon"]["subsidized_dal_kg"],
        }
        unknown = set(items_payload) - set(limits)
        if unknown:
            raise ValueError(f"Unknown commodity: {', '.join(sorted(unknown))}.")
        month = now_ts[:7]
        drawn = {k: 0.0 for k in limits}
        for row in conn.execute(
            "SELECT items_json FROM offline_transactions WHERE card_id = ? AND substr(timestamp, 1, 7) = ?",
            (card_id, month),
        ):
            for k, v in json.loads(row["items_json"]).items():
                if k in drawn:
                    drawn[k] += float(v)
        for k, v in items_payload.items():
            if drawn[k] + float(v) > limits[k] + 1e-9:
                raise ValueError(
                    f"Entitlement exceeded for {card_id} in {month}: {k} would be {drawn[k] + float(v):g}, "
                    f"limit {limits[k]:g} (already drawn {drawn[k]:g})."
                )

        receipt_hash = compute_receipt_hash(
            prev_hash, next_seq, now_ts, card_id, items_json, dealer_id
        )

        secret_key = DEFAULT_KEYS_MAP.get(key_ver, DEFAULT_KEYS_MAP["v1"])
        signature = sign_hash(receipt_hash, secret_key)

        conn.execute(
            """
            INSERT INTO offline_transactions (
                seq, prev_hash, timestamp, card_id, items_json, dealer_id, hash, signature, key_version
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (next_seq, prev_hash, now_ts, card_id, items_json, dealer_id, receipt_hash, signature, key_ver),
        )

        return {
            "seq": next_seq,
            "prev_hash": prev_hash,
            "timestamp": now_ts,
            "card_id": card_id,
            "scheme": ent["scheme"],
            "member_count": ent["member_count"],
            "items": items_payload,
            "cash_payable_inr": ent["total_cash_payable_inr"],
            "dealer_id": dealer_id,
            "hash": receipt_hash,
            "signature": signature,
            "key_version": key_ver,
        }


def format_receipt_slip(tx: Dict[str, Any]) -> str:
    rice = tx["items"].get("rice_kg", 0.0)
    wheat = tx["items"].get("wheat_kg", 0.0)
    dal = tx["items"].get("state_dal_kg", 0.0)
    payable = tx.get("cash_payable_inr", 25.0 if dal > 0 else 0.0)

    lines = [
        "==================================================",
        "        FAIR PRICE SHOP - PDS OFFLINE RECEIPT      ",
        f"        Dealer Terminal: {tx['dealer_id']}        ",
        "==================================================",
        f" Receipt #: {tx['seq']:05d}             Seq: {tx['seq']}",
        f" Date: {tx['timestamp']} (UTC)",
        f" Card ID: {tx['card_id']} ({tx.get('scheme', 'PHH')} - {tx.get('member_count', 4)} Members)",
        "--------------------------------------------------",
        " COMMODITY DISPENSATION SUMMARY:",
        f"  * Central Rice (PMGKAY): {rice:>5.1f} kg  [100% FREE]",
        f"  * Central Wheat:         {wheat:>5.1f} kg  [100% FREE]",
        f"  * State Toor Dal:        {dal:>5.1f} kg  [@ Rs. 25/kg]",
        "--------------------------------------------------",
        f" TOTAL CASH PAYABLE: Rs. {payable:>5.2f}",
        " > NOTICE: Central foodgrains are 100% FREE by law.",
        "   Dealers cannot collect handling fees for rice.",
        "--------------------------------------------------",
        f" Receipt Hash : {tx['hash'][:32]}...",
        f" HMAC Sign    : {tx['signature'][:32]}...",
        f" Key Version  : {tx['key_version']}",
        " Status       : TAMPER-EVIDENT OFFLINE AUDIT VOUCHER",
        "==================================================",
    ]
    return "\n".join(lines)


def run_verify(conn: sqlite3.Connection, checkpoint_hash: Optional[str] = None) -> Tuple[bool, str]:
    cur = conn.execute("SELECT * FROM offline_transactions ORDER BY seq ASC")
    rows = cur.fetchall()
    records = []
    for r in rows:
        records.append({
            "seq": r["seq"],
            "prev_hash": r["prev_hash"],
            "timestamp": r["timestamp"],
            "card_id": r["card_id"],
            "items": json.loads(r["items_json"]),
            "dealer_id": r["dealer_id"],
            "hash": r["hash"],
            "signature": r["signature"],
            "key_version": r["key_version"],
        })

    return verify_chain(records, DEFAULT_KEYS_MAP, checkpoint_hash)


def generate_ivr_dialog(card_row: sqlite3.Row, lang: str = "kn", stock_ts: str = "2026-11-03T08:15:00Z") -> Dict[str, str]:
    ent = calculate_entitlements(card_row)
    rice = int(ent["central_nfsa"]["rice_kg"])
    wheat = int(ent["central_nfsa"]["wheat_kg"])
    dal = int(ent["state_addon"]["subsidized_dal_kg"])
    dal_cost = int(ent["state_addon"]["subsidized_dal_cost_inr"])
    card = card_row["card_id"]

    if lang == "kn":
        # Kannada audio dialogue
        kn_nums = {0: "ಸೊನ್ನೆ", 5: "ಐದು", 10: "ಹತ್ತು", 15: "ಹದಿನೈದು", 20: "ಇಪ್ಪತ್ತು", 25: "ಇಪ್ಪತ್ತೈದು", 35: "ಮೂವತ್ತೈದು"}
        rice_word = kn_nums.get(rice, str(rice))
        wheat_word = kn_nums.get(wheat, str(wheat))
        text = (
            f"ರೇಷನ್ ಕಾರ್ಡ್ {card}. ನವೆಂಬರ್ ತಿಂಗಳ ಕೋಟಾ: "
            f"ಅಕ್ಕಿ: {rice_word} ಕಿಲೋಗ್ರಾಂ — ಉಚಿತ. "
            f"ಗೋಧಿ: {wheat_word} ಕಿಲೋಗ್ರಾಂ. "
            f"ತೊಗರಿ ಬೇಳೆ: {dal} ಕಿಲೋಗ್ರಾಂ, ಬೆಲೆ {dal_cost} ರೂಪಾಯಿ. "
            f"ನ್ಯಾಯಬೆಲೆ ಅಂಗಡಿ ಮಾಹಿತಿ: ಆಹಾರ ಧಾನ್ಯ ದಾಸ್ತಾನು ತಲುಪಿದೆ. "
            f"ಮತ್ತೊಮ್ಮೆ ಕೇಳಲು 1 ಒತ್ತಿರಿ. ಧನ್ಯವಾದಗಳು."
        )
        return {"lang": "kn", "card_id": card, "spoken_audio_script": text}
    else:
        # Hindi audio dialogue
        hi_nums = {0: "शून्य", 5: "पांच", 10: "दस", 15: "पंद्रह", 20: "बीस", 25: "पच्चीस", 35: "पैंतीस"}
        rice_word = hi_nums.get(rice, str(rice))
        wheat_word = hi_nums.get(wheat, str(wheat))
        text = (
            f"राशन कार्ड {card}. नवंबर महीने का कोटा: "
            f"चावल: {rice_word} किलोग्राम — बिल्कुल मुफ़्त. "
            f"गेहूं: {wheat_word} किलोग्राम. "
            f"तूर दाल: {dal} किलोग्राम, मूल्य {dal_cost} रुपये. "
            f"उचित दर दुकान की जानकारी: खाद्यान्न स्टॉक उपलब्ध है. "
            f"दोबारा सुनने के लिए 1 दबाएं. धन्यवाद."
        )
        return {"lang": "hi", "card_id": card, "spoken_audio_script": text}


def main():
    parser = argparse.ArgumentParser(description="PDS Anna-Mitra Offline Counter CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init-db
    p_init = subparsers.add_parser("init-db", help="Initialize local SQLite schema and seed sample households")
    p_init.add_argument("--db", type=str, default=str(DEFAULT_DB_PATH))
    p_init.add_argument("--dealer-id", type=str, default="FPS-42-BANGALORE-RURAL")

    # quota
    p_quota = subparsers.add_parser("quota", help="Calculate statutory entitlement for a ration card")
    p_quota.add_argument("card_id", type=str, help="12-digit ration card number")
    p_quota.add_argument("--db", type=str, default=str(DEFAULT_DB_PATH))

    # dispense
    p_disp = subparsers.add_parser("dispense", help="Record two-tap offline dispense transaction")
    p_disp.add_argument("card_id", type=str, help="Ration card number")
    p_disp.add_argument("--db", type=str, default=str(DEFAULT_DB_PATH))
    p_disp.add_argument("--key-ver", type=str, default="v1")
    p_disp.add_argument("--custom-rice", type=float, default=None)
    p_disp.add_argument("--custom-dal", type=float, default=None)

    # verify-chain
    p_ver = subparsers.add_parser("verify-chain", help="Audit local ledger integrity, signatures, and clock order")
    p_ver.add_argument("--db", type=str, default=str(DEFAULT_DB_PATH))
    p_ver.add_argument("--checkpoint", type=str, default=None)

    # checkpoint
    p_chk = subparsers.add_parser("checkpoint", help="Output current closing hash for daily external pinning")
    p_chk.add_argument("--db", type=str, default=str(DEFAULT_DB_PATH))

    # reconcile
    p_rec = subparsers.add_parser("reconcile", help="Reconcile logs from multiple terminals to detect split-brain duplicates")
    p_rec.add_argument("db_files", nargs="+", help="Paths to SQLite databases or JSON batch log files")

    # ivr-simulate
    p_ivr = subparsers.add_parser("ivr-simulate", help="Generate spoken Kannada or Hindi audio script for card")
    p_ivr.add_argument("card_id", type=str, help="Ration card number")
    p_ivr.add_argument("--lang", choices=["kn", "hi"], default="kn")
    p_ivr.add_argument("--db", type=str, default=str(DEFAULT_DB_PATH))

    args = parser.parse_args()

    if args.command == "init-db":
        conn = get_db(Path(args.db))
        init_database(conn, args.dealer_id)
        print(f"✓ Initialized database at: {args.db}")
        print(f"  Dealer Terminal ID: {args.dealer_id}")
        print("  Sample households seeded: 6 cards (AAY, PHH, NPHH)")

    elif args.command == "quota":
        conn = get_db(Path(args.db))
        init_database(conn)
        cur = conn.execute("SELECT * FROM beneficiary_cards WHERE card_id = ?", (args.card_id,))
        row = cur.fetchone()
        if not row:
            print(f"Error: Card '{args.card_id}' not found.")
            sys.exit(1)
        ent = calculate_entitlements(row)
        print(json.dumps(ent, indent=2))

    elif args.command == "dispense":
        conn = get_db(Path(args.db))
        init_database(conn)
        if args.custom_rice is not None and args.custom_rice < 0:
            print("Error: --custom-rice must be non-negative.", file=sys.stderr)
            sys.exit(1)
        if args.custom_dal is not None and args.custom_dal < 0:
            print("Error: --custom-dal must be non-negative.", file=sys.stderr)
            sys.exit(1)
        custom = None
        if args.custom_rice is not None or args.custom_dal is not None:
            custom = {
                "rice_kg": args.custom_rice if args.custom_rice is not None else 0.0,
                "wheat_kg": 0.0,
                "state_dal_kg": args.custom_dal if args.custom_dal is not None else 0.0,
            }
        try:
            tx = record_transaction(conn, args.card_id, custom, key_ver=args.key_ver)
            print(format_receipt_slip(tx))
        except Exception as e:
            print(f"Transaction Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "verify-chain":
        conn = get_db(Path(args.db))
        valid, msg = run_verify(conn, args.checkpoint)
        if valid:
            print(f"\033[92m✓ INTEGRITY VERIFIED: {msg}\033[0m")
            cur = conn.execute("SELECT COUNT(*) as c FROM offline_transactions")
            c = cur.fetchone()["c"]
            print(f"  Total auditable transactions in chain: {c}")
        else:
            print(f"\033[91m✗ TAMPER DETECTED: {msg}\033[0m", file=sys.stderr)
            sys.exit(1)

    elif args.command == "checkpoint":
        conn = get_db(Path(args.db))
        cur = conn.execute("SELECT seq, hash, timestamp FROM offline_transactions ORDER BY seq DESC LIMIT 1")
        row = cur.fetchone()
        if not row:
            print(GENESIS_HASH)
        else:
            print(json.dumps({
                "seq": row["seq"],
                "timestamp": row["timestamp"],
                "pinned_checkpoint_hash": row["hash"]
            }, indent=2))

    elif args.command == "reconcile":
        batches = []
        for path_str in args.db_files:
            p = Path(path_str)
            if not p.exists():
                print(f"Warning: File {p} not found, skipping.", file=sys.stderr)
                continue
            conn = get_db(p)
            cur = conn.execute("SELECT * FROM offline_transactions ORDER BY seq ASC")
            rows = cur.fetchall()
            b = []
            for r in rows:
                b.append({
                    "seq": r["seq"],
                    "prev_hash": r["prev_hash"],
                    "timestamp": r["timestamp"],
                    "card_id": r["card_id"],
                    "items": json.loads(r["items_json"]),
                    "dealer_id": r["dealer_id"],
                    "hash": r["hash"],
                    "signature": r["signature"],
                    "key_version": r["key_version"],
                })
            batches.append(b)

        accepted, conflicts = reconcile_batch_logs(batches)
        print("==================================================")
        print("       CENTRAL RECONCILIATION AUDIT SUMMARY       ")
        print("==================================================")
        print(f" Total Transactions Processed: {len(accepted) + len(conflicts)}")
        print(f" Accepted Legitimate Drawals : {len(accepted)}")
        print(f" Conflicting Duplicate Drawals: {len(conflicts)}")
        print("--------------------------------------------------")
        if conflicts:
            print("\033[93m⚠ SPLIT-BRAIN DUPLICATE DRAWAL CONFLICTS DETECTED:\033[0m")
            for c in conflicts:
                print(f"  Card ID : {c['card_id']} (Month: {c['month']})")
                print(f"  Reason  : {c['reason']}")
                print(f"  Original Tx    : Seq {c['original_tx']['seq']} at {c['original_tx']['dealer_id']} ({c['original_tx']['timestamp']})")
                print(f"  Conflicting Tx : Seq {c['conflicting_tx']['seq']} at {c['conflicting_tx']['dealer_id']} ({c['conflicting_tx']['timestamp']})")
                print("  Action  : Logged in Central Administrative Dispute Queue for Taluk Food Inspector")
                print("---")
        else:
            print("\033[92m✓ All batch transactions reconciled with zero card conflicts.\033[0m")

    elif args.command == "ivr-simulate":
        conn = get_db(Path(args.db))
        init_database(conn)
        cur = conn.execute("SELECT * FROM beneficiary_cards WHERE card_id = ?", (args.card_id,))
        row = cur.fetchone()
        if not row:
            print(f"Error: Card '{args.card_id}' not found.")
            sys.exit(1)
        dialog = generate_ivr_dialog(row, lang=args.lang)
        print(f"Language: {dialog['lang'].upper()}")
        print(f"Card ID : {dialog['card_id']}")
        print("Audio Voice Prompt:")
        print(f'"{dialog["spoken_audio_script"]}"')


if __name__ == "__main__":
    main()
