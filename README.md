
# Clustering Provinsi Berdasarkan Kredit JP-OP (Indonesia)

Proyek ini bertujuan untuk melakukan segmentasi provinsi-provinsi di Indonesia berdasarkan data Kredit menurut Jenis Penggunaan (JP) dan Orientasi Pengguna (OP) menggunakan metode clustering yang dioptimasi dengan **Artificial Bee Colony (ABC)**.

---

## Tujuan Proyek

- Menemukan pola atau kesamaan struktur kredit antar provinsi
- Menangani outlier besar seperti DKI Jakarta dengan pendekatan segmentasi
- Menyajikan hasil clustering dalam bentuk visual peta dan PCA projection

---

## Dataset

Data bersumber dari:
- **Laporan Statistik Perbankan Indonesia (Februari 2025)**
- Sheet: `Kredit JP-OP per Lok._3.12.a.`
- Fitur: `modal_kerja`, `investasi`, `konsumsi`, `ekspor`, `impor`, `lainnya`

---

## Metodologi

1. **Preprocessing**
   - Menghapus entri `NPL/NPF`, `Total`, dan `Lainnya`
   - Menormalisasi nama provinsi dan membersihkannya

2. **Feature Engineering**
   - Menjumlahkan total kredit
   - Membagi provinsi menjadi dua segmen:
     - `high_volume` (top 25% kredit tertinggi)
     - `normal` (sisanya)

3. **Clustering**
   - Menggunakan **KMeans** dengan **ABC-optimized centroid**
   - Pemilihan jumlah cluster (`k`) menggunakan **Silhouette Score**

---

##  Hasil Segmentasi & Klasterisasi

###  Segmen: `high_volume`
- K optimal: **2**
- Silhouette Score tertinggi: **0.7921**
- Distribusi klaster:
  - Cluster 0: 8 provinsi
  - Cluster 1: 1 provinsi (DKI Jakarta → outlier)

###  Segmen: `normal`
- K optimal: **5**
- Silhouette Score tertinggi: **0.3984**
- Distribusi klaster:
  - Cluster 0: 7 provinsi
  - Cluster 1: 1 provinsi
  - Cluster 2: 8 provinsi
  - Cluster 3: 8 provinsi
  - Cluster 4: 1 provinsi

---

## Visualisasi

- PCA Projection dan Mapping dapat dilihat pada folder `/figures`:
  - `map_cluster_jp_op_segmented.png` → Peta klaster per segmen
  - `cluster_result_pca.png` → Proyeksi PCA hasil clustering

---

## Insight

- Provinsi dengan volume kredit sangat tinggi membentuk klaster tersendiri.
- Segmentasi dua level berhasil mencegah outlier seperti DKI Jakarta mendistorsi clustering.
- Klaster di segmen normal menunjukkan keberagaman karakteristik kredit provinsi.

---

## Tools & Library

- Python, Pandas, Scikit-learn
- GeoPandas, Matplotlib, Seaborn
- Artificial Bee Colony (custom optimizer)

---

## Struktur Folder

```
src/
├── abc_optimizer.py
├── k_selection.py
├── preprocessing.py
├── feature_engineering.py
├── clustering.py
└── mapping.py

data/
├── raw/
├── processed/
└── geo/

figures/
└── *.png
```

---

## Author

- **Yayang Matira**  
  A master's Student of Computer Science at Gadjah Mada University

