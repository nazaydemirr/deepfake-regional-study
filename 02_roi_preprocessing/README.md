# 02 ROI Preprocessing

Bu klasor, Deney 1'de kullanilan bolgesel on isleme adimlarini standartlastirir.

Hedef ROI bolgeleri:

- `eye`: goz bolgesi
- `brow`: kas / kas-cevresi bolgesi
- `mouth`: agiz bolgesi

Literatur tablosuna gore bolgesel deepfake tespitinde agiz, goz, burun ve tum yuz gibi ROI'lerin ayri modellenmesi onemlidir. Bu projede Drive'daki mevcut deney yapisina uygun olarak goz, kas ve agiz bolgeleri kullanilir.

## Cikti Semasi

Her ROI icin onerilen dosya yapisi:

```text
data/processed/<roi>/<split>/<label>/<sample_id>.png
```

Ornek:

```text
data/processed/eye/train/real/video_001_frame_00042.png
data/processed/mouth/test/fake/video_145_frame_00120.png
```

Buyuk gorsel dosyalar GitHub'a commitlenmez; yalnizca betikler ve metadata tutulur.
