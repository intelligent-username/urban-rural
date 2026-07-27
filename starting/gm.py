"""
Exploring the details of the GADM database
Required: Download it locally and placed it in the data/ folder.
Writes summary outputs to ../brainstorm/
"""

import geopandas as gpd
import fiona
from pathlib import Path

gadm_path = Path("../data/gadm_410-gpkg/gadm_410.gpkg")
out_dir = Path("../brainstorm")
out_dir.mkdir(parents=True, exist_ok=True)

if not gadm_path.exists():
    print(f"Error: {gadm_path} not found. Check your path.")
    exit(1)

layers = fiona.listlayers(str(gadm_path))

# --- Overview file ---
overview_lines = []
overview_lines.append("=" * 70)
overview_lines.append("AVAILABLE LAYERS IN GADM GEOPACKAGE")
overview_lines.append("=" * 70)
for i, layer in enumerate(layers, 1):
    overview_lines.append(f"{i}. {layer}")

for layer in layers:
    print(f"Processing layer: {layer} ...")
    gdf = gpd.read_file(gadm_path, layer=layer)

    layer_lines = []
    layer_lines.append("=" * 70)
    layer_lines.append(f"LAYER: {layer}")
    layer_lines.append("=" * 70)
    layer_lines.append(f"Shape: {gdf.shape} (rows, columns)")
    layer_lines.append(f"Geometry type: {list(gdf.geometry.type.unique())}")
    layer_lines.append(f"CRS: {gdf.crs}")

    layer_lines.append(f"\nColumns ({len(gdf.columns)}):")
    for col in gdf.columns:
        dtype = gdf[col].dtype
        non_null = gdf[col].notna().sum()
        layer_lines.append(f"  - {col}: {dtype}, {non_null}/{len(gdf)} non-null")

    layer_lines.append("\nSample row (first):")
    for col in gdf.columns:
        val = gdf[col].iloc[0]
        if col != "geometry":
            layer_lines.append(f"  {col}: {val}")
        else:
            layer_lines.append(f"  {col}: {type(val).__name__}")

    layer_lines.append(f"\nBounds: {list(gdf.total_bounds)}")
    if "COUNTRY" in gdf.columns:
        layer_lines.append(f"Unique countries/regions: {gdf['COUNTRY'].nunique()}")

    # Unique admin unit type names, per level, since these vary by country
    for type_col in ["TYPE_1", "TYPE_2", "TYPE_3", "TYPE_4", "TYPE_5"]:
        if type_col in gdf.columns:
            uniq = sorted(v for v in gdf[type_col].unique() if v)
            if uniq:
                layer_lines.append(f"\nUnique {type_col} values ({len(uniq)}):")
                layer_lines.append(", ".join(uniq))

    # Write per-layer summary
    layer_file = out_dir / f"gadm_summary_{layer}.txt"
    layer_file.write_text("\n".join(layer_lines), encoding="utf-8")
    print(f"  -> wrote {layer_file}")

    overview_lines.append(f"\n{layer}: {gdf.shape[0]} rows, {gdf.shape[1]} columns")

overview_file = out_dir / "gadm_overview.txt"
overview_file.write_text("\n".join(overview_lines), encoding="utf-8")
print(f"\nWrote overview to {overview_file}")
print("Done.")