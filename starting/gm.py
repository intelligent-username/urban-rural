"""
For exploring the details of the GADM database
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

overview_lines = ["GADM LAYERS OVERVIEW", ""]
for i, layer in enumerate(layers, 1):
    overview_lines.append(f"{i}. {layer}")
overview_lines.append("")

for layer in layers:
    print(f"Processing layer: {layer} ...")
    gdf = gpd.read_file(gadm_path, layer=layer)

    layer_lines = [
        f"Layer: {layer}",
        f"Shape: {gdf.shape[0]} rows, {gdf.shape[1]} columns",
        f"Geometry: {', '.join(gdf.geometry.type.unique())}",
        f"CRS: {gdf.crs}",
        f"Bounds: {list(gdf.total_bounds)}",
        "",
        "Columns:",
    ]

    for col in gdf.columns:
        dtype = gdf[col].dtype
        non_null = gdf[col].notna().sum()
        layer_lines.append(f"  {col} ({dtype}): {non_null}/{len(gdf)} non-null")

    layer_lines.extend(["", "Sample Row:"])
    for col in gdf.columns:
        val = gdf[col].iloc[0]
        val_str = type(val).__name__ if col == "geometry" else val
        layer_lines.append(f"  {col}: {val_str}")

    if "COUNTRY" in gdf.columns:
        layer_lines.extend(["", f"Unique Countries: {gdf['COUNTRY'].nunique()}"])

    for type_col in ["TYPE_1", "TYPE_2", "TYPE_3", "TYPE_4", "TYPE_5"]:
        if type_col in gdf.columns:
            uniq = sorted(v for v in gdf[type_col].unique() if v)
            if uniq:
                layer_lines.extend(["", f"Unique {type_col} values ({len(uniq)}):", ", ".join(uniq)])

    layer_file = out_dir / (f"{layer}.txt" if layer.startswith("gadm") else f"gadm_{layer}.txt")
    layer_file.write_text("\n".join(layer_lines) + "\n", encoding="utf-8")
    print(f"  -> wrote {layer_file.name}")

    overview_lines.append(f"{layer}: {gdf.shape[0]} rows, {gdf.shape[1]} columns")

overview_file = out_dir / "gadm_overview.txt"
overview_file.write_text("\n".join(overview_lines) + "\n", encoding="utf-8")
print(f"\nWrote overview to {overview_file.name}")
print("Done.")