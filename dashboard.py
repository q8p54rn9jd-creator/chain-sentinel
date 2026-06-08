"""
dashboard.py — ChainSentinel Interactive Dashboard
Run: python dashboard.py
Open: http://localhost:8050
"""

import pandas as pd
import networkx as nx
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_cytoscape as cyto

from fetch_transcation import fetch_transactions
from clean_data import clean_transactions
from blacklist import is_blacklisted, get_label, BLACKLIST
from check_burst import check_burst_dispersion
from wallet_age_check import check_wallet_age

cyto.load_extra_layouts()
app = dash.Dash(__name__, title="ChainSentinel", suppress_callback_exceptions=True)
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>ChainSentinel</title>
        {%favicon%}
        {%css%}
        <style>
            input::placeholder { color: #334155 !important; }
            * { box-sizing: border-box; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# ── CYTOSCAPE STYLESHEET ──────────────────────────────────────────────────────
STYLESHEET = [
    {
        "selector": "node",
        "style": {
            "background-color": "data(color)",
            "label": "data(label)",
            "color": "#e2e8f0",
            "font-size": "9px",
            "font-family": "monospace",
            "text-valign": "bottom",
            "text-margin-y": "4px",
            "width": "25px",
            "height": "25px",
            "border-width": "2px",
            "border-color": "#1e2d45",
        }
    },
    {
        "selector": "node[category = 'seed']",
        "style": {
            "width": "38px", "height": "38px",
            "border-color": "#ef4444", "border-width": "3px",
        }
    },
    {
        "selector": "node[category = 'blacklisted']",
        "style": {
            "border-color": "#ef4444", "border-width": "3px",
        }
    },
    {
        "selector": "edge",
        "style": {
            "line-color": "#334155",
            "target-arrow-color": "#334155",
            "target-arrow-shape": "triangle",
            "curve-style": "bezier",
            "width": 1.5,
        }
    },
]

# ── LAYOUT ────────────────────────────────────────────────────────────────────
app.layout = html.Div(
    style={
        "background": "#05080f",
        "minHeight": "100vh",
        "fontFamily": "monospace",
        "color": "#e2e8f0",
    },
    children=[

        # Top bar
        html.Div(
            style={
                "background": "#0a0f1a",
                "borderBottom": "1px solid #1e2d45",
                "padding": "1rem 2rem",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
            },
            children=[
                html.Div(
                    style={"display": "flex", "alignItems": "center", "gap": "1rem"},
                    children=[
                        html.Div(style={
                            "width": "10px", "height": "10px",
                            "borderRadius": "50%", "background": "#ef4444",
                        }),
                        html.Span("ChainSentinel",
                                  style={"color": "#22d3ee", "fontWeight": "bold", "fontSize": "1.1rem"}),
                        html.Span("/ On-Chain Fraud Detection",
                                  style={"color": "#475569", "fontSize": "0.8rem"}),
                    ]
                ),
                html.Span("ETHEREUM MAINNET",
                          style={"color": "#475569", "fontSize": "0.7rem", "letterSpacing": "0.1em"}),
            ]
        ),

        # Search bar
        html.Div(
            style={"padding": "1.5rem 2rem"},
            children=[
                html.Div(
                    style={"display": "flex", "gap": "0.75rem", "flexWrap": "wrap"},
                    children=[
                        dcc.Input(
                            id="address-input",
                            type="text",
                            placeholder="Enter Ethereum wallet address (0x...)",
                            style={
                                "flex": "1", "minWidth": "320px",
                                "background": "#0a0f1a",
                                "border": "1px solid #1e2d45",
                                "borderRadius": "4px",
                                "color": "#e2e8f0",
                                "padding": "0.65rem 1rem",
                                "fontFamily": "monospace",
                                "fontSize": "0.85rem",
                                "outline": "none",
                            }
                        ),
                        html.Button(
                            "INVESTIGATE",
                            id="investigate-btn",
                            n_clicks=0,
                            style={
                                "background": "rgba(34,211,238,0.1)",
                                "border": "1px solid rgba(34,211,238,0.4)",
                                "borderRadius": "4px",
                                "color": "#22d3ee",
                                "padding": "0.65rem 1.5rem",
                                "fontFamily": "monospace",
                                "fontSize": "0.75rem",
                                "cursor": "pointer",
                                "fontWeight": "bold",
                                "letterSpacing": "0.1em",
                            }
                        ),
                        html.Button(
                            "▶ DEMO: DRIFT EXPLOITER",
                            id="demo-btn",
                            n_clicks=0,
                            style={
                                "background": "rgba(239,68,68,0.1)",
                                "border": "1px solid rgba(239,68,68,0.4)",
                                "borderRadius": "4px",
                                "color": "#ef4444",
                                "padding": "0.65rem 1.5rem",
                                "fontFamily": "monospace",
                                "fontSize": "0.75rem",
                                "cursor": "pointer",
                                "fontWeight": "bold",
                                "letterSpacing": "0.1em",
                            }
                        ),
                    ]
                ),
                html.Div(id="status-msg",
                         style={"marginTop": "0.5rem", "fontSize": "0.72rem", "color": "#475569"}),
            ]
        ),

        # Main content
        html.Div(id="main-content", style={"padding": "0 2rem 3rem"}),

        # Store
        dcc.Store(id="data-store"),
    ]
)


# ── FILL DEMO ADDRESS ─────────────────────────────────────────────────────────
@app.callback(
    Output("address-input", "value"),
    Input("demo-btn", "n_clicks"),
    prevent_initial_call=True,
)
def fill_demo(_):
    return "0xD3FEEd5DA83D8e8c449d6CB96ff1eb06ED1cF6C7"


# ── RUN ANALYSIS ──────────────────────────────────────────────────────────────
@app.callback(
    Output("data-store", "data"),
    Output("status-msg", "children"),
    Input("investigate-btn", "n_clicks"),
    State("address-input", "value"),
    prevent_initial_call=True,
)
def run_analysis(_, address):
    if not address or not address.strip().startswith("0x"):
        return None, "⚠ Enter a valid Ethereum address (0x...)"

    address = address.strip()

    # Fetch + clean
    raw_df   = fetch_transactions(address)
    clean_df = clean_transactions(raw_df)

    # Checks
    blacklisted = is_blacklisted(address)
    label       = get_label(address) if blacklisted else ""
    burst_flag, burst_msg = check_burst_dispersion(clean_df, address)
    age_result  = check_wallet_age(address)

    # Flags list
    flags = []
    if blacklisted:
        flags.append({"name": "BLACKLISTED", "severity": "HIGH",
                      "detail": label})
    if burst_flag:
        flags.append({"name": "BURST DISPERSION", "severity": "HIGH",
                      "detail": burst_msg})
    if age_result.get("is_fresh"):
        flags.append({"name": "FRESH WALLET", "severity": "MEDIUM",
                      "detail": age_result.get("flag_reason", "")})

    # Score
    score_map = {"HIGH": 30, "MEDIUM": 15, "LOW": 5}
    score     = min(sum(score_map.get(f["severity"], 0) for f in flags), 100)
    level     = ("CRITICAL" if score >= 75 else
                 "HIGH"     if score >= 50 else
                 "MEDIUM"   if score >= 25 else
                 "LOW"      if score > 0  else "CLEAN")

    # Graph elements
    elements = build_cyto_elements(clean_df, address)

    # TX table
    tx_rows = []
    for _, row in clean_df.head(30).iterrows():
        tx_rows.append({
            "from":   row["from"][:10] + "...",
            "to":     row["to"][:10] + "...",
            "ETH":    round(row["amount_eth"], 4),
            "date":   row["date"],
        })

    status = f"// {len(clean_df)} transactions fetched — {len(flags)} flag(s) triggered"

    return {
        "address":  address,
        "score":    score,
        "level":    level,
        "flags":    flags,
        "elements": elements,
        "tx_rows":  tx_rows,
        "age_days": age_result.get("wallet_age_days"),
    }, status


# ── RENDER DASHBOARD ──────────────────────────────────────────────────────────
@app.callback(
    Output("main-content", "children"),
    Input("data-store", "data"),
    prevent_initial_call=True,
)
def render(data):
    if not data:
        return ""

    score   = data["score"]
    level   = data["level"]
    flags   = data["flags"]
    address = data["address"]
    tx_rows = data["tx_rows"]
    elements= data["elements"]

    level_colors = {
        "CRITICAL": "#ef4444",
        "HIGH":     "#f97316",
        "MEDIUM":   "#f59e0b",
        "LOW":      "#22d3ee",
        "CLEAN":    "#4ade80",
    }
    lc = level_colors.get(level, "#475569")

    return html.Div([

        # Row 1: Score + Flags
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "200px 1fr",
                   "gap": "1rem", "marginBottom": "1rem"},
            children=[

                # Score box
                html.Div(
                    style={
                        "background": "#0a0f1a",
                        "border": f"1px solid {lc}44",
                        "borderRadius": "4px",
                        "padding": "1.5rem",
                        "textAlign": "center",
                    },
                    children=[
                        html.Div("RISK SCORE", style={
                            "fontSize": "0.6rem", "letterSpacing": "0.2em",
                            "color": "#475569", "marginBottom": "0.5rem"
                        }),
                        html.Div(str(score), style={
                            "fontSize": "3.5rem", "fontWeight": "bold",
                            "color": lc, "lineHeight": "1"
                        }),
                        html.Div("/ 100", style={
                            "fontSize": "0.75rem", "color": "#475569",
                            "marginBottom": "0.75rem"
                        }),
                        html.Span(level, style={
                            "fontSize": "0.7rem", "fontWeight": "bold",
                            "color": lc,
                            "border": f"1px solid {lc}55",
                            "background": f"{lc}11",
                            "padding": "0.2rem 0.6rem",
                            "borderRadius": "3px",
                        }),
                        html.Div(
                            f"{address[:8]}...{address[-6:]}",
                            style={"fontSize": "0.6rem", "color": "#22d3ee",
                                   "marginTop": "1rem", "wordBreak": "break-all"}
                        ),
                    ]
                ),

                # Flags
                html.Div(
                    style={
                        "background": "#0a0f1a",
                        "border": "1px solid #1e2d45",
                        "borderRadius": "4px",
                        "padding": "1.25rem",
                        "overflowY": "auto",
                        "maxHeight": "220px",
                    },
                    children=[
                        html.Div("TRIGGERED FLAGS", style={
                            "fontSize": "0.6rem", "letterSpacing": "0.2em",
                            "color": "#475569", "marginBottom": "1rem"
                        }),
                        html.Div([flag_card(f) for f in flags]) if flags else
                        html.Div("✓ No suspicious flags detected.",
                                 style={"color": "#4ade80", "fontSize": "0.85rem"}),
                    ]
                ),
            ]
        ),

        # Row 2: Graph + Stats
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 260px",
                   "gap": "1rem", "marginBottom": "1rem"},
            children=[

                # Graph
                html.Div(
                    style={
                        "background": "#0a0f1a",
                        "border": "1px solid #1e2d45",
                        "borderRadius": "4px",
                        "overflow": "hidden",
                    },
                    children=[
                        html.Div(
                            style={"padding": "0.65rem 1.25rem",
                                   "borderBottom": "1px solid #1e2d45",
                                   "fontSize": "0.6rem", "letterSpacing": "0.15em",
                                   "color": "#475569",
                                   "display": "flex", "justifyContent": "space-between"},
                            children=[
                                html.Span("TRANSACTION GRAPH"),
                                html.Span("drag · scroll to zoom · click node for details",
                                          style={"fontSize": "0.58rem"}),
                            ]
                        ),
                        cyto.Cytoscape(
                            id="cyto-graph",
                            elements=elements,
                            style={"width": "100%", "height": "440px", "background": "#05080f"},
                            layout={"name": "cose", "animate": True,
                                    "nodeRepulsion": 8000, "componentSpacing": 80},
                            stylesheet=STYLESHEET,
                            responsive=True,
                        ),
                        # Legend
                        html.Div(
                            style={"padding": "0.65rem 1.25rem",
                                   "borderTop": "1px solid #1e2d45",
                                   "display": "flex", "gap": "1.5rem", "flexWrap": "wrap"},
                            children=[
                                legend_dot("#ef4444", "Seed / Blacklisted"),
                                legend_dot("#22d3ee", "Connected Wallet"),
                            ]
                        ),
                    ]
                ),

                # Stats
                html.Div(
                    style={
                        "background": "#0a0f1a",
                        "border": "1px solid #1e2d45",
                        "borderRadius": "4px",
                        "padding": "1.25rem",
                    },
                    children=[
                        html.Div("WALLET STATS", style={
                            "fontSize": "0.6rem", "letterSpacing": "0.2em",
                            "color": "#475569", "marginBottom": "1rem"
                        }),
                        stat_row("Wallet age", f"{data.get('age_days', '?')} days"),
                        stat_row("Transactions", str(len(tx_rows))),
                        stat_row("Flags", str(len(flags))),
                        stat_row("Risk level", level),
                        html.Div(style={"marginTop": "1rem", "paddingTop": "1rem",
                                        "borderTop": "1px solid #1e2d45"},
                                 children=[
                            html.A(
                                "View on Etherscan →",
                                href=f"https://etherscan.io/address/{address}",
                                target="_blank",
                                style={"color": "#22d3ee", "fontSize": "0.72rem",
                                       "textDecoration": "none", "display": "block",
                                       "marginBottom": "0.5rem"}
                            ),
                            html.A(
                                "View on Arkham →",
                                href=f"https://arkhamintelligence.com/explorer/address/{address}",
                                target="_blank",
                                style={"color": "#22d3ee", "fontSize": "0.72rem",
                                       "textDecoration": "none", "display": "block"}
                            ),
                        ]),
                    ]
                ),
            ]
        ),

        # Node click info
        html.Div(id="node-info", style={"marginBottom": "1rem"}),

        # Transaction table
        html.Div(
            style={
                "background": "#0a0f1a",
                "border": "1px solid #1e2d45",
                "borderRadius": "4px",
            },
            children=[
                html.Div("TRANSACTION HISTORY", style={
                    "padding": "0.65rem 1.25rem",
                    "borderBottom": "1px solid #1e2d45",
                    "fontSize": "0.6rem", "letterSpacing": "0.15em", "color": "#475569",
                }),
                html.Div(
                    style={"padding": "1rem"},
                    children=[
                        dash_table.DataTable(
                            data=tx_rows,
                            columns=[{"name": c, "id": c} for c in ["from", "to", "ETH", "date"]],
                            page_size=10,
                            sort_action="native",
                            style_table={"overflowX": "auto"},
                            style_header={
                                "backgroundColor": "#0f1624",
                                "color": "#64748b",
                                "fontFamily": "monospace",
                                "fontSize": "0.65rem",
                                "letterSpacing": "0.1em",
                                "textTransform": "uppercase",
                                "border": "1px solid #1e2d45",
                            },
                            style_cell={
                                "backgroundColor": "#0a0f1a",
                                "color": "#94a3b8",
                                "fontFamily": "monospace",
                                "fontSize": "0.72rem",
                                "border": "1px solid #1e2d45",
                                "padding": "6px 10px",
                                "textAlign": "left",
                            },
                        ) if tx_rows else
                        html.Div("No transactions.",
                                 style={"color": "#475569", "fontSize": "0.8rem"})
                    ]
                )
            ]
        ),
    ])


