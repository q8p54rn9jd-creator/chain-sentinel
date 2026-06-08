"""
ChainSentinel - On-Chain Fraud Detection
Phase 4: Main entry point - runs the full pipeline from input to output.
Written by: Benedicta
"""

from fetch_transcation import fetch_transactions
from clean_data import clean_transactions
from blacklist import BLACKLIST
from check_burst import check_burst_dispersion
from wallet_age_check import check_wallet_age
from Risk_score import calculate_risk_score
from analyze_wallet import build_and_show_graph


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

    print(f"\n[1/4] Fetching transactions for {shorten_address(wallet_address)} ...")

    # --- Step 2: Fetch raw transactions ---
    raw_transactions = fetch_transactions(wallet_address)

    if not raw_transactions:
        print("[ERROR] No transactions found, or the API request failed.")
        print("        Check your ETHERSCAN_API_KEY and internet connection.")
        return

    # --- Step 3: Clean the data (Wei → ETH, Unix → readable dates) ---
    print(f"[2/4] Cleaning {len(raw_transactions)} transactions ...")
    transactions = clean_transactions(raw_transactions)

    # --- Step 4: Run the 3 fraud checks ---
    print("[3/4] Running fraud detection checks ...")

    blacklist_flag   = any(
        tx["from"].lower() in [b.lower() for b in BLACKLIST] or
        tx["to"].lower()   in [b.lower() for b in BLACKLIST]
        for tx in transactions
    )

    burst_flag      = check_burst_dispersion(transactions)
    fresh_flag      = check_wallet_age(transactions)

    flags = []
    if blacklist_flag:
        flags.append("blacklist contact")
    if burst_flag:
        flags.append("burst dispersion")
    if fresh_flag:
        flags.append("fresh wallet")

    # --- Step 5: Calculate and print risk score ---
    risk_label = calculate_risk_score(flags)

    short = shorten_address(wallet_address)
    flag_str = ", ".join(flags) if flags else "none"

    print("\n" + "=" * 55)
    print(f"  Address : {short}")
    print(f"  Risk    : {risk_label}")
    print(f"  Flags   : {flag_str}")
    print("=" * 55)

    # --- Step 6: Build and display the transaction graph ---
    print("\n[4/4] Building transaction graph ...")
    build_and_show_graph(transactions, wallet_address, BLACKLIST)

    print("\nGraph saved as graph.png")
    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
