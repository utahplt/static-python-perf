from __future__ import annotations
from typing import List
from retic import Void, List, Int, Bool, Dyn, fields
from evolution.player.player_state import PlayerState
import __static__
class CardPlay:
    """
    CardPlay is one of:
    - SupplementSpecies
    - ReplaceCard
    - ExchangeCard
    """

    def __init__(self: CardPlay, played_card_index: Int) -> None:
        """
        :param played_card_index: the card that was played
        :type played_card_index: TraitCard
        :return: None
        """
        self.played_card_index: Int = played_card_index

    def apply(self: CardPlay, player_state: PlayerState) -> None:
        """
        Applies this card play to the given PlayerState
        :param player_state: PlayerState to be applied to
        :type player_state: PlayerState
        :return: None
        """
        raise NotImplementedError("Method not yet implemented.")

    def get_card_indices(self: CardPlay) -> List[Int]:
        """
        Get the indices of the TraitCards used by this CardPlay
        :return: list of the indices used
        :rtype: List[Int]
        """
        return [self.played_card_index]

    #TODO: Fix types for this method
    def verify_self(self: CardPlay, player_state: PlayerState, food_card_index: Int,
                    card_plays_before_this: List[CardPlay]) -> Bool:
        """
        Verifies that this card play is valid
        :param player_state: the player state playing this card
        :type player_state: PlayerState
        :type food_card_index: Int
        :type card_plays_before_this: List[CardPlay]
        :return: True if this is valid, False otherwise
        """
        self_indices: List[Int] = self.get_card_indices()
        previous_indices: set[Int] = {food_card_index}
        for card_play in card_plays_before_this:
            previous_indices = previous_indices.union(set(card_play.get_card_indices()))

        no_dups: Bool = len(self_indices) == len(set(self_indices))
        no_overlap: Bool = previous_indices.intersection(set(self_indices)) == set()
        in_range: Bool = set(self_indices).issubset(set(range(0, len(player_state.hand))))

        return no_dups and no_overlap and in_range

    def update_trait_counts(self: CardPlay, species_trait_count: List[Int]) -> List[Int]:
        """
        Append the species trait count to the given list
        if this is an ExchangeForSpecies
        :param species_trait_count: All trait counts up to this card play
        :type species_trait_count: List[Int]
        :return: updated list of trait counts
        :rtype: List[Int]
        """
        raise NotImplementedError("Method not yet implemented")

    def num_species_created(self: CardPlay) -> Int:
        """
        returns the number of species created
        as a result of this card play
        :return:
        """
        return 0