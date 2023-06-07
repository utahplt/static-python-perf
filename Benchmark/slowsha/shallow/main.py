import __static__
from typing import String, Bytes, Function, Void
from sha1 import SHA1
from sha512 import SHA512


def new(algorithm: String, message: Bytes) -> Function([], Bytes):
    obj = {
        'sha1': SHA1,
        'sha512': SHA512,
    }[algorithm](message)
    return obj


def sha1(message: Bytes) -> SHA1:
    ''' Returns a new sha1 hash object '''
    x = new('sha1', message)
    return x


def sha512(message: Bytes) -> SHA512:
    ''' Returns a new sha512 hash object '''
    return new('sha512', message)


from sha1 import SHA1
from sha512 import SHA512
import os


def main() -> None:
    # To unit test, compare against hashlib

    with open(os.path.join(os.path.dirname(__file__), "mysterious_words.txt"), "rb") as f:
        for line in f:
            for word in line.split():
                sha1(word).hexdigest()
                sha1(word).digest()
                sha512(word).hexdigest()
                sha512(word).digest()
    return None


main()
