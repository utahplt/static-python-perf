from __future__ import annotations
import random
import math
from typing import final, Set
from __static__ import int64, Array, CheckedList, cbool, box
import time

#SIZE: int64 = 9
GAMES: int = 200
#KOMI = 7.5
#EMPTY: int64 = 0
#WHITE: int64 = 1
#BLACK: int64 = 2
#PASS: int64 = -1
MAXMOVES: int = 9*9*3 #bg#SIZE*SIZE*3
TIMESTAMP: int = 0
MOVES: int = 0

def to_pos(x: int64, y: int64) -> int64:
    return y * 9 + x # SIZE + x

@final
class Square:
    def __init__(self: Square, board: Board, pos: int) -> None:
        self.board: Board = board
        self.pos: int64 = int64(pos)
        self.timestamp: int = TIMESTAMP
        self.removestamp: int = TIMESTAMP
        self.zobrist_strings: Array[int64] = Array[int64](3)
        for ii in range(3):
          self.zobrist_strings[ii] = int64(random.randrange(9223372036854775807))
        self.color: int64 = 0
        self.reference: Square = self
        self.ledges: int64 = 0
        self.used: cbool = False
        self.neighbours: CheckedList[Square] = CheckedList[Square]([])
        self.temp_ledges: int64 = 0


    def set_neighbours(self: Square) -> None:
        x: int64 = self.pos % 9 ## SIZE
        y: int64 = self.pos // 9 ## SIZE
        self.neighbours = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            newx: int64 = x + int64(dx)
            newy: int64 = y + int64(dy)
            if 0 <= newx < 9 and 0 <= newy < 9: ## 9 = SIZE
                bbb: Square = self.board.squares[to_pos(newx, newy)]
                self.neighbours.append(bbb)



    def move(self: Square, color: int64) -> None:
        global TIMESTAMP, MOVES
        TIMESTAMP += 1
        MOVES += 1
        self.board.zobrist.update(self, color)
        self.color = (color)
        self.reference = self
        self.ledges = int64(0)
        self.used = True
        for neighbour in self.neighbours:
            neighcolor: int64 = neighbour.color
            if neighcolor == 0: ## bg EMPTY:
                self.ledges += 1
            else:
                neighbour_ref: Square = neighbour.find(True)
                if neighcolor == self.color:
                    if neighbour_ref.reference.pos != self.pos:
                        self.ledges += neighbour_ref.ledges
                        neighbour_ref.reference = self
                    self.ledges -= 1
                else:
                    neighbour_ref.ledges -= 1
                    if neighbour_ref.ledges == 0:
                        neighbour.remove(neighbour_ref, True)
        self.board.zobrist.add()

    def remove(self: Square, reference: Square, update: bool) -> None:
        self.board.zobrist.update(self, 0) #bg EMPTY
        self.removestamp = TIMESTAMP
        if update:
            self.color = 0 #bg EMPTY
            self.board.emptyset.add(self.pos)
            # if color == BLACK:
            #     self.board.black_dead += 1
            # else:
            #     self.board.white_dead += 1
        for neighbour in self.neighbours:
            if neighbour.color != 0 and cbool(neighbour.removestamp != TIMESTAMP): # bg 0 = EMPTY
                neighbour_ref: Square = neighbour.find(update)
                if neighbour_ref.pos == reference.pos:
                    neighbour.remove(reference, update)
                else:
                    if update:
                        neighbour_ref.ledges += 1

    def find(self: Square, update: bool) -> Square:
        reference: Square = self.reference
        if reference.pos != self.pos:
            reference = reference.find(update)
            if update:
                self.reference = reference
        return reference

