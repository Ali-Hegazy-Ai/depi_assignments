"""
extractor.py – Reusable data extraction helpers.

Supported sources
-----------------
- Local CSV / JSON / Excel files
- Public REST APIs (JSON)
- Web pages (HTML tables via pandas)
- SQLite databases
"""

import sqlite3
from pathlib import Path

import pandas as pd
import requests


# ---------------------------------------------------------------------------
# File-based extraction
# ---------------------------------------------------------------------------

def from_csv(path: str, **kwargs) -> pd.DataFrame:
    """Read a CSV file into a DataFrame."""
    df = pd.read_csv(path, **kwargs)
    print(f"[extractor] CSV  → {len(df)} rows  {path}")
    return df


def from_json(path: str, **kwargs) -> pd.DataFrame:
    """Read a JSON file into a DataFrame."""
    df = pd.read_json(path, **kwargs)
    print(f"[extractor] JSON → {len(df)} rows  {path}")
    return df


def from_excel(path: str, sheet_name=0, **kwargs) -> pd.DataFrame:
    """Read an Excel file into a DataFrame."""
    df = pd.read_excel(path, sheet_name=sheet_name, **kwargs)
    print(f"[extractor] Excel → {len(df)} rows  {path}")
    return df


# ---------------------------------------------------------------------------
# API extraction
# ---------------------------------------------------------------------------

def from_api(url: str, params: dict = None, headers: dict = None,
             timeout: int = 30) -> pd.DataFrame:
    """
    Fetch JSON from a REST API and return a DataFrame.

    The function handles both list responses and dict responses that
    contain a single top-level list value.
    """
    response = requests.get(url, params=params, headers=headers,
                            timeout=timeout)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                df = pd.DataFrame(value)
                break
        else:
            df = pd.DataFrame([data])
    else:
        raise ValueError(f"Unexpected API response type: {type(data)}")

    print(f"[extractor] API  → {len(df)} rows  {url}")
    return df


# ---------------------------------------------------------------------------
# Web-page extraction (HTML tables)
# ---------------------------------------------------------------------------

def from_html_table(url: str, table_index: int = 0, **kwargs) -> pd.DataFrame:
    """
    Extract an HTML table from a web page.

    Parameters
    ----------
    url : str
        Page URL.
    table_index : int
        Index of the table on the page (0 = first table).
    """
    tables = pd.read_html(url, **kwargs)
    if not tables:
        raise ValueError(f"No HTML tables found on {url}")
    df = tables[table_index]
    print(f"[extractor] HTML table[{table_index}] → {len(df)} rows  {url}")
    return df


# ---------------------------------------------------------------------------
# SQL extraction
# ---------------------------------------------------------------------------

def from_sqlite(db_path: str, query: str) -> pd.DataFrame:
    """Run a SQL query against a SQLite database."""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query, conn)
    print(f"[extractor] SQLite → {len(df)} rows  {db_path}")
    return df
