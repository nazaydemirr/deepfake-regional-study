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
