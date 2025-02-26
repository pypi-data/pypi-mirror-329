# fast_ascon
A faster implementation of Ascon, using RustCrypto's Ascon crates
## Usage

```py
import fast_ascon
fast_ascon.hash(b"", variant = "Ascon-Hasha") # b'\xae\xcd\x02 ...
```