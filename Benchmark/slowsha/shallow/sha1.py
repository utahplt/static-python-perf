import __static__
from __static__ import Int, Bytes, Tuple, String, List

class SHA1(object):

    def __init__(self, message: Bytes):
        self.h0: Int
        self.h1: Int
        self.h2: Int
        self.h3: Int
        self.h4: Int
        self.h0, self.h1, self.h2, self.h3, self.h4 = (
            0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0)
        length: str = bin(len(message) * 8)[2:].rjust(64, "0")
        while len(message) > 64:
            self.handle(''.join(bin(i)[2:].rjust(8, "0")
                                for i in message[:64]))
            message = message[64:]
        strmessage: str = ''.join(bin(i)[2:].rjust(8, "0") for i in message) + "1"
        strmessage += "0" * ((448 - len(strmessage) % 512) % 512) + length
        for i in range(len(strmessage) // 512):
            self.handle(bytes(strmessage[i * 512:i * 512 + 512], encoding="utf-8"))

    def handle(self, chunk: Bytes) -> None:
        lrot = lambda x, n: (x << n) | (x >> (32 - n))
        w: List[Int] = []

        for j in range(len(chunk) // 32):
            w.append(int(chunk[j * 32:j * 32 + 32], 2))

        for i in range(16, 80):
            w.append(lrot(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1) & 0xffffffff)

        a: Int = self.h0
        b: Int = self.h1
        c: Int = self.h2
        d: Int = self.h3
        e: Int = self.h4

        for i in range(80):

            if 0 <= i <= 19:
                f, k = d ^ (b & (c ^ d)), 0x5a827999
            elif 20 <= i <= 39:
                f, k = b ^ c ^ d, 0x6ed9eba1
            elif 40 <= i <= 59:
                f, k = (b & c) | (d & (b | c)), 0x8f1bbcdc
            elif 60 <= i <= 79:
                f, k = b ^ c ^ d, 0xca62c1d6

            temp = lrot(a, 5) + f + e + k + w[i] & 0xffffffff
            a, b, c, d, e = temp, a, lrot(b, 30), c, d

        self.h0 = (self.h0 + a) & 0xffffffff
        self.h1 = (self.h1 + b) & 0xffffffff
        self.h2 = (self.h2 + c) & 0xffffffff
        self.h3 = (self.h3 + d) & 0xffffffff
        self.h4 = (self.h4 + e) & 0xffffffff

    def _digest(self) -> Tuple[Int, Int, Int, Int, Int]:
        return (self.h0, self.h1, self.h2, self.h3, self.h4)

    def hexdigest(self) -> String:
        return ''.join(hex(i)[2:].rjust(8, "0") for i in self._digest())

    def digest(self) -> Bytes:
        hexdigest = self.hexdigest()
        return bytes(int(hexdigest[i * 2:i * 2 + 2], 16) for i in range(len(hexdigest) // 2))
