from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS
from evolution.situation_flag import SituationFlag
from evolution.trait_cards.cards import TraitCard

__author__ = 'zeinamigeed'


class SymbiosisCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this SymbiosisCard
        :type num_tokens_as_food_card: int
        :return: None
        """
        super().__init__(num_tokens_as_food_card,
                           "Symbiosis prevents an attack if this species has a neighbor to "
                           "the right whose body size is larger than this ones.")

    def blocks_attack(self,
                      defender,
                      attacker,
                      defenders_left_neighbor=None,
                      defenders_right_neighbor=None,
                      owner_flag=None):
        return owner_flag is SituationFlag.DEFENDER and \
               defenders_right_neighbor is not None and \
               (defender.get_body_size(SituationFlag.DEFENDER)
                < defenders_right_neighbor.get_body_size(SituationFlag.DEFENDER_R_NEIGHBOR))


    def get_name(self):
        return "Symbiosis"

    def __eq__(self, other):
        return isinstance(other, SymbiosisCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "SymbiosisCard({})".format(self.num_tokens_as_food_card)