from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS, COOP_FEED_ORDERING
from evolution.trait_cards.cards import TraitCard

__author__ = 'zeinamigeed'


class CooperationCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this CooperationCard
        :type num_tokens_as_food_card: int
        :return: None
        """
        description = "CooperationCard automatically feeds the species to its right one token of food every time it " \
                      "eats (taken from the common food supply at the watering hole)."
        super().__init__(num_tokens_as_food_card, description)

    def on_feed(self, dealer, player_index, species_index):
        species_list = dealer.player_states[player_index].species_list
        feeder_right_neighbor = species_list[species_index+1] if species_index+1 < len(species_list) else None
        if feeder_right_neighbor:
            return feeder_right_neighbor.apply_feed(dealer, player_index, species_index+1)

    def get_name(self):
        return "Cooperation"

    def get_on_feed_ordering(self):
        return COOP_FEED_ORDERING


    def __eq__(self, other):
        return isinstance(other, CooperationCard) and TraitCard.__eq__(self,
                                                                       other)

    def __repr__(self):
        return "CooperationCard({})".format(self.num_tokens_as_food_card)