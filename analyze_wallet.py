from fetch_transcation import fetch_transactions
from blacklist import is_blacklisted, get_label
from wallet_age_check import check_wallet_age

def analyze_wallet(wallet_address: str) -> dict:
    print(f"  Fetching transactions...")
    df = fetch_transactions(wallet_address)

    if df.empty:
        return {"error": "No transactions found."}

    total_txs = len(df)
    unique_counterparties = set(df["to"].tolist() + df["from"].tolist())
    unique_counterparties.discard(wallet_address.lower())

    blacklisted_contacts = []
    for addr in unique_counterparties:
        if is_blacklisted(addr):
            blacklisted_contacts.append({
                "address": addr,
                "label": get_label(addr)
            })

    total_eth_sent = df[df["from"].str.lower() == wallet_address.lower()]["amount_eth"].sum()
    total_eth_received = df[df["to"].str.lower() == wallet_address.lower()]["amount_eth"].sum()

    age_info = check_wallet_age(wallet_address)

    return {
        "wallet": wallet_address,
        "total_transactions": total_txs,
        "total_eth_sent": round(total_eth_sent, 4),
        "total_eth_received": round(total_eth_received, 4),
        "blacklisted_contacts": blacklisted_contacts,
        "blacklisted_contact_count": len(blacklisted_contacts),
        "wallet_age_days": age_info.get("wallet_age_days"),
        "is_fresh_wallet": age_info.get("is_fresh"),
        "first_tx_date": age_info.get("first_tx_date"),
        "df": df
    }clear
    