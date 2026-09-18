# Literature Notes

Bu notlar, Drive'daki `AISC Makale Inceleme ve Literatur Tarama Tablosu` iceriginden bu repo icin secilen ana dayanaklari ozetler.

## Bolgesel Analiz

- Soudy et al. (2024) goz, burun ve tum yuz icin bagimsiz CNN/CViT tahminleri uretip majority voting ile tek karar olusturur. Bizim Eye + Brow + Mouth karar fuzyonuna en yakin yontemsel dayanaklardan biridir.
- Tolosana et al. (2021) yuz bolgelerine gore deepfake performansini sistematik inceler. Agiz, goz ve diger bolgelerin ayri degerlendirilmesini destekler.
- Elhassan et al. (2022) agiz hareketi ve dis gorunurlugu uzerinden deepfake tespitini ele alir. Agiz ROI dalinin bilimsel gerekcesidir.

## Mimari Dayanaklar

- FaceForensics++ (Rossler et al., 2019) proje veri seti ve Xception benchmark temelidir.
- Xception (Chollet, 2017) ROI transfer learning icin temel CNN omurgasidir.
- DenseNet (Huang et al., 2017) alternatif CNN omurgasi olarak kullanilabilir.
- Swin V2 + texture descriptor calismasi, transformer ve klasik texture kanitlarini birlestirmeyi destekler.

## Hafif ve Yorumlanabilir Ozellikler

- Yasir and Kim (2025), HOG + LBP + KAZE ile hafif deepfake detection yaklasimini destekler.
- Goz/gaze/blink calismalari, goz bolgesinin yalniz piksel artefakti degil davranissal ipucu da tasiyabilecegini gosterir.

## Fuzyon

- Majority voting ve decision-level late fusion, bolgesel tahminlerin tek karara donusturulmesi icin dogrudan uygundur.
- Corrected weighted soft voting deneyi, validation AUC tabanli agirliklandirma kullanir.
- Bu repo, hem pozitif hem de negatif bulgulari saklayacak sekilde tasarlanmistir.
