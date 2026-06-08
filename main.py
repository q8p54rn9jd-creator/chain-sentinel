# main.py

from fetch_transcation import fetch_transactions
from Risk_score import compute_risk_score
from build_graph import draw_graph


def shorten_address(address):
    return address[:6] + "..." + address[-4:]


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

    # --- Step 2: Run all fraud checks ---
    risk, flags = compute_risk_score(wallet_address)

    # --- Step 3: Clean one-line output ---
    print("\n" + "=" * 55)
    short = shorten_address(wallet_address)
    flag_str = ", ".join(flags) if flags else "none"
    print(f"Address: {short} | Risk: {risk} | Flags: {flag_str}")
    print("=" * 55)

    # --- Step 4: Generate graph ---
    print("\nGenerating transaction graph...")
    draw_graph(wallet_address)
    print("Graph saved as graph.png")
    print("Analysis complete.")

if __name__ == "__main__":
    main()