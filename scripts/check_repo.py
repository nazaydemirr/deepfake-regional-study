"""Small repository sanity check."""

from __future__ import annotations

from pathlib import Path


REQUIRED = [
    "01_data_splits/README.md",
    "02_roi_preprocessing/README.md",
    "03_regional_models/README.md",
    "04_predictions/README.md",
    "05_fusion/README.md",
    "06_metrics_tables/README.md",
    "07_figures/README.md",
    "08_article/README.md",
    "requirements.txt",
]


def main() -> None:
    missing = [path for path in REQUIRED if not Path(path).exists()]
    if missing:
        raise SystemExit(f"Missing required files: {missing}")
    print("Repository structure OK")


if __name__ == "__main__":
    main()
