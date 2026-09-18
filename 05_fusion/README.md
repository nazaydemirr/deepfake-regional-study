# 05 Fusion

Bu klasor, bolgesel model tahminlerini karar seviyesinde birlestirir.

Deney 1 icin iki ana fuzyon mantigi kullanilir:

1. Majority voting: goz, kas ve agiz tahminlerinden en az 2/3 ayni sinifi secerse final karar olusur.
2. Weighted soft voting: validation ROC-AUC degerlerinden turetilen agirliklarla ROI skorlarini birlestirir.

Corrected weighted soft voting formulu:

```text
raw_weight = max(validation_roc_auc - 0.5, epsilon)
weight = raw_weight / sum(raw_weight)
fusion_score = sum(weight_roi * score_roi)
```

Drive'daki 4 model ailesi:

- xception
- efficientnet_b0
- swinv2_tiny
- swinv2_texture