@app.callback(
    Output("node-info", "children"),
    Input("cyto-graph", "tapNodeData"),
    prevent_initial_call=True,
)
def node_click(node_data):
    if not node_data:
        return ""
    addr  = node_data.get("full_addr", "")
    color = node_data.get("color", "#475569")
    cat   = node_data.get("category", "").upper()
    return html.Div(
        style={
            "background": "#0a0f1a",
            "border": f"1px solid {color}44",
            "borderRadius": "4px",
            "padding": "0.75rem 1.25rem",
            "fontFamily": "monospace",
        },
        children=[
            html.Span("SELECTED  ", style={"fontSize": "0.6rem", "color": "#475569"}),
            html.Span(cat, style={"fontSize": "0.6rem", "color": color,
                                   "border": f"1px solid {color}44",
                                   "padding": "0.1rem 0.4rem", "borderRadius": "2px"}),
            html.Div(addr, style={"fontSize": "0.8rem", "marginTop": "0.4rem",
                                   "wordBreak": "break-all", "color": "#e2e8f0"}),
            html.A("View on Etherscan →",
                   href=f"https://etherscan.io/address/{addr}", target="_blank",
                   style={"fontSize": "0.7rem", "color": "#22d3ee",
                          "textDecoration": "none", "display": "block", "marginTop": "0.3rem"}),
        ]
    )


