# main.py

from fetch_transcation import fetch_transactions as get_transactions
from Risk_score import compute_risk_score
from build_graph import draw_graph as build_graph


def main():
    print("=" * 50)
    print("ChainSentinel - On-Chain Fraud Detection")
    print("=" * 50)

    wallet = input("Enter Ethereum wallet address: ").strip()

    print("\nFetching transaction data...")
    transactions = get_transactions(wallet)

    if not transactions:
        print("No transactions found.")
        return

    print(f"Found {len(transactions)} transactions.")

    # Run fraud checks
    blacklist_flag = check_blacklist(wallet, transactions)
    burst_flag = check_burst_dispersion(transactions)
    fresh_wallet_flag = check_fresh_wallet(transactions)

    risk, flags = compute_risk_score(wallet)

    # ── Clean one-line output ────────────────────────────────────────────────
    print("\n" + "=" * 50)
    short = wallet[:6] + "..." + wallet[-4:]
    flag_str = ", ".join(flags) if flags else "none"
    print(f"Address: {short} | Risk: {risk} | Flags: {flag_str}")
    print("=" * 50)
    # ────────────────────────────────────────────────────────────────────────

    print("\nGenerating transaction graph...")
    build_graph(wallet, transactions)

    print("Graph saved as graph.png")
    print("Analysis complete.")


if __name__ == "__main__":
    main()