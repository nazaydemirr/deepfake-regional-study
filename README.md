# Deepfake Regional Study

Bu repo, `AISC DeepFake Calismalari > Deney 1` calismasindan cikarilan yerel proje snapshot'ini GitHub tarafinda izlenebilir, tekrar okunabilir ve makale yazimina baglanabilir bir yapiya tasir. Calismanin ana fikri, deepfake tespitinde tek bir yuz bolgesine veya tek bir modele yaslanmak yerine goz, kas/kas-cevresi ve agiz ROI'lerinden gelen tahminleri once ayri ayri degerlendirmek, sonra karar seviyesinde birlestirmenin gercekten ek kazanc getirip getirmedigini olcmektir.

Makale sonucu ozellikle temkinli yorumlanmalidir: mevcut protokolde agiz ROI en guclu tek bolge olarak gorunur; validation agirlikli fusion, equal fusion'a gore daha yuksek ROC-AUC verir, fakat ortak test kohortunda agiz-only performansini asmaz. Bu nedenle repo, "fusion her zaman daha iyidir" iddiasindan cok, bolgesel performansi ve fusion kazancinin sinirlarini belgeleyen bir deney setidir.

## Deney 1 Snapshot Kapsami

Bu repo rapor ve makale tarafinda dis linklerine dayanmadan okunacak sekilde duzenlenir. Deney 1 kaynak yapisindan alinip yerel repo karsiligi olusturulan ana bolumler:

- `Deney 1 Frame` kopyalari: frame secimi, Real/Fake klasorleri ve secim metadata dosyalari.
- `Nazlican`: goz ROI, goz kodlari, raporlar, sonuc klasorleri ve kod aciklamalari.
- `Dilara`: agiz ROI, agiz kodlari, raporlar, sonuc klasorleri ve kod aciklamalari.
- `Kader`: kas ROI, kas kodlari, raporlar, sonuc klasorleri, kod aciklamalari ve bolgesel fusion sonuclari.
- `agirlikli fuzyon icin tekrar`: corrected weighted soft voting tekrar calismasi.
- Ek Deney 1 fusion ve goz dallari: `Fusion_Experiments`, ara EfficientNet-B0 goz kosulari, pupil/reflection deney ciktilari ve aktif run id kaydi.

Yerel repo karsiliklari:

- Notebook ve egitim kodlari: `03_regional_models/notebooks/`
- Frame secimi ve metadata: `01_data_splits/source_exports/`
- ROI/on isleme ciktilari: `02_roi_preprocessing/source_outputs/`
- Bolgesel tahmin CSV'leri: `04_predictions/`
- Fusion kodlari ve sonuclari: `05_fusion/`
- Metrik tablolar ve literatur kaynaklari: `06_metrics_tables/`
- Sekiller ve grafikler: `07_figures/`
- Deney raporlari, kod aciklamalari ve makale paketi: `08_article/`

Kaynak-to-repo dosya listesi `01_data_splits/source_exports/DENEY1_SOURCE_ASSET_MANIFEST.csv` icindedir. Bu manifestte 472 yerel kaynak varligin repo hedefi tutulur. Rapor metninde link verilmez; makale ve README yerel dosya yollarini referans alir.

- `01_data_splits/source_exports/DENEY1_SOURCE_FOLDER_MANIFEST.md`
- `01_data_splits/source_exports/SKIPPED_LARGE_FILES.md`
- `08_article/reports/source_large_assets/`

Bu ayrim bilincli yapildi: repo, kodu, notebooklari, raporlari, metrikleri, makale dosyalarini, sekilleri ve izlenebilir envanteri tutar. Makale raporu, dis depolama linki yerine repo icindeki dosyalari ve Deney 1 snapshot ozetlerini kullanir.

## Klasor Yapisi

```text
deepfake-regional-study/
├── 01_data_splits/        # Frame secimi, split metadata ve kaynak manifestleri
├── 02_roi_preprocessing/  # Goz/kas/agiz ROI on isleme ciktilari
├── 03_regional_models/    # Bolgesel model notebooklari, model kartlari, run ciktilari
├── 04_predictions/        # Test tahminleri ve ortak tahmin semasi
├── 05_fusion/             # Majority voting ve weighted soft voting kodlari/sonuclari
├── 06_metrics_tables/     # Makale hazir metrik tablolar ve literatur kaynaklari
├── 07_figures/            # ROC, confusion matrix ve makale sekilleri
├── 08_article/            # Makale taslagi, raporlar, kod aciklamalari, submission paketi
├── scripts/               # Repo kontrol yardimcilari
├── requirements.txt
└── README.md
```

