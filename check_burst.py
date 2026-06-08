
import pandas as pd
from fetch_transcation import fetch_transactions
from clean_data import clean_transactions

def check_burst_dispersion(df, address):
    address = address.lower()
    outgoing = df[df["from"] == address].copy()

    if outgoing.empty:
        return False, "No outgoing transactions found."

    outgoing["date"] = pd.to_datetime(outgoing["date"])
    outgoing = outgoing.sort_values("date")

    for i, row in outgoing.iterrows():
        window_start = row["date"]
        window_end   = window_start + pd.Timedelta(hours=1)

        window = outgoing[
            (outgoing["date"] >= window_start) &
            (outgoing["date"] <= window_end)
        ]

        unique_recipients = window["to"].nunique()

        if unique_recipients >= 5:
            return True, f"FLAGGED — sent to {unique_recipients} different wallets within 1 hour of {window_start}"

    return False, "No burst dispersion detected."


if __name__ == "__main__":
    address = "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"

    df = fetch_transactions(address)
    df = clean_transactions(df)

    flagged, message = check_burst_dispersion(df, address)

    print("=" * 60)
    print("Burst Dispersion Check")
    print("=" * 60)
    print(f"Address : {address}")
    print(f"Flagged : {flagged}")
    print(f"Result  : {message}")
    print("=" * 60)