#@fields({'empties':List(int)
#        ,'board':{'useful':Function(NamedParameters([('pos',int)])
#                 ,int)}
#        ,'empty_pos':List(int)})
@final
class EmptySet:
    #def __init__(self:EmptySet, board:{'useful':Function(NamedParameters([('pos',int)]), int)})->Void:
    def __init__(self, board: Board) -> None:
        self.board: Board = board
        S2 = 9*9 #bg#SIZE*SIZE
        self.empties: Array[int64] = Array[int64](S2)
        self.empty_pos: Array[int64] = Array[int64](S2)
        for kk in range(S2):
          ii: int64 = int64(kk)
          self.empties[ii] = ii
          self.empty_pos[ii] = ii

    #def random_choice(self:EmptySet)->int:
    def random_choice(self) -> int64:
        choices: int64 = int64(len(self.empties)) # TODO ... optional ?!
        while choices:
            i: int64 = int64(int(random.random()*box(choices)))
            pos = self.empties[i]
            if self.board.useful(pos):
                return pos
            choices -= 1
            self.set(i, self.empties[choices])
            self.set(choices, pos)
        return -1 #bg#PASS

    #def add(self:EmptySet, pos:int)->Void:
    def add(self, pos: int64) -> None:
        self.empty_pos[pos] = int64(len(self.empties))
        self.empties[pos] = pos # TODO append

    #def remove(self:EmptySet, pos:int, update:bool)->Void:
    def remove(self, pos: int64, update: bool) -> None:
        self.set(self.empty_pos[pos], self.empties[len(self.empties)-1])
        # self.empties.pop() # TODO pop

    #def set(self:EmptySet, i:int, pos:int)->Void:
    def set(self, i: int64, pos: int64) -> None:
        self.empties[i] = pos
        self.empty_pos[pos] = i

#@fields({'hash':int})
@final
class ZobristHash:
    #def __init__(self:ZobristHash, board:{'squares':List(Square)})->Void:
    def __init__(self, board: Board) -> None:
        self.hash_set: Set[int] = set() # TODO no Set?
        self.hash: int = 0
        for square in board.squares:
            self.hash ^= square.zobrist_strings[0] #bg# EMPTY
        self.hash_set.clear()
        self.hash_set.add(self.hash)

    #def update(self:ZobristHash, square:Square, color:int)->Void:
    def update(self, square: Square, color: int64) -> None:
        self.hash ^= square.zobrist_strings[square.color]
        self.hash ^= square.zobrist_strings[color]

    #def add(self:ZobristHash)->Void:
    def add(self) -> None:
        self.hash_set.add(self.hash)

    def dupe(self) -> bool:
        return self.hash in self.hash_set

