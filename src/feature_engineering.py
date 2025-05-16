import pandas as pd
import os

def generate_features(
    input_path="data/processed/kredit_jp_op_clean.csv",
    output_path="data/processed/kredit_jp_op_features.csv"
):
    print("Membuat fitur dari:", input_path)

    # Load data hasil preprocessing
    df = pd.read_csv(input_path)

    # Pilih kolom numerik untuk clustering
    feature_cols = [
        "modal_kerja", 
        "investasi", 
        "konsumsi", 
        "ekspor", 
        "impor", 
        "lainnya"
    ]

    df_features = df[["provinsi"] + feature_cols].copy()

    # Pastikan semua fitur numerik
    df_features[feature_cols] = df_features[feature_cols].apply(pd.to_numeric, errors='coerce')

    # Drop NaN
    df_features = df_features.dropna()

    # Buang 1 baris terakhir 
    df_features= df_features.iloc[:-1]

    # Simpan hasil fitur
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_features.to_csv(output_path, index=False)
    print(f"Fitur disimpan ke: {output_path}")

if __name__ == "__main__":
    generate_features()