# ── HELPERS ───────────────────────────────────────────────────────────────────

def build_cyto_elements(df, address):
    address = address.lower()
    elements = []
    seen_nodes = set()

    def add_node(addr):
        if addr in seen_nodes:
            return
        seen_nodes.add(addr)
        if addr == address:
            color, cat = "#ef4444", "seed"
        elif is_blacklisted(addr):
            color, cat = "#ef4444", "blacklisted"
        else:
            color, cat = "#22d3ee", "normal"
        elements.append({
            "data": {
                "id":       addr,
                "label":    addr[:6] + "..." + addr[-4:],
                "color":    color,
                "category": cat,
                "full_addr": addr,
            }
        })

    if df.empty:
        add_node(address)
        return elements

    for i, (_, row) in enumerate(df.iterrows()):
        src = str(row.get("from", "")).lower()
        dst = str(row.get("to", "")).lower()
        if not src or not dst:
            continue
        add_node(src)
        add_node(dst)
        elements.append({
            "data": {
                "id":     f"e{i}",
                "source": src,
                "target": dst,
                "weight": round(row.get("amount_eth", 0), 4),
            }
        })

    return elements


def flag_card(flag):
    sev_colors = {"HIGH": "#ef4444", "MEDIUM": "#f59e0b", "LOW": "#22d3ee"}
    c = sev_colors.get(flag["severity"], "#475569")
    return html.Div(
        style={
            "marginBottom": "0.5rem",
            "padding": "0.6rem 0.75rem",
            "background": f"{c}0d",
            "border": f"1px solid {c}33",
            "borderLeft": f"3px solid {c}",
            "borderRadius": "2px",
        },
        children=[
            html.Div(
                style={"display": "flex", "justifyContent": "space-between",
                       "marginBottom": "0.2rem"},
                children=[
                    html.Span(flag["name"],
                              style={"fontSize": "0.75rem", "fontWeight": "bold", "color": c}),
                    html.Span(flag["severity"],
                              style={"fontSize": "0.6rem", "color": c,
                                     "border": f"1px solid {c}44",
                                     "padding": "0.1rem 0.3rem", "borderRadius": "2px"}),
                ]
            ),
            html.Div(flag.get("detail", ""),
                     style={"fontSize": "0.68rem", "color": "#64748b"}),
        ]
    )


def stat_row(label, value):
    return html.Div(
        style={"display": "flex", "justifyContent": "space-between",
               "padding": "0.35rem 0", "borderBottom": "1px solid #1e2d45"},
        children=[
            html.Span(label, style={"fontSize": "0.7rem", "color": "#64748b"}),
            html.Span(value, style={"fontSize": "0.75rem", "fontWeight": "bold"}),
        ]
    )


def legend_dot(color, label):
    return html.Div(
        style={"display": "flex", "alignItems": "center", "gap": "0.4rem"},
        children=[
            html.Div(style={"width": "10px", "height": "10px",
                             "borderRadius": "50%", "background": color}),
            html.Span(label, style={"fontSize": "0.65rem", "color": "#64748b"}),
        ]
    )


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════╗
║  ChainSentinel Dashboard                             ║
║  Open: http://localhost:8050                         ║
║  Click 'DEMO: DRIFT EXPLOITER' to see a live demo   ║
╚══════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host="0.0.0.0", port=8050)