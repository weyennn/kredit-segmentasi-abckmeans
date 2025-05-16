import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from k_selection import find_optimal_k
from abc_optimizer import ABCOptimizer
import os

def segment_and_cluster(
    input_path="data/processed/kredit_jp_op_features.csv",
    output_path="data/processed/kredit_jp_op_clustered_dualsegment.csv",
    high_plot="figures/high_volume_pca.png",
    normal_plot="figures/normal_volume_pca.png"):
    
    df = pd.read_csv(input_path)
    features = ["modal_kerja", "investasi", "konsumsi", "ekspor", "impor", "lainnya"]

    # Hitung total kredit
    df["total_kredit"] = df[features].sum(axis=1)

    # Bagi dua segmen: high & normal
    threshold = df["total_kredit"].quantile(0.75)
    df_high = df[df["total_kredit"] > threshold].copy().reset_index(drop=True)
    df_normal = df[df["total_kredit"] <= threshold].copy().reset_index(drop=True)

    def run_clustering_segment(df_segment, plot_path, segment_name):
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df_segment[features])

        # Tentukan k optimal
        k_optimal, best_centroids = find_optimal_k(X_scaled, k_range=range(2, 7))

        # Clustering
        kmeans = KMeans(n_clusters=k_optimal, init=best_centroids, n_init=1, random_state=42)
        labels = kmeans.fit_predict(X_scaled)

        df_segment["cluster"] = labels
        df_segment["segment"] = segment_name

        # PCA untuk visualisasi
        pca = PCA(n_components=2)
        pcs = pca.fit_transform(X_scaled)
        df_pca = pd.DataFrame(pcs, columns=["PC1", "PC2"])
        df_pca["cluster"] = labels
        df_pca["provinsi"] = df_segment["provinsi"]

        plt.figure(figsize=(7, 5))
        sns.scatterplot(data=df_pca, x="PC1", y="PC2", hue="cluster", palette="Set2", s=120)
        plt.title(f"Segment: {segment_name} (k={k_optimal})")
        for i in range(len(df_pca)):
            plt.text(df_pca["PC1"][i]+0.1, df_pca["PC2"][i], df_pca["provinsi"][i], fontsize=8)
        plt.tight_layout()
        plt.savefig(plot_path)
        plt.close()

        return df_segment

    # Clustering untuk masing-masing segmen
    df_high_clustered = run_clustering_segment(df_high, high_plot, "high_volume")
    df_normal_clustered = run_clustering_segment(df_normal, normal_plot, "normal")

    # Gabungkan dan simpan hasil
    df_final = pd.concat([df_high_clustered, df_normal_clustered], axis=0)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_final.to_csv(output_path, index=False)

    print(f"Clustering 2 level selesai!\nHasil: {output_path}")
    print(f"Plot high: {high_plot}\nPlot normal: {normal_plot}")

if __name__ == "__main__":
    segment_and_cluster()
