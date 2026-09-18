# Experiment Summary

## Data Split

- Total selected frames: 3000
- Real: 1200 train / 150 validation / 150 test
- Fake: 1200 train / 150 validation / 150 test
- Rejected frames: 206

## ROI Branches

- Eye branch: Nazlican / Deney 1 / Goz
- Brow branch: Kader / Deney 1 / Kas
- Mouth branch: Dilara / Deney 1 / Agiz

## Corrected Weighted Fusion

| Model family | Accuracy | F1 | ROC-AUC | Notes |
| --- | ---: | ---: | ---: | --- |
| xception | 0.6888 | 0.6995 | 0.7412 | Fusion AUC is slightly below mouth-only AUC in same cohort |
| efficientnet_b0 | 0.7347 | 0.7263 | 0.8196 | Stronger than xception in this corrected table |
| swinv2_tiny | 0.7959 | 0.7753 | 0.8763 | Best corrected weighted fusion result |
| swinv2_texture | 0.6888 | 0.6667 | 0.7672 | Texture branch improves interpretability but not top score here |

## Interpretation

The corrected weighted soft voting run does not show a statistically clear AUC gain over mouth-only predictions for the listed model families because each delta confidence interval includes zero. This should be reported honestly in the article while emphasizing the system-level robustness motivation of late fusion.
