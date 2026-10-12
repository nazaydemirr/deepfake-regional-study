# Large Asset Inventory Reports

Bu klasor, Deney 1 kaynak yapisindaki buyuk ham veri klasorlerini raporda dis link vermeden belgelemek icin olusturuldu.

Her kaynak bolumu icin:

- dosya ve klasor sayilari,
- Fake/Real ve train/validation/test kirilimlari,
- dosya uzantisi ve MIME tipi dagilimlari,
- ornek dosya yollari

repo icinde saklaniyor.

## Reports

| Report | Markdown | CSV | Summary |
| --- | --- | --- | --- |
| Deney 1 Frame primary raw inventory | `deney1_frame_primary_raw_inventory.md` | `deney1_frame_primary_raw_inventory.csv` | 16 folder, 304 file, 300 JPG raw frame |
| Deney 1 Frame secondary raw inventory | `deney1_frame_secondary_raw_inventory.md` | `deney1_frame_secondary_raw_inventory.csv` | 8 folder, 302 file, 300 JPG raw frame |
| Eye ROI output inventory | `eye_roi_output_inventory.md` | `eye_roi_output_inventory.csv` | 76 folder, 1514 file, 1200 JPG + 300 NPZ ROI payload |

## Repository Decision

Bu dosyalar kitap/makale raporunda "Deney 1 kaynak envanteri" olarak referanslanabilir. Rapor metni dis linki vermek yerine repo icindeki metadata, split ozetleri, model ciktilari, metrikler, figurler ve bu envanter raporlarini kullanir.
