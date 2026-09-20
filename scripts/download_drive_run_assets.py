#!/usr/bin/env python3
"""Download Drive run outputs into the repository.

This is a focused downloader for files discovered by recursively listing Deney 1
run folders. It preserves the repository layout by output type.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def item(file_id: str, target: str, size: int) -> dict[str, object]:
    return {"id": file_id, "target": target, "size": size}


ASSETS: list[dict[str, object]] = [
    # brow / eyebrow DenseNet121 run
    item("1B435FYeF5-UNcwS-ptOMui1tFLc3soES", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/output_manifest.csv", 3873),
    item("1H_GXg0KcdmkK1Q2ctvMsTZmQHKBYwzSI", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/run_summary.json", 1852),
    item("1JAI9ZvWkb2JKDVUX_T0O5znnR5qGeL2Q", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/requirements_lock.txt", 14001),
    item("1-p2-9llgqDxSdqH_RJ6W5k51wfTq2Ybs", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/environment.json", 348),
    item("1Ks4jOSxxcpTUFhMs9hiviQcXrk7wW_gn", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/config_resolved.yaml", 939),
    item("1QWnGwoSoqbTNTkEZ_ch29m_ZypXdG2fi", "07_figures/brow/20260808_1335_eyebrow_densenet121_seed42/test_precision_recall_curve.png", 61591),
    item("1c8U6Zae-7NgrWVVKa34EsTMC7E7QxpTx", "07_figures/brow/20260808_1335_eyebrow_densenet121_seed42/test_roc_curve.png", 60968),
    item("17D6t804OP3GMHboom4RQ-OihUTnfvXXE", "07_figures/brow/20260808_1335_eyebrow_densenet121_seed42/test_confusion_matrix.png", 43936),
    item("1dKsBocDAvJij99V_19x4PUBbWLjyS_Eq", "07_figures/brow/20260808_1335_eyebrow_densenet121_seed42/training_validation_auc.png", 61882),
    item("11d6HnxdiwnY_YwKpHn3xOXW9bCbN1gEN", "07_figures/brow/20260808_1335_eyebrow_densenet121_seed42/training_validation_loss.png", 88723),
    item("1S9lqdjP8D7ODcly1EFZl3DhYizJBsyBZ", "04_predictions/brow/20260808_1335_eyebrow_densenet121_seed42/test_source_predictions.csv", 9829),
    item("1Sfz5PMUuomPD4uiazGBga-TjYIYYWkKV", "04_predictions/brow/20260808_1335_eyebrow_densenet121_seed42/test_image_predictions.csv", 47448),
    item("1iIFxYGaYyOGtJGXvHsZYGF5mQTiIHmJQ", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/metrics/final_source_level_metrics.csv", 230),
    item("1s2sk10Idt2FIRAIAG2Yl6wh3qYFQ1Ubq", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/metrics/classification_report.csv", 406),
    item("10CB5elMi43QYK7MDw_aA69mhkcSlYsOP", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/metrics/final_image_level_metrics.csv", 313),
    item("1RwOYtUYGpM65crotnahs3mTCVURuqbG7", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/metrics/validation_threshold.json", 142),
    item("1yno9CmZqFP1H7DK3VPAWD8V1BdMFrh3A", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/metrics/combined_training_history.csv", 5071),
    item("1ombiWm8-5Sx3s95ETwKYmYN44gb1-cBp", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/metrics/finetune_training_history.csv", 2274),
    item("12a8MI1sCe6w0k1i_-P9OOqhgsgqw0LlJ", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/metrics/frozen_training_history.csv", 2917),
    item("1oS6zdAd32ML23zszUDSXb0CS5TIQ3Eva", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/metrics/quality_gates.json", 122),
    item("1SWPjCAWa6OnaGSEq0XAMGJTD7O6G1Elv", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/logs/finetune_training_log.csv", 2198),
    item("1JE5AocaS0Pom_xWf_o31Lu_ldaB_YaX0", "06_metrics_tables/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/logs/frozen_training_log.csv", 2848),
    item("1xke3RFLQdthmkiDTlqp6tNtfZylzzor4", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/artifacts/final_audit.json", 494),
    item("1dpAf6jRklr26fuxhcE4ezfsE1SeRelyz", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/artifacts/figure_quality_audit.csv", 280),
    item("1oKD7s8FJQkpo3xQ6qSTgAd6jQAYrl-Hm", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/artifacts/model_summary.txt", 2436),
    item("17xYxA_lQRTdzn3yakUdDe3ROsw3QR3EJ", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/artifacts/leakage_check.json", 725),
    item("1XrDO5IUIl3A3pWoSpui2OeYB-RNWGkhk", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/artifacts/accounting_summary.json", 111),
    item("1B_FNLhGfu-o1_uk3tDrGvHdCl_dMnpdZ", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/artifacts/model_manifest.csv", 966711),
    item("17gI9NaRNVKzv1tUYMqulAyvnickQtJxE", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/artifacts/source_group_split_assignment.csv", 562393),
    item("1ICCP3OJx3NOccz_u_tQ-y9anpVQ-cmGz", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/artifacts/content_duplicate_clusters.csv", 57),
    item("1L0EDc34OEitaPOE786xLwR7rB3D6hd6_", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/artifacts/dataset_count_audit.csv", 194),
    item("1Fx8CVZQ5bOUKVR8NGH85I6yyLib5L-m4", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/checkpoints/last.keras", 63805220),
    item("1P3GHtdIbWrGdWDacxwBpD7fqe1eyx368", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/checkpoints/training_state.json", 283),
    item("1hsitZYsCcjrw4K6LYocRnMLQzoqVgdKt", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/checkpoints/best.keras", 63805220),
    item("1MHa-iVmYw14-Y91ADTo0EGpx75qtWU27", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/checkpoints/finetune_backup/latest.weights.h5", 63417056),
    item("1TrmL5LqL3E-M9BheLJbV26oTOIrF2NVF", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/checkpoints/finetune_backup/training_metadata.json", 25),
    item("12GMhU235fUqOs3KgAFG4L1wUVKUkOUbC", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/checkpoints/frozen_backup/latest.weights.h5", 29292352),
    item("1eu1Px1qpcx471Phq8RZIxT56bWShxdzo", "03_regional_models/drive_outputs/brow/20260808_1335_eyebrow_densenet121_seed42/checkpoints/frozen_backup/training_metadata.json", 25),

    # brow / eyebrow EfficientNet-B0 run
    item("1VVRg4IhYzvAwgWqrqLs5pXs10fQKvZzg", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/output_manifest.csv", 3984),
    item("1Rp33JpmgAFJR466nuW2No6oWYxqgxcG0", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/run_summary.json", 2200),
    item("1sZr4Z_C7KT6usaqpasqoVqZrklC4cWUy", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/RUN_COMPLETE.json", 134),
    item("1_C0pC_sFJ39XAYLftEIYeQn5WgXpH2ku", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/data_accounting.json", 1212),
    item("1oMo2aQ5gsTt3Lg53-Fz2jrI3de2XczGQ", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/requirements_lock.txt", 14001),
    item("1jUQCU433Qb_hg1Pm1LFTuwCefNjQEOsS", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/environment.json", 230),
    item("10vVGwc-r827I2GXzgQQtxpSVoFsQhxY0", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/config_resolved.yaml", 515),
    item("1HsAmZ8-Kwb1nNcddR4E2tzIh7hd1ynPw", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/run_schema.json", 181),
    item("1tlZYXS8LCGXbLxiL4K-9cpA--6etoEsO", "07_figures/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/validation_threshold_analysis.png", 97984),
    item("1bLEj9fiu6RSlnXuw6EJ-meXG54df9In0", "07_figures/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/test_confusion_matrix.png", 40717),
    item("1twgjVcIn4Y_niv7Jr_6n9s_X9X-vbjaQ", "07_figures/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/test_precision_recall_curve.png", 58808),
    item("1IUylz8wqIYcAZZJbYk7sa0bEcRAD6mOl", "07_figures/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/test_roc_curve.png", 61932),
    item("1cUWYHX36uFO90cWHNIfeBnmwVWYCLfPX", "07_figures/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/validation_metrics_curve.png", 86721),
    item("1S_QdSr5Uezln7MP-kfWloyoWXcShQqGL", "07_figures/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/training_validation_loss_curve.png", 84645),
    item("18NDOwIe5Z2Oj5Nz0JAY78JTx6zBqLoO5", "04_predictions/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/test_predictions.csv", 43125),
    item("1i6NiZ0tgsmm6P4_UZGOM67xuM2cfyW8q", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/metrics/inference_reload_test.json", 350),
    item("1KyX3Wk0Uu0n1WA6YgWMtoxa9VE0onnjd", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/metrics/final_test_metrics.csv", 302),
    item("1Bp0PSv-9v70enSRx-Lsk68N-aFbkwezb", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/metrics/validation_selected_threshold_metrics.json", 372),
    item("1Yf3ZcmRyVtCR8rXPq8EUkM9wSCCj78--", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/metrics/validation_threshold_search.csv", 31314),
    item("1e9OP_ldE3vk10x_-FEFJsG5HcZjGOPhO", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/metrics/finetune_training_history.csv", 6552),
    item("1tr1up2Kiczw-I-SGyvvWlKYtsJU8yrzY", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/metrics/finetune_training_summary.json", 17524),
    item("19siRRbj_fUAckXYXBfdKqCrzvg_ASiRF", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/metrics/frozen_training_summary.json", 6087),
    item("1gHb5v5i4aSXdg-HtgMcQWGm77AK3ccvW", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/metrics/frozen_training_history.csv", 2391),
    item("116wRkIekEGixiGBTF65H7DGY9WZZi3VI", "06_metrics_tables/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/logs/training.log", 4168),
    item("1Y3SDVE0vjmebegsAF3H41tsONTwQ53if", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/artifacts/model_architecture.txt", 20562),
    item("1rQqTduaBUei2a6cm8NW1qcer9mTZ4pvb", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/artifacts/eligible_metadata.csv", 1682971),
    item("1CbCaWWl9D36psefddkgSMXZCHXLxBLwD", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/artifacts/skipped_or_error_metadata.csv", 595779),
    item("1DUpWN4i9CajDM38nnTTrzrsbSjQ70Few", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/artifacts/eligible_metadata_before_cache.csv", 1494597),
    item("1X74i24kUyXJ161LGd0d47QPMIbKpgBNm", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/artifacts/training_metadata_standardized.csv", 651486),
    item("1UDh8svdUX-KrulNVAmRb6amz9KP46N7J", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/checkpoints/finetune/last.ckpt", 48615533),
    item("1ndjzPdcoJ2ZOn2E86R-AMg4Rk1J9CSuJ", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/checkpoints/finetune/epoch_015.ckpt", 48615533),
    item("1SI2XIxol0RH1jaxCxZ0o0LrAZAhEn0Jk", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/checkpoints/finetune/epoch_014.ckpt", 48614701),
    item("1fMbJ8JFDPH6OoSMu3NZXrZZudxdcH1pG", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/checkpoints/finetune/epoch_013.ckpt", 48613869),
    item("1lDoWfOxwhP85ogFcfIr7DJIqmXnbdShB", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/checkpoints/finetune/best.ckpt", 48613037),
    item("1d6qubMyqJTBxb5ahFGl8ldvgKQiNxWcG", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/checkpoints/frozen/last.ckpt", 16370077),
    item("1GIDOMgLvjs0AiFaLr_uxnXSGgc05OgQX", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/checkpoints/frozen/best.ckpt", 16370077),
    item("1xV-DUhFglU244Qpbo6FDCmqPYIqNB3eV", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/checkpoints/frozen/epoch_005.ckpt", 16370077),
    item("1dFX_6t_hfQV-bZbub85JZunDhWFx508S", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/checkpoints/frozen/epoch_004.ckpt", 16369245),
    item("1W0CXchq3KtWVeLALGQk7oirtWpFN9a53", "03_regional_models/drive_outputs/brow/20260808_1248_eyebrow_efficientnet_b0_seed42/checkpoints/frozen/epoch_003.ckpt", 16368413),

    # brow / HOG-LBP-KAZE SVM/RF run
    item("1nQicMbiEEkZEY9d4jRv0kPHlk8lA6sx3", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/output_manifest.csv", 3682),
    item("105pNczTQnY-63_jA6urxeW6VnNhwxgXE", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/run_summary.json", 1941),
    item("11lw67NMUuXR7fKXxLhehxDCaIGVkXPgn", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/requirements_lock.txt", 12566),
    item("1AIr8POWgI4yhURD6REXQnTdRHnhaotwq", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/environment.json", 197),
    item("1kmhozybTAFVFlJM5MkkPl4vNnVgRir55", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/config_resolved.yaml", 1556),
    item("1yOfzG67DKiWmcr1l-FQnhQjTCl5r7mQL", "07_figures/brow/hog_lbp_kaze_svm_rf_kas/roc_curves.png", 523030),
    item("1Z3tgm9qovwUTwj9_aQgNvpaQDUs4z9iC", "07_figures/brow/hog_lbp_kaze_svm_rf_kas/confusion_matrices.png", 294331),
    item("1aCwNP6HDzuUA6vgLnT9tMS3Jd07Ivpmw", "07_figures/brow/hog_lbp_kaze_svm_rf_kas/model_performance_comparison.png", 461098),
    item("1E8zO_1tlnSXPMG4G9aMo5OmU_JD76L-X", "04_predictions/brow/hog_lbp_kaze_svm_rf_kas/test_predictions.csv", 58057),
    item("1KAyFZDto4yyZu5oE0n02ahtypouCXWa9", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/metrics/classification_report_E3_HOG_LBP_KAZE_RF.csv", 406),
    item("1o_lLKCfHW2BmYLThlFFineVHhAExk5W9", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/metrics/classification_report_E2_HOG_LBP_KAZE_SVM.csv", 405),
    item("1oKbMB4-_rkB8t_0YKUIq6hbNaFwzTVUD", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/metrics/classification_report_E1_HOG_LBP_SVM.csv", 413),
    item("1Y87bZhPry5z1yw3I6U1DUln-D9WGTw-c", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/metrics/final_test_metrics.csv", 612),
    item("1ZVtieloe0FaV8BjQoOrRaTwBnVKU0Uxr", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/metrics/hog_lbp_kaze_rf_validation_metrics.csv", 704),
    item("1yDDsYooAnYpfO9euSwyf6g2cISQdPb0g", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/metrics/hog_lbp_kaze_svm_validation_metrics.csv", 581),
    item("1Z_5s6FYfl1BXlbQ5T9fX6PDCO1gP0LNq", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/metrics/hog_lbp_svm_validation_metrics.csv", 573),
    item("1MX3Sz3D5BfZd7qpKzLIBfBmT7zE_yJDm", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/metrics/fresh_load_inference_test.json", 47),
    item("1LRAYQ7nMCKsC-pQAY8jpB9FJKivsWEPG", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/metrics/data_accounting.json", 236),
    item("1ce33AWlNduYtt8A0ema6IyPYmus-VCcc", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/metrics/split_audit.json", 197),
    item("1OD9wXwLcHxF9BZPNs1_o_gr3m67PVRzv", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/logs/audit_summary.txt", 623),
    item("1r4j58pIG96QzodEHFyLlg0X7sG-5Ss0w", "06_metrics_tables/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/logs/training.log", 692),
    item("1NKBs2_PO9KQNgIpEjDmfBpfkFWkD02ya", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/feature_metadata.csv", 81247),
    item("1vjv0ZRri-1nymbW97t2Pg6OF2FZF5TER", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/features_full.npz", 36322296),
    item("1i3Zna8kl-eaBnjcueislbkDNFxwBa7Ny", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/dataset_index.csv", 699616),
    item("1TsBHSSRIJD9lTztPzOtfzCIx2RxD7GF-", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/feature_chunks/features_0008.npz", 3933577),
    item("1eM0vM7TbmNf74aR89bD42MeDDt0xzmAv", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/feature_chunks/features_0007.npz", 4641782),
    item("1g6MAd5XK84fll5HBIKRoJN3E9EGK4VMY", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/feature_chunks/features_0006.npz", 4625242),
    item("1tOMKprfWeBwMXdxfBral7ufUg9DxsjMW", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/feature_chunks/features_0005.npz", 4648855),
    item("1lVvlRxJEtq7jSus7Kf3kOmlNyLno9LDA", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/feature_chunks/features_0004.npz", 4618221),
    item("14NcuyRBNugh2qgYC6IAUJiL4YieeMr91", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/feature_chunks/features_0003.npz", 4640961),
    item("1sITBFR6KBEEjn2cN9x6SJEMF70I3uq4W", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/feature_chunks/features_0002.npz", 4586711),
    item("1FLzHeltk6JcOTDWJU9ngdNEgs3g96VEM", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/artifacts/feature_chunks/features_0001.npz", 4649851),
    item("10Rh4Am-86c53Rxro1uIJ90BqecmSWyxY", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/checkpoints/best_hog_lbp_kaze_random_forest.joblib", 8236505),
    item("13UFccuyMRGkJv726pqU8_kFEfmlcz7wP", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/checkpoints/best_hog_lbp_kaze_rbf_svm.joblib", 76435677),
    item("1V49v_YGLni6RRBZa1bqVHAIAgoANxyQj", "03_regional_models/drive_outputs/brow/hog_lbp_kaze_svm_rf_kas/checkpoints/best_hog_lbp_rbf_svm.joblib", 76041533),

    # brow / VGG16 feature extractor + SVM run
    item("1XCF6gnWEFFytYsP3nse3SeTuv8Aiou-v", "06_metrics_tables/drive_outputs/brow/vgg16_feature_extractor_svm_kas/output_manifest.csv", 1982),
    item("1o-ngZDPVcub2_QDNU1WjSDzU0Ucg1FZa", "06_metrics_tables/drive_outputs/brow/vgg16_feature_extractor_svm_kas/run_summary.json", 1421),
    item("10huk0CL6asRXS2YsxSQpfBffD6Gq076f", "06_metrics_tables/drive_outputs/brow/vgg16_feature_extractor_svm_kas/requirements_lock.txt", 14001),
    item("1qWgGKTGl627Yue4sfhrJJ4_Uu11LGKNr", "06_metrics_tables/drive_outputs/brow/vgg16_feature_extractor_svm_kas/environment.json", 375),
    item("1fh4eT8CVajWk4U2qRJRGPeKro3P4-EAw", "06_metrics_tables/drive_outputs/brow/vgg16_feature_extractor_svm_kas/config_resolved.yaml", 765),
    item("1qgSh_1EBn4NRyOZpsxyzXFKtRxcSPj2q", "07_figures/brow/vgg16_feature_extractor_svm_kas/precision_recall_curve.png", 59102),
    item("1ABM3Zs_wx4GVM8jxIe5rTUw6S_xhz0sJ", "07_figures/brow/vgg16_feature_extractor_svm_kas/roc_curve.png", 58653),
    item("1FJ3TT4RJn-4xVBZLT8T0ypyfikxHUN8A", "07_figures/brow/vgg16_feature_extractor_svm_kas/confusion_matrix.png", 31058),
    item("19Wm75b5rzH1z8223GUyzjETMBpcJckl6", "04_predictions/brow/vgg16_feature_extractor_svm_kas/test_predictions.csv", 36059),
    item("1ckEnqmY0FQGi7YhvQKg7DEFFHfGoNioL", "06_metrics_tables/drive_outputs/brow/vgg16_feature_extractor_svm_kas/metrics/metrics.json", 534),
    item("1x6Hew91BHp5A10ibqL0L4iPchZr4zNCb", "06_metrics_tables/drive_outputs/brow/vgg16_feature_extractor_svm_kas/metrics/confusion_matrix.csv", 56),
    item("1WBcpIu_8WOOSqGC6pYTyaYJcARie3bCd", "06_metrics_tables/drive_outputs/brow/vgg16_feature_extractor_svm_kas/metrics/classification_report.csv", 386),
    item("17HrWx_uqiabuWcw_Hx0N6TULHpP_oXiP", "06_metrics_tables/drive_outputs/brow/vgg16_feature_extractor_svm_kas/metrics/svm_validation_search.csv", 1556),
    item("1s3eLIIWqvtwWF1ycyjWl0FMz5cgT1MYf", "06_metrics_tables/drive_outputs/brow/vgg16_feature_extractor_svm_kas/logs/training.log", 1126),
    item("1POU4GzAH1_QTywAB0xUf6w_QLdqoKMGX", "03_regional_models/drive_outputs/brow/vgg16_feature_extractor_svm_kas/artifacts/test_features.npz", 289174),
    item("1WGFGwI_zbUwtquxAujMmqmMOTCnKZ1nw", "03_regional_models/drive_outputs/brow/vgg16_feature_extractor_svm_kas/artifacts/val_features.npz", 299807),
    item("1DSqB4sS-o2rolKeVSPPt7vH_v6xvNBg9", "03_regional_models/drive_outputs/brow/vgg16_feature_extractor_svm_kas/artifacts/train_features.npz", 2258948),
    item("1CCrtcUP0DsKy801R1Are238d3Fipmwos", "03_regional_models/drive_outputs/brow/vgg16_feature_extractor_svm_kas/artifacts/feature_extractor.json", 189),
    item("1uSDeSDxUZ2GnbD6YaH140_BxXB-HuKnO", "03_regional_models/drive_outputs/brow/vgg16_feature_extractor_svm_kas/artifacts/dataset_inventory.csv", 286038),
    item("14iTx4uyfdboj_69WwJQ673ZkGaIU1WMV", "03_regional_models/drive_outputs/brow/vgg16_feature_extractor_svm_kas/checkpoints/scaler.joblib", 12903),
    item("1byF0QNL_S9ipffyTWHwQAkZC4bHpnbgL", "03_regional_models/drive_outputs/brow/vgg16_feature_extractor_svm_kas/checkpoints/svm_model.joblib", 6517259),

    # brow / Xception run (large .keras files are downloaded and split separately)
    item("1U1AT6TxfYk9M6zKGrm2OaPE8POWXs6wg", "06_metrics_tables/drive_outputs/brow/xception_kas/output_manifest.csv", 4361),
    item("15ITCujq4Yec9-yFbfI0PBpbfvkJ86EQ8", "06_metrics_tables/drive_outputs/brow/xception_kas/run_summary.json", 2489),
    item("1vl_1Lmo3ToI-A5Jnxj9ZwR889DiY2d_g", "06_metrics_tables/drive_outputs/brow/xception_kas/environment.json", 316),
    item("1sKHem3sIRr6DaufWMUcsXeghj8cE7aU1", "06_metrics_tables/drive_outputs/brow/xception_kas/requirements_lock.txt", 14001),
    item("1dsV_L3x1oKNMnIW6OkcX5-Qj9voda_ND", "06_metrics_tables/drive_outputs/brow/xception_kas/config_resolved.yaml", 860),
    item("1isOY_RxhlUe_kQmMnb5Wk5B7T-Qh8N_z", "03_regional_models/drive_outputs/brow/xception_kas/artifacts/model_summary.txt", 75),
    item("1j81KOxBalDGh5HbtrrWs1Z67V9RWE1Nh", "03_regional_models/drive_outputs/brow/xception_kas/artifacts/xception_model_config.json", 732),
    item("1pVY0W4UVtJEZe-57qQu4h3ofYV_2xx1z", "07_figures/brow/xception_kas/10_final_test_metrics.png", 230837),
    item("1vv_fIkg8sz7gsbASkfQK-34rfTJ-Nb0o", "07_figures/brow/xception_kas/09_frozen_vs_finetuned.png", 198942),
    item("1Zr1eyWfDH37mBO_wXDKf2YpS3T6fFrsu", "07_figures/brow/xception_kas/08_finetune_loss.png", 322167),
    item("1gAwDMEWDKuB8e5mD93LV1HeeA2UnPVgo", "07_figures/brow/xception_kas/07_finetune_auc.png", 281639),
    item("1S4t-b5sBio9e_HkpTgKh4Z3FQZ_xjbrZ", "07_figures/brow/xception_kas/06_finetune_accuracy.png", 332159),
    item("16mbHXSGVOb5PGoUrjb0NDuXPOzudl-eU", "07_figures/brow/xception_kas/05_frozen_loss.png", 344981),
    item("1FRgXWG8mhqcyWHodEEqgD6o3fIwyTBk2", "07_figures/brow/xception_kas/04_frozen_auc.png", 299353),
    item("1pHJJ-wyNuW2_RKVz6x67MEcS_ih9c5I9", "07_figures/brow/xception_kas/03_frozen_accuracy.png", 339063),
    item("14Q4SLK8r4eZMUXrUZZc2iJkHd_2vdfO2", "07_figures/brow/xception_kas/02_roc_curve.png", 302066),
    item("18GPWrn5DybMMNBms5rTqZavHHIxhe4vg", "07_figures/brow/xception_kas/01_confusion_matrix.png", 179016),
    item("1H7jxt2jrHxmAwEmhHyIm3oJXIUb2CZpV", "04_predictions/brow/xception_kas/test_predictions.csv", 17928),
    item("1wZ-6M3z6vaJvoSnJj3iKaBb95BrMfAez", "06_metrics_tables/drive_outputs/brow/xception_kas/metrics/figure_manifest.json", 445),
    item("1OAT0s9CIv46SeN_i0z7cGju6iI2m1Gtn", "06_metrics_tables/drive_outputs/brow/xception_kas/metrics/final_test_metrics.csv", 274),
    item("1kHJS5TwkyThANNedKEms3_sLzDb_S_eL", "06_metrics_tables/drive_outputs/brow/xception_kas/metrics/classification_report.txt", 326),
    item("1Ja1TCm60f_ZyCUi9cHJu0RMWlTeYHCV9", "06_metrics_tables/drive_outputs/brow/xception_kas/metrics/final_test_metrics.json", 746),
    item("1XTM3NFQoxE6rJs0W8AEAWPi-FiNInzqd", "06_metrics_tables/drive_outputs/brow/xception_kas/metrics/model_selection_and_test_summary.json", 886),
    item("1d2MJWl1TgdthVMEpkaMs-3ENUjwaHkaF", "06_metrics_tables/drive_outputs/brow/xception_kas/metrics/finetune_training_summary.json", 600),
    item("1dirnqQ1m5MtSgttmOlP9QtogCD1ZjcIm", "06_metrics_tables/drive_outputs/brow/xception_kas/metrics/finetune_training_history.csv", 2247),
    item("1fPdEn3HbBantU2nWEi4ysSqtGjd7LfdW", "06_metrics_tables/drive_outputs/brow/xception_kas/metrics/frozen_training_summary.json", 621),
    item("1n6K8IfWBbHI8G8bC7qJPu1EKYHP5um-m", "06_metrics_tables/drive_outputs/brow/xception_kas/metrics/frozen_training_history.csv", 1608),
    item("1jWIUZbgAU_u1q1bp2IiqJ2498M9EIXdb", "06_metrics_tables/drive_outputs/brow/xception_kas/metrics/augmentation_config.json", 468),
    item("1HpzuUdi3oaveYxkWzkRUtsxrdA7rglsV", "06_metrics_tables/drive_outputs/brow/xception_kas/logs/finetune_training_log.csv", 2254),
    item("1XsaHnZFgY6XgLFd1fLNvHC0Xrat_UyWj", "06_metrics_tables/drive_outputs/brow/xception_kas/logs/frozen_training_log.csv", 1613),
    item("1q2yXPiSFyhElL7OMLsFO-3QorxozPO-Y", "06_metrics_tables/drive_outputs/brow/xception_kas/logs/skipped_or_invalid_dataset_files.csv", 23),
    item("19W3xmQagepEpKI46yYLJxWHJqRYhYLE4", "06_metrics_tables/drive_outputs/brow/xception_kas/logs/dataset_copy_failures.csv", 32),

    # brow / HOG-LBP SVM run
    item("1s-gWTCuWTzgFKY1VidgHTjTSbDWFzBbE", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/output_manifest.csv", 3782),
    item("1O3Oc-p0NDjI6gv05eyYn9nR0B63EnsKy", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/run_summary.json", 3863),
    item("1a8hf3dJdqVRC0SugPDq5TxZCboKZO6Rp", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/environment.json", 295),
    item("1d-l_Iaj7fLYScKVlEp4IfVioeu6nfcSo", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/requirements_lock.txt", 12614),
    item("13kv9TS-cDOxiz0ZLvXEieTVce8D2R22v", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/config_resolved.yaml", 1171),
    item("1MJA1ntExWWmDn__XzC4S1QHRI-WlSOJT", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/artifacts/svm_model.joblib", 30677205),
    item("1Z8wZURR_zxc919z6d3WS41RxqnDPanzI", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/artifacts/feature_preprocessing.joblib", 91575),
    item("1NQZkY35yTFw_S4nugi6Lnv8VmPI8NjYV", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/artifacts/feature_pipeline.json", 554),
    item("1w_RxgYiCQaikysvTVU_gEHEmU7mPZAw9", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/artifacts/feature_dimensions.json", 98),
    item("1JB1B8YL56rMzBxfKrYXYCj_IJn-BSVTy", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/artifacts/features_test.npz", 3920141),
    item("14whTjchtXk-pQy9RbKPWcB3s7HWhriMj", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/artifacts/features_val.npz", 4105238),
    item("14NWVRbmYYjCZPWrc_ggkkBBQCiq2-LsS", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/artifacts/features_train.npz", 31255926),
    item("1Ar1-UElWfeiG9-J60upuDHI49GERwn_E", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/artifacts/metadata_used.csv", 1656194),
    item("1HxzQany4RMcpw7Va44isQQarzmkrfoHd", "07_figures/brow/hog_lbp_svm_kas/test_decision_score_distribution.png", 41973),
    item("1K0CntP5ZzlcQakoMzzZttGT3iWggQEf8", "07_figures/brow/hog_lbp_svm_kas/test_precision_recall_curve_video_level.png", 63164),
    item("1lybw7xZmWOSbkcU84RQD0ziUBcjqc7Sl", "07_figures/brow/hog_lbp_svm_kas/test_precision_recall_curve_frame_level.png", 60328),
    item("1IJL65E1PsedxOBdNcw_hxZvXx1t9P4Aw", "07_figures/brow/hog_lbp_svm_kas/test_roc_curve_video_level.png", 59444),
    item("1MT2rzWC3fxx20ADVcSR_7e8Rz8pxDIvx", "07_figures/brow/hog_lbp_svm_kas/test_roc_curve_frame_level.png", 59986),
    item("1eE8gY-txUJZk6_rHW4WQS9mGQesYkxyr", "07_figures/brow/hog_lbp_svm_kas/test_confusion_matrix_video_level.png", 30763),
    item("1Yiq_V__ECz-S2fGi_q6BwEdLImWBl44P", "07_figures/brow/hog_lbp_svm_kas/test_confusion_matrix_frame_level.png", 30806),
    item("1tNZ_haPLkdm3Wv39mgxPH_b9ym3-08m4", "07_figures/brow/hog_lbp_svm_kas/svm_validation_f1_comparison.png", 96946),
    item("1mczs_Jiy3ZbUCS069r6Abjj8WxOSpvw-", "07_figures/brow/hog_lbp_svm_kas/dataset_distribution.png", 43111),
    item("1vmiBur99maBbxqil-A7fOoT-zYNR6pvn", "04_predictions/brow/hog_lbp_svm_kas/test_predictions_video_level.csv", 15937),
    item("1YXZRRUUNWHcEiDpNi6P8y9uJhIj-z_ud", "04_predictions/brow/hog_lbp_svm_kas/test_predictions_frame_level.csv", 58701),
    item("1CYMZhRKcMR59gbNAW1spzd29OpvwaaDg", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/metrics/figure_quality_audit.csv", 540),
    item("1-XUjrl0Uguo2R1QmK6Fw7hwUXZaCVU3u", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/metrics/test_metrics_summary.csv", 351),
    item("1WSHoQKTayF_i9NaVEB7SZ0gg0gJWdJmK", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/metrics/test_metrics_video_level.json", 244),
    item("19_giz-7zUS5L0hqWG71afyeveE4gq_Wo", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/metrics/test_metrics_frame_level.json", 244),
    item("1UC31dIxofpBu75Un8hA6fNmCNFou7rN4", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/metrics/quality_gates.json", 357),
    item("1Ac5aOfZJP6dE6V6tWyVkNgFIy1TVwqe4", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/metrics/fresh_load_inference_test.json", 168),
    item("1oXB9JgIuPD14ORo8HqeqEFpXv_YV9-82", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/metrics/svm_selection.json", 501),
    item("1ws2FKltNMtq11dKGkEuOevm-rEw03aVS", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/metrics/svm_validation_search.csv", 2337),
    item("1E8CjcYmdbDE_Ae9qnCOoH3C5a4DgmXsQ", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/metrics/data_accounting.json", 616),
    item("1isFWZF7Yt6OHBliEnTJxqq9ACdZOrz-J", "06_metrics_tables/drive_outputs/brow/hog_lbp_svm_kas/logs/run.log", 4059),
    item("1r0hYFPUnP-mHfiQvJ0nmXF_QDlOVBMp-", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/checkpoints/checkpoint_quality_gate.ckpt", 30683788),
    item("1eszRhP4XXlb6iJq7ifNL_ml7xaXc4IM0", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/checkpoints/last.ckpt", 30683788),
    item("1zZCiXe7XhIYzDxY82Gh0MvFkecmRtRXb", "03_regional_models/drive_outputs/brow/hog_lbp_svm_kas/checkpoints/best.ckpt", 30683788),

    # brow / SwinV2 Tiny run (large checkpoints are downloaded and split separately)
    item("1D-MCqgxD42b3T1I1JZ4N-ZILymddHi2W", "06_metrics_tables/drive_outputs/brow/swinv2_tiny_kas/output_manifest.csv", 6896),
    item("18Mtkey7s50ZlOuj9eof7LxSHgZKtTn2R", "06_metrics_tables/drive_outputs/brow/swinv2_tiny_kas/run_summary.json", 2081),
    item("1XTctPS42M5GGiwYV4ID2eAsddfpqKaTF", "06_metrics_tables/drive_outputs/brow/swinv2_tiny_kas/environment.json", 313),
    item("1i7gkPVQoVI1sdiNjkfznXsKfSgVFYAKs", "06_metrics_tables/drive_outputs/brow/swinv2_tiny_kas/requirements_lock.txt", 154),
    item("1MlBndlo5To64G9b9rp-5DsysMHWsAkN5", "06_metrics_tables/drive_outputs/brow/swinv2_tiny_kas/config_resolved.yaml", 2360),
    item("1YStLlNDeO3HYMpAQsBUCifoPk1WTRVeJ", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/artifacts/checkpoint_continuity_test.json", 160),
    item("1w4WcCRY8WkGZ0ktbHWPx47sj3Bxws4nx", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/artifacts/input_numerical_sanity.json", 245),
    item("1p7-6TOs1L6404OAq3k-36WGPq4-uR7lJ", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/artifacts/normalization_audit.json", 473),
    item("1QFt3L3irPsHWX4k7pvwO07q3bHR5VWAf", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/artifacts/dataset_summary.csv", 145),
    item("1LvdqRI1_yjspVXWdM5EWK7fDskzrgUhh", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/artifacts/metadata_used.csv", 2071959),
    item("1AA52HHao1h7vl56Mp1Z7LrRKs5xHuSkD", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/artifacts/split_leakage_report.json", 786),
    item("1hAtYAcrvgksI3ZBcr3VD1I6Gui9QiiBd", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/artifacts/data_accounting.json", 201),
    item("12QqxzAB9lBByMmEFvpeLW-IQbQpnub60", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/artifacts/metadata_schema_audit.json", 1195),
    item("12FNzVPh9_eBtxq5LS8yMciYYx1HK0KaN", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/artifacts/source_hash_manifest.json", 3222),
    item("1xsFlcWSRJgi7-NcqQFnx18v0t9n4c-BL", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/__init__.py", 0),
    item("1H8e0d0xZUVIYdQldOw_SJ2Zc9pdAZht5", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/models/swin.py", 898),
    item("1LPR8IHo3op-maTWyrY35mo28SkdpvQoa", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/models/__init__.py", 0),
    item("16H_hGUo7i7wAEuhABSmQ0xV-_uxTQgiN", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/training/engine.py", 8100),
    item("10jPDquiiAT9CgYg3oNA15kqokBmblVUQ", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/training/__init__.py", 0),
    item("191HZfVEj7VbK3MWFwn9NniPTAzQHEt8l", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/utils/io.py", 2596),
    item("1EPbx43648PdmDCAZUOeC19OV9KFtq-1l", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/utils/repro.py", 1419),
    item("1AF2bLI0AUfT4TY9kwU8M1yfvsJMVLXjv", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/utils/__init__.py", 0),
    item("128zMmd6hHOeFDOEUlJqCHJvv86PlouFI", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/evaluation/plots.py", 5730),
    item("1R-sNGifCcBvDHv5P9K5CrqDBYmau_qxv", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/evaluation/__init__.py", 0),
    item("1ANBXjAN9iuPWguI34MKSm37KvVA3-eBJ", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/data/dataset.py", 3584),
    item("1CgHQNjKX0yaAEHHCtV_KFIAQGdmbqdxM", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/data/__init__.py", 0),
    item("1vmZOFNwElBl_dlkJt_M7V5dszC59hA_Y", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/__pycache__/__init__.cpython-312.pyc", 160),
    item("1pxBOkmxvw97d5h5FhLKzf62Im2bsXVdp", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/models/__pycache__/__init__.cpython-312.pyc", 167),
    item("1nrMqqwWj1t4FaJGFboEvviuFy2n-wLcg", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/models/__pycache__/swin.cpython-312.pyc", 1928),
    item("1OQiQkkFBnuPpgECJGEXASEOS74Q0TcnL", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/training/__pycache__/__init__.cpython-312.pyc", 169),
    item("1MVXhjZKw6ZiqSr4EN8U1arcmN6qnLS7Z", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/training/__pycache__/engine.cpython-312.pyc", 9455),
    item("16ACJitIOLizZOXLadrGkNC-aLmoU0TwD", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/utils/__pycache__/__init__.cpython-312.pyc", 166),
    item("142Dj8xoup28lkaCykCi5TfNEI2nKU_sY", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/utils/__pycache__/io.cpython-312.pyc", 4315),
    item("1Y8sk6Xs2_PpsuX0wwLDgKp2ZlKmzmpQL", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/utils/__pycache__/repro.cpython-312.pyc", 3120),
    item("1LY7r5NtmPBpKmuhKyRBTHIIjvqbEqKso", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/evaluation/__pycache__/__init__.cpython-312.pyc", 171),
    item("1yFyHhW-TpmTY8mjoCMiPLcSk6ebnr0KO", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/evaluation/__pycache__/plots.cpython-312.pyc", 7309),
    item("17OXIZJEWpKhQv9CAV_Ti-yOra39_zwj8", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/data/__pycache__/__init__.cpython-312.pyc", 165),
    item("19uO_PlkPR688A4MVD0TxsDcOsf3EfU77", "03_regional_models/drive_outputs/brow/swinv2_tiny_kas/source_snapshot/deepfake_roi/data/__pycache__/dataset.cpython-312.pyc", 5037),
    item("1WvOsIDzDLAsHBVvkNKzWs8ES8mR5kmOt", "07_figures/brow/swinv2_tiny_kas/test_precision_recall_curve.png", 61752),
    item("1ixvDxwDnhFgrSRldVQMNgcLrm8Rt-yGq", "07_figures/brow/swinv2_tiny_kas/test_roc_curve.png", 72714),
    item("1KcaBoxjz0C4bEmHOyrKWa6y8Cxvc7bya", "07_figures/brow/swinv2_tiny_kas/test_confusion_matrix.png", 40277),
    item("1eqNdHnsoLxpFOA9RBPOq2VZaRxy-mxjX", "07_figures/brow/swinv2_tiny_kas/validation_roc_auc.png", 42548),
    item("1indpUnhyu2a6ODzyd9kustRdY0B1fy8L", "07_figures/brow/swinv2_tiny_kas/training_validation_accuracy.png", 62527),
    item("1bZa1MnARRxsJCpQ_5GrtbRMrvA-9vPhs", "07_figures/brow/swinv2_tiny_kas/training_validation_loss.png", 87360),
    item("1-XlFLpqwo61TViKViVmFtSmpRvEIbCT2", "04_predictions/brow/swinv2_tiny_kas/test_video_predictions.csv", 6311),
    item("1DLu_Ywvy_3TwHAUR6WhoGhXdTCe_GDEj", "04_predictions/brow/swinv2_tiny_kas/test_frame_predictions.csv", 46475),
    item("1AE_6M5PRWCRAyveJs-k5wNwWDSWqQ3ta", "06_metrics_tables/drive_outputs/brow/swinv2_tiny_kas/metrics/test_video_metrics.json", 281),
    item("1vSi8NbONzoQB2-SmZYfOMLEbYe02xqF3", "06_metrics_tables/drive_outputs/brow/swinv2_tiny_kas/metrics/test_frame_metrics.json", 292),
    item("1Vt9pvhY1gq4MMlFtRWPmUacJycvCkcnn", "06_metrics_tables/drive_outputs/brow/swinv2_tiny_kas/metrics/training_history.csv", 6964),
    item("1ucvEg3yafWfxWQc0kbN_L1jzk-Jgjxxf", "06_metrics_tables/drive_outputs/brow/swinv2_tiny_kas/logs/pipeline.log", 1405),
]


def download(asset: dict[str, object]) -> str:
    target = ROOT / str(asset["target"])
    size = int(asset["size"])
    if target.exists() and target.stat().st_size == size:
        return "exists"
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".download")
    url = f"https://drive.google.com/uc?export=download&id={asset['id']}"
    cmd = [
        "curl",
        "-L",
        "--fail",
        "--silent",
        "--show-error",
        "--connect-timeout",
        "20",
        "--max-time",
        "240",
        url,
        "-o",
        str(tmp),
    ]
    subprocess.run(cmd, cwd=ROOT, check=True)
    tmp.replace(target)
    return "downloaded"


def main() -> int:
    counts: dict[str, int] = {}
    for asset in ASSETS:
        status = download(asset)
        counts[status] = counts.get(status, 0) + 1
        print(f"{status:10} {asset['target']}", flush=True)
    print("Summary:", counts, flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"download failed: {exc}", file=sys.stderr)
        raise
