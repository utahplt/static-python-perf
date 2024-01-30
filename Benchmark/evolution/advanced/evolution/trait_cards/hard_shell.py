from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS, HARD_SHELL_OFFSET
from evolution.situation_flag import SituationFlag
from evolution.trait_cards.cards import TraitCard

__author__ = 'zeinamigeed'


class HardShellCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this HardShellCard
        :type num_tokens_as_food_card: int
        :return: None
        """
        super().__init__(num_tokens_as_food_card,
                           "Hard Shell prevents an attack unless the attacker is "
                           "at least 4 units larger than this species in body size.")

    def blocks_attack(self,
                      defender,
                      attacker,
                      defenders_left_neighbor=None,
                      defenders_right_neighbor=None,
                      owner_flag=None):
        return owner_flag is SituationFlag.DEFENDER and \
               ((attacker.get_body_size(SituationFlag.ATTACKER) - defender.get_body_size(SituationFlag.DEFENDER))
                < HARD_SHELL_OFFSET)

    def get_name(self):
        return "Hard Shell"

    def __eq__(self, other):
        return isinstance(other, HardShellCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "HardShellCard({})".format(self.num_tokens_as_food_card)