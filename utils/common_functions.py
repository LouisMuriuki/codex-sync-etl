from pathlib import Path
import pandas as pd


def basic_cleanup(df: pd.DataFrame) -> pd.DataFrame:
    """
    Shared cleanup logic for all codexes:
    - Normalize and trim text fields
    """
    if "code" in df.columns:
        df["code"] = df["code"].astype(str).str.strip().str.upper()

    if "description" in df.columns:
        df["description"] = df["description"].astype(str).str.strip().str.title()

    return df


def save_to_formats(df: pd.DataFrame, base_path: Path):
    """
    Save DataFrame to standardized CSV format.

    base_path: a Path without extension, e.g. output/csv/icd10who_clean
    """
    base_path.parent.mkdir(parents=True, exist_ok=True)

    output_csv = base_path.with_suffix(".csv")
    df.to_csv(output_csv, index=False)

    print(f"✅ Clean file saved: {output_csv}")


def save_invalid_rows(df: pd.DataFrame, base_path: Path):
    """
    Save invalid rows for inspection.

    base_path: a Path without extension, e.g. output/errors/icd10who_invalid
    """
    if df.empty:
        return

    base_path.parent.mkdir(parents=True, exist_ok=True)

    output_csv = base_path.with_suffix(".csv")
    df.to_csv(output_csv, index=False)

    print(f"⚠️ Invalid rows saved: {output_csv}")
