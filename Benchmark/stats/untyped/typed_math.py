import math

_pow = pow
_abs = abs
_round = round

def pow(x, y):
    return _pow(x,y)

def sqrt(x):
    try:
        return math.sqrt(x)
    except ValueError as e:
        raise ValueError(e, x, type(x))
    return 0

def exp(x):
    return math.exp(x)

def abs(x):
    return _abs(x)

def fabs(x):
    return math.fabs(x)

def log(x):
    return math.log(x)

def round(n,d):
    return _round(n,d)

pi = float(math.pi)