#!/usr/bin/env python3
"""Rank GSC comparison-query exports for content refresh analysis."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path


ALIASES = {
    "query": ("Top queries", "Query", "Queries", "استعلامات البحث"),
    "current_clicks": ("Last 3 months Clicks", "Current Clicks", "Clicks current"),
    "previous_clicks": ("Previous 3 months Clicks", "Previous Clicks", "Clicks previous"),
    "current_impressions": ("Last 3 months Impressions", "Current Impressions", "Impressions current"),
    "previous_impressions": ("Previous 3 months Impressions", "Previous Impressions", "Impressions previous"),
    "current_ctr": ("Last 3 months CTR", "Current CTR", "CTR current"),
    "previous_ctr": ("Previous 3 months CTR", "Previous CTR", "CTR previous"),
    "current_position": ("Last 3 months Position", "Current Position", "Position current"),
    "previous_position": ("Previous 3 months Position", "Previous Position", "Position previous"),
}


def number(value: str | None) -> float:
    if value is None:
        return 0.0
    text = value.strip().replace(",", "")
    if not text:
        return 0.0
    if text.endswith("%"):
        return float(text[:-1]) / 100.0
    return float(text)


def resolve(headers: list[str], key: str) -> str:
    for candidate in ALIASES[key]:
        if candidate in headers:
            return candidate
    suffix = key.replace("current_", "").replace("previous_", "").replace("_", " ")
    period = "last" if key.startswith("current_") else "previous"
    if key == "query":
        for header in headers:
            if "quer" in header.lower() or "استعلام" in header:
                return header
    for header in headers:
        lower = header.lower()
        if suffix in lower and period in lower:
            return header
    raise ValueError(f"Missing required column for {key!r}. Headers: {headers}")


def load(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("CSV has no header row")
        headers = list(reader.fieldnames)
        cols = {key: resolve(headers, key) for key in ALIASES}
        rows = []
        for raw in reader:
            query = (raw.get(cols["query"]) or "").strip()
            if not query:
                continue
            row = {"query": query}
            for key in ALIASES:
                if key != "query":
                    row[key] = number(raw.get(cols[key]))
            row["click_delta"] = row["current_clicks"] - row["previous_clicks"]
            row["impression_delta"] = row["current_impressions"] - row["previous_impressions"]
            row["ctr_delta"] = row["current_ctr"] - row["previous_ctr"]
            row["position_delta"] = row["current_position"] - row["previous_position"]
            lost = max(0.0, -row["impression_delta"])
            near_page_one = max(0.15, 1.0 - max(0.0, row["current_position"] - 3.0) / 20.0)
            rank_loss = 1.0 + min(max(row["position_delta"], 0.0), 10.0) / 10.0
            row["recovery_score"] = round(lost * near_page_one * rank_loss, 2)
            row["protection_score"] = round(
                row["current_impressions"]
                + row["current_clicks"] * 50.0
                + max(0.0, row["impression_delta"]) * 0.5
                + max(0.0, row["click_delta"]) * 75.0,
                2,
            )
            rows.append(row)
        return rows


def compact(row: dict) -> dict:
    keys = (
        "query", "current_clicks", "previous_clicks", "click_delta",
        "current_impressions", "previous_impressions", "impression_delta",
        "current_ctr", "previous_ctr", "ctr_delta",
        "current_position", "previous_position", "position_delta",
        "recovery_score", "protection_score",
    )
    return {key: row[key] for key in keys}


def fmt(value: float, percent: bool = False) -> str:
    if percent:
        return f"{value * 100:.2f}%"
    if math.isclose(value, round(value)):
        return f"{int(round(value)):,}"
    return f"{value:,.2f}"


def markdown_table(rows: list[dict], mode: str) -> str:
    if mode == "recover":
        lines = [
            "| Query | Impressions before | Current | Delta | Position before → now | Click delta |",
            "|---|---:|---:|---:|---:|---:|",
        ]
        for row in rows:
            lines.append(
                f"| {row['query']} | {fmt(row['previous_impressions'])} | {fmt(row['current_impressions'])} | "
                f"{fmt(row['impression_delta'])} | {fmt(row['previous_position'])} → {fmt(row['current_position'])} | "
                f"{fmt(row['click_delta'])} |"
            )
        return "\n".join(lines)
    lines = [
        "| Query | Current impressions | Delta | Current clicks | Click delta | Current position |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['query']} | {fmt(row['current_impressions'])} | {fmt(row['impression_delta'])} | "
            f"{fmt(row['current_clicks'])} | {fmt(row['click_delta'])} | {fmt(row['current_position'])} |"
        )
    return "\n".join(lines)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, help="GSC Queries.csv comparison export")
    parser.add_argument("--limit", type=int, default=25, help="Rows per ranked list")
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    try:
        rows = load(args.csv_path)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    recover = sorted(
        (row for row in rows if row["impression_delta"] < 0),
        key=lambda row: (row["recovery_score"], -row["impression_delta"]),
        reverse=True,
    )[: args.limit]
    protect = sorted(rows, key=lambda row: row["protection_score"], reverse=True)[: args.limit]
    growing = sorted(
        (row for row in rows if row["impression_delta"] > 0 or row["click_delta"] > 0),
        key=lambda row: (row["impression_delta"], row["click_delta"]),
        reverse=True,
    )[: args.limit]

    if args.format == "json":
        print(json.dumps({
            "row_count": len(rows),
            "recover_candidates": [compact(row) for row in recover],
            "protect_candidates": [compact(row) for row in protect],
            "growing_candidates": [compact(row) for row in growing],
        }, ensure_ascii=False, indent=2))
    else:
        print(f"Rows analyzed: {len(rows)}\n")
        print("## Recover candidates\n")
        print(markdown_table(recover, "recover"))
        print("\n## Protect candidates\n")
        print(markdown_table(protect, "protect"))
        print("\n## Growing candidates\n")
        print(markdown_table(growing, "protect"))
        print("\nSemantic relevance and page ownership must be reviewed before recommendations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
