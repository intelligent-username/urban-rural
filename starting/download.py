"""
Downloads and extracts the required GADM and GHS-DUC databases into the data/ folder.
"""

import os
import sys
import shutil
import zipfile
import urllib.request
from pathlib import Path

# Paths relative to script location
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Download links from README.md
DATASETS = [
    {
        "name": "GADM 4.1 GeoPackage",
        "url": "https://geodata.ucdavis.edu/gadm/gadm4.1/gadm_410-gpkg.zip",
        "filename": "gadm_410-gpkg.zip",
        "extract_dir": "gadm_410-gpkg",
    },
    {
        "name": "GHS-DUC Urbanisation Labelling",
        "url": "https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_DUC_GLOBE_R2023A/V2-0/GHS_DUC_MT_GLOBE_R2023A_V2_0.zip",
        "filename": "GHS_DUC_MT_GLOBE_R2023A_V2_0.zip",
        "extract_dir": "GHS_DUC_MT_GLOBE_R2023A_V2_0",
    },
]


def download_progress_hook(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100.0, downloaded * 100 / total_size)
        mb_downloaded = downloaded / (1024 * 1024)
        mb_total = total_size / (1024 * 1024)
        sys.stdout.write(
            f"\rProgress: {percent:.1f}% ({mb_downloaded:.1f} MB / {mb_total:.1f} MB)"
        )
    else:
        mb_downloaded = downloaded / (1024 * 1024)
        sys.stdout.write(f"\rDownloaded: {mb_downloaded:.1f} MB")
    sys.stdout.flush()


def download_and_extract():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for item in DATASETS:
        print(f"\n--- Processing {item['name']} ---")
        zip_path = DATA_DIR / item["filename"]
        extract_path = DATA_DIR / item["extract_dir"]

        # Download if zip does not already exist
        if not zip_path.exists():
            print(f"Downloading from {item['url']} ...")
            try:
                urllib.request.urlretrieve(
                    item["url"], zip_path, reporthook=download_progress_hook
                )
                print("\nDownload complete.")
            except Exception as e:
                print(f"\nFailed to download {item['name']}: {e}")
                continue
        else:
            print(f"File {item['filename']} already exists. Skipping download.")

        # Extract if target directory does not already exist
        if not extract_path.exists():
            print(f"Extracting {item['filename']} to {extract_path.name}/ ...")
            try:
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_path)
                print("Extraction complete.")
            except Exception as e:
                print(f"Failed to extract {item['filename']}: {e}")
        else:
            print(f"Directory {extract_path.name}/ already exists. Skipping extraction.")

    # Copy level2 CSV to data/ root directory if extracted
    csv_src = DATA_DIR / "GHS_DUC_MT_GLOBE_R2023A_V2_0" / "GHS_DUC_GLOBE_R2023A_V2_0_GADM41_2025_level2.csv"
    csv_dst = DATA_DIR / "GHS_DUC_GLOBE_R2023A_V2_0_GADM41_2025_level2.csv"
    if csv_src.exists() and not csv_dst.exists():
        print(f"\nCopying {csv_src.name} to {DATA_DIR.name}/ ...")
        shutil.copy2(csv_src, csv_dst)
        print("Copy complete.")


if __name__ == "__main__":
    download_and_extract()
