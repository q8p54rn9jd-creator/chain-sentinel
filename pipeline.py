# pipeline.py — Om's Phase 3 contribution
# End-to-end test: Drift exploiter → risk score → graph

import os
import networkx as nx
from Risk_score import compute_risk_score
from build_graph import draw_graph
from fetch_transcation import fetch_transactions
from clean_data import clean_transactions
from blacklist import BLACKLIST

DRIFT_EXPLOITER = "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"

if __name__ == "__main__":
    # Step 1: Print risk score
    compute_risk_score(DRIFT_EXPLOITER)

    # Step 2: Build graph manually and draw
    df = fetch_transactions(DRIFT_EXPLOITER)
    df = clean_transactions(df)

    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row["from"], row["to"], weight=row["amount_eth"])

    draw_graph(G, DRIFT_EXPLOITER)

    # Step 3: Open the graph image
    os.startfile(os.path.abspath("graph.png"))