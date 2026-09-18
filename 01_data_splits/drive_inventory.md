# Drive Inventory

Bu dosya, Drive'dan okunan Deney 1 klasor yapisinin GitHub tarafindaki karsiligini ozetler.

| Drive bolumu | Sahip / kapsam | Repo karsiligi |
| --- | --- | --- |
| `Deney 1 Frame` | Ortak frame secimi, Real/Fake splitleri, metadata | `01_data_splits/` |
| `Nazlican / Deney 1 / Goz` | Goz ROI deneyleri | `02_roi_preprocessing/`, `03_regional_models/`, `04_predictions/` |
| `Dilara / Deney 1 / Agiz` | Agiz ROI deneyleri | `02_roi_preprocessing/`, `03_regional_models/`, `04_predictions/` |
| `Kader / Deney 1 / Kas` | Kas ROI deneyleri | `02_roi_preprocessing/`, `03_regional_models/`, `04_predictions/` |
| `fuzyon sonuclari` | Bolgesel karar fuzyonu | `05_fusion/`, `06_metrics_tables/` |
| `agirlikli fuzyon icin tekrar` | Corrected weighted soft voting, 4 model ailesi | `05_fusion/results/`, `06_metrics_tables/` |
| `AISC Makale Inceleme ve Literatur Tarama Tablosu` | Literatur dayanaklari | `08_article/literature_notes.md`, `06_metrics_tables/literature_sources.csv` |

## Indirilen Deney 1 Varliklari

Drive'daki Deney 1 dosyalarindan notebook, PDF, CSV, JSON, TXT, DOCX ve GitHub limitleri icinde kalan ZIP dosyalari repo'ya indirildi.

- Kod/notebook dosyalari: `03_regional_models/notebooks/brow`, `03_regional_models/notebooks/mouth`, `03_regional_models/notebooks/eye`, `03_regional_models/notebooks/fusion`
- ROI ve frame secimi dosyalari: `01_data_splits/drive_exports`, `02_roi_preprocessing/drive_outputs`
- Sonuc/metrik dosyalari: `05_fusion/results`, `06_metrics_tables/drive_outputs`
- Raporlar ve kod aciklamalari: `08_article/reports`, `08_article/code_explanations`
- Indirme listesi ve kaynak Drive ID'leri: `01_data_splits/drive_exports/DENEY1_DRIVE_ASSET_MANIFEST.csv`
- GitHub'a fiziksel eklenmeyen buyuk Drive paketleri: `01_data_splits/drive_exports/SKIPPED_LARGE_FILES.md`
- Ham frame/ROI klasor kaynaklari: `01_data_splits/drive_exports/DENEY1_DRIVE_FOLDER_MANIFEST.md`
