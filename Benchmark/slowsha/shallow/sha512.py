from __future__ import annotations
from typing import Tuple
from sha2_64 import sha2_64
import __static__
class SHA512(sha2_64):
    h0: int = 0x6a09e667f3bcc908
    h1: int = 0xbb67ae8584caa73b
    h2: int = 0x3c6ef372fe94f82b
    h3: int = 0xa54ff53a5f1d36f1
    h4: int = 0x510e527fade682d1
    h5: int = 0x9b05688c2b3e6c1f
    h6: int = 0x1f83d9abfb41bd6b
    h7: int = 0x5be0cd19137e2179

    # maybe Self instead of SHA512 not sure
    def _digest(self: SHA512) -> Tuple[int, int, int, int, int, int, int, int]:
        return (self.h0, self.h1, self.h2, self.h3, self.h4, self.h5, self.h6, self.h7)
