from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)


def save_figure(
    fig,
    output_path: Path,
    min_short_edge: int = 600,
) -> None:
    fig.tight_layout()
    fig.savefig(
        output_path,
        dpi=150,
        bbox_inches="tight",
    )
    plt.close(fig)

    with Image.open(output_path) as image:
        if min(image.size) < min_short_edge:
            raise RuntimeError(
                f"Figure resolution failed: "
                f"{output_path} -> {image.size}"
            )


def generate_all_figures(
    *,
    history_df,
    labels,
    probabilities,
    threshold: float,
    figures_dir: Path,
    min_short_edge: int,
) -> None:
    figures_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.plot(
        history_df["epoch"],
        history_df["train_loss"],
        label="Training Loss",
        linewidth=2,
    )
    ax.plot(
        history_df["epoch"],
        history_df["val_loss"],
        label="Validation Loss",
        linewidth=2,
        linestyle="--",
    )
    ax.set_title(
        "Training and Validation Loss Curve",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("Epoch", fontsize=11)
    ax.set_ylabel("Loss", fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.25)
    save_figure(
        fig,
        figures_dir / "training_validation_loss.png",
        min_short_edge,
    )

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.plot(
        history_df["epoch"],
        history_df["train_accuracy"],
        label="Training Accuracy",
        linewidth=2,
    )
    ax.plot(
        history_df["epoch"],
        history_df["val_accuracy"],
        label="Validation Accuracy",
        linewidth=2,
        linestyle="--",
    )
    ax.set_title(
        "Training and Validation Accuracy",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("Epoch", fontsize=11)
    ax.set_ylabel("Accuracy", fontsize=11)
    ax.set_ylim(0, 1.01)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.25)
    save_figure(
        fig,
        figures_dir / "training_validation_accuracy.png",
        min_short_edge,
    )

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    ax.plot(
        history_df["epoch"],
        history_df["val_roc_auc"],
        label="Validation ROC-AUC",
        linewidth=2,
    )
    ax.set_title(
        "Validation ROC-AUC by Epoch",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("Epoch", fontsize=11)
    ax.set_ylabel("ROC-AUC", fontsize=11)
    ax.set_ylim(0, 1.01)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.25)
    save_figure(
        fig,
        figures_dir / "validation_roc_auc.png",
        min_short_edge,
    )

    preds = (probabilities >= threshold).astype(np.int64)
    cm = confusion_matrix(
        labels,
        preds,
        labels=[0, 1],
    )

    fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
    image = ax.imshow(cm)
    ax.set_title(
        "Test Confusion Matrix",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("Predicted Class", fontsize=11)
    ax.set_ylabel("True Class", fontsize=11)
    ax.set_xticks([0, 1], labels=["Real", "Fake"])
    ax.set_yticks([0, 1], labels=["Real", "Fake"])

    for i in range(2):
        for j in range(2):
            ax.text(
                j,
                i,
                str(cm[i, j]),
                ha="center",
                va="center",
                fontsize=14,
            )

    fig.colorbar(image, ax=ax)
    save_figure(
        fig,
        figures_dir / "test_confusion_matrix.png",
        min_short_edge,
    )

    if len(np.unique(labels)) == 2:
        fpr, tpr, _ = roc_curve(labels, probabilities)
        auc = roc_auc_score(labels, probabilities)

        fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
        ax.plot(
            fpr,
            tpr,
            linewidth=2,
            label=f"Swin V2 Tiny (AUC = {auc:.4f})",
        )
        ax.plot(
            [0, 1],
            [0, 1],
            linestyle="--",
            linewidth=1.5,
            label="Random Classifier",
        )
        ax.set_title(
            "Test ROC Curve",
            fontsize=14,
            fontweight="bold",
        )
        ax.set_xlabel(
            "False Positive Rate",
            fontsize=11,
        )
        ax.set_ylabel(
            "True Positive Rate",
            fontsize=11,
        )
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1.01)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.25)
        save_figure(
            fig,
            figures_dir / "test_roc_curve.png",
            min_short_edge,
        )

    precision, recall, _ = precision_recall_curve(
        labels,
        probabilities,
    )
    ap = average_precision_score(
        labels,
        probabilities,
    )

    fig, ax = plt.subplots(figsize=(10, 8), dpi=150)
    ax.plot(
        recall,
        precision,
        linewidth=2,
        label=f"Swin V2 Tiny (AP = {ap:.4f})",
    )
    ax.set_title(
        "Test Precision-Recall Curve",
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("Recall", fontsize=11)
    ax.set_ylabel("Precision", fontsize=11)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.01)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.25)
    save_figure(
        fig,
        figures_dir / "test_precision_recall_curve.png",
        min_short_edge,
    )
