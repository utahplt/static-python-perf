from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS
from evolution.situation_flag import SituationFlag
from evolution.trait_cards.cards import TraitCard

__author__ = 'zeinamigeed'


class BurrowingCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this BurrowingCard
        :type num_tokens_as_food_card: int
        :return None
        """
        super().__init__(num_tokens_as_food_card, "BurrowingCard deflects an attack when its species has a food"
                                                          " supply equal to its population size.")

    def blocks_attack(self,
                      defender,
                      attacker,
                      defenders_left_neighbor=None,
                      defenders_right_neighbor=None,
                      owner_flag= None):
        return owner_flag is SituationFlag.DEFENDER and \
               defender.num_food_tokens == defender.get_population(SituationFlag.DEFENDER)

    def get_name(self):
        return "Burrowing"

    def __eq__(self, other):
        return isinstance(other, BurrowingCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "BurrowingCard({})".format(self.num_tokens_as_food_card)

