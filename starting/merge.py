"""
Merging GAM with GAM_DUC to prepare for classification
Requires gadm_410-gpkg and 
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path

def merge_data():

    GADM_PATH = Path("../data/gadm_410-gpkg/gadm_410.gpkg")
    DUC_FILE = Path("../data/GHS_DUC_GLOBE_R2023A_V2_0_GADM41_2025_level2.csv")
    GADM_LEVEL_COL = "GID_2"  # must match the level in DUC_FILE
    out_dir = Path("../brainstorm")
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- Inspect the DUC csv first ---
    duc = pd.read_csv(DUC_FILE)
    print("DUC columns:", list(duc.columns))
    print(f"DUC shape: {duc.shape}")
    print("\nSample row:")
    print(duc.iloc[0])

    # --- Load GADM level 2 ---
    gdf = gpd.read_file(GADM_PATH, layer="gadm_410")

    # --- Merge ---
    merged = gdf.merge(duc, on=GADM_LEVEL_COL, how="left", suffixes=("", "_duc"))

    print(f"\nMerged shape: {merged.shape}")
    print(f"Rows with no DUC match: {merged[duc.columns[1]].isna().sum() if len(duc.columns) > 1 else 'check manually'}")

    # Save a summary
    summary_lines = [
        f"DUC file used: {DUC_FILE.name}",
        f"DUC columns: {list(duc.columns)}",
        f"DUC shape: {duc.shape}",
        f"GADM shape: {gdf.shape}",
        f"Merged shape: {merged.shape}",
        f"\nSample merged row:\n{merged.iloc[0].to_dict()}",
    ]
    (out_dir / "duc_merge_summary.txt").write_text("\n".join(str(l) for l in summary_lines), encoding="utf-8")
    print(f"\nSummary written to {out_dir / 'duc_merge_summary.txt'}")

    # Save merged file for actual modeling use (drop to a lighter format if huge)
    merged.to_file("../data/gadm_level2_with_duc.gpkg", driver="GPKG")
    print("Merged geopackage saved to ../data/gadm_level2_with_duc.gpkg")

if __name__ == "__main__":
    merge_data()