## Veri Nasil Isledi

### 1. Frame havuzu olusturma

Deney havuzu FaceForensics project dagitimindan derlenen 3,000 kaynak frameden olusur: 1,500 REAL ve 1,500 FAKE. FAKE sinifi birden fazla manipulasyon kaynagini kapsar; bu nedenle veri tanimi yalnizca standart tek bir FaceForensics++ alt kumesiyle es anlamli kabul edilmemelidir.

Frame seciminde sinif dengesi korunarak 80/10/10 bolunme kullanildi:

| Split | REAL | FAKE | Toplam |
| --- | ---: | ---: | ---: |
| Train | 1200 | 1200 | 2400 |
| Validation | 150 | 150 | 300 |
| Test | 150 | 150 | 300 |
| Toplam | 1500 | 1500 | 3000 |

Frame secim metadata dosyalari `01_data_splits/source_exports/deney_1_frame_primary/`, `01_data_splits/source_exports/deney_1_frame_secondary/` ve `01_data_splits/source_exports/deney_1_frame_tertiary/` altindadir. `yuzsuz_veya_okunamayan_frameler.csv` dosyalari yuz bulunamayan veya okunamayan frame kayitlarini tutar; mevcut ozet 206 reddedilen/okunamayan frame kaydini belgeler.

### 2. Split ve leakage kontrolleri

Split etiketleri frame secim asamasinda korunur ve ROI kayitlarina tasinir. Metadata kontrolleri, ayni sinif icindeki orijinal kaynak klasorlerin birden fazla split'e dagilmadigini raporlar. Bu kontrol faydalidir, ancak makalede de belirtildigi gibi tum manipulations icin ortak root-video veya identity-level ayrimi tam olarak kanitlamaz. Bu nedenle README ve makale, leakage riskini sinirlilik olarak acikca yazar.

### 3. ROI cikarma

ROI cikarma asamasinda yuz ve landmark tespiti icin MediaPipe Face Landmarker kullanildi. Uc bolge ayri ayri islenir:

- Agiz ROI: 40 dudak landmark'i ve cevre margin'i.
- Goz ROI: iki gozu birlikte kapsayan combined eye ROI.
- Kas ROI: 20 kas landmark'i; minimum genislik 48 piksel, minimum yukseklik 14 piksel ve goz-landmark dahil olma orani en fazla 0.25.

Kas ROI kosullari daha siki oldugu icin kullanilabilir kayit sayisi goz ve agizdan dusuktur. Makalede raporlanan ROI kayit sayilari:

| ROI | Train | Validation | Test | Toplam |
| --- | ---: | ---: | ---: | ---: |
| Kas | 1562 | 204 | 196 | 1962 |
| Goz | 2388 | 296 | 302 | 2986 |
| Agiz | 2389 | 296 | 302 | 2987 |

Eye ve mouth test pipeline'lari 300 kaynak frameden 310 face record uretmis, 8 kayitta yuz bulunamadigi icin 302 basarili ROI kalmistir. Kas pipeline'i 196 basarili test kaydi uretmistir; 104 kayit geometri veya yuz tespit kosullari nedeniyle reddedilmistir. Bu nedenle fusion icin ortak kohort, uc ROI skoru da bulunan 196 kayittir.

### 4. Model aileleri

Bolgesel deneylerde dort ana model ailesi kullanildi:

- `Xception`: depthwise separable convolution tabanli CNN transfer learning.
- `EfficientNet-B0`: compound scaling kullanan CNN transfer learning.
- `SwinV2-Tiny`: shifted-window self-attention kullanan transformer tabanli model.
- `SwinV2-Tiny + Texture`: SwinV2 temsilini LBP, GLCM, Gabor ve wavelet texture descriptor'lariyla birlestiren hibrit model.

Ek rapor ve notebooklarda DenseNet121, VGG16, HOG/LBP/KAZE ve SVM/RF baseline'lari da bulunur. Bunlar makale ve deney raporlarina baglam saglar; corrected ALL4 fusion tablosu ise yukaridaki dort aileyi ortak formulle karsilastirir.

### 5. Egitim ve threshold secimi

Egitimler agirlikli olarak Google Colab/Python ortaminda calistirildi ve ilgili notebooklar `03_regional_models/notebooks/` altina alindi. Train verisi model ogrenimi ve augmentation icin, validation verisi checkpoint/model secimi, threshold secimi ve fusion agirliklari icin, test verisi final raporlama icin kullanildi.

Karar threshold'lari test verisinden secilmedi:

