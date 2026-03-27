"""
transformer.py – Reusable data transformation helpers.

Functions
---------
- normalize_columns       : standardise column names
- drop_duplicates_and_nulls : basic deduplication and null handling
- strip_strings           : strip whitespace from string columns
- parse_dates             : convert string columns to datetime
- fill_missing            : fill missing values with a strategy
- rename_columns          : rename columns from a mapping
- filter_rows             : filter rows by a column condition
- add_derived_column      : add a new column from a formula
"""

import pandas as pd


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Lowercase column names, replace spaces with underscores,
    and remove non-alphanumeric characters.
    """
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^a-z0-9_]", "", regex=True)
    )
    return df


def drop_duplicates_and_nulls(df: pd.DataFrame,
                               null_threshold: float = 1.0) -> pd.DataFrame:
    """
    Remove duplicate rows and columns where the null fraction exceeds
    ``null_threshold`` (default 1.0 = drop only fully-null columns).
    """
    before = len(df)
    df = df.drop_duplicates()
    df = df.dropna(axis=1, thresh=int(len(df) * (1 - null_threshold)) + 1)
    print(f"[transformer] Removed {before - len(df)} duplicate rows")
    return df


def strip_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from all string columns."""
    df = df.copy()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    return df


def parse_dates(df: pd.DataFrame, columns: list,
                date_format: str = None) -> pd.DataFrame:
    """Convert the specified columns to datetime."""
    df = df.copy()
    for col in columns:
        df[col] = pd.to_datetime(df[col], format=date_format, errors="coerce")
    return df


def fill_missing(df: pd.DataFrame, strategy: str = "mean",
                 fill_value=None) -> pd.DataFrame:
    """
    Fill missing values.

    Parameters
    ----------
    strategy : str
        'mean', 'median', 'mode', or 'constant'.
    fill_value :
        Used only when strategy='constant'.
    """
    df = df.copy()
    numeric_cols = df.select_dtypes(include="number").columns
    if strategy == "mean":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == "median":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif strategy == "mode":
        for col in df.columns:
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])
    elif strategy == "constant":
        df = df.fillna(fill_value)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
    return df


def rename_columns(df: pd.DataFrame, mapping: dict) -> pd.DataFrame:
    """Rename columns according to a dictionary mapping."""
    return df.rename(columns=mapping)


def filter_rows(df: pd.DataFrame, column: str,
                operator: str, value) -> pd.DataFrame:
    """
    Filter rows based on a column condition.

    Parameters
    ----------
    column : str
    operator : str
        One of '==', '!=', '>', '>=', '<', '<=', 'contains', 'startswith'.
    value :
        The comparison value.
    """
    ops = {
        "==": df[column] == value,
        "!=": df[column] != value,
        ">":  df[column] > value,
        ">=": df[column] >= value,
        "<":  df[column] < value,
        "<=": df[column] <= value,
        "contains":   df[column].astype(str).str.contains(str(value), na=False),
        "startswith": df[column].astype(str).str.startswith(str(value), na=False),
    }
    if operator not in ops:
        raise ValueError(f"Unknown operator: {operator}")
    return df[ops[operator]].reset_index(drop=True)


def add_derived_column(df: pd.DataFrame, new_col: str,
                       formula) -> pd.DataFrame:
    """
    Add a derived column.

    Parameters
    ----------
    new_col : str
        Name of the new column.
    formula : callable
        A function that takes the DataFrame and returns a Series.
        Example: lambda df: df["price"] * df["qty"]
    """
    df = df.copy()
    df[new_col] = formula(df)
    return df
