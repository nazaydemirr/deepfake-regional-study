from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import pandas as pd
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
from torchvision.models import Swin_V2_T_Weights


LABEL_TO_INDEX = {
    "real": 0.0,
    "fake": 1.0,
}


def build_transforms(
    image_size: int,
    augmentation: Dict[str, float],
):
    # Methodological choice:
    # For ImageNet-pretrained Swin V2, the normalization attached to the
    # pretrained weights is used. No validation/test statistics are learned.
    weights = Swin_V2_T_Weights.IMAGENET1K_V1
    weight_transform = weights.transforms()
    mean = weight_transform.mean
    std = weight_transform.std

    train_transform = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(
                p=float(augmentation["horizontal_flip_probability"])
            ),
            transforms.RandomRotation(
                degrees=float(augmentation["rotation_degrees"])
            ),
            transforms.ColorJitter(
                brightness=float(augmentation["brightness"]),
                contrast=float(augmentation["contrast"]),
                saturation=float(augmentation["saturation"]),
                hue=float(augmentation["hue"]),
            ),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ]
    )

    eval_transform = transforms.Compose(
        [
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=mean, std=std),
        ]
    )

    normalization_info = {
        "source": "Swin_V2_T_Weights.IMAGENET1K_V1",
        "mean": list(mean),
        "std": list(std),
        "learned_from_project_data": False,
        "uses_validation_or_test_statistics": False,
    }

    return train_transform, eval_transform, normalization_info


class EyebrowROIDataset(Dataset):
    def __init__(
        self,
        dataframe: pd.DataFrame,
        transform,
        sample_col: str,
        video_col: str,
        label_col: str,
        resolved_path_col: str = "_resolved_image_path",
    ) -> None:
        self.df = dataframe.reset_index(drop=True).copy()
        self.transform = transform
        self.sample_col = sample_col
        self.video_col = video_col
        self.label_col = label_col
        self.resolved_path_col = resolved_path_col

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, index: int) -> Dict[str, Any]:
        row = self.df.iloc[index]
        path = Path(str(row[self.resolved_path_col]))

        if not path.is_file():
            raise FileNotFoundError(
                f"ROI image disappeared after audit: {path}"
            )

        try:
            with Image.open(path) as img:
                image = img.convert("RGB")
        except Exception as exc:
            raise RuntimeError(f"Image decode failed: {path}") from exc

        image = self.transform(image)

        label_text = str(row[self.label_col])
        if label_text not in LABEL_TO_INDEX:
            raise ValueError(f"Unexpected label: {label_text}")

        return {
            "image": image,
            "label": torch.tensor(
                LABEL_TO_INDEX[label_text],
                dtype=torch.float32,
            ),
            "sample_id": str(row[self.sample_col]),
            "video_id": str(row[self.video_col]),
            "path": str(path),
        }
