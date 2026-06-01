# clean_data.py  — Tan's Phase 1 contribution
import pandas as pd

def clean_transactions(df):
    """
    Takes the raw DataFrame from fetch_transactions() and returns a clean version.
    Columns expected: from, to, amount_eth, date
    """

    if df.empty:
        return df

    # Drop rows where 'to' is missing (contract-creation transactions)
    df = df[df["to"].notna() & (df["to"] != "")]

    # Normalise addresses to lowercase so blacklist matching works later
    df["from"] = df["from"].str.lower()
    df["to"]   = df["to"].str.lower()

    # Drop exact duplicate rows
    df = df.drop_duplicates()

    # Reset index after drops
    df = df.reset_index(drop=True)
    df["amount_eth"] = df["amount_eth"].round(6)

    return df


# Quick test — run this file directly to verify
if __name__ == "__main__":
    from fetch_transcation import fetch_transactions

    address = "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"
    print(f"Fetching and cleaning transactions for: {address}\n")

    raw_df   = fetch_transactions(address)
    clean_df = clean_transactions(raw_df)

    print(f"Raw rows:   {len(raw_df)}")
    print(f"Clean rows: {len(clean_df)}\n")
    print(clean_df.to_string(index=False))