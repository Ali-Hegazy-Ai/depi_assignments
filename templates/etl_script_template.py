"""
ETL Script Template
===================
Reusable template for data engineering assignments.

Usage:
  Copy this file to your assignment folder and fill in the sections marked TODO.
  Run:  python etl_script_template.py
"""

import os
import sys
import sqlite3
import pandas as pd
import requests

# ---------------------------------------------------------------------------
# CONFIGURATION  – update these for each assignment
# ---------------------------------------------------------------------------
ASSIGNMENT_NAME = "assignment_01"

# Paths (relative to project root)
RAW_DIR = os.path.join("..", "data", "raw")
PROCESSED_DIR = os.path.join("..", "data", "processed")
OUTPUT_DIR = os.path.join("..", "data", "output")

# Source
CSV_SOURCE = ""       # path to a local CSV, or leave empty
API_URL = ""          # URL of a public REST API, or leave empty
DB_PATH = ""          # path to a SQLite database file, or leave empty


# ---------------------------------------------------------------------------
# STEP 1 – EXTRACT
# ---------------------------------------------------------------------------

def extract_from_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    df = pd.read_csv(path)
    print(f"[extract] Loaded {len(df)} rows from {path}")
    return df


def extract_from_api(url: str, params: dict = None) -> pd.DataFrame:
    """Fetch JSON data from a public API and convert to DataFrame."""
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    # API may return a list or a dict with a nested list – handle both
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        # Try to find the first list value
        for value in data.values():
            if isinstance(value, list):
                df = pd.DataFrame(value)
                break
        else:
            df = pd.DataFrame([data])
    print(f"[extract] Fetched {len(df)} rows from {url}")
    return df


def extract_from_sql(db_path: str, query: str) -> pd.DataFrame:
    """Run a SQL query against a SQLite database."""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query, conn)
    print(f"[extract] Queried {len(df)} rows from {db_path}")
    return df


# ---------------------------------------------------------------------------
# STEP 2 – CLEAN / TRANSFORM
# ---------------------------------------------------------------------------

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning:
    - Drop fully-duplicate rows
    - Strip whitespace from string columns
    - Drop columns that are entirely null
    """
    before = len(df)
    df = df.drop_duplicates()
    df = df.dropna(axis=1, how="all")
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    print(f"[clean] {before - len(df)} duplicate rows removed; {len(df)} rows remaining")
    return df


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Add your assignment-specific transformations here.
    Examples:
      - Rename columns
      - Parse dates
      - Compute derived columns
      - Filter rows
      - Merge/join with another dataset
    """
    # --- example: normalise column names ---
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    print(f"[transform] Transformation complete; columns: {list(df.columns)}")
    return df


# ---------------------------------------------------------------------------
# STEP 3 – VALIDATE
# ---------------------------------------------------------------------------

def validate(df: pd.DataFrame, required_columns: list = None) -> bool:
    """
    Basic validation checks.
    Returns True if the DataFrame passes all checks, False otherwise.
    """
    passed = True

    if df.empty:
        print("[validate] FAIL – DataFrame is empty")
        return False

    if required_columns:
        missing = [c for c in required_columns if c not in df.columns]
        if missing:
            print(f"[validate] FAIL – missing required columns: {missing}")
            passed = False

    null_pct = df.isnull().mean() * 100
    high_null = null_pct[null_pct > 50]
    if not high_null.empty:
        print(f"[validate] WARNING – columns with >50 % nulls:\n{high_null.to_string()}")

    if passed:
        print(f"[validate] PASS – {len(df)} rows, {len(df.columns)} columns")
    return passed


# ---------------------------------------------------------------------------
# STEP 4 – LOAD
# ---------------------------------------------------------------------------

def load_to_csv(df: pd.DataFrame, filename: str, directory: str = OUTPUT_DIR) -> str:
    """Save DataFrame to a CSV file."""
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    df.to_csv(path, index=False)
    print(f"[load] Saved {len(df)} rows to {path}")
    return path


def load_to_sqlite(df: pd.DataFrame, table_name: str, db_path: str) -> None:
    """Write DataFrame to a SQLite table (replace if exists)."""
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"[load] Written {len(df)} rows to table '{table_name}' in {db_path}")


# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------

def run_pipeline():
    print(f"\n{'='*60}")
    print(f"  ETL Pipeline – {ASSIGNMENT_NAME}")
    print(f"{'='*60}\n")

    # --- EXTRACT ---
    # TODO: choose your extraction method and uncomment the relevant line

    if CSV_SOURCE:
        df = extract_from_csv(CSV_SOURCE)
    elif API_URL:
        df = extract_from_api(API_URL)
    elif DB_PATH:
        df = extract_from_sql(DB_PATH, "SELECT * FROM source_table")
    else:
        # Demo: use a built-in sample so the script runs out of the box
        print("[extract] No source configured – using built-in sample data")
        df = pd.DataFrame({
            "id": [1, 2, 3, 4, 5],
            "Name": ["  Alice", "Bob  ", "Charlie", "Bob  ", None],
            "Score": [85, 92, 78, 92, 88],
            "Category": ["A", "B", "A", "B", "C"],
        })

    # --- CLEAN ---
    df = clean(df)

    # --- TRANSFORM ---
    df = transform(df)

    # --- VALIDATE ---
    validate(df)

    # --- LOAD ---
    output_path = load_to_csv(df, f"{ASSIGNMENT_NAME}_output.csv")

    print(f"\n[done] Pipeline finished. Output → {output_path}\n")
    return df


if __name__ == "__main__":
    run_pipeline()
