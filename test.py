from src.fetcher import get_normal_transactions

address = "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"

df = get_normal_transactions(address)

print(df)
print("\nTotal transactions:", len(df))
print("\nColumns:", list(df.columns))
