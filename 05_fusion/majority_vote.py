"""Majority-vote fusion for eye, brow and mouth ROI predictions."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score


def majority_vote(values: pd.Series) -> int:
    return int(values.sum() >= 2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model-family", required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.predictions)
    df = df[df["model_family"] == args.model_family]
    pivot_pred = df.pivot_table(index="sample_id", columns="roi", values="y_pred", aggfunc="first")
    pivot_score = df.pivot_table(index="sample_id", columns="roi", values="y_score", aggfunc="mean")
    truth = df.groupby("sample_id")["y_true"].first()

    out = pd.DataFrame(index=pivot_pred.index)
    out["y_true"] = truth
    out["fusion_pred"] = pivot_pred[["eye", "brow", "mouth"]].apply(majority_vote, axis=1)
    out["fusion_score"] = pivot_score[["eye", "brow", "mouth"]].mean(axis=1)

    metrics = {
        "accuracy": accuracy_score(out["y_true"], out["fusion_pred"]),
        "precision": precision_score(out["y_true"], out["fusion_pred"], zero_division=0),
        "recall": recall_score(out["y_true"], out["fusion_pred"], zero_division=0),
        "f1": f1_score(out["y_true"], out["fusion_pred"], zero_division=0),
        "roc_auc": roc_auc_score(out["y_true"], out["fusion_score"]),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    out.reset_index().to_csv(args.output, index=False)
    pd.Series(metrics).to_csv(args.output.with_suffix(".metrics.csv"), header=["value"])


if __name__ == "__main__":
    main()
