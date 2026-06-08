"""
ChainSentinel - On-Chain Fraud Detection
Phase 4: Main entry point - runs the full pipeline from input to output.
Written by: Benedicta
"""

from fetch_transcation import fetch_transactions
from clean_data import clean_transactions
from Risk_score import compute_risk_score
from analyze_wallet import analyze_wallet


def shorten_address(address):
    """Return a shortened wallet address: first 6 + last 4 chars."""
    return f"{address[:6]}...{address[-4:]}"


def main():
    print("=" * 55)
    print("  ChainSentinel · On-Chain Fraud Detection")
    print("=" * 55)

    # --- Step 1: Get wallet address from user ---
    wallet_address = input("\nEnter an Ethereum wallet address to analyse:\n> ").strip()

    if not wallet_address.startswith("0x") or len(wallet_address) != 42:
        print("\n[ERROR] That doesn't look like a valid Ethereum address.")
        print("        Addresses start with 0x and are 42 characters long.")
        return

    print(f"\n[1/3] Fetching transactions for {shorten_address(wallet_address)} ...")

    # --- Step 2: Fetch and clean transactions ---
    raw_transactions = fetch_transactions(wallet_address)

    if raw_transactions is None or raw_transactions.empty:
        print("[ERROR] No transactions found, or the API request failed.")
        print("        Check your ETHERSCAN_API_KEY and internet connection.")
        return

    print(f"[2/3] Cleaning {len(raw_transactions)} transactions ...")
    clean_transactions(raw_transactions)

    # --- Step 3: Run fraud checks + risk score (handled by Risk_score.py) ---
    print("[3/3] Running fraud detection checks ...\n")
    compute_risk_score(wallet_address)

    # --- Step 4: Full wallet analysis and graph ---
    analyze_wallet(wallet_address)

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
