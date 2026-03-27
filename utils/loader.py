"""
loader.py – Reusable data loading helpers.

Supported targets
-----------------
- CSV file
- JSON file
- SQLite database table
- In-memory report (print summary)
"""

import os
import json
import sqlite3

import pandas as pd


def to_csv(df: pd.DataFrame, path: str, **kwargs) -> str:
    """
    Save a DataFrame to a CSV file.

    Creates parent directories automatically.
    Returns the absolute path of the saved file.
    """
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    df.to_csv(path, index=False, **kwargs)
    print(f"[loader] CSV  → {len(df)} rows  {path}")
    return os.path.abspath(path)


def to_json(df: pd.DataFrame, path: str,
            orient: str = "records", indent: int = 2) -> str:
    """
    Save a DataFrame to a JSON file.

    Returns the absolute path of the saved file.
    """
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    df.to_json(path, orient=orient, indent=indent, force_ascii=False)
    print(f"[loader] JSON → {len(df)} rows  {path}")
    return os.path.abspath(path)


def to_sqlite(df: pd.DataFrame, table_name: str, db_path: str,
              if_exists: str = "replace") -> None:
    """
    Write a DataFrame to a SQLite table.

    Parameters
    ----------
    if_exists : str
        'replace' (default) | 'append' | 'fail'
    """
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    print(f"[loader] SQLite → table '{table_name}'  {db_path}")


def print_summary(df: pd.DataFrame, title: str = "Dataset Summary") -> None:
    """Print a concise summary of the DataFrame to stdout."""
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  {title}")
    print(sep)
    print(f"  Rows    : {len(df)}")
    print(f"  Columns : {len(df.columns)}")
    print(f"\n  Dtypes\n{df.dtypes.to_string()}")
    print(f"\n  Null counts\n{df.isnull().sum().to_string()}")
    print(f"\n  Head (3 rows)\n{df.head(3).to_string()}")
    print(sep + "\n")
