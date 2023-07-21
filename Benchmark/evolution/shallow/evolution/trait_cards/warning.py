from evolution.trait_cards.ambush import AmbushCard
import evolution.trait_cards.cards
from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS
from evolution.situation_flag import SituationFlag
from evolution.trait_cards.cards import TraitCard

__author__ = 'Edwin Cowart, Kevin McDonough'


class WarningCallCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this WarningCallCard
        :type num_tokens_as_food_card: int
        :return None
        """
        super().__init__(num_tokens_as_food_card,
                                                       "Warning Call prevents an attack from a Carnivore on Rest "
                                                       "neighboring species unless the attacker has the AmbushCard "
                                                       "property.")

    def blocks_attack(self,
                      defender,
                      attacker,
                      defenders_left_neighbor=None,
                      defenders_right_neighbor=None,
                      owner_flag=None):
        return SituationFlag.is_defender_neighbor(owner_flag) and not attacker.has_trait(AmbushCard)

    def get_name(self):
        return "Warning"

    def __eq__(self, other):
        return isinstance(other, WarningCallCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "WarningCallCard({})".format(self.num_tokens_as_food_card)
