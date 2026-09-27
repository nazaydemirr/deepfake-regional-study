from __future__ import annotations

import torch
import torch.nn as nn
from torchvision.models import Swin_V2_T_Weights, swin_v2_t


class SwinV2TinyBinaryClassifier(nn.Module):
    def __init__(
        self,
        pretrained: bool = True,
        dropout: float = 0.20,
    ) -> None:
        super().__init__()

        weights = (
            Swin_V2_T_Weights.IMAGENET1K_V1
            if pretrained
            else None
        )

        self.backbone = swin_v2_t(weights=weights)

        in_features = self.backbone.head.in_features
        self.backbone.head = nn.Identity()

        self.classifier = nn.Sequential(
            nn.LayerNorm(in_features),
            nn.Dropout(p=dropout),
            nn.Linear(in_features, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.backbone(x)
        return self.classifier(features).squeeze(1)
