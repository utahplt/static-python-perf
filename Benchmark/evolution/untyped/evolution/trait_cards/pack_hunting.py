from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS
from evolution.situation_flag import SituationFlag
from evolution.trait_cards.cards import TraitCard

__author__ = 'Edwin Cowart, Kevin McDonough'


class PackHuntingCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this PackHuntingCard
        :type num_tokens_as_food_card: int
        :return: None
        """
        description = "Pack Hunting adds this species population size to its body size for " \
                      "attacks on other species."
        super().__init__(num_tokens_as_food_card, description)

    def mod_owner_body_size(self,
                            owner,
                            owner_current_body_size,
                            owner_flag=None):
        """ Modify the owner Species' body_size
        :param owner: The owner Species
        :type owner: Species
        :param owner_current_body_size: The owner's current body_size
        :type owner_current_body_size: Nat
        :param owner_flag: The owner's situation flag
        :type owner_flag: SituationFlag or None
        :return: The Modified Body Size of the Owner
        :rtype: Nat
        """
        if SituationFlag.is_attacker(owner_flag):
            return owner_current_body_size + owner.get_population(owner_flag)
        else:
            return owner_current_body_size

    def get_name(self):
        return "Pack Hunting"

    def __eq__(self, other):
        return isinstance(other, PackHuntingCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "PackHuntingCard({})".format(self.num_tokens_as_food_card)