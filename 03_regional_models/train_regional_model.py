"""Train a classical ROI baseline from precomputed features.

Deep-learning notebooks in Drive can stay as notebooks; this baseline keeps the
repo runnable without storing heavy images or model weights.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.svm import SVC


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--features", required=True, type=Path)
    parser.add_argument("--output-model", required=True, type=Path)
    parser.add_argument("--output-report", required=True, type=Path)
    parser.add_argument("--label-col", default="label")
    parser.add_argument("--split-col", default="split")
    args = parser.parse_args()

    df = pd.read_csv(args.features)
    train = df[df[args.split_col] == "train"]
    test = df[df[args.split_col] == "test"]
    drop_cols = {args.label_col, args.split_col, "sample_id", "frame_path"}
    feature_cols = [col for col in df.columns if col not in drop_cols]

    clf = SVC(kernel="rbf", probability=True, class_weight="balanced", random_state=42)
    clf.fit(train[feature_cols], train[args.label_col])

    proba = clf.predict_proba(test[feature_cols])[:, 1]
    pred = (proba >= 0.5).astype(int)
    auc = roc_auc_score(test[args.label_col], proba)
    report = classification_report(test[args.label_col], pred)

    args.output_model.parent.mkdir(parents=True, exist_ok=True)
    args.output_report.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": clf, "feature_cols": feature_cols, "roc_auc": auc}, args.output_model)
    args.output_report.write_text(f"ROC-AUC: {auc:.6f}\n\n{report}", encoding="utf-8")


if __name__ == "__main__":
    main()
