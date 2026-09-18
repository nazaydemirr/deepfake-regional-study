"""Aggregate ROI prediction files into one long-format table."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "sample_id",
    "split",
    "roi",
    "model_family",
    "y_true",
    "y_score",
    "y_pred",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("prediction_files", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    frames = []
    for path in args.prediction_files:
        df = pd.read_csv(path)
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"{path} is missing columns: {sorted(missing)}")
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
