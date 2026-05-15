import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
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
        G
    )

    modularity = community_louvain.modularity(
        partition,
        G
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

    pos = nx.spring_layout(
        G,
        seed=42,
        k=1.3
    )

    communities = list(set(partition.values()))

    color_map = plt.cm.Set3

    node_colors = [
        color_map(partition[node] / len(communities))
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
        font_weight="bold"
    )

    plt.title(
        "Financial Asset Community Network\n"
        "Node Colors Represent Communities",
        fontsize=18
    )

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        "outputs/graphs/community_network.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print("\nCommunity graph oluşturuldu.")


if __name__ == "__main__":

    G = load_network()

    partition, modularity = detect_communities(G)

    save_communities(partition)

    visualize_communities(G, partition)




    