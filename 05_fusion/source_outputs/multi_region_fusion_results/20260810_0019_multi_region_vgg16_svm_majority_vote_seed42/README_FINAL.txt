3-REGION VGG16 + SVM LATE FUSION
================================

Run ID: 20260810_0019_multi_region_vgg16_svm_majority_vote_seed42
Status: COMPLETED AND VALIDATED

SOURCE RUNS
-----------
Eyebrow : VGG16_FeatureExtractor_SVM_Kas
Mouth   : 20260808_1240_mouth_vgg16_svm_seed42
Eye     : 20260808_1124_eye_vgg16_svm_seed42

FUSION METHOD
-------------
Method         : Equal-weight 3-way Majority-Vote Late Fusion
New training   : NO
Meta-model     : NO
Calibration fit: NO
Weights        : Eyebrow=1/3, Mouth=1/3, Eye=1/3
Final rule     : FAKE if at least 2 of 3 regional models predict FAKE

MATCHING
--------
Canonical key        : real_test_XXXXX / fake_test_XXXXX
Mouth/Eye face policy: face_index=0
Matched test samples : 196
Mouth extra faces excluded from fusion: 10
Eye extra faces excluded from fusion  : 10
Ground-truth agreement: PASS

FINAL TEST RESULTS
------------------
Accuracy          : 0.596939
Balanced Accuracy : 0.599531
Precision (FAKE)  : 0.570175
Recall (FAKE)     : 0.684211
Specificity (REAL): 0.514851
F1-score (FAKE)   : 0.622010
ROC-AUC (vote score): 0.624596
Average Precision (vote score): 0.570261
MCC               : 0.201675

CONFUSION MATRIX
----------------
TN=52, FP=49, FN=30, TP=65

IMPORTANT
---------
The fusion uses only saved regional model decisions. The Mouth source run does not provide a saved fake_probability comparable to the Eyebrow/Eye probabilities.
Therefore raw SVM decision scores are NOT averaged with probabilities and no new calibration/model is fitted.

OUTPUT CONTENTS
---------------
predictions/ : Fused sample-level test predictions
metrics/     : Final metrics, classification report, region comparison
figures/     : English PNG/PDF figures, verified >=600 px short side
artifacts/   : Matching audit and excluded non-zero-face rows
logs/        : Run log
checkpoints/ : README only; no checkpoint because no training
