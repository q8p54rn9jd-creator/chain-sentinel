from blacklist import is_blacklisted, get_label
from wallet_age_check import check_wallet_age

def analyze_wallet(wallet_address):
    flags = []

    print(f"\n Analyzing wallet: {wallet_address}\n")

    # Phase 1: Blacklist check
    if is_blacklisted(wallet_address):
        label = get_label(wallet_address)
        reason = f" Address is blacklisted: {label}"
        flags.append(reason)
        print(f" Blacklist : {reason}")
    else:
        print(" Blacklist : Clean")

    # Phase 2: Fresh wallet check
    age_result = check_wallet_age(wallet_address)
    if age_result["is_fresh"]:
        flags.append(age_result["flag_reason"])
        print(f" Wallet Age: {age_result['flag_reason']}")
    else:
        print(f" Wallet Age: {age_result['wallet_age_days']} days old — OK")

    # Final verdict
    print("\n" + "="*50)
    if flags:
        print(f" SUSPICIOUS WALLET — {len(flags)} flag(s) found")
        for i, flag in enumerate(flags, 1):
            print(f"   {i}. {flag}")
    else:
        print(" WALLET LOOKS CLEAN — No flags found")
    print("="*50)

    return {
        "wallet": wallet_address,
        "flags": flags,
        "is_suspicious": len(flags) > 0
    }


if __name__ == "__main__":
    address = "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"
    analyze_wallet(address)