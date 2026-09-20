This directory stores the original Drive file `epoch_012.ckpt` as split parts
because GitHub rejects single files larger than 100 MB.

Original Drive file:
- Name: `epoch_012.ckpt`
- Size: `331726897` bytes
- SHA-256: `53dc1612b2d9e8d900e79db0a7f43b89252f9719134f6044677613dd554deabc`

Reassemble from this directory:

```bash
cat epoch_012.ckpt.part-* > epoch_012.ckpt
shasum -a 256 epoch_012.ckpt
```
