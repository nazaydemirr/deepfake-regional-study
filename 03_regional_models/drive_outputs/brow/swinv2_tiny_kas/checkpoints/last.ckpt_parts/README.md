This directory stores the original Drive file `last.ckpt` as split parts
because GitHub rejects single files larger than 100 MB.

Original Drive file:
- Name: `last.ckpt`
- Size: `331730929` bytes
- SHA-256: `952fe5608ab07c31c187e23d4f2b30b100cd2018098b5a84f6019432cfc373ab`

Reassemble from this directory:

```bash
cat last.ckpt.part-* > last.ckpt
shasum -a 256 last.ckpt
```
