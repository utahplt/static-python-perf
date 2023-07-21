from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS
from evolution.situation_flag import SituationFlag
from evolution.trait_cards.cards import TraitCard

__author__ = 'zeinamigeed'


class HerdingCard(TraitCard):
    def __init__(self, num_tokens_as_food_card: int = TRAIT_CARD_DEFAULT_FOOD_TOKENS) -> None:
        """
        :param num_tokens_as_food_card: The food tokens associated with this HerdingCard
        """
        super().__init__(num_tokens_as_food_card,
                           "Herding stops attacks from Carnivore species whose populations "
                           "are smaller or equal in size to this species population.")

    def blocks_attack(self,
                      defender,
                      attacker,
                      defenders_left_neighbor=None,
                      defenders_right_neighbor=None,
                      owner_flag=None):
        return owner_flag is SituationFlag.DEFENDER and \
               attacker.get_population(SituationFlag.ATTACKER) <= defender.get_population(SituationFlag.DEFENDER)

    def get_name(self):
        return "Herding"

    def __eq__(self, other):
        return isinstance(other, HerdingCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "HerdingCard({})".format(self.num_tokens_as_food_card)