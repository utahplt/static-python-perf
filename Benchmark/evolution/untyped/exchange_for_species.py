from cardplay import CardPlay
from evolution.species import Species # we may need a file from "both" directory

class ExchangeForSpecies(CardPlay):
    """
    Represents exchanging cards for more species
    """

    def __init__(self, played_card_index, loi):
        """
        :param played_card_index: index of the card
        :type played_card_index: Nat
        :param loi: the indices of the trait cards to put on the
        species
        :type loi: [Nat, ...]

        behavioral contract:
        len(loc) <= 3

        """
        super().__init__(played_card_index)
        self.loi = loi

    def apply(self, player_state):
        traits = [player_state.hand[i] for i in self.loi]
        new_species = Species(played_cards=traits)
        player_state.species_list.append(new_species)

    def get_card_indices(self):
        indices = super(ExchangeForSpecies, self).get_card_indices() + self.loi
        return indices

    def verify_self(self, player_state, food_card_index, card_plays_before_this):
        verify_rest = super(ExchangeForSpecies, self).verify_self(player_state, food_card_index, card_plays_before_this)
        verify_loi = player_state.validate_trait_cards_indicies(self.loi)

        return verify_loi and verify_rest

    def num_species_created(self):
        return 1

    def update_trait_counts(self, species_trait_count):
        species_trait_count.append(len(self.loi))
        return species_trait_count