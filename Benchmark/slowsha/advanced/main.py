import __static__
from typing import Callable
from sha1 import SHA1
from sha512 import SHA512
import time

def new(algorithm: str, message: bytes) -> Callable:
    obj = {
        'sha1': SHA1,
        'sha512': SHA512,
    }[algorithm](message)
    return obj


def sha1(message: bytes) -> SHA1:
    ''' Returns a new sha1 hash object '''
    x = new('sha1', message)
    return x


def sha512(message: bytes) -> SHA512:
    ''' Returns a new sha512 hash object '''
    return new('sha512', message)


def main() -> None:
    # To unit test, compare against hashlib

    with open("../mysterious_words.txt", "rb") as f:
        for line in f:
            for word in line.split():
                sha1(word).hexdigest()
                sha1(word).digest()
                sha512(word).hexdigest()
                sha512(word).digest()
    return None


startTime = time.time()
main()
endTime = time.time()
runtime = endTime - startTime
print(runtime)
