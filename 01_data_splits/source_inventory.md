# Deney 1 Source Inventory

Bu dosya, Deney 1 kaynak klasor yapisinin GitHub tarafindaki karsiligini ozetler. Rapor metninde dis linki verilmez; karsiliklar repo icindeki dosya ve klasorlerdir.

| Kaynak bolumu | Sahip / kapsam | Repo karsiligi |
| --- | --- | --- |
| `Deney 1 Frame` | Ortak frame secimi, Real/Fake splitleri, metadata | `01_data_splits/` |
| `Nazlican / Deney 1 / Goz` | Goz ROI deneyleri | `02_roi_preprocessing/`, `03_regional_models/`, `04_predictions/` |
| `Dilara / Deney 1 / Agiz` | Agiz ROI deneyleri | `02_roi_preprocessing/`, `03_regional_models/`, `04_predictions/` |
| `Kader / Deney 1 / Kas` | Kas ROI deneyleri | `02_roi_preprocessing/`, `03_regional_models/`, `04_predictions/` |
| `fuzyon sonuclari` | Bolgesel karar fuzyonu | `05_fusion/`, `06_metrics_tables/` |
| `agirlikli fuzyon icin tekrar` | Corrected weighted soft voting, 4 model ailesi | `05_fusion/results/`, `06_metrics_tables/` |
| `AISC Makale Inceleme ve Literatur Tarama Tablosu` | Literatur dayanaklari | `08_article/literature_notes.md`, `06_metrics_tables/literature_sources.csv` |

## Yerel Deney 1 Varliklari

Deney 1 kaynak dosyalarindan notebook, PDF, CSV, JSON, TXT, DOCX ve GitHub limitleri icinde kalan ZIP dosyalari repo'ya alindi.

- Kod/notebook dosyalari: `03_regional_models/notebooks/brow`, `03_regional_models/notebooks/mouth`, `03_regional_models/notebooks/eye`, `03_regional_models/notebooks/fusion`
- ROI ve frame secimi dosyalari: `01_data_splits/source_exports`, `02_roi_preprocessing/source_outputs`
- Sonuc/metrik dosyalari: `05_fusion/results`, `06_metrics_tables/source_outputs`
- Raporlar ve kod aciklamalari: `08_article/reports`, `08_article/code_explanations`
- Yerel varlik listesi ve repo hedefleri: `01_data_splits/source_exports/DENEY1_SOURCE_ASSET_MANIFEST.csv`
- GitHub tekil dosya limitini asan ama parca olarak temsil edilen paketler: `01_data_splits/source_exports/SKIPPED_LARGE_FILES.md`
- Ham frame/ROI kaynak envanteri: `01_data_splits/source_exports/DENEY1_SOURCE_FOLDER_MANIFEST.md`
