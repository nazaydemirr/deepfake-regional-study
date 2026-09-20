This directory stores the original Drive file `epoch_011.ckpt` as split parts
because GitHub rejects single files larger than 100 MB.

Original Drive file:
- Name: `epoch_011.ckpt`
- Size: `331726449` bytes
- SHA-256: `87e67f0b07c3da6e926c1c20e2bd36ac1bb5f1186c3786b51a6cc1aecbcddbe9`

Reassemble from this directory:

```bash
cat epoch_011.ckpt.part-* > epoch_011.ckpt
shasum -a 256 epoch_011.ckpt
```
