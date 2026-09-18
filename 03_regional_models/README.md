# 03 Regional Models

Bu klasor, goz, kas ve agiz icin bagimsiz model egitimlerini toplar.

Drive ve literatur tablosuna gore kullanilan / raporlanan model aileleri:

- Xception
- EfficientNet-B0
- SwinV2-Tiny
- SwinV2 + texture descriptors
- DenseNet121 / CNN tabanli transfer learning icin literatur dayanaklari
- HOG + LBP + KAZE gibi hafif feature-fusion yontemleri

## Standart Deney Kimligi

Her egitim kosusu icin onerilen alanlar:

- `run_id`
- `roi`
- `model_family`
- `train_split`
- `validation_split`
- `test_split`
- `seed`
- `metrics_path`
- `predictions_path`

Model agirliklari GitHub'a eklenmez; Drive, release asset veya dis depolama ile saklanir.
