from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS, FERTILE_POP_INC, FERTILE_ORDERING, SPECIES_MAX_POP
from evolution.trait_cards.cards import TraitCard

__author__ = 'Edwin Cowart, Kevin McDonough'


class FertileCard(TraitCard):

    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this FertileCard
        :type num_tokens_as_food_card: int
        :return: None
        """
        description = "FertileCard automatically adds one animal to the population when the food cards are revealed."
        super().__init__(num_tokens_as_food_card, description)

    def apply_before_feeding(self, dealer, player_index, species_index):
        player_state = dealer.player_states[player_index]
        species = player_state.species_list[species_index]
        species.population = min(species.population + FERTILE_POP_INC, SPECIES_MAX_POP)

    def get_name(self):
        return "Fertile Card"


    def get_on_feed_ordering(self):
        return FERTILE_ORDERING

    def __eq__(self, other):
        return isinstance(other, FertileCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "FertileCard({})".format(self.num_tokens_as_food_card)