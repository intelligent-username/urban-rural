"""
Explore GHS-DUC (Degree of Urbanisation) dataset.
This code is run after downloading the dataset locally and placing it in the data/ folder.
Writes summary outputs to ../brainstorm/
"""

import pandas as pd
from pathlib import Path

def import_gs():

    duc_path = Path("../data/GHS_DUC_GLOBE_R2023A_V2_0_GADM41_2025_level2.csv")
    fallback_path = (
        Path("../data/GHS_DUC_MT_GLOBE_R2023A_V2_0")
        / "GHS_DUC_GLOBE_R2023A_V2_0_GADM41_2025_level2.csv"
    )
    out_dir = Path("../brainstorm")
    out_dir.mkdir(parents=True, exist_ok=True)

    if duc_path.exists():
        target_csv = duc_path
    elif fallback_path.exists():
        target_csv = fallback_path
    else:
        print(f"Error: Neither {duc_path} nor {fallback_path} found. Check your path.")
        exit(1)

    print(f"Loading {target_csv.name} ...")
    df = pd.read_csv(target_csv)

    summary_lines = [
        f"File: {target_csv.name}",
        f"Shape: {df.shape[0]} rows, {df.shape[1]} columns",
        "",
        "Columns:",
    ]

    for col in df.columns:
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        summary_lines.append(f"  {col} ({dtype}): {non_null}/{len(df)} non-null")

    summary_lines.extend(["", "Sample Row:"])
    for col in df.columns:
        summary_lines.append(f"  {col}: {df[col].iloc[0]}")

    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) > 0:
        summary_lines.extend(["", "Numeric Columns Summary:"])
        stats = df[numeric_cols].describe().T
        for col, row in stats.iterrows():
            summary_lines.append(
                f"  {col} -> min: {row['min']}, mean: {row['mean']:.2f}, max: {row['max']}, std: {row['std']:.2f}"
            )

    summary_lines.append("")
    if "GID_2" in df.columns:
        summary_lines.append(f"Unique GID_2 regions: {df['GID_2'].nunique()}")
    if "GID_0" in df.columns:
        summary_lines.append(f"Unique GID_0 countries: {df['GID_0'].nunique()}")

    summary_file = out_dir / "duc_summary.txt"
    summary_file.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print(f"Wrote detailed summary to {summary_file.name}")

    overview_lines = [
        f"File: {target_csv.name}",
        f"Rows: {df.shape[0]}",
        f"Columns: {df.shape[1]}",
        f"Column Names: {', '.join(df.columns)}",
    ]
    overview_file = out_dir / "duc_overview.txt"
    overview_file.write_text("\n".join(overview_lines) + "\n", encoding="utf-8")
    print(f"Wrote overview to {overview_file.name}")

    print("Done.")

if __name__ == "__main__":
    import_gs()
