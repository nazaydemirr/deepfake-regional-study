# 01 Data Splits

Bu klasor, Deney 1 icin frame secimi, sinif dengesi ve train/validation/test ayrimini belgeler.

`Deney 1 Frame` kaynak klasorlerinden alinan yerel ozet:

- Genel toplam: 3000 frame
- Real: train 1200, validation 150, test 150
- Fake: train 1200, validation 150, test 150
- Reddedilen / yuzsuz veya okunamayan frame sayisi: 206
- Tamamlanan splitler: `Real/train`, `Real/val`, `Real/test`, `Fake/train`, `Fake/val`, `Fake/test`

Repo, frame secim mantigini, metadata semasini ve makalede kullanilan sayisal ozetleri yerel olarak tutar. Rapor metninde dis linki kullanilmaz.

## Beklenen Metadata

`secim_metadata.csv` icin beklenen kolonlar:

- `source_video`
- `frame_path`
- `label`
- `split`
- `face_detected`
- `roi_status`
- `notes`

## Yerel Kaynak Karsiliklari

- Frame secim metadata dosyalari: `01_data_splits/source_exports/deney_1_frame_primary/`
- Ikincil/kontrol metadata dosyalari: `01_data_splits/source_exports/deney_1_frame_secondary/`
- Frame kaynak envanterleri: `08_article/reports/source_large_assets/`
