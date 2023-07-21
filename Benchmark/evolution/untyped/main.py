import sys
from evolution.player.player import Player
from Timer import Timer

from dealer.dealer import Dealer
from dealer.deck import Deck


MIN_PLAYERS = 3
MAX_PLAYERS = 8


def main(argv):
    """
    create and run the game
    :return:
    """
    n = int(argv[0])
    if n < MIN_PLAYERS or n > MAX_PLAYERS:
        raise ValueError('Number of players not in range')

    for i in range(20):
        dealer = make_dealer(n)
        dealer.run_game()
        score = dealer.get_sorted_scores()

def make_dealer(n):
    """
    creates and returns an instance of a dealer
    :param n: number of players in the game
    :type n: Nat
    :return: the dealer
    :rtype: Dealer
    """
    players = [Player() for i in range(n)]
    dealer = Dealer(players, Deck.make_deck())
    return dealer


def print_score(score):
    """
    Prints the score of the game
    :param score: [(id, score), ...]
    :type score:[(Nat, Nat), ...]
    :return: None
    """
    for i, s in enumerate(score):
        print("%s player id: %s info: %s score: %s" % (i + 1, s[0], s[1], s[2]))

if __name__ == "__main__":
    t = Timer()
    with t:
        if len(sys.argv) == 1:
            main(["7"])
        else:
            main(sys.argv[1:])

