from __future__ import annotations
from typing import List
from cardplay import CardPlay
from retic import Int, Bool, List, Void, Dyn, String, fields
from evolution.player.player_state import PlayerState
import __static__
class ExchangeForPopulation(CardPlay):
    """
    Represents exchanging cards for Population
    """

    def __init__(self: ExchangeForPopulation, played_card_index: Int, species_index: Int) -> None:
        """
        :param played_card_index: index of the card
        :type played_card_index: Int
        :param species_index: index of the species to change
        :type species_index: Int
        """
        super().__init__(played_card_index)
        self.species_index: Int = species_index

    def apply(self: ExchangeForPopulation, player_state: PlayerState) -> None:
        species = player_state.species_list[self.species_index]
        species.population += 1

    def verify_self(self: ExchangeForPopulation, player_state: PlayerState, food_card_index: Int,
                    card_plays_before_this: List[CardPlay]) -> Bool:
        return super(ExchangeForPopulation, self).verify_self(player_state, food_card_index, card_plays_before_this) \
               and player_state.validate_species_index(self.species_index, card_plays_before_this)

    def update_trait_counts(self: ExchangeForPopulation, species_trait_count: List[Int]) -> List[Int]:
        return species_trait_count


