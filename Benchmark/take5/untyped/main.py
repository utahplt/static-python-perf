import time

from player import Player
from dealer import Dealer


def generate_dealer(players, cards_per_game):
    """
    Instantiates the dealer which will take over the game
    :return: Dealer
    """
    points = [0 for i in range(len(players))]
    return Dealer(players, points, cards_per_game)


def generate_players(num_players):
    """
    instantiates n players with an empty list of cards
    :param num_players: int
    :return: [Players...]
    """
    players = []
    for i in range(num_players):
        players.append(Player(i, []))
    return players


def main():
    num = 3  # number of players
    cards_per_player = 10
    cards_per_game = 210

    if num < 2:
        print('Too few players!')

    if cards_per_game / cards_per_player < num:
        print("Too many players!")
        exit()

    players = generate_players(num)
    dealer = generate_dealer(players, cards_per_game)
    dealer.simulate_game()

start_time = time.time()
for i in range(500):
    main()
end_time = time.time()
runtime = end_time - start_time
print(runtime)
