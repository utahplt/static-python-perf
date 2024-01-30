from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS, CARNIVORE_MIN_FOOD_TOKENS, CARNIVORE_MAX_FOOD_TOKENS
from evolution.data_defs import is_int_in_inclusive_range
from evolution.trait_cards.cards import TraitCard

__author__ = 'Edwin Cowart, Kevin McDonough'


class CarnivoreCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this CarnivoreCard
        :type num_tokens_as_food_card: int
        :return: None
        """
        super().__init__(num_tokens_as_food_card, "CarnivoreCard must attack to eat during the evolution stage.")

    def set_num_tokens_as_food_card(self, num_tokens_as_food_card):
        """ Set the Number of Food Tokens
        :param num_tokens_as_food_card: The new number_of_tokens
        :type num_tokens_as_food_card: int
        :return: None
        :raise: ValueError if sent invalid value
        """
        if not is_int_in_inclusive_range(num_tokens_as_food_card, CARNIVORE_MIN_FOOD_TOKENS, CARNIVORE_MAX_FOOD_TOKENS):
            raise ValueError(self.__class__.__name__ + " - set_number_of_food_tokens: Number of Food Tokens must be " +
                             "in range [" + str(CARNIVORE_MIN_FOOD_TOKENS) + ", " + str(CARNIVORE_MAX_FOOD_TOKENS) +
                             "]")
        self.num_tokens_as_food_card = num_tokens_as_food_card

    def get_name(self):
        return "Carnivore"

    @classmethod
    def get_min(cls):
        return CARNIVORE_MIN_FOOD_TOKENS

    @classmethod
    def get_max(cls):
        return CARNIVORE_MAX_FOOD_TOKENS

    def __eq__(self, other):
        return isinstance(other, CarnivoreCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "CarnivoreCard({})".format(self.num_tokens_as_food_card)