#@fields({'squares':List(Square)
#        ,'emptyset':EmptySet
#        ,'zobrist':ZobristHash
#        ,'color':int
#        ,'finished':Bool
#        ,'history':List(int)
#        ,'white_dead':int
#        ,'black_dead':int
#        ,'lastmove':int})
@final
class Board:
    #def __init__(self:Board)->Void:
    def __init__(self) -> None:
        self.squares: CheckedList[Square] = CheckedList[Square]([])
        self.emptyset: EmptySet = EmptySet(self)
        self.zobrist: ZobristHash = ZobristHash(self)
        self.color: int64 = 2 #bg#BLACK
        self.finished: bool = False
        self.lastmove: int64 = -2
        self.history: CheckedList[int] = CheckedList[int]([])
        self.white_dead: int = 0
        self.black_dead: int = 0
        #bgWHYYY#self.squares = [Square(self, pos) for pos in range(9*9)] #bg#SIZE*SIZE)
        for pos in range(9*9):
          self.squares.append(Square(self, pos))
        for square in self.squares:
            square.set_neighbours()
            square.color = 0 #bg#EMPTY
            square.used = False

    #def reset(self:Board)->Void:
    def reset(self) -> None:
        for square in self.squares:
            square.color = 0 #bg#EMPTY
            square.used = False
        self.emptyset = EmptySet(self)
        self.zobrist = ZobristHash(self)
        self.color = 2 #bg#BLACK
        self.finished = False
        self.lastmove = -2
        self.history = []
        self.white_dead = 0
        self.black_dead = 0

    #def move(self:Board, pos:int)->Void:
    def move(self, pos: int64) -> None:
        square = self.squares[pos]
        if pos != -1: #bg# PASS:
            square.move(self.color)
            self.emptyset.remove(square.pos, True)
        elif self.lastmove == -1: #bg# PASS:
            self.finished = True
        if self.color == 2: self.color = 1 #bg#BLACK WHITE #bg#WHITE
        else: self.color = 2 #bg#BLACK 
        self.lastmove = pos
        self.history.append(box(pos))

    #def random_move(self:Board)->int:
    def random_move(self) -> int64:
        return self.emptyset.random_choice()

    #def useful_fast(self:Board, square:Square)->bool:
    def useful_fast(self, square: Square) -> bool:
        if not square.used:
            for neighbour in square.neighbours:
                if neighbour.color == 0: #bg# EMPTY
                    return True
        return False

    #def useful(self:Board, pos:int)->int:
    def useful(self, pos: int64) -> int:
        global TIMESTAMP
        TIMESTAMP += 1
        square = self.squares[pos]
        if self.useful_fast(square):
            return True
        old_hash = self.zobrist.hash
        self.zobrist.update(square, self.color)
        empties = opps = weak_opps = neighs = weak_neighs = 0
        for neighbour in square.neighbours:
            neighcolor = neighbour.color
            if neighcolor == 0: #bg#EMPTY
                empties += 1
                continue
            neighbour_ref = neighbour.find(False)
            if neighbour_ref.timestamp != TIMESTAMP:
                if neighcolor == self.color:
                    neighs += 1
                else:
                    opps += 1
                neighbour_ref.timestamp = TIMESTAMP
                neighbour_ref.temp_ledges = neighbour_ref.ledges
            neighbour_ref.temp_ledges -= 1
            if neighbour_ref.temp_ledges == 0:
                if neighcolor == self.color:
                    weak_neighs += 1
                else:
                    weak_opps += 1
                    neighbour_ref.remove(neighbour_ref, False)
        dupe = self.zobrist.dupe()
        self.zobrist.hash = old_hash
        strong_neighs = neighs-weak_neighs
        strong_opps = opps-weak_opps
        return not dupe and \
               (empties or weak_opps or (strong_neighs and (strong_opps or weak_neighs)))

    #def useful_moves(self:Board)->List(int):
    def useful_moves(self) -> CheckedList[int]:
        return CheckedList[int]([pos for pos in self.emptyset.empties if self.useful(pos)])

    #def replay(self:Board, history:List(int))->Void:
    def replay(self, history: Array[int64]) -> None:
        for pos in history:
            self.move(pos)

    #def score(self:Board, color:int)->float:
    def score(self, color: int64) -> float:
        if color == 1: #bg#WHITE
            count = 7.5 + self.black_dead #bg#KOMI
        else:
            count = self.white_dead
        for square in self.squares:
            squarecolor = square.color
            if squarecolor == color:
                count += 1
            elif squarecolor == 0: #bg#EMPTY
                surround = 0
                for neighbour in square.neighbours:
                    if neighbour.color == color:
                        surround += 1
                if surround == len(square.neighbours):
                    count += 1
        return count

    #def check(self:Board)->Void:
    def check(self) -> None:
        for square in self.squares:
            if square.color == 0: #bg#EMPTY
                continue

            members1 = set([square])
            changed = True
            while changed:
                changed = False
                for member in members1.copy():
                    for neighbour in member.neighbours:
                        if int64(neighbour.color) == square.color and cbool(neighbour not in members1):
                            changed = True
                            members1.add(neighbour)
            ledges1 = 0
            for member in members1:
                for neighbour in member.neighbours:
                    if neighbour.color == 0: #bg#EMPTY
                        ledges1 += 1

            root = square.find(False)

            members2 = set()
            for square2 in self.squares:
                if square2.color != 0 and cbool(square2.find(False) == root): #bg#EMPTY
                    members2.add(square2)

            ledges2 = root.ledges

            # TODO
            # assert members1 == members2
            # assert ledges1 == ledges2, ('ledges differ at %r: %d %d' % (square, ledges1, ledges2))

            empties1 = set(self.emptyset.empties)

            empties2 = set()
            for square in self.squares:
                if square.color == 0: #bg#EMPTY
                    empties2.add(box(square.pos))


