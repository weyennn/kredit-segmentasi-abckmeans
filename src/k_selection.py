import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from abc_optimizer import ABCOptimizer

def find_optimal_k(data, k_range=range(2, 10), seed=42, save_plot=True):
    silhouette_scores = []
    inertia_scores = []
    best_k = None
    best_score = -1
    best_centroids = None

    print("Mencari k optimal berdasarkan silhouette score...")

    for k in k_range:
        abc = ABCOptimizer(data=data, num_clusters=k, seed=seed)
        init_centroids = abc.optimize()

        kmeans = KMeans(n_clusters=k, init=init_centroids, n_init=1, random_state=seed)
        labels = kmeans.fit_predict(data)

        sil_score = silhouette_score(data, labels)
        inertia = kmeans.inertia_

        silhouette_scores.append(sil_score)
        inertia_scores.append(inertia)

        print(f"k={k} | Silhouette Score: {sil_score:.4f} | SSE: {inertia:.2f}")

        if sil_score > best_score:
            best_score = sil_score
            best_k = k
            best_centroids = init_centroids

    # Plot hasil evaluasi
    if save_plot:
        plt.figure(figsize=(8, 4))
        plt.subplot(1, 2, 1)
        plt.plot(list(k_range), silhouette_scores, marker='o')
        plt.title("Silhouette Score vs k")
        plt.xlabel("Jumlah Klaster (k)")
        plt.ylabel("Silhouette Score")

        plt.subplot(1, 2, 2)
        plt.plot(list(k_range), inertia_scores, marker='o', color='orange')
        plt.title("SSE (Inertia) vs k")
        plt.xlabel("Jumlah Klaster (k)")
        plt.ylabel("Inertia")

        plt.tight_layout()
        plt.savefig("figures/k_evaluation.png")
        plt.close()

    print(f"\nK optimal: {best_k} (silhouette={best_score:.4f})")
    return best_k, best_centroids