- Xception kas/agiz deneylerinde threshold 0.50 sabit tutuldu.
- Xception goz, EfficientNet-B0, SwinV2-Tiny ve hibrit deneylerde validation F1'i maksimize eden threshold kullanildi.
- Ortak kohorttaki fusion/error analizlerinde bolgeler arasi karsilastirma icin 0.50 threshold kullanildi.

Bu nedenle accuracy/F1 degerleri yorumlanirken model aileleri arasinda threshold secim kurallarinin farkli olabildigi unutulmamalidir. Ana bolgesel karsilastirma metriklerinden biri threshold bagimsiz ROC-AUC'dir.

### 6. Tahmin dosyalari ve sema

Her bolgesel modelin test tahminleri `04_predictions/` altinda tutulur. Klasorler ROI'ye gore ayrilir:

- `04_predictions/eye/`
- `04_predictions/brow/`
- `04_predictions/mouth/`

Tahmin dosyalarinda frame/source anahtari, gercek etiket, olasilik skoru ve karar ciktilari korunur. Ortak sema `04_predictions/prediction_schema.csv` ile belgelenir. Fusion scriptleri, ayni model ailesindeki kas, goz ve agiz FAKE olasiliklarini source-frame key uzerinden eslestirir.

## Fusion Nasil Yapildi

Fusion asamasinda bolgesel modeller yeniden egitilmedi. Ayni model ailesindeki uc ROI tahmini ortak source-frame anahtariyla inner join yapildi. Sadece kas, goz ve agiz skoru birlikte bulunan kayitlar tutuldu; bu da 101 REAL ve 95 FAKE olmak uzere `n=196` ortak test kohortu verdi.

Iki fusion kurali kullanildi:

1. Equal soft voting:

```text
P_equal = (P_brow + P_eye + P_mouth) / 3
```

2. Validation-AUC weighted soft voting:

```text
r_i = max(validation_auc_i - 0.5, epsilon)
w_i = r_i / sum_j(r_j)
P_weighted = sum_i(w_i * P_i)
```

Agirliklar yalnizca validation ROC-AUC degerlerinden uretildi; test bilgisi agirlik hesaplamasina sokulmadi. Mevcut corrected ALL4 agirlik tablosu `05_fusion/results/corrected_validation_weights_ALL4.csv` dosyasindadir.

Weighted fusion icin validasyon agirliklari:

| Model ailesi | w_brow | w_eye | w_mouth |
| --- | ---: | ---: | ---: |
| Xception | 0.2378 | 0.3132 | 0.4490 |
| EfficientNet-B0 | 0.2630 | 0.3078 | 0.4292 |
| SwinV2-Tiny | 0.2306 | 0.3634 | 0.4060 |
| SwinV2-Tiny + Texture | 0.2812 | 0.2742 | 0.4446 |

Tum dort ailede agiz ROI en yuksek agirligi alir.

## Ana Sonuclar

Bolgesel sonuc ozeti:

- Dort model ailesinde de ROC-AUC siralamasi genel olarak agiz > goz > kas seklindedir.
- SwinV2-Tiny uc ROI'de de en yuksek AUC point estimate'i verir.
- Hibrit SwinV2 + texture modeli, bu protokolde base SwinV2-Tiny AUC'sini gecmez.
- Kas ROI, daha siki kabul kosullari ve daha dusuk kullanilabilir kayit sayisi nedeniyle daha sinirli degerlendirilir.

Corrected weighted fusion ortak kohort sonuclari:

| Model ailesi | n | Accuracy | F1 | ROC-AUC | Mouth-only AUC | Delta AUC |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Xception | 196 | 0.6888 | 0.6995 | 0.7412 | 0.7527 | -0.0115 |
| EfficientNet-B0 | 196 | 0.7347 | 0.7263 | 0.8196 | 0.8334 | -0.0138 |
| SwinV2-Tiny | 196 | 0.7959 | 0.7753 | 0.8763 | 0.8803 | -0.0040 |
| SwinV2-Tiny + Texture | 196 | 0.6888 | 0.6667 | 0.7672 | 0.7897 | -0.0225 |

Paired bootstrap analizi 5,000 resample ve random seed 42 ile yapildi. Dort weighted fusion satirinda da fusion-minus-mouth delta AUC guven araligi sifiri dislamaz. Bu, "fusion kesin daha kotu" anlamina gelmez; ancak mevcut orneklem ve protokolde mouth-only uzerine ek ROC-AUC kazanci gosterilemedigi anlamina gelir.

Ana sonuc dosyalari:

