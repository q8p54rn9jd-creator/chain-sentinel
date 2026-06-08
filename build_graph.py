# build_graph.py — Phase 3
# Builds a directed graph from the transaction table
# Each wallet = one node. Each transaction = one arrow (from → to)

import networkx as nx
import matplotlib.pyplot as plt
from fetch_transcation import fetch_transactions
from clean_data import clean_transactions

def build_graph(df):
    G = nx.DiGraph()  # directed graph

    for _, row in df.iterrows():
        sender   = row["from"]
        receiver = row["to"]
        amount   = row["amount_eth"]

        # Add both wallets as nodes (if not already there)
        if not G.has_node(sender):
            G.add_node(sender)
        if not G.has_node(receiver):
            G.add_node(receiver)

        # Add arrow from sender to receiver
        G.add_edge(sender, receiver, weight=amount)

    return G


def draw_graph(G, address):
    plt.figure(figsize=(14, 10))

    # Layout
    pos = nx.spring_layout(G, seed=42)

    # All nodes grey by default
    node_colors = ["red" if node == address.lower() else "lightgrey" for node in G.nodes()]

    nx.draw(
        G, pos,
        node_color=node_colors,
        with_labels=False,
        node_size=300,
        arrows=True,
        arrowsize=15,
        edge_color="steelblue",
        width=1,
    )

    # Short labels (first 6 + last 4 characters)
    labels = {node: f"{node[:6]}...{node[-4:]}" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=6, font_color="black")

    plt.title(f"Transaction Graph — {address[:10]}...{address[-6:]}")
    plt.tight_layout()
    plt.savefig("graph.png")
    plt.show()
    print("Graph saved as graph.png")


if __name__ == "__main__":
    address = "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"

    df = fetch_transactions(address)
    df = clean_transactions(df)

    G = build_graph(df)

    print(f"Nodes (unique wallets) : {G.number_of_nodes()}")
    print(f"Edges (transactions)   : {G.number_of_edges()}")

    draw_graph(G, address)