# =============================================================================
# blacklist.py
# ChainSentinel — On-Chain Fraud Detection
# Compiled by: Benedicta
# Description: Reference list of known malicious Ethereum addresses.
#              Includes sanctioned Tornado Cash mixer contracts and
#              confirmed hacker wallets sourced from Etherscan & rekt.news.
# =============================================================================


# -----------------------------------------------------------------------------
# TORNADO CASH CONTRACT ADDRESSES (Ethereum Mainnet)
# Sanctioned by the U.S. Treasury OFAC in August 2022.
# These contracts are used to obfuscate the origin of stolen funds
# by breaking the on-chain transaction trail.
# Source: etherscan.io (verified labels) & coincenter.org OFAC list
# -----------------------------------------------------------------------------

TORNADO_CASH_ADDRESSES = [
    # -- ETH Pools --
    "0x12D66f87A04A9E220C9D9010cAe61B776352BC6a",  # Tornado.Cash: 0.1 ETH Pool
    "0x47CE0C6eD5B0Ce3d3A51fdb1C52DC66a7c3c2936",  # Tornado.Cash: 1 ETH Pool
    "0x910Cbd523D972eb0a6f4cAe4618aD62622b39DbF",  # Tornado.Cash: 10 ETH Pool
    "0xA160cdAB225685dA1d56aa342Ad8841c3b53f291",  # Tornado.Cash: 100 ETH Pool

    # -- DAI Pools --
    "0xD4B88Df4D29F5CedD6857912842cff3b20C8Cfa3",  # Tornado.Cash: DAI 100 Pool
    "0xFD8610d20aA15b7B2E3Be39B396a1bC3516c7144",  # Tornado.Cash: DAI 1,000 Pool
    "0x07687e702b410Fa43f4cB4Af7FA097918ffD2730",  # Tornado.Cash: DAI 10,000 Pool
    "0x23773E65ed146A459667494014f9422A91E84FC2",  # Tornado.Cash: DAI 100,000 Pool

    # -- cDAI Pools --
    "0x22aaA7720ddd5388A3c0A3333430953C68f1849b",  # Tornado.Cash: cDAI 5,000 Pool
    "0xBA214C1c1928a32Bffe790263E38B4Af9bFCD659",  # Tornado.Cash: cDAI 50,000 Pool
    "0xb1C8094B234DcE6e03f10a5b673c1d8C69739A00",  # Tornado.Cash: cDAI 500,000 Pool

    # -- USDC / USDT / WBTC Pools --
    "0xd96f2B1c14Db8458374d9Aca76E26c3950113463",  # Tornado.Cash: USDC 100 Pool
    "0x4736dCf1b7A3d580672CcE6E7c65cd5cc9cFBa9D",  # Tornado.Cash: USDC 1,000 Pool
    "0xD691F27f38B395864Ea86CfC7253969B409c362d",  # Tornado.Cash: USDT 100 Pool
    "0xaEaaC358560e11f52454D997AAFF2c5731B6f8a6",  # Tornado.Cash: USDT 1,000 Pool
    "0x178169B423a011fff22B9e3F3abeA13414dDD0F1",  # Tornado.Cash: WBTC 0.1 Pool
    "0x610B717796ad172B316836AC95a2ffad065CeaB4",  # Tornado.Cash: WBTC 1 Pool
    "0xbB93e510BbCD0B7beb5A853875f9eC60275CF498",  # Tornado.Cash: WBTC 10 Pool

    # -- Router & Governance --
    "0xd90e2f925DA726b50C4ED8D0Fb90Ad053324F31b",  # Tornado.Cash: Router (main entry point)
    "0x5efda50f22d34F262c29268506C5Fa42cB56A1Ce",  # Tornado.Cash: Governance Proxy
    "0x722122dF12D4e14e13Ac3b6895a86e84145b6967",  # Tornado.Cash: Proxy (Relayer)
]


# -----------------------------------------------------------------------------
# KNOWN HACKER WALLET ADDRESSES
# Confirmed exploit addresses sourced from rekt.news, Etherscan, and
# on-chain investigation reports. All linked to major DeFi hacks.
# -----------------------------------------------------------------------------

HACKER_WALLETS = [
    # Drift Protocol Exploiter — April 2026
    # North Korean state hackers (Lazarus Group). $285M stolen in 128 seconds.
    # Funded operation via Tornado Cash with just 10 ETH.
    "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7",  # Drift Protocol Exploiter (main)

    # Ronin Bridge Exploiter — March 2022
    # Lazarus Group (North Korea). $625M stolen (173,600 ETH + $25.5M USDC).
    # Confirmed by FBI and sanctioned by OFAC.
    # Source: rekt.news/ronin-rekt | etherscan.io confirmed label
    "0x098B716B8Aaf21512996dC57EB0615e2383E2f96",  # Ronin Bridge Exploiter (primary)

    # Euler Finance Exploiter — March 2023
    # $197M flash loan attack. Funds initially sent through Tornado Cash.
    # Attacker later returned majority of funds after negotiations.
    # Source: rekt.news/euler-rekt
    "0xb66cd966670d962C227B3EABA30a872DbFb995db",  # Euler Finance Exploiter

    # Harmony Horizon Bridge Exploiter — June 2022
    # Lazarus Group (North Korea). ~$100M stolen.
    # Confirmed by FBI in January 2023.
    # Source: rekt.news/harmony-rekt
    "0x0d043128146654C7683Fbf30ac98D7B2285DeD00",  # Harmony Bridge Exploiter

    # Nomad Bridge Exploiter — August 2022
    # ~$190M chaotic free-for-all exploit.
    # One of the largest bridge hacks in DeFi history.
    # Source: rekt.news/nomad-rekt
    "0xB5C55f76f90Cc528B2609109Ca14d8d84593590E",  # Nomad Bridge Exploiter
]


