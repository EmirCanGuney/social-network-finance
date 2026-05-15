import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os


CORRELATION_PATH = "outputs/metrics/correlation_matrix.csv"

THRESHOLD = 0.4


def load_correlation_matrix():

    corr_matrix = pd.read_csv(
        CORRELATION_PATH,
        index_col=0
    )

    print("Korelasyon matrisi yüklendi.")
    print(corr_matrix.head())

    return corr_matrix


def create_network(corr_matrix):

    G = nx.Graph()

    assets = corr_matrix.columns

    for asset in assets:
        G.add_node(asset)

    for i in range(len(assets)):
        for j in range(i + 1, len(assets)):

            asset_1 = assets[i]
            asset_2 = assets[j]

            correlation = corr_matrix.iloc[i, j]

            if abs(correlation) > THRESHOLD:

                G.add_edge(
                    asset_1,
                    asset_2,
                    weight=correlation
                )

    print("\nNetwork oluşturuldu.")
    print(f"Node sayısı: {G.number_of_nodes()}")
    print(f"Edge sayısı: {G.number_of_edges()}")

    return G


def save_edge_list(G):

    os.makedirs("data/edges", exist_ok=True)

    edge_list = nx.to_pandas_edgelist(G)

    edge_list.to_csv(
        "data/edges/network_edges.csv",
        index=False
    )

    print("\nEdge list kaydedildi.")

def visualize_network(G):

    os.makedirs("outputs/graphs", exist_ok=True)

    plt.figure(figsize=(20, 14))

    pos = nx.spring_layout(
        G,
        seed=42,
        k=1.3,
        iterations=100
)

    degree_centrality = nx.degree_centrality(G)

    node_sizes = [
        degree_centrality[node] * 9000 + 1000
        for node in G.nodes()
    ]

    node_colors = [
        degree_centrality[node]
        for node in G.nodes()
    ]

    positive_edges = [
        (u, v) for u, v in G.edges()
        if G[u][v]["weight"] > 0
    ]

    negative_edges = [
        (u, v) for u, v in G.edges()
        if G[u][v]["weight"] < 0
    ]

    positive_widths = [
        abs(G[u][v]["weight"]) * 8
        for u, v in positive_edges
    ]

    negative_widths = [
        abs(G[u][v]["weight"]) * 8
        for u, v in negative_edges
    ]

    nodes = nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=node_colors,
        cmap=plt.cm.plasma,
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
        alpha=0.65,
        label="Pozitif korelasyon"
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=negative_edges,
        width=negative_widths,
        edge_color="blue",
        alpha=0.65,
        label="Negatif korelasyon"
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=9,
        font_weight="bold",
        font_color="black"
    )

    edge_labels = {
        (u, v): f"{G[u][v]['weight']:.2f}"
        for u, v in G.edges()
    }

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=8,
        bbox=dict(
            facecolor="white",
            edgecolor="none",
            alpha=0.7
        )
    )

    cbar = plt.colorbar(nodes)
    cbar.set_label(
        "Degree Centrality",
        fontsize=12
    )

    plt.legend(
        loc="upper right",
        fontsize=11,
        frameon=True
    )

    plt.title(
        "Financial Asset Correlation Network\n"
        "Node Size & Color: Degree Centrality | Edge Width: Correlation Strength",
        fontsize=18
    )

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        "outputs/graphs/network_graph_enhanced.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print("\nGeliştirilmiş network graph oluşturuldu.")


if __name__ == "__main__":

    corr_matrix = load_correlation_matrix()

    G = create_network(corr_matrix)

    save_edge_list(G)

    visualize_network(G)