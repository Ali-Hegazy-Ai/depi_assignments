"""
report_template.py – Generate a plain-text summary report for an assignment.

Usage:
  from templates.report_template import generate_report
  generate_report(df, title="Assignment 01 Report", output_path="report.txt")
"""

import os
from datetime import datetime

import pandas as pd


def generate_report(df: pd.DataFrame, title: str = "Assignment Report",
                    student_name: str = "", output_path: str = None) -> str:
    """
    Build a plain-text report for a completed DataFrame and optionally
    write it to a file.

    Returns the report as a string.
    """
    sep = "=" * 60
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        sep,
        f"  {title}",
        f"  Student : {student_name or '(not set)'}",
        f"  Date    : {now}",
        sep,
        "",
        "DATASET OVERVIEW",
        "-" * 40,
        f"  Rows          : {len(df)}",
        f"  Columns       : {len(df.columns)}",
        f"  Column names  : {', '.join(df.columns.tolist())}",
        "",
        "NULL VALUES",
        "-" * 40,
    ]

    null_counts = df.isnull().sum()
    for col, count in null_counts.items():
        pct = count / len(df) * 100 if len(df) else 0
        lines.append(f"  {col:<25} {count:>5} ({pct:.1f} %)")

    lines += [
        "",
        "NUMERIC SUMMARY",
        "-" * 40,
        df.describe(include="number").to_string(),
        "",
        "SAMPLE (first 5 rows)",
        "-" * 40,
        df.head(5).to_string(index=False),
        "",
        sep,
    ]

    report = "\n".join(lines)

    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[report] Saved → {output_path}")

    return report
