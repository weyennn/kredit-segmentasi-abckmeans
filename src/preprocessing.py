import pandas as pd
import os

def preprocess_kredit_jp_op(
    input_path="/Users/wayeien/Documents/JOB/Portofolio/github/credit-segmentation-indonesia/data/raw/STATISTIK_PERBANKAN_FEBRUARI 2025.xlsx",
    sheet_name="Kredit JP-OP per Lok._3.12.a.",
    output_path="/Users/wayeien/Documents/JOB/Portofolio/github/credit-segmentation-indonesia/data/processed/kredit_jp_op_clean.csv"
):
    print("Membaca sheet:", sheet_name)

    # Load dengan skip baris header multi-baris
    df_raw = pd.read_excel(input_path, sheet_name=sheet_name, skiprows=3)

    # Drop kolom kosong
    df = df_raw.dropna(axis=1, how='all').reset_index(drop=True)

    # Clean kolom yang punya \n atau spasi
    df.columns = df.columns.str.strip().str.replace("\n", " ", regex=False)

    # Rename dengan mapping kasar
    df = df.rename(columns={
    "Lokasi / Location": "provinsi",
    "Modal Kerja (Working Capital)": "modal_kerja",
    "Investasi (Investment)": "investasi",
    "Konsumsi (Consumption)": "konsumsi",
    "Ekspor": "ekspor",
    "Impor": "impor",
    "Lainnya": "lainnya"
    })


    df = df[["provinsi", "modal_kerja", "investasi", "konsumsi", "ekspor", "impor", "lainnya"]]

    # Filter: hanya baris utama yaitu nama provinsi, buang "NPL/NPF"
    df = df[~df["provinsi"].str.contains("NPL", case=False, na=False)]

    # Buang 3 baris terakhir (biasanya Total atau Luar Negeri)
    df = df.iloc[:-5]

    # Drop jika masih ada NaN
    df = df.dropna()

    # Simpan
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Data hasil preprocessing disimpan di {output_path}")

if __name__ == "__main__":
    preprocess_kredit_jp_op()
