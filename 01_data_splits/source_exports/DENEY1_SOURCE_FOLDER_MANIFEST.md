# Deney 1 Source Folder Manifest

Bu manifest, Deney 1 kaynak bolumlerinin repo icindeki karsiliklarini ozetler. Rapor metninde dis linki verilmez; makale ve README yerel dosya yollarini kullanir.

| Kaynak bolumu | Repo karsiligi | Notes |
| --- | --- | --- |
| Deney 1 root | Bu manifest ve alt klasorler | Top-level experiment snapshot |
| Deney 1 Frame primary | `01_data_splits/source_exports/deney_1_frame_primary/` | Selected Real/Fake frame metadata and summaries |
| Deney 1 Frame secondary | `01_data_splits/source_exports/deney_1_frame_secondary/` | Duplicate/alternate selected frame metadata |
| Brow / Kas Deney 1 | `03_regional_models/notebooks/brow/`, `08_article/reports/brow/`, `08_article/code_explanations/brow/` | Brow notebooks, reports, outputs |
| Mouth / Agiz Deney 1 | `03_regional_models/notebooks/mouth/`, `08_article/reports/mouth/`, `08_article/code_explanations/mouth/` | Mouth notebooks, reports, outputs |
| Eye / Goz Deney 1 | `03_regional_models/notebooks/eye/`, `08_article/reports/eye/`, `08_article/code_explanations/eye/` | Eye notebooks, reports, outputs |
| Weighted fusion corrected ALL4 | `05_fusion/results/`, `05_fusion/source_outputs/corrected_weighted_soft_voting_all4_seed42/`, `06_metrics_tables/` | Corrected weighted soft-voting outputs |
| Eye results | `03_regional_models/source_outputs/eye/`, `06_metrics_tables/source_outputs/eye/`, `03_regional_models/source_archives/eye/` | Run folders, metrics, checkpoints and split archive parts |
| Eye ROI output | `02_roi_preprocessing/source_outputs/eye/`, `08_article/reports/source_large_assets/eye_roi_output_inventory.*` | ROI metadata and source inventory |
| Mouth results | `03_regional_models/source_outputs/mouth/`, `06_metrics_tables/source_outputs/mouth/`, `03_regional_models/source_archives/mouth/` | Run folders and local VGG16 SVM ZIP archive |
