This directory stores the original Drive file `epoch_010.ckpt` as split parts
because GitHub rejects single files larger than 100 MB.

Original Drive file:
- Name: `epoch_010.ckpt`
- Size: `331726001` bytes
- SHA-256: `fb32e8e2166ae28d7a0bde9c2cd1e4d761a6a0c4f3c5ba9d0bae031d93aabe78`

Reassemble from this directory:

```bash
cat epoch_010.ckpt.part-* > epoch_010.ckpt
shasum -a 256 epoch_010.ckpt
```
