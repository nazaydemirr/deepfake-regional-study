# Deepfake Regional Study

Bu repo, AISC DeepFake Calismalari > Deney 1 klasorundeki bolgesel deepfake tespit deneylerini duzenli ve tekrar edilebilir bir GitHub yapisina tasir.

Calisma, yuzun farkli ROI bolgelerinden gelen bagimsiz tahminleri birlestirmeye odaklanir:

- Goz
- Kas / kas-cevresi
- Agiz
- Bolgesel model ciktilarindan majority voting ve weighted soft voting fuzyonu

## Klasor Yapisi

```text
deepfake-regional-study/
├── 01_data_splits/
├── 02_roi_preprocessing/
├── 03_regional_models/
├── 04_predictions/
├── 05_fusion/
├── 06_metrics_tables/
├── 07_figures/
├── 08_article/
├── requirements.txt
└── README.md
```

## Drive Kaynaklari

Ana Drive klasoru:

- AISC DeepFake Calismalari
- Deney 1
- AISC Makale Inceleme ve Literatur Tarama Tablosu

Deney 1 iceriginde kisi bazli calismalar bulunur:

- Nazlican: Goz ROI, PupilReflection_FusionCNN, goz sonuclari
- Dilara: Agiz ROI, agiz sonuclari
- Kader: Kas ROI, kas sonuclari, fuzyon sonuclari
- Ortak: Deney 1 Frame veri bolme/metadata dosyalari
- Ortak: agirlikli fuzyon tekrar calismasi ve corrected weighted fusion sonuclari

Drive'dan indirilen Deney 1 dosyalari repo icinde su sekilde yerlestirildi:

- Notebook ve egitim kodlari: `03_regional_models/notebooks/`
- ROI/frame secimi ve on isleme ciktilari: `01_data_splits/drive_exports/`, `02_roi_preprocessing/drive_outputs/`
- Fusion ve metrik ciktilari: `05_fusion/results/`, `06_metrics_tables/drive_outputs/`
- Deney raporlari: `08_article/reports/`
- Kod aciklama raporlari: `08_article/code_explanations/`
- Kucuk arsivler: `03_regional_models/drive_archives/`

Tam Drive-to-repo envanteri `01_data_splits/drive_exports/DENEY1_DRIVE_ASSET_MANIFEST.csv` dosyasindadir. GitHub tek dosya limitini asan buyuk ZIP/checkpoint/frame paketleri fiziksel olarak commitlenmedi; Drive linkleri `01_data_splits/drive_exports/SKIPPED_LARGE_FILES.md` ve `01_data_splits/drive_exports/DENEY1_DRIVE_FOLDER_MANIFEST.md` icinde tutuldu.

## Ana Deney Akisi

1. Frame secimi ve train/validation/test ayrimi `01_data_splits/` altinda belgelenir.
2. Goz, kas ve agiz ROI on islemesi `02_roi_preprocessing/` altinda tutulur.
3. Bolgesel model egitimleri `03_regional_models/` altinda standartlasir.
4. Her bolgeden uretilen tahmin CSV dosyalari `04_predictions/` formatini izler.
5. Majority voting ve weighted soft voting fuzyonlari `05_fusion/` altinda calistirilir.
6. Sonuc ve literatur tablolari `06_metrics_tables/` altinda makale hazir formatta tutulur.
7. Sekil ve grafik ciktilari `07_figures/` altinda toplanir.
8. Makale taslagi, literatur notlari ve yontem anlatimi `08_article/` altinda gelisir.

## Mevcut Corrected Weighted Fusion Ozeti

Drive'daki 17 Eylul 2026 tarihli agirlikli soft voting tekrarinda ortak kohort `n=196` olarak raporlanmistir. En yuksek ROC-AUC degeri `swinv2_tiny` ailesinde `0.8763`, en yuksek accuracy degeri yine `swinv2_tiny` ailesinde `0.7959` olarak gorulmektedir.

Detayli tablolar:

- `05_fusion/results/corrected_weighted_fusion_metrics_ALL4.csv`
- `05_fusion/results/corrected_validation_weights_ALL4.csv`
- `06_metrics_tables/paper_ready_corrected_fusion_table.csv`

## Literatur Dayanagi

Literatur tablosunda one cikan yaklasimlar:

- Bolgesel yuz analizi: goz, burun, agiz, tum yuz ve diger bolgeler
- CNN / Xception / DenseNet transfer learning
- CViT, ViT, Linformer, Swin V2 gibi transformer tabanli mimariler
- HOG, LBP, KAZE ve texture descriptor tabanli hafif modeller
- Decision-level late fusion, majority voting ve weighted soft voting

Bu repo, Drive'daki deneyleri ve literatur tablosunu ayni proje yapisinda birlestirmek icin hazirlandi.
