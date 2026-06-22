import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

def build_fraud_graph():
    G = nx.DiGraph()

    # Scammer phone numbers
    scammer_nodes = ["Phone: +91-9876XXXX01", "Phone: +91-9876XXXX02", "Phone: +91-9876XXXX03"]
    # Bank mule accounts
    bank_nodes = ["Mule Acc: HDFC-XXX1", "Mule Acc: SBI-XXX2", "Mule Acc: ICICI-XXX3"]
    # Victims
    victim_nodes = [f"Victim {i+1}" for i in range(7)]
    # Master controller
    controller = "Controller Node\n(Fraud Ring HQ)"

    for n in scammer_nodes:
        G.add_node(n, type="scammer")
    for n in bank_nodes:
        G.add_node(n, type="bank")
    for n in victim_nodes:
        G.add_node(n, type="victim")
    G.add_node(controller, type="controller")

    # Controller to scammers
    for s in scammer_nodes:
        G.add_edge(controller, s, label="directs")

    # Scammers to victims
    G.add_edge(scammer_nodes[0], victim_nodes[0], label="called")
    G.add_edge(scammer_nodes[0], victim_nodes[1], label="called")
    G.add_edge(scammer_nodes[0], victim_nodes[2], label="called")
    G.add_edge(scammer_nodes[1], victim_nodes[3], label="called")
    G.add_edge(scammer_nodes[1], victim_nodes[4], label="called")
    G.add_edge(scammer_nodes[2], victim_nodes[5], label="called")
    G.add_edge(scammer_nodes[2], victim_nodes[6], label="called")

    # Victims to bank accounts (money flow)
    G.add_edge(victim_nodes[0], bank_nodes[0], label="transferred")
    G.add_edge(victim_nodes[1], bank_nodes[0], label="transferred")
    G.add_edge(victim_nodes[2], bank_nodes[1], label="transferred")
    G.add_edge(victim_nodes[3], bank_nodes[1], label="transferred")
    G.add_edge(victim_nodes[4], bank_nodes[2], label="transferred")
    G.add_edge(victim_nodes[5], bank_nodes[2], label="transferred")
    G.add_edge(victim_nodes[6], bank_nodes[0], label="transferred")

    # Bank accounts back to controller
    for b in bank_nodes:
        G.add_edge(b, controller, label="laundered")

    return G


def draw_fraud_graph():
    G = build_fraud_graph()

    color_map = {
        "controller": "#e74c3c",
        "scammer": "#e67e22",
        "bank": "#8e44ad",
        "victim": "#2980b9"
    }

    node_colors = [color_map[G.nodes[n]["type"]] for n in G.nodes()]

    pos = nx.spring_layout(G, seed=42, k=2.5)

    fig, ax = plt.subplots(figsize=(14, 9))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1800, ax=ax, alpha=0.95)
    nx.draw_networkx_labels(G, pos, font_size=6.5, font_color="white", ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color="#aaaaaa", arrows=True,
                           arrowsize=15, width=1.5, ax=ax,
                           connectionstyle="arc3,rad=0.1")

    legend_items = [
        mpatches.Patch(color="#e74c3c", label="Fraud Ring Controller"),
        mpatches.Patch(color="#e67e22", label="Scammer Phone"),
        mpatches.Patch(color="#8e44ad", label="Mule Bank Account"),
        mpatches.Patch(color="#2980b9", label="Victim"),
    ]
    ax.legend(handles=legend_items, loc="upper left",
              facecolor="#161b22", labelcolor="white", fontsize=9)

    ax.set_title("SentinelAI — Fraud Network Intelligence Graph",
                 color="white", fontsize=13, pad=12)
    ax.axis("off")
    plt.tight_layout()
    return fig