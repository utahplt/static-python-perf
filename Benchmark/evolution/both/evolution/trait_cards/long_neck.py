from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS, LONG_NECK_ORDERING
from evolution.trait_cards.cards import TraitCard

__author__ = 'zeinamigeed'


class LongNeckCard(TraitCard):
    def __init__(self,
                 num_tokens_as_food_card: int = TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this LongNeckCard
        :type num_tokens_as_food_card: int
        :return: None
        """
        description = "Long Neck automatically adds one food token for the entire species when the food cards are " \
                      "revealed."
        super().__init__(num_tokens_as_food_card, description)

    def get_name(self):
        return "Long Neck"


    def get_on_feed_ordering(self):
        return LONG_NECK_ORDERING


    def apply_before_feeding(self, dealer, player_index, species_index):
        player_state = dealer.player_states[player_index]
        species = player_state.species_list[species_index]
        species.apply_feed(dealer, player_index, species_index)

    def __eq__(self, other):
        return isinstance(other, LongNeckCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "LongNeckCard({})".format(self.num_tokens_as_food_card)