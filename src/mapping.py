import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import os

def plot_cluster_map(
    geojson_path="/Users/wayeien/Documents/JOB/Portofolio/github/credit-segmentation-indonesia/data/geo/indonesia-prov.geojson",
    clustered_csv="/Users/wayeien/Documents/JOB/Portofolio/github/credit-segmentation-indonesia/data/processed/kredit_jp_op_clustered_dualsegment.csv",
    output_path="figures/map_cluster_jp_op_segmented.png"
):
    # Load clustering data
    df = pd.read_csv(clustered_csv)
    df = df[df["provinsi"].str.lower() != "lainnya"]

    # Normalisasi nama provinsi
    df["provinsi"] = (
        df["provinsi"]
        .str.lower()
        .str.strip()
        .str.replace("d.i ", "daerah istimewa ")
        .str.replace("kep.", "kepulauan ")
    )

    provinsi_map = {
        "d.i yogyakarta": "daerah istimewa yogyakarta",
        "bangka belitung": "bangka belitung",
        "kepulauan riau": "kepulauan riau",
        "nusa tenggara barat": "nusatenggara barat",
        "nusa tenggara timur": "nusa tenggara timur",
        "sulawesi tenggara": "sulawesi tenggara",
        "maluku utara": "maluku utara",
        "papua barat": "papua barat",
        "aceh": "di. aceh"
    }
    df["provinsi"] = df["provinsi"].replace(provinsi_map)

    # Load GeoJSON
    gdf = gpd.read_file(geojson_path)
    gdf = gdf.rename(columns={"Propinsi": "provinsi"})
    gdf["provinsi"] = gdf["provinsi"].str.lower().str.strip()

    # Gabungkan clustering dan geometri
    gdf_merged = gdf.merge(df[["provinsi", "cluster", "segment"]], on="provinsi", how="left")

    # Setup colormap
    cmap = plt.cm.get_cmap("tab10")
    cluster_labels = sorted(gdf_merged["cluster"].dropna().unique())
    colors = [cmap(i) for i in range(len(cluster_labels))]
    color_map = dict(zip(cluster_labels, colors))

    # Buat subplot per segmen
    segments = gdf_merged["segment"].dropna().unique()
    fig, axs = plt.subplots(1, len(segments), figsize=(14, 7))

    if len(segments) == 1:
        axs = [axs]

    for i, segment in enumerate(segments):
        ax = axs[i]
        subset = gdf_merged[gdf_merged["segment"] == segment].copy()

        # Mapping warna berdasarkan cluster
        subset["color"] = subset["cluster"].map(color_map)

        # Plot dengan warna
        subset.plot(color=subset["color"], edgecolor='black', ax=ax)

        # Tambah legend manual
        legend_patches = [
            Patch(facecolor=color_map[cl], label=f"Cluster {int(cl)}")
            for cl in subset["cluster"].dropna().unique()
        ]
        ax.legend(handles=legend_patches, title="Cluster", loc="lower left", fontsize=8)

        # Tambah nama provinsi
        for idx, row in subset.iterrows():
            try:
                x, y = row["geometry"].centroid.coords[0]
                ax.text(x, y, row["provinsi"].title(), fontsize=7, ha="center", color="black")
            except:
                continue

        ax.set_title(f"Segment: {segment.capitalize()}", fontsize=12)
        ax.axis("off")

    plt.suptitle("Peta Klaster Provinsi Berdasarkan Kredit JP-OP", fontsize=16)
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.show()

    print(f"Peta klaster segmented disimpan di: {output_path}")

if __name__ == "__main__":
    plot_cluster_map()
