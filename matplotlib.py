# draw_graph.py — Benedicta's Phase 3 contribution
# Draws the transaction graph and saves it as graph.png

import matplotlib
matplotlib.use("Agg")  # non-interactive backend — works without a display

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

from fetch_transcation import fetch_transactions
from clean_data import clean_transactions
from blacklist import is_blacklisted


def shorten(address: str) -> str:
    """Returns first 6 + last 4 characters of an address e.g. 0xD3FE...F6C7"""
    address = str(address)
    if len(address) <= 10:
        return address
    return f"{address[:6]}...{address[-4:]}"


def draw_transaction_graph(wallet_address: str, output_file: str = "graph.png") -> None:
    """
    Builds a directed graph from transaction data and saves it as a PNG.

    Node colours:
        🔵 Blue  — the wallet being investigated
        🔴 Red   — any blacklisted address
        ⚫ Grey  — everyone else
    """

    # ── Fetch & clean data ───────────────────────────────────────────────────
    print(f"Fetching transactions for: {wallet_address}")
    raw_df   = fetch_transactions(wallet_address)
    clean_df = clean_transactions(raw_df)

    if clean_df.empty:
        print("No transactions found — cannot draw graph.")
        return

    # ── Build directed graph ─────────────────────────────────────────────────
    G = nx.DiGraph()

    for _, tx in clean_df.iterrows():
        sender   = str(tx.get("from", "")).lower()
        receiver = str(tx.get("to",   "")).lower()

        if sender and receiver:
            G.add_node(sender)
            G.add_node(receiver)
            G.add_edge(sender, receiver)

    # ── Assign node colours ──────────────────────────────────────────────────
    investigated = wallet_address.lower()
    node_colors  = []

    for node in G.nodes():
        if node == investigated:
            node_colors.append("#2196F3")       # blue  — wallet under investigation
        elif is_blacklisted(node):
            node_colors.append("#F44336")       # red   — blacklisted
        else:
            node_colors.append("#9E9E9E")       # grey  — everyone else

    # ── Shorten labels for readability ───────────────────────────────────────
    labels = {node: shorten(node) for node in G.nodes()}

    # ── Layout & draw ────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor("#0F1923")
    ax.set_facecolor("#0F1923")

    pos = nx.spring_layout(G, seed=42, k=2.5)

    # Draw edges
    nx.draw_networkx_edges(
        G, pos,
        ax=ax,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=18,
        edge_color="#AAAAAA",
        alpha=0.6,
        width=1.2,
        connectionstyle="arc3,rad=0.08",
        min_source_margin=18,
        min_target_margin=18,
    )

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        ax=ax,
        node_color=node_colors,
        node_size=800,
        alpha=0.95,
    )

    # Draw labels
    nx.draw_networkx_labels(
        G, pos,
        labels=labels,
        ax=ax,
        font_size=7.5,
        font_color="#FFFFFF",
        font_weight="bold",
    )

    # ── Title & legend ───────────────────────────────────────────────────────
    ax.set_title(
        f"ChainSentinel — Transaction Graph\n{shorten(wallet_address)}",
        color="#FFFFFF", fontsize=14, fontweight="bold", pad=16
    )

    legend_handles = [
        mpatches.Patch(color="#2196F3", label="Investigated Wallet"),
        mpatches.Patch(color="#F44336", label="Blacklisted Address"),
        mpatches.Patch(color="#9E9E9E", label="Other Wallet"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower left",
        fontsize=9,
        facecolor="#1A2B3C",
        edgecolor="#444444",
        labelcolor="#FFFFFF",
    )

    ax.axis("off")
    plt.tight_layout()

    # ── Save ─────────────────────────────────────────────────────────────────
    plt.savefig(output_file, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()

    print(f"Graph saved as: {output_file}")
    print(f"Nodes (wallets)   : {G.number_of_nodes()}")
    print(f"Edges (transactions): {G.number_of_edges()}")


# ── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    address = "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"
    draw_transaction_graph(address, output_file="graph.png")