#@fields({'pos':int, 'wins':int, 'losses':int})
@final
class UCTNode:
    #def __init__(self:UCTNode)->Void:
    def __init__(self) -> None:
        self.bestchild: None | UCTNode = None
        self.pos: int64 = -1
        self.wins: int64 = 0
        self.losses: int64 = 0
        self.pos_child: CheckedList[None | UCTNode] = CheckedList[None | UCTNode]([None for x in range(9*9)]) #bg#SIZE*SIZE
        self.parent: None | UCTNode = None
        self.unexplored: CheckedList[int]  = CheckedList[int]([])

    #def play(self:UCTNode, board:Board)->Void:
    def play(self, board: Board) -> None:
        """ uct tree search """
        color: int = box(board.color)
        node: UCTNode = self
        path: CheckedList[UCTNode] = CheckedList[UCTNode]([node])
        pos: int64 = 0
        while True:
            pos = node.select(board)
            if pos == -1:
                break
            board.move(pos)
            child = node.pos_child[pos]
            if not child:
                child = node.pos_child[pos] = UCTNode()
                child.unexplored = board.useful_moves()
                child.pos = pos
                child.parent = node
                path.append(child)
                break
            path.append(child)
            node = child
        self.random_playout(board)
        self.update_path(board, color, path)

    #def select(self:UCTNode, board:Board)->int:
    def select(self, board: Board) -> int64:
        """ select move; unexplored children first, then according to uct value """
        if self.unexplored:
            i:int = random.randrange(len(self.unexplored))
            pos:int64 = int64(self.unexplored[i])
            self.unexplored[i] = self.unexplored[len(self.unexplored)-1]
            self.unexplored.pop()
            return pos
        elif self.bestchild is not None:
            return self.bestchild.pos
        else:
            return -1

    #def random_playout(self:UCTNode, board:Board)->Void:
    def random_playout(self, board: Board) -> None:
        """ random play until both players pass """
        for x in range(MAXMOVES): # XXX while not self.finished?
            if board.finished:
                break
            board.move(board.random_move())

    #def update_path(self:UCTNode, board:Board, color:int, path:List(UCTNode))->Void:
    def update_path(self, board: Board, color: int, path: CheckedList[UCTNode]) -> None:
        """ update win/loss count along path """
        wins = board.score(2) >= board.score(1) #bg#BLACK #bg#WHITE
        for node in path:
            if color == 2: color = 1 #bg#BLACK #bg#WHITE
            else: color = 2 #bg#BLACK
            if wins == (color == 2): #bg#BLACK
                node.wins += 1
            else:
                node.losses += 1
            if node.parent is not None:
                mypar = node.parent
                bc = mypar.best_child()
                if node.parent is not None:
                    node.parent.bestchild = bc

    #def score(self:UCTNode)->float:
    def score(self) -> float:
        winrate = box(self.wins)/float(box(self.wins)+box(self.losses))
        parentvisits: int = 0
        if self.parent is not None:
            parentvisits += box(self.parent.wins)
        if self.parent is not None:
            parentvisits += box(self.parent.losses)
        if not parentvisits:
            return winrate
        nodevisits: int = box(self.wins+self.losses)
        return winrate + math.sqrt((math.log(parentvisits))/(5*nodevisits))

    #def best_child(self:UCTNode)->UCTNode:
    def best_child(self) -> None | UCTNode:
        maxscore = -1
        maxchild = None
        for child in self.pos_child:
            if child and child.score() > maxscore:
                maxchild = child
                maxscore = child.score()
        return maxchild

    #def best_visited(self:UCTNode)->UCTNode:
    def best_visited(self) -> None | UCTNode:
        maxvisits: int64 = -1
        maxchild = None
        for child in self.pos_child:
            if child is not None and box((child.wins+child.losses) > maxvisits):
                maxvisits = (child.wins+child.losses)
                maxchild = child
        return maxchild

#def computer_move(board:{'useful_moves':Function([], List(int)),
#                         'random_move':Function([], int),
#                         'history':List(int)})->int:
def computer_move(board: Board) -> int:
    global MOVES
    pos = board.random_move()
    if pos == -1:
        return -1 #bg#PASS
    tree = UCTNode()
    tree.unexplored = board.useful_moves()
    nboard = Board()
    num_hist = len(board.history)
    ahist = Array[int64](num_hist)
    for ii in range(num_hist):
      ahist[ii] = int64(board.history[ii])
    for game in range(GAMES):
        node = tree
        nboard.reset()
        nboard.replay(ahist)
        node.play(nboard)
    bvv = tree.best_visited()
    if bvv is not None:
        return box(bvv.pos)
    return -1

ITERATIONS = 2

# Histogram of method call counts:
#      328486 Board
#      235994 EmptySet
#     1001986 SQUARE
#       30810 UCTNode
#      242536 ZobristHash
# (obtained by adding a `print` at the top of each method call, counting the prints from 1 run)

if __name__ == "__main__":
    start_time = time.time()

    for i in range(ITERATIONS):
        random.seed(1)
        board = Board()
        pos = computer_move(board)

    end_time = time.time()
    runtime = end_time - start_time
    print(runtime)
