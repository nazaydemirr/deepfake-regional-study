# 04 Predictions

Bu klasor, bolgesel modellerden gelen tahmin dosyalarinin ortak semasini tanimlar.

## Beklenen Tahmin CSV Semasi

```csv
sample_id,video_id,frame_id,split,label,roi,model_family,y_true,y_score,y_pred
```

Alanlar:

- `sample_id`: frame veya video duzeyinde tekil kimlik
- `video_id`: kaynak video kimligi
- `frame_id`: frame kimligi
- `split`: train, val veya test
- `label`: real veya fake
- `roi`: eye, brow veya mouth
- `model_family`: xception, efficientnet_b0, swinv2_tiny, swinv2_texture vb.
- `y_true`: 0/1 gercek etiket
- `y_score`: fake olasiligi veya karar skoru
- `y_pred`: 0/1 tahmin

Fuzyon betikleri bu semayi bekler.
