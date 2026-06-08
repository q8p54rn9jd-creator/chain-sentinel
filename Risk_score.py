# risk_score.py — Benedicta's Phase 2 contribution
# Combines all 3 checks into a final risk score

from fetch_transcation import fetch_transactions
from clean_data import clean_transactions
from blacklist import is_blacklisted, get_label
from wallet_age_check import check_wallet_age
from check_burst import check_burst_dispersion


def check_blacklist_connection(wallet_address, transactions):
    """Tan's check — reused from test.py"""
    if is_blacklisted(wallet_address):
        return True, f"Wallet is blacklisted: {get_label(wallet_address)}"

    for _, tx in transactions.iterrows():
        from_address = str(tx.get("from", ""))
        to_address   = str(tx.get("to", ""))

        if is_blacklisted(from_address):
            return True, f"Sender is blacklisted: {get_label(from_address)}"

        if is_blacklisted(to_address):
            return True, f"Receiver is blacklisted: {get_label(to_address)}"

    return False, "No blacklist connection found"


def compute_risk_score(wallet_address: str) -> tuple:
    """
    Runs all 3 fraud detection checks and combines them into a risk score.

    Scoring:
        0 flags → CLEAN
        1 flag  → LOW RISK
        2 flags → MEDIUM RISK
        3 flags → HIGH RISK

    Returns:
        (risk_label: str, flags_list: list)
    """

    print("=" * 60)
    print("  ChainSentinel — Phase 2: Fraud Detection & Risk Scoring")
    print("=" * 60)
    print(f"\n  Wallet : {wallet_address}\n")
    print("-" * 60)

    # ── Fetch & clean transactions once, share across all checks ────────────
    raw_df   = fetch_transactions(wallet_address)
    clean_df = clean_transactions(raw_df)

    flags       = 0
    flags_list  = []   # ← NEW: track flag names for clean output
    results     = []

    # ── CHECK 1: Blacklist (Tan) ─────────────────────────────────────────────
    bl_flagged, bl_reason = check_blacklist_connection(wallet_address, clean_df)
    status = "⚠  FLAGGED" if bl_flagged else "✔  CLEAR"
    if bl_flagged:
        flags += 1
        flags_list.append("blacklist contact")   # ← NEW
    results.append(("Blacklist Check     (Tan)", status, bl_reason))

    # ── CHECK 2: Burst Dispersion (Aaliyah) ──────────────────────────────────
    burst_flagged, burst_reason = check_burst_dispersion(clean_df, wallet_address)
    status = "⚠  FLAGGED" if burst_flagged else "✔  CLEAR"
    if burst_flagged:
        flags += 1
        flags_list.append("burst dispersion")    # ← NEW
    results.append(("Burst Dispersion  (Aaliyah)", status, burst_reason))

    # ── CHECK 3: Wallet Age (Om) ─────────────────────────────────────────────
    age_result   = check_wallet_age(wallet_address)
    age_flagged  = age_result["is_fresh"]
    age_reason   = (
        age_result["flag_reason"]
        if age_flagged
        else f"Wallet is {age_result['wallet_age_days']} day(s) old — acceptable."
    )
    status = "⚠  FLAGGED" if age_flagged else "✔  CLEAR"