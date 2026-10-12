from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from torch.utils.data import DataLoader
from tqdm.auto import tqdm


def safe_roc_auc(y_true: np.ndarray, probs: np.ndarray) -> float:
    if len(np.unique(y_true)) < 2:
        return float("nan")
    return float(roc_auc_score(y_true, probs))


def safe_pr_auc(y_true: np.ndarray, probs: np.ndarray) -> float:
    if len(np.unique(y_true)) < 2:
        return float("nan")
    return float(average_precision_score(y_true, probs))


def compute_metrics(
    y_true: np.ndarray,
    probs: np.ndarray,
    threshold: float,
) -> Dict[str, float]:
    preds = (probs >= threshold).astype(np.int64)
    return {
        "accuracy": float(accuracy_score(y_true, preds)),
        "precision": float(
            precision_score(y_true, preds, zero_division=0)
        ),
        "recall": float(
            recall_score(y_true, preds, zero_division=0)
        ),
        "f1": float(
            f1_score(y_true, preds, zero_division=0)
        ),
        "roc_auc": safe_roc_auc(y_true, probs),
        "pr_auc": safe_pr_auc(y_true, probs),
    }


def select_best_f1_threshold(
    y_true: np.ndarray,
    probs: np.ndarray,
    *,
    threshold_min: float,
    threshold_max: float,
    threshold_steps: int,
    default_threshold: float,
) -> Tuple[float, float]:
    if len(y_true) == 0:
        raise ValueError("Cannot select threshold from an empty validation set.")
    if threshold_steps < 2:
        raise ValueError("threshold_steps must be >= 2.")

    thresholds = np.linspace(
        float(threshold_min),
        float(threshold_max),
        int(threshold_steps),
    )
    best_threshold = float(default_threshold)
    best_f1 = -1.0

    for threshold in thresholds:
        preds = (probs >= threshold).astype(np.int64)
        score = f1_score(
            y_true,
            preds,
            zero_division=0,
        )
        if score > best_f1:
            best_f1 = float(score)
            best_threshold = float(threshold)

    return best_threshold, best_f1


def assert_finite_tensor(
    tensor: torch.Tensor,
    name: str,
) -> None:
    if not torch.isfinite(tensor).all():
        raise FloatingPointError(
            f"NaN/Inf detected in {name}."
        )


def assert_finite_gradients(model: nn.Module) -> None:
    for name, parameter in model.named_parameters():
        if parameter.grad is None:
            continue
        if not torch.isfinite(parameter.grad).all():
            raise FloatingPointError(
                f"NaN/Inf gradient in parameter: {name}"
            )


def run_epoch(
    *,
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
    amp_enabled: bool,
    scaler,
    gradient_clip_norm: float,
    amp_overflow_abort_after: int = 8,
    optimizer: Optional[torch.optim.Optimizer] = None,
) -> Dict[str, Any]:
    training = optimizer is not None
    model.train(training)

    running_loss = 0.0
    total_samples = 0
    amp_overflow_steps = 0
    consecutive_amp_overflows = 0

    labels_all: List[float] = []
    probs_all: List[float] = []
    sample_ids: List[str] = []
    video_ids: List[str] = []
    paths: List[str] = []

    grad_context = (
        torch.enable_grad()
        if training
        else torch.no_grad()
    )

    with grad_context:
        progress = tqdm(
            loader,
            leave=False,
            desc="Train" if training else "Evaluate",
        )

        for batch in progress:
            images = batch["image"].to(
                device,
                non_blocking=True,
            )
            labels = batch["label"].to(
                device,
                non_blocking=True,
            )

            assert_finite_tensor(images, "input images")
            assert_finite_tensor(labels, "labels")

            if training:
                optimizer.zero_grad(set_to_none=True)

            with torch.autocast(
                device_type=device.type,
                dtype=(
                    torch.float16
                    if device.type == "cuda"
                    else torch.bfloat16
                ),
                enabled=amp_enabled,
            ):
                logits = model(images)
                assert_finite_tensor(logits, "logits")
                loss = criterion(logits, labels)
                assert_finite_tensor(loss, "loss")

            if training:
                if amp_enabled:
                    # Dynamic loss scaling may transiently create Inf gradients.
                    # GradScaler is designed to skip that optimizer step and
                    # reduce its scale, so a single AMP overflow is not fatal.
                    scaler.scale(loss).backward()
                    scaler.unscale_(optimizer)

                    if gradient_clip_norm > 0:
                        torch.nn.utils.clip_grad_norm_(
                            model.parameters(),
                            max_norm=gradient_clip_norm,
                            error_if_nonfinite=False,
                        )

                    previous_scale = float(scaler.get_scale())
                    scaler.step(optimizer)
                    scaler.update()
                    current_scale = float(scaler.get_scale())

                    overflow = current_scale < previous_scale
                    if overflow:
                        amp_overflow_steps += 1
                        consecutive_amp_overflows += 1
                        optimizer.zero_grad(set_to_none=True)

                        if consecutive_amp_overflows >= amp_overflow_abort_after:
                            raise FloatingPointError(
                                "Persistent AMP gradient overflow: "
                                f"{consecutive_amp_overflows} consecutive steps. "
                                "Disable mixed precision or inspect inputs/model."
                            )
                    else:
                        consecutive_amp_overflows = 0

                else:
                    # FP32 baseline: non-finite gradients are always fatal.
                    loss.backward()
                    assert_finite_gradients(model)

                    if gradient_clip_norm > 0:
                        torch.nn.utils.clip_grad_norm_(
                            model.parameters(),
                            max_norm=gradient_clip_norm,
                            error_if_nonfinite=True,
                        )

                    optimizer.step()

            probs = (
                torch.sigmoid(logits)
                .detach()
                .float()
                .cpu()
                .numpy()
            )
            labels_np = (
                labels.detach()
                .float()
                .cpu()
                .numpy()
            )

            batch_size = int(images.shape[0])
            running_loss += float(loss.item()) * batch_size
            total_samples += batch_size

            labels_all.extend(labels_np.tolist())
            probs_all.extend(probs.tolist())
            sample_ids.extend(list(batch["sample_id"]))
            video_ids.extend(list(batch["video_id"]))
            paths.extend(list(batch["path"]))

            postfix = {"loss": f"{loss.item():.4f}"}
            if amp_enabled:
                postfix["amp_overflows"] = amp_overflow_steps
            progress.set_postfix(**postfix)

    if total_samples == 0:
        raise RuntimeError("No samples processed.")

    return {
        "loss": running_loss / total_samples,
        "labels": np.asarray(labels_all, dtype=np.int64),
        "probabilities": np.asarray(probs_all, dtype=np.float64),
        "sample_ids": sample_ids,
        "video_ids": video_ids,
        "paths": paths,
        "amp_overflow_steps": int(amp_overflow_steps),
    }
