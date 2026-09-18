"""Plot corrected fusion metrics from the paper-ready CSV table."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics", default="../06_metrics_tables/paper_ready_corrected_fusion_table.csv", type=Path)
    parser.add_argument("--output", default="fusion_metrics.png", type=Path)
    args = parser.parse_args()

    df = pd.read_csv(args.metrics)
    plot_df = df.set_index("model_family")[["accuracy", "f1", "roc_auc", "pr_auc"]]
    ax = plot_df.plot(kind="bar", figsize=(10, 5), ylim=(0, 1), rot=30)
    ax.set_ylabel("Score")
    ax.set_xlabel("Model family")
    ax.set_title("Corrected weighted fusion metrics")
    ax.legend(loc="lower right")
    plt.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(args.output, dpi=200)


if __name__ == "__main__":
    main()
