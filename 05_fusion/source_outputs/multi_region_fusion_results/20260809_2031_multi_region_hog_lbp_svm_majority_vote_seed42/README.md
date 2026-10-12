# 20260809_2031_multi_region_hog_lbp_svm_majority_vote_seed42

## Method
Decision-Level Late Fusion with Majority Voting.

No new model was trained. Existing HOG + LBP + SVM test predictions from
Eyebrow, Eye and Mouth regions were aligned on the same original selected
test frames. Face 0 was used for strict cross-region one-to-one matching.

Final rule:
- fake_votes >= 2 -> Fake
- fake_votes < 2 -> Real

## Fair comparison
All single-region metrics and fusion metrics in this run were recalculated
on the exact same common test-frame intersection.

## Outputs
- predictions/majority_vote_common_test_predictions.csv
- metrics/common_test_metrics.csv
- metrics/fusion_improvement_vs_single_regions.csv
- metrics/improvement_summary.json
- figures/*.png
- artifacts/input_alignment_audit.csv
- artifacts/quality_gates.json
- config_resolved.yaml
- run_summary.json
- output_manifest.csv
