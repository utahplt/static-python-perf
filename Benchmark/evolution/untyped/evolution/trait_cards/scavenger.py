from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS
from evolution.trait_cards.cards import TraitCard

__author__ = 'zeinamigeed'


class ScavengerCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this ScavengerCard
        :type num_tokens_as_food_card: int
        :return None
        """
        description = "Scavenger automatically eats one food token every time a Carnivore eats another species."
        super().__init__(num_tokens_as_food_card, description)

    def get_name(self):
        return "Scavenger"

    def __eq__(self, other):
        return isinstance(other, ScavengerCard) and TraitCard.__eq__(self,
                                                                     other)

    def __repr__(self):
        return "ScavengerCard({})".format(self.num_tokens_as_food_card)