- `05_fusion/results/corrected_weighted_fusion_metrics_ALL4.csv`
- `05_fusion/results/corrected_validation_weights_ALL4.csv`
- `06_metrics_tables/paper_ready_corrected_fusion_table.csv`
- `05_fusion/source_outputs/corrected_weighted_soft_voting_all4_seed42/`
- `05_fusion/source_outputs/Fusion_Experiments/`
- `05_fusion/source_outputs/multi_region_fusion_results/`
- `06_metrics_tables/source_outputs/eye/20260808_0729_eye_efficientnet_b0_seed42/`
- `06_metrics_tables/source_outputs/eye/20260808_0747_eye_efficientnet_b0_seed42/`
- `06_metrics_tables/source_outputs/eye/PupilReflection_FusionCNN/`
- `06_metrics_tables/source_outputs/eye/PupilSegmentation_CornealReflectionConsistency_FusionCNN/README.md`

Pupil segmentation + corneal reflection consistency dali kaynak agacta goruldu, ancak bu snapshot sirasinda dosya icermeyen bir alt klasor yapisi olarak geldi. Bu nedenle repo, bos klasor yerine yukaridaki README notuyla bu dali temsil eder.

## Makale Nasil Hazirlandi

Makale, Deney 1 kaynak paketinden repo'ya alinan notebook/rapor/metrik ciktilari ile repo icindeki corrected fusion tablolarini birlestirerek hazirlandi. Yazimda su akisa sadik kalindi:

1. Deney 1 kaynak klasorleri envanterlendi ve repo karsiliklari olusturuldu.
2. Frame secim metadata'si, Real/Fake dengesi ve reddedilen frame kayitlari belgelendi.
3. ROI cikarma kosullari ve ROI basari/reddetme sayilari raporlandi.
4. Bolgesel model aileleri ve validasyon tabanli threshold/agirlik secimleri ozetlendi.
5. Full regional test sonuclari ile ortak kohort sonuclari ayrildi.
6. Equal ve validation-weighted late fusion ayni `n=196` ortak kohortta karsilastirildi.
7. Mouth-only ile fusion AUC farklari paired bootstrap ile yorumlandi.
8. Sonuclar, literatur tablosu ve sinirliliklar makale formatina tasindi.

Makale ve gonderim dosyalari zip paketinden repo'ya `08_article/submission_package/` altinda eklendi. Paket iki dilde gelir:

- `08_article/submission_package/English/Deepfake_Anonymous.pdf`: dergi basvurusu icin anonim Ingilizce ana makale.
- `08_article/submission_package/English/Deepfake_English.pdf`: yazar isimli Ingilizce kontrol kopyasi.
- `08_article/submission_package/Turkce/Deepfake_Turkce_Anonim.pdf`: Turkce anonim kontrol kopyasi.
- `08_article/submission_package/Turkce/Deepfake_Turkce.pdf`: yazar isimli Turkce kontrol kopyasi.
- `Title_Page_*` ve `Cover_Letter_*`: ana makaleden ayri gonderim belgeleri.
- `assets/`, `figures/`, `fonts/`, `elektr.cls`, `elksty.tex`: XeLaTeX derleme icin gereken yardimci dosyalar.

Paket notlarindaki gonderim oncesi maddeler repo talimati olarak uygulanmadi; sadece belge durumu olarak korundu. Eksik ORCID, sorumlu yazar e-postasi, kurum/onay/beyan bilgileri ekip tarafindan gercek bilgilerle tamamlanmadan dosyalar dogrudan dergiye gonderilmemelidir.

## Calistirma ve Kontrol

Kurulum:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Repo kontrol scripti:

```bash
python3 scripts/check_repo.py
```

Fusion scriptleri:

```bash
python3 05_fusion/majority_vote.py
python3 05_fusion/weighted_soft_voting.py
```

Tahmin birlestirme yardimcisi:

```bash
python3 04_predictions/aggregate_predictions.py
```

Sekil uretimi:

```bash
python3 07_figures/plot_fusion_metrics.py
```

Makale LaTeX dosyalari ilgili dil klasorunden XeLaTeX ile derlenmelidir. Ornek:

```bash
cd 08_article/submission_package/English
xelatex Deepfake_Anonymous.tex
xelatex Deepfake_Anonymous.tex
```

## Push Oncesi Kontrol Listesi

- `git status --short` ile yeni makale paketi ve README degisikliklerini kontrol et.
- `08_article/submission_package/README.md` dosyasindaki paket aciklamasini oku.
- Rapor metninde dis linki kalmamis mi kontrol et.
- Makale gonderimi yapilacaksa anonim dosya, title page ve cover letter ayrimini koru.
- Eksik yazar/ORCID/sorumlu yazar/beyan alanlarini uydurma; ekipten gercek bilgiyle tamamla.
