import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os

ALL_NODES = [
    "Gold",
    "Silver",
    "Brent_Oil",
    "WTI_Oil",
    "Natural_Gas",
    "SP500",
    "NASDAQ",
    "Dow_Jones",
    "DAX",
    "FTSE100",
    "Nikkei225",
    "BIST100",
    "USD_TRY",
    "EUR_TRY",
    "Bitcoin",
    "VIX",
    "US_10Y_Bond",
    "Dollar_Index"
]

EDGE_PATH = "data/edges/network_edges.csv"


def load_network():

    edge_df = pd.read_csv(EDGE_PATH)

    G = nx.Graph()

    G.add_nodes_from(ALL_NODES)

    for _, row in edge_df.iterrows():

        G.add_edge(
            row["source"],
            row["target"],
            weight=row["weight"]
        )

    print("Network yüklendi.")
    print(f"Node sayısı: {G.number_of_nodes()}")
    print(f"Edge sayısı: {G.number_of_edges()}")

    return G

def calculate_metrics(G):

    metrics = pd.DataFrame()

    metrics["Degree_Centrality"] = pd.Series(
        nx.degree_centrality(G)
    )

    metrics["Betweenness_Centrality"] = pd.Series(
        nx.betweenness_centrality(
            G,
            weight="weight"
        )
    )

    metrics["Closeness_Centrality"] = pd.Series(
        nx.closeness_centrality(G)
    )

    metrics["Eigenvector_Centrality"] = pd.Series(
        nx.eigenvector_centrality(
            G,
            max_iter=1000
        )
    )

    metrics["Clustering_Coefficient"] = pd.Series(
        nx.clustering(
            G
        )
    )

    return metrics


def calculate_global_metrics(G):

    density = nx.density(G)

    average_degree = (
        2 * G.number_of_edges() / G.number_of_nodes()
        if G.number_of_nodes() > 0
        else 0
    )

    avg_clustering = nx.average_clustering(G)

    components = list(nx.connected_components(G))

    connected_components = len(components)

    largest_component = (
        G.subgraph(max(components, key=len)).copy()
        if components
        else nx.Graph()
    )

    largest_component_size = largest_component.number_of_nodes()

    diameter = (
        nx.diameter(largest_component)
        if largest_component.number_of_nodes() > 1
        else 0
    )

    print("\nGLOBAL NETWORK METRICS")
    print("-" * 40)

    print(f"Network Density: {density:.4f}")
    print(f"Average Degree: {average_degree:.4f}")
    print(f"Average Clustering Coefficient: {avg_clustering:.4f}")
    print(f"Connected Components: {connected_components}")
    print(f"Largest Component Size: {largest_component_size}")
    print(f"Largest Component Diameter: {diameter}")

    return {
        "Density": density,
        "Average_Degree": average_degree,
        "Average_Clustering": avg_clustering,
        "Connected_Components": connected_components,
        "Largest_Component_Size": largest_component_size,
        "Largest_Component_Diameter": diameter
    }


def save_metrics(metrics):

    os.makedirs("outputs/metrics", exist_ok=True)

    metrics.to_csv(
        "outputs/metrics/network_metrics.csv"
    )

    print("\nNode metricleri kaydedildi.")


def save_global_metrics(global_metrics):

    os.makedirs("outputs/metrics", exist_ok=True)

    pd.DataFrame([global_metrics]).to_csv(
        "outputs/metrics/global_network_metrics_from_script.csv",
        index=False
    )

    print("\nGlobal network metricleri kaydedildi.")


def visualize_top_nodes(metrics):

    top_degree = metrics.sort_values(
        by="Degree_Centrality",
        ascending=False
    ).head(10)

    plt.figure(figsize=(12, 6))

    plt.bar(
        top_degree.index,
        top_degree["Degree_Centrality"]
    )

    plt.title(
        "Top 10 Nodes by Degree Centrality"
    )

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        "outputs/graphs/top_degree_nodes.png",
        dpi=300
    )

    plt.show()

    print("\nTop node grafiği oluşturuldu.")


if __name__ == "__main__":

    G = load_network()

    metrics = calculate_metrics(G)

    print("\nNODE METRICS")
    print("-" * 40)

    print(metrics.sort_values(
        by="Degree_Centrality",
        ascending=False
    ))

    global_metrics = calculate_global_metrics(G)

    save_metrics(metrics)

    save_global_metrics(global_metrics)

    visualize_top_nodes(metrics)
