# 01 Data Splits

Bu klasor, Deney 1 icin frame secimi, sinif dengesi ve train/validation/test ayrimini belgeler.

Drive'daki `Deney 1 Frame` klasorlerinden okunan ortak ozet:

- Genel toplam: 3000 frame
- Real: train 1200, validation 150, test 150
- Fake: train 1200, validation 150, test 150
- Reddedilen / yuzsuz veya okunamayan frame sayisi: 206
- Tamamlanan splitler: `Real/train`, `Real/val`, `Real/test`, `Fake/train`, `Fake/val`, `Fake/test`

Buyuk gorsel veri GitHub'a eklenmez. Repo, frame secim mantigini ve metadata semasini tutar; raw veri Drive'da kalir.

## Beklenen Metadata

`secim_metadata.csv` icin beklenen kolonlar:

- `source_video`
- `frame_path`
- `label`
- `split`
- `face_detected`
- `roi_status`
- `notes`

## Drive Klasorleri

- Ana Deney 1: `https://drive.google.com/drive/folders/1aUHJOgb9YVdqJuIQZrF0q5-nlo506Fue`
- Frame secim klasorleri: Drive'da birden fazla `Deney 1 Frame` kopyasi bulunur.
