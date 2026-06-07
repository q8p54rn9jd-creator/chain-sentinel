# test.py — Aaliyah's Phase 1 contribution

from fetch_transcation import fetch_transactions
from clean_data import clean_transactions
from blacklist import is_blacklisted, get_label
def check_blacklist_connection(wallet_address, transactions):
    # Check wallet itself
    if is_blacklisted(wallet_address):
        return True, f"Wallet is blacklisted: {get_label(wallet_address)}"

    # Check all transactions
    for _, tx in transactions.iterrows():
        from_address = str(tx.get("from", ""))
        to_address = str(tx.get("to", ""))

        if is_blacklisted(from_address):
            return True, f"Sender is blacklisted: {get_label(from_address)}"

        if is_blacklisted(to_address):
            return True, f"Receiver is blacklisted: {get_label(to_address)}"

    return False, "No blacklist connection found"

address = "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"

print("=" * 60)
print("ChainSentinel — Phase 1 Test")
print("=" * 60)

# Step 1 — check blacklist
print(f"\nAddress : {address}")
print(f"Blacklisted : {is_blacklisted(address)}")
print(f"Label       : {get_label(address)}")

# Step 2 — fetch
print(f"\nFetching transactions...")
raw_df = fetch_transactions(address)
print(f"Raw rows fetched: {len(raw_df)}")

# Step 3 — clean
clean_df = clean_transactions(raw_df)
flag, reason = check_blacklist_connection(address, clean_df)

print("\n--- Phase 2: Blacklist Check ---")
print(f"Blacklist flag: {flag}")
print(f"Reason: {reason}")print(f"Clean rows after filtering: {len(clean_df)}")

# Step 4 — print the table
print("\n--- Transaction Table ---\n")
print(clean_df.to_string(index=False))
print("\n" + "=" * 60)
print("Phase 1 complete.")
print("=" * 60)
