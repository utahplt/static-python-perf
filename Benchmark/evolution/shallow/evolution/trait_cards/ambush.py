from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS
from evolution.trait_cards.cards import TraitCard

__author__ = 'zeinamigeed'


class AmbushCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this AmbushCard
        :type num_tokens_as_food_card: int
        :return: None
        """
        super().__init__(num_tokens_as_food_card, "AmbushCard overcomes a Warning Call during an evolution.")

    def get_name(self):
        return "Ambush"

    def __eq__(self, other):
        return isinstance(other, AmbushCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "AmbushCard({})".format(self.num_tokens_as_food_card)