# -----------------------------------------------------------------------------
# MASTER BLACKLIST
# Combined list used by the rest of the ChainSentinel tool.
# Import this in other modules: from blacklist import BLACKLIST
# -----------------------------------------------------------------------------

BLACKLIST = TORNADO_CASH_ADDRESSES + HACKER_WALLETS


# -----------------------------------------------------------------------------
# BLACKLIST METADATA
# Optional: human-readable labels for reporting/display purposes.
# Used in Phase 3 graph visualization to annotate red nodes.
# -----------------------------------------------------------------------------

BLACKLIST_LABELS = {
    # Tornado Cash Pools
    "0x12D66f87A04A9E220C9D9010cAe61B776352BC6a": "Tornado.Cash: 0.1 ETH",
    "0x47CE0C6eD5B0Ce3d3A51fdb1C52DC66a7c3c2936": "Tornado.Cash: 1 ETH",
    "0x910Cbd523D972eb0a6f4cAe4618aD62622b39DbF": "Tornado.Cash: 10 ETH",
    "0xA160cdAB225685dA1d56aa342Ad8841c3b53f291": "Tornado.Cash: 100 ETH",
    "0xD4B88Df4D29F5CedD6857912842cff3b20C8Cfa3": "Tornado.Cash: DAI 100",
    "0xFD8610d20aA15b7B2E3Be39B396a1bC3516c7144": "Tornado.Cash: DAI 1K",
    "0x07687e702b410Fa43f4cB4Af7FA097918ffD2730": "Tornado.Cash: DAI 10K",
    "0x23773E65ed146A459667494014f9422A91E84FC2": "Tornado.Cash: DAI 100K",
    "0x22aaA7720ddd5388A3c0A3333430953C68f1849b": "Tornado.Cash: cDAI 5K",
    "0xBA214C1c1928a32Bffe790263E38B4Af9bFCD659": "Tornado.Cash: cDAI 50K",
    "0xb1C8094B234DcE6e03f10a5b673c1d8C69739A00": "Tornado.Cash: cDAI 500K",
    "0xd96f2B1c14Db8458374d9Aca76E26c3950113463": "Tornado.Cash: USDC 100",
    "0x4736dCf1b7A3d580672CcE6E7c65cd5cc9cFBa9D": "Tornado.Cash: USDC 1K",
    "0xD691F27f38B395864Ea86CfC7253969B409c362d": "Tornado.Cash: USDT 100",
    "0xaEaaC358560e11f52454D997AAFF2c5731B6f8a6": "Tornado.Cash: USDT 1K",
    "0x178169B423a011fff22B9e3F3abeA13414dDD0F1": "Tornado.Cash: WBTC 0.1",
    "0x610B717796ad172B316836AC95a2ffad065CeaB4": "Tornado.Cash: WBTC 1",
    "0xbB93e510BbCD0B7beb5A853875f9eC60275CF498": "Tornado.Cash: WBTC 10",
    "0xd90e2f925DA726b50C4ED8D0Fb90Ad053324F31b": "Tornado.Cash: Router",
    "0x5efda50f22d34F262c29268506C5Fa42cB56A1Ce": "Tornado.Cash: Governance",
    "0x722122dF12D4e14e13Ac3b6895a86e84145b6967": "Tornado.Cash: Proxy",

    # Hacker Wallets
    "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7": "Drift Protocol Exploiter (2026)",
    "0x098B716B8Aaf21512996dC57EB0615e2383E2f96": "Ronin Bridge Exploiter / Lazarus Group (2022)",
    "0xb66cd966670d962C227B3EABA30a872DbFb995db": "Euler Finance Exploiter (2023)",
    "0x0d043128146654C7683Fbf30ac98D7B2285DeD00": "Harmony Bridge Exploiter / Lazarus Group (2022)",
    "0xB5C55f76f90Cc528B2609109Ca14d8d84593590E": "Nomad Bridge Exploiter (2022)",
}


# -----------------------------------------------------------------------------
# QUICK LOOKUP HELPER FUNCTION
# Other team members can call this instead of doing manual 'in' checks.
# -----------------------------------------------------------------------------

def is_blacklisted(address: str) -> bool:
    """
    Check if an Ethereum address is in the blacklist.
    Case-insensitive comparison.

    Args:
        address (str): Ethereum wallet address to check.

    Returns:
        bool: True if blacklisted, False otherwise.
    """
    return address.lower() in [a.lower() for a in BLACKLIST]


def get_label(address: str) -> str:
    """
    Get a human-readable label for a blacklisted address.

    Args:
        address (str): Ethereum wallet address.

    Returns:
        str: Label string, or 'Unknown Blacklisted Address' if not found.
    """
    for key, label in BLACKLIST_LABELS.items():
        if key.lower() == address.lower():
            return label
    return "Unknown Blacklisted Address"


# -----------------------------------------------------------------------------
# STATS (for reference)
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("ChainSentinel Blacklist — Summary")
    print("=" * 60)
    print(f"  Tornado Cash addresses : {len(TORNADO_CASH_ADDRESSES)}")
    print(f"  Hacker wallet addresses: {len(HACKER_WALLETS)}")
    print(f"  Total blacklisted      : {len(BLACKLIST)}")
    print("=" * 60)

    # Quick test
    test_addr = "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"
    print(f"\n  Test address : {test_addr}")
    print(f"  Blacklisted  : {is_blacklisted(test_addr)}")
    print(f"  Label        : {get_label(test_addr)}")
    print("=" * 60)
