import os
import re
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
from typing import Tuple
import sys

# Ensure project root is on sys.path when running this file directly
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import requests

from utils.common_functions import (
    save_to_formats,
    basic_cleanup,
    save_invalid_rows,
)

# ===========================
# PATHS & CONFIG
# ===========================

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_CSV_DIR = BASE_DIR / "output" / "csv"
ERROR_DIR = BASE_DIR / "output" / "errors"
LOG_DIR = BASE_DIR / "logs"

RAW_FILE = INPUT_DIR / "icd10who_codes_2024.csv"

# Optional: set this in your environment or .env
# Example (PowerShell):
#   $env:ICD10WHO_URL="https://your-download-url/icd10who_codes_2024.csv"
DATA_URL = os.getenv("ICD10WHO_URL", "")

# Simple ICD-10 code pattern (e.g. A00, E11, A01.1, Z99.89)
ICD10_PATTERN = re.compile(r"^[A-Z][0-9][0-9](\.[0-9A-Z]{1,4})?$")


# ===========================
# LOGGING SETUP
# ===========================

def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Avoid adding handlers multiple times if script is re-run in same session
    if logger.handlers:
        return

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler with rotation
    log_file = LOG_DIR / "icd10who.log"
    fh = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,  # ~1MB
        backupCount=3,
        encoding="utf-8",
    )
    fh.setFormatter(formatter)
    logger.addHandler(fh)


# ===========================
# DOWNLOAD & LOADING
# ===========================

def download_icd10_file(url: str, target_path: Path, retries: int = 3, timeout: int = 30) -> None:
    """
    Download ICD-10 file from given URL with basic retry logic.
    """
    if not url:
        raise ValueError(
            "ICD10WHO_URL is not set. "
            "Set it in your environment or place the file manually in input/."
        )

    logging.info(f"Attempting to download ICD-10 file from: {url}")

    target_path.parent.mkdir(parents=True, exist_ok=True)

    last_error = None
    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Download attempt {attempt}/{retries}...")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()

            if not response.content:
                raise ValueError("Downloaded file is empty")

            target_path.write_bytes(response.content)
            logging.info(f"✅ Downloaded ICD-10 file to {target_path}")
            return

        except Exception as e:
            last_error = e
            logging.warning(f"Download attempt {attempt} failed: {e}")

    logging.error("All download attempts failed")
    raise last_error


def ensure_raw_file_exists() -> Path:
    """
    Ensure the raw ICD-10 file exists locally.
    If not, try to download it using DATA_URL.
    """
    if RAW_FILE.exists():
        logging.info(f"Using existing ICD-10 file: {RAW_FILE}")
        return RAW_FILE

    logging.warning(f"Raw ICD-10 file not found at {RAW_FILE}")

    if DATA_URL:
        download_icd10_file(DATA_URL, RAW_FILE)
        return RAW_FILE

    raise FileNotFoundError(
        f"ICD-10 input file not found at {RAW_FILE} and ICD10WHO_URL is not set."
    )


def load_icd10_data(filepath: Path) -> pd.DataFrame:
    """Load raw ICD-10 data file as CSV."""
    try:
        df = pd.read_csv(filepath, dtype=str)
        logging.info(f"Loaded {len(df)} rows from {filepath.name}")
        return df
    except Exception as e:
        logging.error(f"Failed to load file '{filepath}': {e}")
        raise


# ===========================
# VALIDATION & CLEANING
# ===========================

def validate_icd10_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate ICD-10 structure & code format.

    Returns:
        valid_rows, invalid_rows
    """

    # 1. Required columns
    required_columns = ["Code", "Description"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    total_rows = len(df)
    logging.info(f"Validating {total_rows} ICD-10 rows")

    # 2. Basic null checks
    missing_code = df["Code"].isnull().sum()
    missing_desc = df["Description"].isnull().sum()

    if missing_code:
        logging.warning(f"⚠️ {missing_code} rows are missing Code")
    if missing_desc:
        logging.warning(f"⚠️ {missing_desc} rows are missing Description")

    # 3. ICD-10 format check using regex
    df["Code"] = df["Code"].astype(str).str.strip().str.upper()
    valid_mask = df["Code"].str.match(ICD10_PATTERN, na=False)

    valid_rows = df[valid_mask].copy()
    invalid_rows = df[~valid_mask].copy()

    logging.info(f"Valid ICD-10 rows: {len(valid_rows)}")
    logging.info(f"Invalid ICD-10 rows (format issues): {len(invalid_rows)}")

    # 4. Duplicate code check (in valid set only)
    duplicate_codes = valid_rows[valid_rows.duplicated(subset=["Code"], keep=False)]
    if not duplicate_codes.empty:
        logging.warning(
            f"⚠️ {duplicate_codes['Code'].nunique()} codes appear multiple times"
        )

    return valid_rows, invalid_rows


def clean_icd10_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform validated ICD-10 data into standardized format.
    Expects df with columns 'Code' and 'Description'.
    """

    # Rename to standard column names
    df = df.rename(
        columns={
            "Code": "code",
            "Description": "description",
        }
    )

    # Generic cleanup (strip, normalize)
    df = basic_cleanup(df)

    # Drop any remaining nulls in key columns
    df = df.dropna(subset=["code", "description"])

    # Remove duplicates based on code, keeping first
    before = len(df)
    df = df.drop_duplicates(subset=["code"])
    after = len(df)
    if before != after:
        logging.info(f"Removed {before - after} duplicate codes")

    # Add timestamp
    df["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    logging.info(f"Final clean dataset contains {len(df)} rows")

    return df


# ===========================
# MAIN ENTRYPOINT
# ===========================

def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting ICD-10 WHO pipeline...")

    try:
        # Ensure we have a raw file (local or downloaded)
        raw_path = ensure_raw_file_exists()

        # Load
        raw_df = load_icd10_data(raw_path)

        # Validate
        valid_df, invalid_df = validate_icd10_data(raw_df)

        # Save invalid rows (if any)
        if not invalid_df.empty:
            save_invalid_rows(invalid_df, ERROR_DIR / "icd10who_invalid")

        # Clean only the valid rows
        clean_df = clean_icd10_data(valid_df)

        # Save clean output
        save_to_formats(clean_df, OUTPUT_CSV_DIR / "icd10who_clean")

        logger.info("✅ ICD-10 WHO processing completed successfully")

    except Exception as e:
        logger.exception(f"❌ ICD-10 WHO processing failed: {e}")
        raise


if __name__ == "__main__":
    main()
