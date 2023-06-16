from cardplay import CardPlay
class ExchangeForPopulation(CardPlay):
    """
    Represents exchanging cards for Population
    """

    def __init__(self, played_card_index, species_index):
        """
        :param played_card_index: index of the card
        :type played_card_index: Nat
        :param species_index: index of the species to change
        :type species_index: Nat
        """
        super().__init__(played_card_index)
        self.species_index = species_index

    def apply(self, player_state):
        species = player_state.species_list[self.species_index]
        species.population += 1

    def verify_self(self, player_state, food_card_index, card_plays_before_this):
        return super(ExchangeForPopulation, self).verify_self(player_state, food_card_index, card_plays_before_this)\
        and player_state.validate_species_index(self.species_index, card_plays_before_this)

    def update_trait_counts(self, species_trait_count):
        return species_trait_count


