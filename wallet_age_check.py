from datetime import datetime, timezone
import pandas as pd
from fetch_transcation import fetch_transactions  # reuse existing function

def check_wallet_age(wallet_address: str) -> dict:
    """
    Returns a dict with:
      - first_tx_date: datetime of the very first transaction
      - wallet_age_days: how many days old the wallet is
      - is_fresh: True if wallet is less than 7 days old
      - flag_reason: human-readable explanation if flagged
    """
    df = fetch_transactions(wallet_address)

    if df.empty:
        return {
            "first_tx_date": None,
            "wallet_age_days": None,
            "is_fresh": False,
            "flag_reason": "No transactions found — cannot determine wallet age."
        }

    # df is sorted asc, so first row = oldest tx
    first_tx_date_str = df.iloc[0]["date"]  # format: "YYYY-MM-DD HH:MM"
    first_tx_date = datetime.strptime(first_tx_date_str, "%Y-%m-%d %H:%M")

    now = datetime.now()
    age_days = (now - first_tx_date).days

    is_fresh = age_days < 7

    return {
        "first_tx_date": first_tx_date.strftime("%Y-%m-%d %H:%M"),
        "wallet_age_days": age_days,
        "is_fresh": is_fresh,
        "flag_reason": (
            f"  FLAGGED: Wallet is only {age_days} day(s) old. "
            f"Fresh wallets are often created for one-time operations."
            if is_fresh else None
        )
    }


if __name__ == "__main__":
    address = "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"
    print(f"Checking wallet age for: {address}\n")

    result = check_wallet_age(address)

    print(f"First Transaction : {result['first_tx_date']}")
    print(f"Wallet Age        : {result['wallet_age_days']} day(s)")
    print(f"Fresh Wallet?     : {'YES' if result['is_fresh'] else 'NO'}")
    if result["flag_reason"]:
        print(f"\n{result['flag_reason']}")
    else:
        print("\n Wallet age is acceptable (7+ days old).")