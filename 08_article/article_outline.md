# Article Outline

## 1. Introduction

- Deepfake detection problem and regional artifacts
- Motivation for ROI-specific analysis
- Why eye, brow and mouth regions are useful

## 2. Related Work

- FaceForensics++ benchmark
- Facial region analysis and mouth movement methods
- CNN and transformer backbones
- Lightweight feature fusion methods
- Decision-level late fusion and majority voting

## 3. Dataset and Preprocessing

- Frame extraction and filtering
- Real/Fake balanced split
- ROI extraction for eye, brow and mouth
- Exclusion criteria for unreadable/no-face frames

## 4. Regional Models

- Xception
- EfficientNet-B0
- SwinV2-Tiny
- SwinV2 + texture descriptors
- Optional DenseNet121 / HOG-LBP-KAZE baselines

## 5. Fusion Strategy

- Majority voting
- Validation-AUC weighted soft voting
- Weight formula and thresholding

## 6. Results

- Corrected weighted fusion table
- ROI-level comparison
- Mouth-only vs fusion delta AUC
- Confidence interval interpretation

## 7. Discussion

- Why fusion may not always improve AUC
- Robustness vs top-line metric tradeoff
- Dataset leakage and cross-dataset generalization risks
- Future work: temporal modeling and multimodal extension

## 8. Conclusion

- Summarize regional framework and honest corrected fusion result
