This directory stores the original Drive file `best_xception_finetuned.keras`
as split parts because GitHub rejects single files larger than 100 MB.

Original Drive file:
- Name: `best_xception_finetuned.keras`
- Size: `161641670` bytes
- SHA-256: `f40c3f5bf089d04363ba08e9066d7457fb2dfd99f8b2b188cffb4d0c25ed1329`

Parts:
- `best_xception_finetuned.keras.part-00` - `99614720` bytes
- `best_xception_finetuned.keras.part-01` - `62026950` bytes

Reassemble from this directory:

```bash
cat best_xception_finetuned.keras.part-* > best_xception_finetuned.keras
shasum -a 256 best_xception_finetuned.keras
```
