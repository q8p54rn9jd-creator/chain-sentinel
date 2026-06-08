# main.py

from data_fetcher import get_transactions
from fraud_checks import (
    check_blacklist,
    check_burst_dispersion,
    check_fresh_wallet,
    calculate_risk_score
)
from visualizer import build_graph


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

    flags = []

    if blacklist_flag:
        flags.append("blacklist contact")

    if burst_flag:
        flags.append("burst dispersion")

    if fresh_wallet_flag:
        flags.append("fresh wallet")

    risk = calculate_risk_score(
        blacklist_flag,
        burst_flag,
        fresh_wallet_flag
    )

    print("\n" + "=" * 50)
    print(f"Address: {wallet}")
    print(f"Risk Level: {risk}")

    if flags:
        print(f"Flags Triggered: {', '.join(flags)}")
    else:
        print("Flags Triggered: None")

    print("=" * 50)

    print("\nGenerating transaction graph...")
    build_graph(wallet, transactions)

    print("Graph saved as graph.png")
    print("Analysis complete.")


if __name__ == "__main__":
    main()
