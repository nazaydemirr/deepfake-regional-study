# Submission Package

Bu klasor, `Deepfake_TR_EN_Tum_Dosyalar (2).zip` paketinden eklenen makale ve gonderim dosyalarini tutar. Zip icindeki notlar proje talimati olarak uygulanmadi; sadece paket icerigi ve gonderim durumu olarak korundu.

## Icerik

- `English/Deepfake_Anonymous.*`: dergi basvurusu icin anonim Ingilizce ana makale.
- `English/Deepfake_English.*`: yazar isimli Ingilizce kontrol kopyasi.
- `English/Title_Page_English.*`: ana makaleden ayri yuklenecek baslik sayfasi.
- `English/Cover_Letter_English.*`: Ingilizce sunus mektubu.
- `Turkce/Deepfake_Turkce_Anonim.*`: Turkce anonim kontrol kopyasi.
- `Turkce/Deepfake_Turkce.*`: yazar isimli Turkce kontrol kopyasi.
- `Turkce/Title_Page_Turkce.*`: Turkce baslik sayfasi.
- `Turkce/Cover_Letter_Turkce.*`: Turkce sunus mektubu.
- `assets/`: makale icinde kullanilan PNG sekiller.
- `figures/`: ayri yuklenebilecek PDF/TIFF sekiller.
- `fonts/`, `elektr.cls`, `elksty.tex`, `elk-creative.eps`: XeLaTeX ve dergi sablonu icin yardimci dosyalar.
- `README.txt`, `Kontrol_Notlari.txt`, `Gonderim_Oncesi_Tamamlanacaklar.txt`: zip paketinin kendi aciklama ve kontrol notlari.

## Derleme

LaTeX dosyalari bulunduklari dil klasorunden XeLaTeX ile derlenmelidir:

```bash
cd 08_article/submission_package/English
xelatex Deepfake_Anonymous.tex
xelatex Deepfake_Anonymous.tex
```

Turkce dosya icin ayni islem `Turkce/` klasorunde yapilir.

## Gonderim Notu

Dergi gonderimi icin anonim ana makale, ayri title page ve ayri cover letter ayrimi korunmalidir. ORCID, sorumlu yazar e-postasi, kurum onayi, cikar catismasi, finansman/destek ve etik/onam beyanlari ekip tarafindan gercek bilgilerle tamamlanmadan paket dogrudan gonderime hazir kabul edilmemelidir.
