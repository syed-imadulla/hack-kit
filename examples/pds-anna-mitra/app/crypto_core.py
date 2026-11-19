"""Cryptographic primitives and offline chain validation for PDS Anna-Mitra.

Provides:
- HMAC-SHA256 signature generation and validation with key versioning support.
- SHA-256 append-only hash-chaining.
- Monotonic sequence numbering AND strict timestamp monotonicity validation.
- Detection of tampering, truncation, non-monotonic sequences, clock rollback, and full-rewrite attacks.
- Detection of multi-device duplicate card redemptions during central reconciliation.
"""
import datetime
import hashlib
import hmac
import json
from typing import Any, Dict, List, Optional, Tuple, Union


def compute_receipt_hash(prev_hash: str, seq: int, timestamp: str, card_id: str, items_json: str, dealer_id: str) -> str:
    """Compute deterministic SHA-256 payload hash for a receipt record."""
    payload = f"{prev_hash}|{seq}|{timestamp}|{card_id}|{items_json}|{dealer_id}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sign_hash(payload_hash: str, secret_key: str) -> str:
    """Generate HMAC-SHA256 signature for a payload hash using the dealer/terminal secret key."""
    return hmac.new(secret_key.encode("utf-8"), payload_hash.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_chain(
    records: List[Dict[str, Any]],
    keys: Union[str, Dict[str, str]],
    pinned_checkpoint_hash: Optional[str] = None
) -> Tuple[bool, str]:
    """Verify integrity of an append-only hash-chained ledger.

    Supports:
    - Single secret key (string) or key rotation dictionary mapping key_version -> secret_key.
    - Pinned checkpoint hash matching the final (or designated) record hash.

    Checks:
    1. Monotonic sequence numbering (seq = prev_seq + 1, starting at 1).
    2. Strict timestamp monotonicity (timestamp >= prev_timestamp) to detect clock rollback.
    3. Exact prev_hash linkage (record[i].prev_hash == record[i-1].hash).
    4. Recomputed payload SHA-256 hash match.
    5. Valid HMAC-SHA256 signature under the active (or rotated) secret key.
    6. Pinned checkpoint hash matching against external anchor.
    """
    if not records:
        if pinned_checkpoint_hash:
            return False, "Ledger is empty but external checkpoint was expected (full truncation attack)"
        return True, "Empty chain valid"

    expected_prev = "GENESIS_ROOT_HASH_00000000000000000000000000000000000000000000000000"
    last_timestamp = ""

    for i, r in enumerate(records):
        expected_seq = i + 1
        if r.get("seq") != expected_seq:
            return False, f"Sequence gap or rollback detected at row {i + 1}: expected seq {expected_seq}, found {r.get('seq')}"

        curr_ts = r.get("timestamp", "")
        try:
            parsed_ts = datetime.datetime.fromisoformat(curr_ts.replace("Z", "+00:00"))
            if parsed_ts.year > 2030:
                return False, f"Timestamp out of bounds at row {i + 1}: year {parsed_ts.year} exceeds operational horizon (2030)"
        except Exception:
            return False, f"Invalid timestamp format at row {i + 1}: {curr_ts}"

        if i > 0 and curr_ts < last_timestamp:
            return False, f"Clock rollback detected at row {i + 1}: timestamp {curr_ts} is earlier than previous timestamp {last_timestamp}"
        last_timestamp = curr_ts

        if r.get("prev_hash") != expected_prev:
            return False, f"Hash chain broken at row {i + 1}: prev_hash does not match preceding record hash"

        # Recompute hash
        items_str = json.dumps(r.get("items"), sort_keys=True) if isinstance(r.get("items"), (dict, list)) else str(r.get("items", ""))
        computed_hash = compute_receipt_hash(
            r["prev_hash"],
            r["seq"],
            r["timestamp"],
            r["card_id"],
            items_str,
            r["dealer_id"]
        )

        if computed_hash != r.get("hash"):
            return False, f"Tampered record payload at row {i + 1}: hash mismatch"

        # Determine secret key for signature verification (supports key rotation)
        key_ver = r.get("key_version", "v1")
        if isinstance(keys, dict):
            if key_ver not in keys:
                return False, f"Unknown key version '{key_ver}' at row {i + 1}"
            active_key = keys[key_ver]
        else:
            active_key = keys

        # Verify HMAC
        expected_sig = sign_hash(computed_hash, active_key)
        if expected_sig != r.get("signature"):
            return False, f"Invalid signature at row {i + 1}: HMAC verification failed under key version '{key_ver}'"

        expected_prev = computed_hash

    # Checkpoint pinning check against ledger truncation or full-ledger substitution
    if pinned_checkpoint_hash and records[-1]["hash"] != pinned_checkpoint_hash:
        return False, f"Checkpoint verification failed: final ledger hash {records[-1]['hash']} does not match pinned external anchor {pinned_checkpoint_hash}"

    return True, "Chain verified successfully"


def reconcile_batch_logs(batches: List[List[Dict[str, Any]]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Reconcile transaction logs collected from multiple disconnected offline shops.

    Detects split-brain duplicate card disbursements within the same month.
    Returns:
    - accepted_records: Deduplicated, chronologically ordered valid transactions.
    - conflict_flags: List of conflicting duplicate drawal attempts.
    """
    all_records = []
    for b in batches:
        all_records.extend(b)

    # Sort deterministically by timestamp and sequence
    all_records.sort(key=lambda x: (x.get("timestamp", ""), x.get("seq", 0)))

    seen_cards = {}
    accepted = []
    conflicts = []

    for r in all_records:
        card = r.get("card_id")
        month = r.get("timestamp", "")[:7]  # YYYY-MM
        key = (card, month)

        if key in seen_cards:
            prev_tx = seen_cards[key]
            conflicts.append({
                "type": "CONFLICT_DUPLICATE_OFFLINE_DRAWAL",
                "card_id": card,
                "month": month,
                "original_tx": prev_tx,
                "conflicting_tx": r,
                "reason": f"Card {card} already drew rations at terminal {prev_tx.get('dealer_id')} on {prev_tx.get('timestamp')}; duplicate drawal attempted at terminal {r.get('dealer_id')}"
            })
        else:
            seen_cards[key] = r
            accepted.append(r)

    return accepted, conflicts
