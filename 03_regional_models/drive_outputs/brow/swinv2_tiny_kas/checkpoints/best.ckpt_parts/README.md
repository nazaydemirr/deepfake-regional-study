This directory stores the original Drive file `best.ckpt` as split parts
because GitHub rejects single files larger than 100 MB.

Original Drive file:
- Name: `best.ckpt`
- Size: `331728241` bytes
- SHA-256: `fc42f70b8ba88eb899f83bc6553afe4ff0b5e45f70af88acf123086297cfa420`

Reassemble from this directory:

```bash
cat best.ckpt.part-* > best.ckpt
shasum -a 256 best.ckpt
```
