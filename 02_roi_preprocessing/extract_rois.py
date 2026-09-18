"""Extract simple face-region ROI crops from frame metadata.

This script is intentionally lightweight: it documents the project contract and
can be adapted to the exact landmark detector used in the Drive notebooks.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
import pandas as pd
from tqdm import tqdm


ROI_COLUMNS = {
    "eye": ("eye_x1", "eye_y1", "eye_x2", "eye_y2"),
    "brow": ("brow_x1", "brow_y1", "brow_x2", "brow_y2"),
    "mouth": ("mouth_x1", "mouth_y1", "mouth_x2", "mouth_y2"),
}


def crop_region(image_path: Path, bounds: tuple[int, int, int, int]):
    image = cv2.imread(str(image_path))
    if image is None:
        return None
    x1, y1, x2, y2 = bounds
    h, w = image.shape[:2]
    x1, x2 = max(0, x1), min(w, x2)
    y1, y2 = max(0, y1), min(h, y2)
    if x2 <= x1 or y2 <= y1:
        return None
    return image[y1:y2, x1:x2]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--roi", choices=sorted(ROI_COLUMNS), required=True)
    parser.add_argument("--image-root", type=Path, default=Path("."))
    args = parser.parse_args()

    metadata = pd.read_csv(args.metadata)
    required = {"frame_path", "label", "split", *ROI_COLUMNS[args.roi]}
    missing = required - set(metadata.columns)
    if missing:
        raise ValueError(f"Missing columns for {args.roi}: {sorted(missing)}")

    columns = ROI_COLUMNS[args.roi]
    for _, row in tqdm(metadata.iterrows(), total=len(metadata)):
        frame_path = args.image_root / str(row["frame_path"])
        bounds = tuple(int(row[col]) for col in columns)
        crop = crop_region(frame_path, bounds)
        if crop is None:
            continue

        out_dir = args.output_root / args.roi / str(row["split"]) / str(row["label"])
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / Path(row["frame_path"]).name
        cv2.imwrite(str(out_path), crop)


if __name__ == "__main__":
    main()
