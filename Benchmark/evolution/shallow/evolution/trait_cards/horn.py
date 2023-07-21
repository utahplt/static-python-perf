from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS
from evolution.trait_cards.cards import TraitCard

__author__ = 'Edwin Cowart, Kevin McDonough'


class HornCard(TraitCard):

    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this HornCard
        :type num_tokens_as_food_card: int
        :return: None
        """
        description = "Horns kills one animal of an attacking CarnivoreCard species before the attack is completed."
        super().__init__(num_tokens_as_food_card, description)

    def get_name(self):
        return "Horns"

    def __eq__(self, other):
        return isinstance(other, HornCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "HornCard({})".format(self.num_tokens_as_food_card)