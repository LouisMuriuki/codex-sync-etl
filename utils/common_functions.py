from pathlib import Path
import os
import logging
from logging.handlers import RotatingFileHandler
import pandas as pd
import requests


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


def setup_logging(log_file: Path):
    """
    Configure root logger (console + rotating file).
    Safe to call multiple times in one session.
    """
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    if logger.handlers:
        return

    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    fh = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)


def ensure_file(raw_path: Path, url_env_var: str, timeout: int = 60, retries: int = 3) -> Path:
    """
    Ensure file exists at raw_path; otherwise try to download using URL from `url_env_var`.
    """
    if raw_path.exists():
        logging.info(f"Using existing file: {raw_path}")
        return raw_path

    url = os.getenv(url_env_var, "")
    if not url:
        raise FileNotFoundError(f"Input not found at {raw_path} and {url_env_var} is not set.")

    logging.info(f"Attempting download from {url}")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            logging.info(f"Download attempt {attempt}/{retries}...")
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
            if not resp.content:
                raise ValueError("Downloaded file is empty")
            raw_path.write_bytes(resp.content)
            logging.info(f"✅ Downloaded to {raw_path}")
            return raw_path
        except Exception as e:
            last_error = e
            logging.warning(f"Download failed: {e}")
    logging.error("All download attempts failed")
    raise last_error


def iso_utc_now() -> str:
    """
    ISO 8601 UTC timestamp (seconds precision).
    """
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
