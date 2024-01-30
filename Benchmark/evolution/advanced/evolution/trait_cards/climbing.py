from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS
from evolution.situation_flag import SituationFlag
from evolution.trait_cards.cards import TraitCard

__author__ = 'zeinamigeed'


class ClimbingCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this ClimbingCard
        :type num_tokens_as_food_card: int
        :return None
        """
        super().__init__(num_tokens_as_food_card,
                           "ClimbingCard prevents an attack unless the Carnivore"
                           " also has the ClimbingCard attribute.")

    def blocks_attack(self,
                      defender,
                      attacker,
                      defenders_left_neighbor=None,
                      defenders_right_neighbor=None,
                      owner_flag=None):
        return owner_flag is SituationFlag.DEFENDER and not attacker.has_trait(ClimbingCard)

    def get_name(self):
        return "Climbing"

    def __eq__(self, other):
        return isinstance(other, ClimbingCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "ClimbingCard({})".format(self.num_tokens_as_food_card)