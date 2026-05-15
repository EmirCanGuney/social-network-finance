import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


DATA_PATH = "data/processed/returns_2014_2024.csv"


def load_returns_data():
    df = pd.read_csv(
        DATA_PATH,
        index_col="Date",
        parse_dates=True
    )

    print("Return dataseti yüklendi.")
    print(df.head())

    return df


def calculate_correlation_matrix(df):

    correlation_matrix = df.corr(method="pearson")

    print("\nKorelasyon Matrisi:")
    print(correlation_matrix)

    return correlation_matrix


def save_correlation_matrix(correlation_matrix):

    os.makedirs("outputs/metrics", exist_ok=True)

    correlation_matrix.to_csv(
        "outputs/metrics/correlation_matrix.csv"
    )

    print("\nKorelasyon matrisi kaydedildi.")


def plot_heatmap(correlation_matrix):

    os.makedirs("outputs/heatmaps", exist_ok=True)

    plt.figure(figsize=(16, 12))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Financial Asset Correlation Heatmap")

    plt.tight_layout()

    plt.savefig(
        "outputs/heatmaps/correlation_heatmap.png",
        dpi=300
    )

    plt.show()

    print("\nHeatmap oluşturuldu.")


# # sonradan eklenen 
# def run_correlation_analysis(data_path, output_prefix):

#     df = pd.read_csv(
#         data_path,
#         index_col="Date",
#         parse_dates=True
#     )

#     correlation_matrix = df.corr(method="pearson")

#     correlation_matrix.to_csv(
#         f"outputs/metrics/{output_prefix}_correlation_matrix.csv"
#     )

#     plt.figure(figsize=(16, 12))

#     sns.heatmap(
#         correlation_matrix,
#         annot=True,
#         cmap="coolwarm",
#         fmt=".2f"
#     )

#     plt.title(
#         f"{output_prefix} Correlation Heatmap"
#     )

#     plt.tight_layout()

#     plt.savefig(
#         f"outputs/heatmaps/{output_prefix}_heatmap.png",
#         dpi=300
#     )

#     plt.close()

#     print(f"{output_prefix} korelasyon analizi tamamlandı.")

#     return correlation_matrix


if __name__ == "__main__":

    df = load_returns_data()

    correlation_matrix = calculate_correlation_matrix(df)

    save_correlation_matrix(correlation_matrix)

    plot_heatmap(correlation_matrix)


# if __name__ == "__main__":

#     run_correlation_analysis(
#         "data/processed/returns_pre_crisis.csv",
#         "pre_crisis"
#     )

#     run_correlation_analysis(
#         "data/processed/returns_post_crisis.csv",
#         "post_crisis"
#     )

#     run_correlation_analysis(
#         "data/processed/returns_2014_2024.csv",
#         "full_period"
#     )