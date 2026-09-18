# 07 Figures

Bu klasor, makalede kullanilacak grafik ve sekil ciktilarini toplar.

Onerilen figurlar:

- Veri akisi: Frame split -> ROI preprocessing -> bolgesel modeller -> fuzyon
- ROI ornekleri: eye, brow, mouth crop ornekleri
- Model karsilastirma bar chart
- ROC-AUC karsilastirma grafigi
- Confusion matrix panelleri
- Weighted soft voting agirliklari

Buyuk gorseller ve ornek frame'ler GitHub'a eklenmeden once etik, izin ve dosya boyutu acisindan kontrol edilmelidir.

## Drive'dan Acilan Deney 1 Figurlari

ZIP arsivlerinden acilan figurlar bolge ve run adina gore ayrildi:

- `eye/20260808_1214_eye_densenet121_seed42/`: DenseNet121 goz run'i icin training curves, confusion matrix, ROC/PR ve probability distribution figurlari.
- `mouth/20260808_1240_mouth_vgg16_svm_seed42/`: VGG16+SVM agiz run'i icin confusion matrix, ROC, precision-recall ve test metrik figurlari.
