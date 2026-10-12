VGG16 FEATURE EXTRACTOR + SVM — MOUTH REGION
============================================================

Run ID: 20260808_1240_mouth_vgg16_svm_seed42
Status: COMPLETED AND VALIDATED

DATASET
-------
Total Mouth ROI : 2987
Train           : 2389
Validation      : 296
Test            : 302
Debug used      : No

MODEL
-----
Feature extractor : VGG16 ImageNet
Include top       : False
Pooling           : Global Average Pooling
Feature dimension : 512
Classifier        : Linear SVM
C                 : 0.1
Class weight      : Balanced
Seed              : 42

FINAL TEST RESULTS
------------------
Accuracy          : 0.569536
Balanced Accuracy : 0.567088
Precision (Fake)  : 0.574713
Recall (Fake)     : 0.641026
Specificity       : 0.493151
F1-score (Fake)   : 0.606061
ROC-AUC           : 0.626932
Average Precision : 0.637725
MCC               : 0.135686

CONFUSION MATRIX
----------------
TN=72, FP=74, FN=56, TP=100

VALIDATION
----------
Model reload test        : PASS
Prediction equality      : PASS
Decision-score equality  : PASS
Mouth-only dataset       : PASS
Debug exclusion          : PASS
Split/class distribution : PASS
302 test predictions     : PASS
600 DPI figures          : PASS

OUTPUT CONTENTS
---------------
artifacts/ : Metrics, predictions, summaries and manifests
models/    : Final pipeline, scaler and SVM classifier
figures/   : 600 DPI PNG and PDF figures
logs/      : Experiment log

Overall status: PASS
