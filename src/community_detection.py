import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import community as community_louvain
import os


EDGE_PATH = "data/edges/network_edges.csv"


def load_network():

    edge_df = pd.read_csv(EDGE_PATH)

    G = nx.Graph()

    for _, row in edge_df.iterrows():

        correlation = row["weight"]

        G.add_edge(
            row["source"],
            row["target"],
            weight=abs(correlation),
            correlation=correlation,
            relation_type="positive" if correlation > 0 else "negative"
        )

    print("Network yüklendi.")

    return G


def detect_communities(G):

    partition = community_louvain.best_partition(
        G,
        weight="weight",
        random_state=42
    )

    modularity = community_louvain.modularity(
        partition,
        G,
        weight="weight"
    )

    print("\nCOMMUNITY RESULTS")
    print("-" * 40)

    for node, community_id in partition.items():
        print(f"{node} -> Community {community_id}")

    print(f"\nModularity Score: {modularity:.4f}")

    return partition, modularity


def save_communities(partition):

    community_df = pd.DataFrame({
        "Node": partition.keys(),
        "Community": partition.values()
    })

    os.makedirs("outputs/metrics", exist_ok=True)

    community_df.to_csv(
        "outputs/metrics/community_results.csv",
        index=False
    )

    print("\nCommunity sonuçları kaydedildi.")


def visualize_communities(G, partition):

    os.makedirs("outputs/graphs", exist_ok=True)

    plt.figure(figsize=(18, 14))

    base_pos = nx.spring_layout(
        G,
        seed=42,
        k=1.4,
        weight="weight"
    )

    community_colors = {
        0: "#1f5a9d",
        1: "#008080",
        2: "#3f7f52",
        3: "#c43d3d",
    }

    community_labels = {
        0: "Topluluk 0: EUR_TRY, USD_TRY",
        1: "Topluluk 1: Dollar_Index, Gold, Silver",
        2: "Topluluk 2: DAX, Dow_Jones, FTSE100, NASDAQ, SP500, VIX",
        3: "Topluluk 3: Brent_Oil, WTI_Oil",
    }

    community_anchors = {
        0: (-2.2, 1.25),
        1: (-0.9, 0.15),
        2: (1.05, -0.65),
        3: (-2.2, -1.15),
    }

    pos = {}
    for node, (x, y) in base_pos.items():
        anchor_x, anchor_y = community_anchors.get(partition[node], (0, 0))
        pos[node] = (anchor_x + x * 0.65, anchor_y + y * 0.65)

    node_colors = [
        community_colors.get(partition[node], "#777777")
        for node in G.nodes()
    ]

    degree_centrality = nx.degree_centrality(G)

    node_sizes = [
        degree_centrality[node] * 9000 + 1000
        for node in G.nodes()
    ]

    positive_edges = [
        (u, v) for u, v in G.edges()
        if G[u][v]["correlation"] > 0
]

    negative_edges = [
        (u, v) for u, v in G.edges()
        if G[u][v]["correlation"] < 0
]

    positive_widths = [
        abs(G[u][v]["weight"]) * 8
        for u, v in positive_edges
    ]

    negative_widths = [
        abs(G[u][v]["weight"]) * 8
        for u, v in negative_edges
    ]

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors="black",
        linewidths=1.5,
        alpha=0.92
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=positive_edges,
        width=positive_widths,
        edge_color="red",
        alpha=0.6
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=negative_edges,
        width=negative_widths,
        edge_color="blue",
        alpha=0.6
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=9,
        font_weight="bold",
        font_color="black"
    )

    legend_items = [
        Line2D(
            [0],
            [0],
            marker="o",
            color="w",
            markerfacecolor=community_colors[community_id],
            markeredgecolor="black",
            markersize=10,
            label=community_labels[community_id]
        )
        for community_id in sorted(community_colors)
    ]

    edge_items = [
        Line2D([0], [0], color="red", lw=2.5, label="Pozitif korelasyon"),
        Line2D([0], [0], color="blue", lw=2.5, label="Negatif korelasyon"),
    ]

    plt.legend(
        handles=legend_items + edge_items,
        loc="lower left",
        frameon=True,
        fontsize=9
    )

    plt.title(
        "Finansal Varlik Topluluk Agi\n"
        "Renkler Louvain yontemiyle bulunan 4 toplulugu gosterir",
        fontsize=18
    )

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        "outputs/graphs/community_network.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("\nCommunity graph oluşturuldu.")


if __name__ == "__main__":

    G = load_network()

    partition, modularity = detect_communities(G)

    save_communities(partition)

    visualize_communities(G, partition)




    
