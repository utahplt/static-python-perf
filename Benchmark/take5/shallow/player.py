from typing import List, Tuple
import __static__


class Player:
    """
    To represent a player in the game
    """

    def __init__(self, name: int, cards: List[Tuple[int, int]]) -> None:
        """
        :param name: Int
        :param cards: [Tuple...]
        :param strat: Function, to be called on face values of cards
        :return: Player
        """
        self.name = name
        self.cards = cards

    def discard(self) -> int:
        """
        Return index of card to be discarded
        :return: Int
        """
        face_values = list(map(lambda card: card[0], self.cards))
        discarded_index = face_values.index(max(face_values))
        return discarded_index

    def choose_correct_stack(self, stacks: List[List[Tuple[int, int]]]) -> int:
        """
        Returns the index of the correct stack
        :param stacks: [[Tuple ...]...]
        :return: Int
        """
        top_cards = list(map(lambda stack: stack[-1], stacks))
        discarded_index = self.discard()
        discarded = self.cards[discarded_index]
        if discarded[0] < min(list(map(lambda card: card[0], top_cards))):

            sums = []
            for stack in stacks:
                bull_points = list(map(lambda card: card[1], stack))
                sums.append(sum(bull_points))

            return sums.index(min(sums))

        else:
            return self.get_index_of_closest_stack(top_cards, discarded)

    def get_index_of_closest_stack(self, cards: List[Tuple[int, int]], card: Tuple[int, int]) -> int:
        """
        gets index of stack closest to card in value
        :param cards: [Tuple ...]
        :return: Int
        """
        diffs = []
        for c in cards:
            diff = abs(card[0] - c[0])
            diffs.append(diff)
        return diffs.index(min(diffs))
