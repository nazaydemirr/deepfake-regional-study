"""Validation-weighted soft voting for regional deepfake predictions."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, precision_score, recall_score, roc_auc_score


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True, type=Path)
    parser.add_argument("--weights", required=True, type=Path)
    parser.add_argument("--model-family", required=True)
    parser.add_argument("--threshold", type=float, default=0.5)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    predictions = pd.read_csv(args.predictions)
    weights = pd.read_csv(args.weights)
    weights = weights[weights["model_family"] == args.model_family].iloc[0]
    roi_weights = {
        "eye": float(weights["weight_eye"]),
        "brow": float(weights["weight_brow"]),
        "mouth": float(weights["weight_mouth"]),
    }

    df = predictions[predictions["model_family"] == args.model_family].copy()
    score_table = df.pivot_table(index="sample_id", columns="roi", values="y_score", aggfunc="first")
    truth = df.groupby("sample_id")["y_true"].first()

    out = pd.DataFrame(index=score_table.index)
    out["y_true"] = truth
    out["fusion_score"] = sum(score_table[roi] * weight for roi, weight in roi_weights.items())
    out["fusion_pred"] = (out["fusion_score"] >= args.threshold).astype(int)

    metrics = {
        "accuracy": accuracy_score(out["y_true"], out["fusion_pred"]),
        "balanced_accuracy": balanced_accuracy_score(out["y_true"], out["fusion_pred"]),
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
