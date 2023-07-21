from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS, FORAGING_FEED_ORDERING
from evolution.trait_cards.cards import TraitCard

__author__ = 'zeinamigeed'


class ForagingCard(TraitCard):
    def __init__(self, num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS):
        """
        :param num_tokens_as_food_card: The food tokens associated with this ForagingCard
        :type num_tokens_as_food_card: int
        :return: None
        """
        description = "Foraging enables this species to eat two tokens of food for every evolution."
        super().__init__(num_tokens_as_food_card, description)

    def on_feed(self, dealer, player_index, species_index):
        player_state = dealer.player_states[player_index]
        feeding_species = player_state.species_list[species_index]
        return feeding_species.apply_feed(dealer, player_index, species_index, [self])

    def get_on_feed_ordering(self):
        return FORAGING_FEED_ORDERING


    def get_name(self):
        return "Foraging"

    def __eq__(self, other):
        return isinstance(other, ForagingCard) and TraitCard.__eq__(self, other)

    def __repr__(self):
        return "ForagingCard({})".format(self.num_tokens_as_food_card)