This directory stores the original Drive file `Xception_Eyebrow_Final.keras`
as split parts because GitHub rejects single files larger than 100 MB.

Original Drive file:
- Name: `Xception_Eyebrow_Final.keras`
- Size: `161641670` bytes
- SHA-256: `f40c3f5bf089d04363ba08e9066d7457fb2dfd99f8b2b188cffb4d0c25ed1329`

Parts:
- `Xception_Eyebrow_Final.keras.part-00` - `99614720` bytes
- `Xception_Eyebrow_Final.keras.part-01` - `62026950` bytes

Reassemble from this directory:

```bash
cat Xception_Eyebrow_Final.keras.part-* > Xception_Eyebrow_Final.keras
shasum -a 256 Xception_Eyebrow_Final.keras
```
