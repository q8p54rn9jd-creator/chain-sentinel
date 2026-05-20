import requests
import pandas as pd
from datetime import datetime

API_KEY = "XW8KDJR8MR9JAJJWAI765PWZF698UDI9JR"

def fetch_transactions(wallet_address):
    url = "https://api.etherscan.io/v2/api"
    params = {
        "chainid":1,
        "module": "account",
        "action": "txlist",
        "address": wallet_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "1":
        print(f"Error: {data['message']}")
        return pd.DataFrame(columns=["from", "to", "amount_eth", "date"])

    rows = []
    for tx in data["result"]:
        rows.append({
            "from": tx["from"],
            "to": tx["to"],
            "amount_eth": int(tx["value"]) / 10**18,
            "date": datetime.fromtimestamp(int(tx["timeStamp"])).strftime("%Y-%m-%d %H:%M"),
        })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    address ="0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"
    print(f"Fetching transactions for: {address}\n")
    df = fetch_transactions(address)
    if df.empty:
        print("No transactions found.")
    else:
        print(f"Found {len(df)} transactions:\n")
        print(df.to_string(index=False))