# The Computer Language Benchmarks Game
# http://shootout.alioth.debian.org/
#
# contributed by Daniel Nanz, 2008-08-21

"""
bg:
- remove
  - `rotate.rd` param (never passed)
  - `flip.fd` param (never passed)
  - `permute` `rotate` and `flip` params (never passed)
  - `get_puzzle`, the w,h params. Never supplied
  - `print_board`
  - `solve`, optional arguments `fps` `se_nh` `bisect` never supplied
- add `ITERATIONS` parameter
- replace `timer` with `Timer` class
- replace xrange with range
- replace `frozenset` with `list`
- increased size of board to `20 x 40`
- time `get_puzzle()`, `get_footprints()` `get_senh()` calls
"""
from typing import List, Dict, Set
import __static__
from bisect import bisect
import time
w: int = 20
h: int = 40
dir_no: int = 6
S: int = w * h
E: int = 2
SE: float = S + (E / 2)
SW: float = SE - E
W: float = -E
NW: float = -SE
NE: float = -SW


def rotate(ido: List[int]) -> List[float]:
    rd: Dict[float, float] = {E: NE, NE: NW, NW: W, W: SW, SW: SE, SE: E}
    return [rd[o] for o in ido]
def flip(ido: List[int]) -> List[float]:
    fd: Dict[float, float] = {E: E, NE: SE, NW: SW, W: W, SW: NW, SE: NE} # make dict?
    return [fd[o] for o in ido]

def permute(ido: List[int], r_ido: List[int]) -> List[float]:
    ps: List[List[int]] = [ido]
    for r in range(dir_no - 1):
        ps.append(rotate(ps[-1]))
        if ido == r_ido:  # C2-symmetry
            ps = ps[0:dir_no // 2]
    for pp in ps[:]:
        ps.append(flip(pp))
    return ps


def convert(ido: List[float]) -> List[float]:
    '''incremental direction offsets -> "coordinate offsets" '''
    out: List[float] = [0.0]
    for o in ido:
        out.append(out[-1] + o)
    return list(set(out))

def get_footprints(board: List[float], cti: Dict[float, int], pieces: List[List[List[float]]]) -> \
        List[List[List[Set[List[int]]]]]:
    fps: List[List[List[Set[List[int]]]]] = [[[] for p in range(len(pieces))] for ci in range(len(board))]
    for c in board:
        for pi, p in enumerate(pieces):
            for pp in p:
                fp = list([cti[c + o] for o in pp if (c + o) in cti])
                if len(fp) == 5:
                    fps[min(fp)][pi].append(fp)
    return fps


def get_senh(board: List[float], cti: Dict[float, int]) -> List[Set[List[int]]]:
    '''-> south-east neighborhood'''
    se_nh: List[Set[List[int]]] = []
    nh: List[float] = [E, SW, SE]
    for c in board:
        se_nh.append(frozenset([cti[c + o] for o in nh if (c + o) in cti]))
    return se_nh


def get_puzzle() -> (List[float], Dict[float, int], List[List[List[float]]]):
    board: List[float] = [E * x + S * y + (y % 2) for y in range(h) for x in range(w)]
    cti: Dict[float, int] = dict((board[i], i) for i in range(len(board)))

    idos: List[List[float]] = [[E, E, E, SE],  # incremental direction offsets
                               [SE, SW, W, SW],
                               [W, W, SW, SE],
                               [E, E, SW, SE],
                               [NW, W, NW, SE, SW],
                               [E, E, NE, W],
                               [NW, NE, NE, W],
                               [NE, SE, E, NE],
                               [SE, SE, E, SE],
                               [E, NW, NW, NW]]

    perms = (permute(p, idos[3]) for p in idos)  # restrict piece 4
    pieces: List[List[List[float]]] = [[convert(pp) for pp in p] for p in perms]
    return (board, cti, pieces)


def solve(n: int, i_min: int, free: List[int], curr_board: List[int], pieces_left: List[int], fps:List[List[List[Set[List[int]]]]], se_nh: List[Set[List[int]]], solutions: List[int]) -> None:
    fp_i_cands: List[List[List[Set[List[int]]]]] = fps[i_min]
    for p in pieces_left:
        fp_cands: List[Set[List[int]]] = fp_i_cands[p]
        for fp in fp_cands:
            if fp <= free:
                n_curr_board: List[int] = curr_board[:]
                for ci in fp:
                    n_curr_board[ci] = p
                if len(pieces_left) > 1:
                    n_free: List[int] = free - fp
                    n_i_min: int = min(n_free)
                    if len(n_free & se_nh[n_i_min]) > 0:
                        n_pieces_left: List[int] = pieces_left[:]
                        n_pieces_left.remove(p)
                        solve(n, n_i_min, n_free, n_curr_board,
                              n_pieces_left, fps, se_nh, solutions)
                else:
                    s: str = ''.join(map(str, n_curr_board))
                    solutions.insert(bisect(solutions, s), s)
                    rs: str = s[::-1]
                    solutions.insert(bisect(solutions, rs), rs)
                    if len(solutions) >= n:
                        return
        if len(solutions) >= n:
            return
    return

SOLVE_ARG = 6000


if __name__ == "__main__":
    board, cti, pieces = get_puzzle()
    fps = get_footprints(board, cti, pieces)
    se_nh = get_senh(board, cti)
    free = list(range(len(board)))
    curr_board = [-1] * len(board)
    pieces_left = list(range(len(pieces)))
    solutions = []

    start = time.time()

    solve(SOLVE_ARG, 0, free, curr_board, pieces_left, fps, se_nh, solutions)

    endTime = time.time()
    runtime = endTime - start
    print(runtime)
