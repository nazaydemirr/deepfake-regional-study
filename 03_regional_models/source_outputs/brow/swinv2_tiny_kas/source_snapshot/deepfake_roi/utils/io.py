from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable

import torch


CHECKPOINT_REQUIRED_KEYS = {
    "epoch",
    "model_state_dict",
    "optimizer_state_dict",
    "scheduler_state_dict",
    "scaler_state_dict",
    "best_metric_score",
    "best_threshold",
    "best_epoch",
    "epochs_without_improvement",
    "history",
    "config",
    "rng_state",
    "loader_generator_state",
}


def atomic_save_checkpoint(state: Dict[str, Any], target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temp_path = target.with_suffix(target.suffix + ".tmp")

    if temp_path.exists():
        temp_path.unlink()

    try:
        torch.save(state, temp_path)

        loaded = torch.load(
            temp_path,
            map_location="cpu",
            weights_only=False,
        )

        missing = CHECKPOINT_REQUIRED_KEYS.difference(loaded.keys())
        if missing:
            raise RuntimeError(
                f"Checkpoint integrity failed. Missing keys: {sorted(missing)}"
            )

        if int(loaded["epoch"]) != int(state["epoch"]):
            raise RuntimeError("Checkpoint epoch integrity mismatch.")

        os.replace(temp_path, target)

    except Exception:
        if temp_path.exists():
            temp_path.unlink()
        raise


def load_checkpoint(path: Path, device: torch.device) -> Dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(path)

    state = torch.load(
        path,
        map_location=device,
        weights_only=False,
    )

    missing = CHECKPOINT_REQUIRED_KEYS.difference(state.keys())
    if missing:
        raise RuntimeError(
            f"Checkpoint incomplete. Missing keys: {sorted(missing)}"
        )

    return state


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def save_json_atomic(data: Dict[str, Any], target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.replace(tmp, target)


def hash_source_tree(paths: Iterable[Path]) -> Dict[str, str]:
    return {
        str(path): sha256_file(path)
        for path in sorted(paths)
        if path.is_file()
    }
