#!/usr/bin/env python3
"""Download selected Deney 1 Google Drive assets into the repository.

The list below mirrors the Drive "Deney 1" experiment material into the
repository layout. Files larger than GitHub's practical single-file limit are
recorded as split-part assets when the split directory exists.
"""

from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_GITHUB_FILE_BYTES = 95 * 1024 * 1024


def asset(file_id: str, target: str, size: int, source: str) -> dict[str, object]:
    return {"id": file_id, "target": target, "size": size, "source": source}


ASSETS: list[dict[str, object]] = [
    # 01_data_splits: common Deney 1 frame selection metadata
    asset("13Azgj_yGMZhj7llmGZeDwOzKuA44KsBH", "01_data_splits/drive_exports/deney_1_frame_primary/islem_checkpoint.json", 204, "Deney 1 Frame"),
    asset("1Z-PxJeUrxBIuFQ2r0TVJt02G0ysUHMK4", "01_data_splits/drive_exports/deney_1_frame_primary/yuzsuz_veya_okunamayan_frameler.csv", 37329, "Deney 1 Frame"),
    asset("1WEeCNk5VjMfRMx7ERwjqJz1LidE47DWj", "01_data_splits/drive_exports/deney_1_frame_primary/secim_metadata.csv", 794241, "Deney 1 Frame"),
    asset("1Qmm0rF0mPFQcTP85oE9R0X3dOMIazq80", "01_data_splits/drive_exports/deney_1_frame_primary/islem_ozeti.json", 541, "Deney 1 Frame"),
    asset("1Amer0KOvJ7fIyiTh1UvniUDI6GaIOpP9", "01_data_splits/drive_exports/deney_1_frame_secondary/yuzsuz_veya_okunamayan_frameler.csv", 37329, "Deney 1 Frame duplicate"),
    asset("1ykC4ZjO2O_EivBa4xHcB2MFSPKq0pDXE", "01_data_splits/drive_exports/deney_1_frame_secondary/secim_metadata.csv", 767241, "Deney 1 Frame duplicate"),

    # Weighted fusion repeat
    asset("1yVNzSnutBNjzTxXBN4mO756Xv40ZJdVI", "03_regional_models/notebooks/fusion/corrected_weighted_fusion_all4_same_formula.ipynb", 29544, "agirlikli fuzyon tekrar"),
    asset("1BRbuYky0tM-yl6UGCraZvli22gLqH8Hq", "05_fusion/results/weighted_soft_voting_corrected_all4_seed42/paper_ready_corrected_fusion_table.csv", 1239, "04_weighted_soft_voting_CORRECTED_ALL4_seed42"),
    asset("1pI56OjiWLivQ-vVHOS3aDZ_psclfphoK", "05_fusion/results/weighted_soft_voting_corrected_all4_seed42/corrected_weighted_fusion_metrics_ALL4.csv", 1991, "04_weighted_soft_voting_CORRECTED_ALL4_seed42"),
    asset("1XIXWPWtZF0g8oTUiDOrh82SMWWYvndr9", "05_fusion/results/weighted_soft_voting_corrected_all4_seed42/corrected_validation_weights_ALL4.csv", 1095, "04_weighted_soft_voting_CORRECTED_ALL4_seed42"),

    # Brow / Kas notebooks
    asset("1exlI40qRLSzbwh7ElA3BVB8c0L6Ej_e2", "03_regional_models/notebooks/brow/AISC_VGG16_SVM_3Region_LateFusion.ipynb", 61875, "Kas Kodlar"),
    asset("1hSb1ARMFcn3IwSG4MNHhNUuwvcuO4Vfr", "03_regional_models/notebooks/brow/HOG_LBP_SVM_Majority_Vote_Region_Fusion_Deney1_CORRECTED.ipynb", 107478, "Kas Kodlar"),
    asset("1mJpeqhsnp0bmENtOnJF0i0Cb62jb4xnM", "03_regional_models/notebooks/brow/20260809_multi_region_calibrated_weighted_score_fusion_seed42_V4_PROVENANCE_FIXED.ipynb", 57888, "Kas Kodlar"),
    asset("1j8R9eNg_j19edYu0jN8GNqh-s_aHKCT-", "03_regional_models/notebooks/brow/DenseNet121_Kas_Deepfake_AISC_Standard_STABILIZED_V3 (1).ipynb", 119411, "Kas Kodlar"),
    asset("1pEkwNKMLsKaTOZ8gRI_qWgqSOm-wmmOC", "03_regional_models/notebooks/brow/EfficientNet_B0_Eyebrow_Nazlican_FINAL_STABLE.ipynb", 533667, "Kas Kodlar"),
    asset("1nWpiVeSOSxficnAuRI5wukSgTi8UbpfX", "03_regional_models/notebooks/brow/HOG_LBP_KAZE_SVM_RF_Kas_Deepfake_Colab_OPENCV4_FIXED.ipynb", 321344, "Kas Kodlar"),
    asset("1oqbCjl1w1116Fg_oe1LWaMoC4eomt8jH", "03_regional_models/notebooks/brow/VGG16_FeatureExtractor_SVM_Kas_Deney1_FIXED.ipynb", 242020, "Kas Kodlar"),
    asset("1xWxgf5Jq-wCJclfhivS0M3TZGQYlT7NN", "03_regional_models/notebooks/brow/Xception_Eyebrow_Deepfake_Colab_ROBUST_FIXED.ipynb", 1037491, "Kas Kodlar"),
    asset("1-XInwpe3n9BAU6GvXz8-iZhaHjfS7nji", "03_regional_models/notebooks/brow/Eyebrow_SwinV2_Tiny_PDF_Standard_Nazlican.ipynb", 445963, "Kas Kodlar"),
    asset("1Ib0_f8t8VxqX5HpuwrCo5zpfDgLoQJpH", "03_regional_models/notebooks/brow/HOG_LBP_SVM_Eyebrow_Deepfake_Colab_FIXED.ipynb", 56572, "Kas Kodlar"),
    asset("1QLfiNCNNdKE0N2bAi5nUOiTA_C67g6Ss", "03_regional_models/notebooks/brow/Eyebrow_SwinV2_LBP_GLCM_Gabor_Wavelet_Fusion_Nazlican_v2.ipynb", 157098, "Kas Kodlar"),
    asset("19btWrCqmLpeBYthwbXritJq6RdYe02mj", "03_regional_models/notebooks/brow/VGG16_sifirdan_egitim_HOG_GIST_RBF_SVM.ipynb", 172063, "Kas Kodlar"),
    asset("1xQQsKA3dDxOfByYOTw8DxnWuGhYG57b5", "02_roi_preprocessing/drive_outputs/brow/kas_roi_cikarma_pipeline_colab_duzeltilmis.ipynb", 2809910, "Kas Kodlar"),

    # Brow / Kas reports
    asset("139bgGT5CAjzS1yjzpVBlCEdPtRG_1FzY", "08_article/reports/brow/VGG16_SVM_Kas_Agiz_Goz_MajorityVote_LateFusion_Sonuclari_Detayli_Rapor.pdf", 581758, "Kas Raporlar"),
    asset("1kxhUKhKZVRJaGhSVVESfWNbvn_wYqznE", "08_article/reports/brow/HOG_LBP_SVM_Majority_Vote_Fuzyon_Sonuc_Analiz_Raporu.pdf", 339101, "Kas Raporlar"),
    asset("1pKpbvDNef_EmFzFZSQkcXqW22mZZgJB5", "08_article/reports/brow/Multi_Region_Fuzyon_Ayrintili_Sonuc_Analiz_Raporu.pdf", 319072, "Kas Raporlar"),
    asset("1V6w8DiPtQOQNh6j_rNLHUHH52NMOplVw", "08_article/reports/brow/DenseNet121_Kas_Detayli_Sonuc_Analiz_Raporu.pdf", 710101, "Kas Raporlar"),
    asset("1TyxeBWzDqTR-d9mzW-0CV0wXc1MaxAVS", "08_article/reports/brow/EfficientNet_B0_Kas_ROI_Detayli_Sonuc_Raporu.pdf", 676237, "Kas Raporlar"),
    asset("1PEk6lRZZpb5Fm325P0WvFkgxHzJoWkCE", "08_article/reports/brow/HOG_LBP_KAZE_SVM_RF_Kas_Deneyi_Detayli_Rapor.pdf", 729883, "Kas Raporlar"),
    asset("16MkhF0ccaf7XQf-1EF7higTvcfOlTOG-", "08_article/reports/brow/VGG16_FeatureExtractor_SVM_Kas_Detayli_Rapor.pdf", 377126, "Kas Raporlar"),
    asset("1YTUv2qgE92hqto8_MVv7QiWBm4fHaEsI", "08_article/reports/brow/Xception_Kas_Deepfake_Detayli_Sonuc_Raporu.pdf", 1542104, "Kas Raporlar"),
    asset("1Eync-w4LLkMbs_Uac44FLs9CsGHxXMgO", "08_article/reports/brow/Kas_SwinV2_Tiny_Detayli_Sonuc_Analiz_Raporu.pdf", 616836, "Kas Raporlar"),
    asset("1JBgmG-ur9CE7R5XN1vfmhxRf_m-HJBY2", "08_article/reports/brow/HOG_LBP_SVM_Kas_Deneyi_Sonuc_Analiz_Raporu.pdf", 823221, "Kas Raporlar"),
    asset("1znjwV8Ky9rTStSIFsp4UWuxQQBmQ29uN", "08_article/reports/brow/Swin_V2_Tiny_LBP_GLCM_Gabor_Wavelet_Fusion.pdf", 896965, "Kas Raporlar"),
    asset("1iElquP0lY_hJbEpNObo-ce-AKXpXpvrK", "08_article/reports/brow/kas_roi_cikarma_kod_ve_cikti_raporu.pdf", 831499, "Kas Raporlar"),
    asset("1b3UT4FRbQOSbJmwbwUhZ_nQGrhpCXxJv", "08_article/reports/brow/VGG16_sifirdan_egitim_HOG_GIST_RBF_SVM.pdf", 496396, "Kas Raporlar"),
    asset("1_SolptVwUR6HhWJUNne_7_VPQgpPsf1v", "08_article/reports/brow/Kas_Uzerinden_Deepfake_Tespiti_Model_Onceliklendirme.pdf", 93572, "Kas Raporlar"),

    # Brow / Kas code explanations
    asset("15T9CEaw4PZB8ckjEBXMupiWxMJGjzy_N", "08_article/code_explanations/brow/Fusion_Notebook_Kod_Aciklamasi.pdf", 293506, "Kas Kod Aciklamalari"),
    asset("1HegsET0Mk9WcoZe1fddukoNdirUJRZoA", "08_article/code_explanations/brow/HOG_LBP_SVM_Majority_Vote_Fuzyon_Kod_Aciklama_Raporu.pdf", 175193, "Kas Kod Aciklamalari"),
    asset("1XYC17_QlzkdbDLHdPlXajZbfupjhieKY", "08_article/code_explanations/brow/Multi_Region_Fuzyon_Notebook_Kod_Aciklama_Raporu.pdf", 63458, "Kas Kod Aciklamalari"),
    asset("1Pxj5TZWU6yfl6YGBVjzBeWqkuBT6S4Gb", "08_article/code_explanations/brow/DenseNet121_Kas_Kod_Calisma_Mantigi_Teknik_Raporu.pdf", 561898, "Kas Kod Aciklamalari"),
    asset("106icgkY1d6gWxAI5BcmhV0_FSgHrokIw", "08_article/code_explanations/brow/EfficientNet_B0_Kas_ROI_Kod_Calisma_Mantigi_Teknik_Raporu.pdf", 361417, "Kas Kod Aciklamalari"),
    asset("1ywo6Guy8TaYBh_kNJ49pBdVQbHMKvUYx", "08_article/code_explanations/brow/HOG_LBP_KAZE_SVM_RF_Kas_Kod_Metodoloji_Raporu.pdf", 273801, "Kas Kod Aciklamalari"),
    asset("15GqLDzvaCHnuHWG-5BkQ_aLrDDDwl5Kq", "08_article/code_explanations/brow/VGG16_FeatureExtractor_SVM_Kas_Kod_Aciklama_Raporu.pdf", 270996, "Kas Kod Aciklamalari"),
    asset("1pyin7A5ajCkMtklqfzub9K5h7vHickPf", "08_article/code_explanations/brow/Xception_Kas_ROI_Kod_Calisma_Raporu.pdf", 288021, "Kas Kod Aciklamalari"),
    asset("1bZQt10Quz5nJk3NW0v1RWJ-Xd1Z5_N1-", "08_article/code_explanations/brow/Kas_SwinV2_Tiny_Kod_Calisma_Mantigi_Teknik_Raporu.pdf", 359140, "Kas Kod Aciklamalari"),
    asset("1pEV123R0z1-mirA4TsSJLnT4t0v_b0nv", "08_article/code_explanations/brow/HOG_LBP_SVM_Kas_Deepfake_Kod_Aciklama_Raporu.pdf", 213945, "Kas Kod Aciklamalari"),
    asset("1VqhIbZ__DhfPgmpj9dmHoTno1xFNIF9r", "08_article/code_explanations/brow/Swin_V2_Tiny_LBP_GLCM_Gabor_Wavelet_Fusion.pdf", 634944, "Kas Kod Aciklamalari"),
    asset("16bRqHfJlrflfStgZS9LsvOD6FCRBePiU", "08_article/code_explanations/brow/vgg16_hog_gist_rbf_svm_kod_raporu.pdf", 207668, "Kas Kod Aciklamalari"),
    asset("1GDS36L9yYTk1WpQEeScvSZqLHW2CH06o", "08_article/code_explanations/brow/kas_roi_cikarma_kod_ve_cikti_raporu.pdf", 831499, "Kas Kod Aciklamalari"),

    # Mouth / Agiz notebooks and archive
    asset("1e_KfKib3SGlbhCD8XK-Fk-IR2HZXWDCP", "03_regional_models/notebooks/mouth/EfficientNet_B0_Mouth_Baseline_FINAL_STABLE.ipynb", 571195, "Agiz Kodlar"),
    asset("1sWObE8qTuZUkpHT-PriVhU-ABnWcQCp-", "03_regional_models/notebooks/mouth/Mouth_SwinV2_Tiny_Baseline_Resume_Ready (1).ipynb", 398798, "Agiz Kodlar"),
    asset("1HlyzxFK5j8fyWAyckQ8W2RUOGxGsOL-d", "03_regional_models/notebooks/mouth/VGG16_FeatureExtractor_SVM_Mouth_Deepfake_Colab_FIXED.ipynb", 724308, "Agiz Kodlar"),
    asset("1vGKR7zfFo2i-yYNo9ggZ_7fgoaFfI9A5", "03_regional_models/notebooks/mouth/DenseNet121_Mouth_Deepfake_Colab_FIXED.ipynb", 561030, "Agiz Kodlar"),
    asset("1xzqW6HMsDRfzYUyJ2KhY57I7FErPPL1m", "03_regional_models/notebooks/mouth/HOG_LBP_SVM_Mouth_Deepfake_Colab_FIXED.ipynb", 160733, "Agiz Kodlar"),
    asset("1SKaj-Buo3z77SQ3lDhS-wnShpCNfkLM3", "03_regional_models/notebooks/mouth/SwinV2_Tiny_LBP_GLCM_Gabor_Wavelet_Mouth_Deepfake_Colab (2).ipynb", 200860, "Agiz Kodlar"),
    asset("18zTLwXA75kVMW2iqrrumOikcTAbG2SO9", "03_regional_models/notebooks/mouth/VGG16_HOG_GIST_RBF_SVM_Mouth_Deepfake_Colab_FIXED (2).ipynb", 527021, "Agiz Kodlar"),
    asset("1GURMzGij142qY-BusjIvCYdfXEJlT845", "03_regional_models/notebooks/mouth/HOG_LBP_KAZE_SVM_RF_Mouth_Deepfake_Colab.ipynb", 1217976, "Agiz Kodlar"),
    asset("1CufdSTRfFMP780zk-W0fislQjG_aB_W8", "03_regional_models/notebooks/mouth/Xception_Mouth_Deepfake_Colab_FIXED.ipynb", 961174, "Agiz Kodlar"),
    asset("14hzFHsnlMn5VL3Y1cm4bAezVfACX7Hbl", "02_roi_preprocessing/drive_outputs/mouth/Untitled4 (2).ipynb", 2900736, "Agiz Kodlar"),
    asset("1vF6_1flkUTwT3_z_WHgEajaAbhjjVNRw", "03_regional_models/drive_archives/mouth/20260808_1240_mouth_vgg16_svm_seed42.zip.sha256", 107, "Agiz Sonuclar"),
    asset("1cbCatGKJYdgbrNSyZBDCo-aww2ttWlrg", "03_regional_models/drive_archives/mouth/20260808_1240_mouth_vgg16_svm_seed42.zip", 12908786, "Agiz Sonuclar"),

    # Mouth / Agiz reports
    asset("1Lqf6OholQ3mqN5IIxpiGzvFnfh0Hd2n_", "08_article/reports/mouth/EfficientNet_B0_Agiz_ROI_Deney_Sonuc_Raporu.pdf", 88717, "Agiz Raporlar"),
    asset("1nuqd-bn3T5RK9JVnE9nIw-JPQ-FGdO0V", "08_article/reports/mouth/DenseNet121_Kas_Goz_Agiz_LeakageSafe_Fuzyon_Deney_Raporu.pdf", 1392839, "Agiz Raporlar"),
    asset("1O6rllQZSTOpzIZ5EV1gi2y4Z6-K8HxGb", "08_article/reports/mouth/HOG_LBP_KAZE_RBFSVM_Kas_Goz_Agiz_Fuzyon_Deney_Raporu.pdf", 1630652, "Agiz Raporlar"),
    asset("1k5NjUPyG4PN0qyZu8Q_v6-mfbKyfmmNx", "08_article/reports/mouth/Xception_Kas_Goz_Agiz_Weighted_Fusion_Deney_Raporu.pdf", 2396930, "Agiz Raporlar"),
    asset("1ykzX9d8enUavdGfEnjk7lt1R4_yHE7JQ", "08_article/reports/mouth/Agiz_SwinV2_Tiny_Deney_Raporu.pdf", 440156, "Agiz Raporlar"),
    asset("1r8CiEzRFOHkfCRYedQaAwx_-PZuxeZ0u", "08_article/reports/mouth/VGG16_SVM_Agiz_Detayli_Deney_Raporu.pdf", 554752, "Agiz Raporlar"),
    asset("1Eq49cDt7zdbbR18D0CQ5u6TSklvxCSPz", "08_article/reports/mouth/DenseNet121_Mouth_Deney_Sonuc_Analiz_Raporu (1).pdf", 570512, "Agiz Raporlar"),
    asset("1RogOm85gVYShzMcRcuLGo9KQAvS0m8M5", "08_article/reports/mouth/HOG_LBP_SVM_Agiz_Deneyi_Sonuc_Analiz_Raporu.pdf", 708967, "Agiz Raporlar"),
    asset("1slcyBYfwnHfowkqXVLNdInWPKnMquVjV", "08_article/reports/mouth/VGG16_HOG_GIST_RBF_SVM_Agiz_Deney_Sonuc_Raporu (1).pdf", 1049209, "Agiz Raporlar"),
    asset("1YYBtKlYd0wERTd7DYC5fUwTPxK7VXz7C", "08_article/reports/mouth/HOG_LBP_KAZE_Mouth_Deney_Raporu.pdf", 842160, "Agiz Raporlar"),
    asset("1FuHFHvppThpWMZewEoUKp2hwp5SN66HW", "08_article/reports/mouth/Xception_Mouth_Deney1_Sonuc_Raporu_Guncellenmis.pdf", 562666, "Agiz Raporlar"),

    # Mouth / Agiz code explanations
    asset("1lDFv_-iqyd6whaZfyZYnZjz9B_UpAimU", "08_article/code_explanations/mouth/EfficientNet_B0_Agiz_ROI_Kod_Aciklama_Teknik_Raporu.pdf", 88147, "Agiz Kod Aciklamalari"),
    asset("12qcqoTK-4sksZ8QPLCRr9feEDZrWeG5M", "08_article/code_explanations/mouth/DenseNet121_Kas_Goz_Agiz_LeakageSafe_Fuzyon_Kod_Aciklama_Raporu.pdf", 5222, "Agiz Kod Aciklamalari"),
    asset("1SfGQaB9oLCgg12vdpOJbb2n1RM5ygVp9", "08_article/code_explanations/mouth/HOG_LBP_KAZE_RBFSVM_Kas_Goz_Agiz_Fuzyon_Kod_Aciklama_Raporu.pdf", 5155, "Agiz Kod Aciklamalari"),
    asset("1tXuGeZfReCP_1GWd-b1TOY43o-T18CaF", "08_article/code_explanations/mouth/Xception_Kas_Goz_Agiz_Weighted_Fusion_Kod_Aciklama_Raporu.pdf", 5448, "Agiz Kod Aciklamalari"),
    asset("1MjJt4Cw-I_zYL1bPA_NpMjV6WTnN_AN_", "08_article/code_explanations/mouth/Agiz_SwinV2_Tiny_Kod_Raporu.pdf", 61274, "Agiz Kod Aciklamalari"),
    asset("1D_NzF1mx610Vat_qjWynVhnn7v8qBCOl", "08_article/code_explanations/mouth/VGG16_SVM_Agiz_Kod_Aciklama_Raporu.pdf", 224138, "Agiz Kod Aciklamalari"),
    asset("1bEi0HATcPIfmMjLnOnJBrce87CCtjg-Z", "08_article/code_explanations/mouth/DenseNet121_Mouth_Kod_Aciklama_Raporu.pdf", 87739, "Agiz Kod Aciklamalari"),
    asset("1LMHV5asajxFdlZhY1OXL9Cstj0dIfGUT", "08_article/code_explanations/mouth/VGG16_HOG_GIST_RBF_SVM_Agiz_Kod_Aciklama_Raporu (1).pdf", 259382, "Agiz Kod Aciklamalari"),
    asset("1K0-4Wwrm7zQTSNq0hgtLUK7Dcy9JOkeh", "08_article/code_explanations/mouth/HOG_LBP_KAZE_Mouth_Kod_Aciklamasi.pdf", 584810, "Agiz Kod Aciklamalari"),
    asset("1OpmYUUZ53rsv71ui33WkLTPazdafhxEk", "08_article/code_explanations/mouth/Xception_Agiz_Deepfake_Deney_Raporu (1).pdf", 132365, "Agiz Kod Aciklamalari"),
    asset("1XmGLbbgtI8dTwjNylZKceaihrmz13kKB", "08_article/code_explanations/mouth/Xception_Mouth_Kod_Aciklama_Raporu.pdf", 326172, "Agiz Kod Aciklamalari"),

    # Eye / Goz notebooks
    asset("1spDk00SVIp-_M4jaUkeDod1m1o3caWWN", "03_regional_models/notebooks/fusion/03_Calibrated_Weighted_Fusion_AUTO_ARTIFACTS_MY_MODELS.ipynb", 66592, "Goz Kodlar"),
    asset("13impwDNH1JFsIrGUx1C9aNYD_jmuEg3L", "03_regional_models/notebooks/fusion/03_Calibrated_Weighted_Score_Fusion_MY_MODELS.ipynb", 56416, "Goz Kodlar"),
    asset("1yIIsNFJmhMZsOq6sL_Y1YLWDXNctzeeY", "03_regional_models/notebooks/fusion/03_Calibrated_Weighted_Fusion_3_Model_Ailesi_CLEAN.ipynb", 88471, "Goz Kodlar"),
    asset("150bCuLqIsEBhYtt_L8f9B2NUEB7muy7S", "03_regional_models/notebooks/fusion/03_Calibrated_Weighted_Fusion_3_Model_Ailesi.ipynb", 80202, "Goz Kodlar"),
    asset("1c7H4EK-qC1ax2Pxyh3dxnhhQlwvHw36P", "03_regional_models/notebooks/fusion/00_Generate_Validation_Predictions_For_Logistic_Fusion_v2.ipynb", 200075, "Goz Kodlar"),
    asset("1hxeEPeImfN68EIF_2hDXo_hpa5HgeER3", "03_regional_models/notebooks/fusion/00_Generate_Validation_Predictions_For_Logistic_Fusion.ipynb", 59985, "Goz Kodlar"),
    asset("1M9v7wBie-rNxCQALo_RzpVSr764qJkHI", "03_regional_models/notebooks/fusion/03_Learnable_Logistic_Fusion_3_Model_Ailesi_REVISED_FROM_SCRATCH.ipynb", 131188, "Goz Kodlar"),
    asset("1jDp7MhVjfL6-tZFgcgXbcK773an7cGPO", "03_regional_models/notebooks/fusion/02_Weighted_Soft_Voting_3_Model_Ailesi_REVISED_FROM_SCRATCH.ipynb", 194169, "Goz Kodlar"),
    asset("1Gfe76IGB7YROKuTBlqAS3cm69yAfn5Ad", "03_regional_models/notebooks/fusion/01_Equal_Soft_Voting_3_Model_Ailesi_REVISED.ipynb", 177439, "Goz Kodlar"),
    asset("1BAXedcSygjETcxvbmry7-OEJuZR-fTfV", "03_regional_models/notebooks/fusion/01_Equal_Soft_Voting_3_Model_Ailesi.ipynb", 43400, "Goz Kodlar"),
    asset("1M1eOkUrv16TH-Nk6L9uzbOJLDOmi-4m6", "03_regional_models/notebooks/eye/DenseNet121_Eye_Deepfake_Colab_REVISED.ipynb", 345477, "Goz Kodlar"),
    asset("1KIDOOc88JJRW0awxh759ZAfvtMRi6fLE", "03_regional_models/notebooks/eye/Goz_VGG16_SVM_SSOT_Deney.ipynb", 256792, "Goz Kodlar"),
    asset("1YKxLsgih98qCZvnPobj6mnOxJpLZPxDw", "03_regional_models/notebooks/eye/Kader_Deney1_Goz_VGG16_SVM_SSOT_v2_FIXED_v3.ipynb", 185845, "Goz Kodlar"),
    asset("1g_oZiv68KV-atF89xSNj9qdwVmD7RUBy", "03_regional_models/notebooks/eye/efficientnet_b0_eye_baseline_FINAL_STABLE.ipynb", 517696, "Goz Kodlar"),
    asset("1f1D2nYaRLq6HYIW6ZyE_qbXBBgnY0vGE", "03_regional_models/notebooks/eye/Kader_Deney1_Goz_VGG16_SVM_SSOT_v2_FIXED_v2.ipynb", 89496, "Goz Kodlar"),
    asset("1CXVHL-9XvckY5dhzkHsKRbWuoHGIMCY_", "03_regional_models/notebooks/eye/Kader_Deney1_Goz_VGG16_SVM_SSOT_v2_FIXED.ipynb", 64103, "Goz Kodlar"),
    asset("1bVGUTeEYvAAlPRnmhkUYB2ecjGYWD_mL", "03_regional_models/notebooks/eye/Kader_Deney1_Goz_VGG16_FeatureExtractor_SVM_FIXED.ipynb", 49930, "Goz Kodlar"),
    asset("17jAa5NUf5ohK4iDrtNyHIdhkXQcIk5Hw", "03_regional_models/notebooks/eye/efficientnet_b0_eye_baseline_FAST_STABLE.ipynb", 135903, "Goz Kodlar"),
    asset("1c_G43Rc-bp2a7EK7Y5KQJCOOGQ1dHQsW", "03_regional_models/notebooks/eye/efficientnet_b0_eye_baseline_REVIZED.ipynb", 70374, "Goz Kodlar"),
    asset("1GITPxxXjFDoYlVJ-IOPTi8yd-947TDJX", "03_regional_models/notebooks/eye/efficientnet_b0_eye_baseline.ipynb", 99588, "Goz Kodlar"),
    asset("15IRdBJ-P36mbBk_MLxiDeIVwRjWw3snX", "03_regional_models/notebooks/eye/HOG_LBP_KAZE_SVM_RF_Eye_Deepfake_Deney.ipynb", 163547, "Goz Kodlar"),
    asset("1_juYb8Jbfb4Yo61nr2VWbxgV9aWWCnTv", "03_regional_models/notebooks/eye/HOG_LBP_SVM_Eye_Deepfake_Deney.ipynb", 146156, "Goz Kodlar"),
    asset("1GtMbormjpFxYSxAh8YM8vcN-wkxpiWea", "03_regional_models/notebooks/eye/HOG_LBP_SVM_Eye_Deepfake_Colab_REVISED.ipynb", 108221, "Goz Kodlar"),
    asset("1KMyS1iek4aZ56YvIURR-YJ5yDQxoLFUE", "03_regional_models/notebooks/eye/Eye_SwinV2_Tiny_Baseline_Stabilized.ipynb", 370979, "Goz Kodlar"),
    asset("1GBoz6gI1IpY3tj8Suh2nHa4r64nSaSP_", "03_regional_models/notebooks/eye/Xception_Eye_Deepfake_Deney.ipynb", 887065, "Goz Kodlar"),
    asset("1ShWdZaFRiOJNlEvdUKAkPbxS_VES8kGt", "03_regional_models/notebooks/eye/Kader_Deney1_Eye_Xception_SSOT_v2.ipynb", 561778, "Goz Kodlar"),
    asset("1Vj6J9KmzSDe68qiDMrDZREES9saBTmEd", "03_regional_models/notebooks/eye/Swin-Tiny_Swin_LBP_GLCM_Gabor_Wavelet_Deney.ipynb", 147298, "Goz Kodlar"),
    asset("12n-NVuCkEIHZcDbc_MkGi8exITmxnIg0", "03_regional_models/notebooks/eye/Deney1_Eye_SwinV2_Tiny_Baseline_v2.ipynb", 109849, "Goz Kodlar"),
    asset("1o--qr_mmDwomaRRGaGeZXIXuRteD1GVb", "03_regional_models/notebooks/eye/VGG16_HOG_GIST_SVM_Deney.ipynb", 210839, "Goz Kodlar"),
    asset("1HD8qcDRzd_q3mfiXrF6TM--hsE97tZMn", "03_regional_models/notebooks/eye/Pupil_Segmentasyonu_Korneal_Yansima_FusionCNN_Deney.ipynb", 388860, "Goz Kodlar"),
    asset("1QZkASejRyPGiv1ATdxmrRn_y_9V3KVBZ", "03_regional_models/notebooks/eye/Experiment_02_Eye_SwinV2_TextureFusion.ipynb", 111463, "Goz Kodlar"),
    asset("1iqaZAvHl43op-Cteg1b0qfGhjH_Ijizw", "03_regional_models/notebooks/eye/Deney_1_Pupil_Kornea_CNN_v2_Tam_Gorsellestirmeli.ipynb", 161401, "Goz Kodlar"),
    asset("1Yv-0XLLd7JJarDXx_NlKoXjUY3TMHIzv", "02_roi_preprocessing/drive_outputs/eye/Goz_ROI_Cikarma.ipynb", 55418, "Goz Kodlar"),
    asset("1JBnHiJj6mppI2h4-0LKPMBLxnjcfS_9Q", "01_data_splits/drive_exports/deney1_frame_secimi.ipynb", 140303, "Goz Kodlar"),
    asset("1J7FyYiBySAk4DL8kKJyFztJQhAtOM2C6", "01_data_splits/drive_exports/deney1_frame_secimi_tasksapi_revize.ipynb", 88062, "Goz Kodlar"),
    asset("1EgdPy10e4OaVKyx2jwrdYtO9JXq41fRi", "01_data_splits/drive_exports/deney1_frame_secimi_duzeltilmis.ipynb", 23408, "Goz Kodlar"),

    # Eye / Goz ROI metadata and selected result-run summaries
    asset("1JlJf699Ja4DceQhhRd8hJqmu_8tEGDhD", "02_roi_preprocessing/drive_outputs/eye/eye_roi_output/metadata.csv", 2044382, "Goz ROI output"),
    asset("14F8cxOOQEbRiAGRJ4xgCyEGQrq7CoXH7", "02_roi_preprocessing/drive_outputs/eye/eye_roi_output/run_config.json", 696, "Goz ROI output"),
    asset("1L_sGILh-WuaNVspKENO_WqtO_itDHgkA", "03_regional_models/drive_archives/eye/20260808_1214_eye_densenet121_seed42.zip.sha256", 107, "Goz Sonuclar"),
    asset("1W9JInC-atMC75P5Mq5Jfv7rl3SD1noyF", "03_regional_models/drive_archives/eye/20260808_1214_eye_densenet121_seed42.zip", 215263815, "Goz Sonuclar"),
    asset("13UDMn5jk9VzfPtwjgkngnEAmIYdg93xe", "06_metrics_tables/drive_outputs/eye_densenet121/artifact_manifest.csv", 4228, "Goz Sonuclar"),
    asset("19RBdwezZEv9cpMdgD3B2FE4Ws6BHTRsb", "06_metrics_tables/drive_outputs/eye_densenet121/final_audit.json", 1817, "Goz Sonuclar"),
    asset("1nwBysOm7An3MpbZh4pWDH_oAAWR2LfPl", "06_metrics_tables/drive_outputs/eye_densenet121/RUN_SUMMARY.txt", 1687, "Goz Sonuclar"),
    asset("1Py6wH2uQt7Fs48vdhcpcoiiPRXMVo5gi", "06_metrics_tables/drive_outputs/eye_densenet121/requirements_snapshot.txt", 146, "Goz Sonuclar"),
    asset("13c0NolZsQhYUG30ObWi0thdznyG4P97n", "06_metrics_tables/drive_outputs/eye_densenet121/config_resolved.yaml", 1979, "Goz Sonuclar"),
    asset("10oaNEWha8fhiEwU2qs6XOwE0OxE5vxs5", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/figure_quality_audit.csv", 938, "Goz Sonuclar"),
    asset("1MwhE7ijwpQI44gyMOnUR61qcp0B71IBa", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/final_evaluation_summary.json", 3755, "Goz Sonuclar"),
    asset("1JhLa07Ykl_fpyNbD6JsV_HJlNHQtLqft", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/validation_threshold.json", 374, "Goz Sonuclar"),
    asset("1dH6mxY9OZtHZsI9nyYFTqWDQX95hUfxU", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/classification_report.csv", 409, "Goz Sonuclar"),
    asset("1sIryI9XiwmG2bAY_g1vV99eXhXPi68na", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/default_threshold_metrics.csv", 387, "Goz Sonuclar"),
    asset("12GS4ON0QnxE-PPfB_9q_yonxfuONGOL5", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/final_source_level_metrics.csv", 274, "Goz Sonuclar"),
    asset("1qPfxynkhIRJn_gdOn5Mg07A3vYlc3pT7", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/final_image_level_metrics.csv", 401, "Goz Sonuclar"),
    asset("1_H4G4PHNEt1QYhPQPk_UPz104WU8oWRg", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/finetune_training_summary.json", 879, "Goz Sonuclar"),
    asset("1_J24raPK51dofFdEEZAEB86hll8ZWlLB", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/combined_training_history.csv", 8436, "Goz Sonuclar"),
    asset("1iAphi_q_cW0nhT1e4C3QsUw5YJ4Fp7Wb", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/finetune_training_history.csv", 5345, "Goz Sonuclar"),
    asset("1Su3lR9fTOZMw14Q2mfDEAt_tP4Xl8jLW", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/frozen_training_summary.json", 704, "Goz Sonuclar"),
    asset("1PN1abjzh-EDFzN-q6PvlNqCDn8bg1ZwG", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/frozen_training_history.csv", 3225, "Goz Sonuclar"),
    asset("11kPqJYrcJ1TutAaOToKOJ6QvrAtFmdAF", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/smoke_test_report.json", 1251, "Goz Sonuclar"),
    asset("1S7JniypeqImRLTglbFpln-WcCTd6l9Bd", "06_metrics_tables/drive_outputs/eye_densenet121/metrics/model_summary.txt", 2432, "Goz Sonuclar"),

    # Eye / Goz reports
    asset("1kq-1cA9mzeD2Hcs-_mmOPYJSf0yurix7", "08_article/reports/eye/DenseNet121_Goz_Deney_Sonuc_Raporu_20260808.pdf", 603882, "Goz Raporlar"),
    asset("1uEZfS9mM4BrRA9coAJmu-Xy4VYUTfom_", "08_article/reports/eye/VGG16_SVM_Goz_Deney_Raporu.pdf", 341185, "Goz Raporlar"),
    asset("17_PuLcgayk8xSE0n-YfbDgwWAsLtwiq4", "08_article/reports/eye/EfficientNet_B0_Goz_ROI_Deney_Raporu.pdf", 400909, "Goz Raporlar"),
    asset("13BRouPXF_l-mcD9fOZhn6__QvHJBusUM", "08_article/reports/eye/HOG_LBP_KAZE_SVM_RF_Deney_Raporu.pdf", 837846, "Goz Raporlar"),
    asset("1MNpJbv4F7g7zI614-TmBFFxyt7js40ZO", "08_article/reports/eye/HOG_LBP_SVM_Goz_Deney_Raporu.pdf", 739344, "Goz Raporlar"),
    asset("16Eu1I2o-4-cM_4MbslFFT8KJlSIxNyAM", "08_article/reports/eye/Goz_SwinV2_Tiny_Deney_Raporu.pdf", 966020, "Goz Raporlar"),
    asset("1lT2m-xW1zcWq7XFj4x8hWW8pEKkWMT4o", "08_article/reports/eye/VGG16_HOG_GIST_RBF_SVM_Sonuc_Raporu.pdf", 933716, "Goz Raporlar"),
    asset("1bbtjt1z8drGg342MRvzJhNbiKkbdgQhS", "08_article/reports/eye/Xception_Eye_Deepfake_Deney_Raporu.pdf", 674675, "Goz Raporlar"),
    asset("1SijAgMryN21yZvvKlg6AHXg4gWW2MpYw", "08_article/reports/eye/Swin-Tiny_Swin_V2_LBP_GLCM_Gabor_Wavelet_Deney_Raporu.pdf", 779120, "Goz Raporlar"),
    asset("1fkPshy4AOznOim6hKEueE0N20hCv8tbl", "08_article/reports/eye/Pupil_Segmentasyonu_Korneal_Yansima_FusionCNN_Deney_Raporu.pdf", 1540451, "Goz Raporlar"),
    asset("1ZVTYmhx6kr0qTlwP6iJQhSBMWuhNqsRo", "08_article/reports/eye/Goz_Uzerinden_Deepfake_Tespiti_Model_Onceliklendirme.pdf", 52614, "Goz Raporlar"),

    # Eye / Goz code explanations
    asset("1rHs-EHMrLPZcQZTZJ8D8TAvUn3_DVZd3", "08_article/code_explanations/eye/DenseNet121_Goz_ROI_Kod_Aciklama_Raporu.pdf", 238338, "Goz Kod Aciklamalari"),
    asset("1lww-0fWoW55YNDEAlgbm0XHC5JXHojPB", "08_article/code_explanations/eye/VGG16_SVM_Goz_Kod_Aciklamasi.pdf", 249335, "Goz Kod Aciklamalari"),
    asset("1GcjtuOEbYw7zn7jLG-r4-OlFmMyZ1TyL", "08_article/code_explanations/eye/EfficientNet_B0_Goz_ROI_Kod_Aciklama_Raporu.pdf", 244291, "Goz Kod Aciklamalari"),
    asset("1IPXYmb3ITa2HvcP2pT_9hnnM0KwdIIf2", "08_article/code_explanations/eye/HOG_LBP_KAZE_SVM_RF_Goz_Kod_Aciklamasi.pdf", 258304, "Goz Kod Aciklamalari"),
    asset("1aBAAPdaLIvNrUg0fM92_x6bqQIMi-mtt", "08_article/code_explanations/eye/HOG_LBP_SVM_Goz_Deepfake_Kod_Aciklamasi.pdf", 215026, "Goz Kod Aciklamalari"),
    asset("1LGIEY1WS8f6WnczZ6dHPWH9eYXM1wkYC", "08_article/code_explanations/eye/Goz_SwinV2_Tiny_Kod_Raporu.pdf", 477155, "Goz Kod Aciklamalari"),
    asset("1WQFpNOkqt7n2FfnnEJKLuey2Ct1uaVJG", "08_article/code_explanations/eye/Xception_Eye_Deepfake_Kod_Aciklamalari.pdf", 512237, "Goz Kod Aciklamalari"),
    asset("17IuhJUUF5XFNSmYwcVr_52uXjoha47Au", "08_article/code_explanations/eye/VGG16_HOG_GIST_SVM_Kod_Aciklamasi.pdf", 398116, "Goz Kod Aciklamalari"),
    asset("18ds6DVSNe3VeWb1GffMT7ucbSxTDaUes", "08_article/code_explanations/eye/Pupil_Segmentasyonu_Korneal_Yansima_FusionCNN_Kod_Aciklamasi.pdf", 388812, "Goz Kod Aciklamalari"),
    asset("10e6IdfUPtGAUE7p3CSFHPbXd7kTbFHqi", "08_article/code_explanations/eye/Swin-Tiny_Swin_V2_LBP_GLCM_Gabor_Wavelet_Kod_Aciklamasi.pdf", 457042, "Goz Kod Aciklamalari"),
    asset("1omTiE1eoacYtDnJ6XZq-gArQYxGDtqi2", "08_article/code_explanations/eye/Goz_ROI_Cikarma_Kodu_Detayli_Teknik_Analiz.docx", 49578, "Goz Kod Aciklamalari"),
    asset("1OLvV4mFDnr1u5hfNrtGvB1UUccQm1wCr", "08_article/code_explanations/eye/Deney1_Frame_Secimi_Tam_Feedback_ve_Fonksiyon_Analizi.docx", 49685, "Goz Kod Aciklamalari"),
]


DRIVE_FOLDERS: list[tuple[str, str, str]] = [
    ("Deney 1 root", "https://drive.google.com/drive/folders/1aUHJOgb9YVdqJuIQZrF0q5-nlo506Fue", "Top-level experiment folder"),
    ("Deney 1 Frame primary", "https://drive.google.com/drive/folders/1Jk0kO0MA1NCDTfdhUDEmfn9Toi2R59KQ", "Raw selected Real/Fake frame folders plus metadata"),
    ("Deney 1 Frame secondary", "https://drive.google.com/drive/folders/1IO-T8Bjg7ztuOZOft5uG4U9bXXGHqWin", "Duplicate/alternate selected Real/Fake frame folders plus metadata"),
    ("Brow / Kas Deney 1", "https://drive.google.com/drive/folders/1u1EYIcqjPoQP4oE8uXu79M5qzwSkeA8n", "Brow notebooks, reports, outputs"),
    ("Mouth / Agiz Deney 1", "https://drive.google.com/drive/folders/1siJN9pd15V2C3hupFtIenm9tvdiC3mAq", "Mouth notebooks, reports, outputs"),
    ("Eye / Goz Deney 1", "https://drive.google.com/drive/folders/1I1-eEZ2bYiIchMsBgRsuBjEGiVI4j4Pd", "Eye notebooks, reports, outputs"),
    ("Weighted fusion corrected ALL4", "https://drive.google.com/drive/folders/1hRvjj4dyvGuuC_b-TTD5rM9ncJiC4Khv", "Corrected weighted soft-voting outputs"),
    ("Eye results", "https://drive.google.com/drive/folders/1aN_3OsBw-b9d6EhNySEYfDr-ARRavOWc", "Run folders; large ZIP/checkpoint artifacts stay in Drive"),
    ("Eye ROI output", "https://drive.google.com/drive/folders/1Tw3NDqzQ-FeVBXI-tB8mdL8jDZnGeLjQ", "ROI metadata plus raw eye ROI image folders"),
    ("Mouth results", "https://drive.google.com/drive/folders/1W2XTGqdDOhH_bZbTABGkeVlUidWqRYq3", "Run folders and one small VGG16 SVM ZIP archive"),
]


def download(asset_entry: dict[str, object]) -> tuple[str, str]:
    size = int(asset_entry["size"])
    target = ROOT / str(asset_entry["target"])
    file_id = str(asset_entry["id"])
    if size > MAX_GITHUB_FILE_BYTES:
        parts_dir = target.with_name(target.name.replace(".zip", "_zip_parts"))
        if parts_dir.exists():
            return "stored_as_split_parts", str(parts_dir.relative_to(ROOT))
        return "skipped_large", str(target.relative_to(ROOT))
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size == size:
        return "exists", str(target.relative_to(ROOT))

    tmp = target.with_suffix(target.suffix + ".download")
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    cmd = [
        "curl",
        "-L",
        "--fail",
        "--silent",
        "--show-error",
        "--connect-timeout",
        "20",
        "--max-time",
        "120",
        url,
        "-o",
        str(tmp),
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)
    tmp.replace(target)
    return "downloaded", str(target.relative_to(ROOT))


def write_manifest(rows: list[dict[str, object]], statuses: list[tuple[dict[str, object], str]]) -> None:
    manifest = ROOT / "01_data_splits/drive_exports/DENEY1_DRIVE_ASSET_MANIFEST.csv"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["status", "source", "drive_id", "size_bytes", "repo_target", "drive_url"])
        for item, status in statuses:
            file_id = str(item["id"])
            writer.writerow([
                status,
                item["source"],
                file_id,
                item["size"],
                item["target"],
                f"https://drive.google.com/file/d/{file_id}/view",
            ])

    md = ROOT / "01_data_splits/drive_exports/SKIPPED_LARGE_FILES.md"
    large = [item for item in rows if int(item["size"]) > MAX_GITHUB_FILE_BYTES]
    with md.open("w", encoding="utf-8") as handle:
        handle.write("# Large Deney 1 Files\n\n")
        handle.write("These Drive files exceed the GitHub-safe single-file threshold. If split parts exist in the repo, they are the committed representation of the original file.\n\n")
        handle.write("| Source | Original file | Repo parts | Size bytes | Drive link |\n")
        handle.write("| --- | --- | --- | ---: | --- |\n")
        for item in large:
            file_id = str(item["id"])
            target = Path(str(item["target"]))
            parts = target.with_name(target.name.replace(".zip", "_zip_parts"))
            handle.write(
                f"| {item['source']} | `{target.name}` | `{parts}` | {item['size']} | "
                f"https://drive.google.com/file/d/{file_id}/view |\n"
            )

    folders = ROOT / "01_data_splits/drive_exports/DENEY1_DRIVE_FOLDER_MANIFEST.md"
    with folders.open("w", encoding="utf-8") as handle:
        handle.write("# Deney 1 Drive Folder Manifest\n\n")
        handle.write("Raw frame folders, ROI image folders, model checkpoints, and large run archives remain in Drive. The repository stores code, reports, metadata, metrics, and small archives directly.\n\n")
        handle.write("| Folder | Drive URL | Notes |\n")
        handle.write("| --- | --- | --- |\n")
        for name, url, note in DRIVE_FOLDERS:
            handle.write(f"| {name} | {url} | {note} |\n")


def main() -> int:
    statuses: list[tuple[dict[str, object], str]] = []
    counts: dict[str, int] = {}
    for item in ASSETS:
        status, target = download(item)
        statuses.append((item, status))
        counts[status] = counts.get(status, 0) + 1
        print(f"{status:14} {target}", flush=True)
    write_manifest(ASSETS, statuses)
    print("\nSummary:")
    for status, count in sorted(counts.items()):
        print(f"  {status}: {count}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"download failed: {exc}", file=sys.stderr)
        raise
