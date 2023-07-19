from evolution.constants import TRAIT_CARD_DEFAULT_FOOD_TOKENS, FAT_TISSUE_STARTING_FOOD
from evolution.trait_cards.cards import TraitCard

__author__ = 'Edwin Cowart, Kevin McDonough'


class FatTissueCard(TraitCard):
    def __init__(self,
                 num_tokens_as_food_card=TRAIT_CARD_DEFAULT_FOOD_TOKENS,
                 stored_food=FAT_TISSUE_STARTING_FOOD):
        """
        Construct a FatTissue Trait Card
        :param num_tokens_as_food_card: The number of food tokens associated with this FatTissueCard
        :type num_tokens_as_food_card: int
        :param stored_food: The food currently stored on the FatTissueCard from last round's storage
        :type stored_food: Nat
        :return: None
        """
        description = "Fat Tissue allows a species to store as many food tokens as its body-size count. In a " \
                      "physical game, the additional food is stored on the actual card. It must be used to feed the " \
                      "species at the beginning of the next evolution round, before any food is taken from the " \
                      "watering hole."
        super().__init__(num_tokens_as_food_card, description)
        self.stored_food = stored_food

    def store_food(self, stored_food, owner_body_size):
        """
        Adds the given number food tokens to this card's fat tissue, and returns the new number of tokens stored
        :param stored_food: number of food tokens to add
        :type stored_food: Nat
        :param owner_body_size: body size of the owning Species
        :type owner_body_size: Nat
        :return: the total number of food tokens stored
        :rtype: Nat
        """
        return self.add_stored_fat_food(self.stored_food + stored_food, owner_body_size)

    def take_food(self):
        """ Takes the food from this FatTissue card, returning the food stored and reducing the food stored to 0
        :return: the number of food tokens taken
        :rtype: Nat
        """
        num_tokens_taken = self.stored_food
        self.stored_food = FAT_TISSUE_STARTING_FOOD
        return num_tokens_taken

    def get_food_stored(self):
        """
        Gets the number of food tokens stored on this FatTissue card
        :return: the number of food tokens stored
        :rtype: Nat
        """
        return self.stored_food

    def add_stored_fat_food(self, stored_fat_food, owner_body_size):
        """ Set the stored fat food which is always GEN_TRAIT_CARD_STORED_FOOD for Non-FatTissueCards
        :param stored_fat_food: The amount of food you wish to store
        :type stored_fat_food: Nat
        :param owner_body_size: The owner's body size
        :type owner_body_size: Nat
        :return: The new self.food
        :rtype: Nat
        """
        TraitCard.add_stored_fat_food(self, stored_fat_food, owner_body_size)
        self.stored_food += stored_fat_food
        return self.stored_food

    def fat_tissue_need(self, owner_body_size):
        """ How many tokens of food can this TraitCard store?
        :param owner_body_size: body size of the owning Species
        :rtype Nat
        """
        return owner_body_size - self.stored_food

    def apply_before_feeding(self, dealer, player_index, species_index):
        player = dealer.player_states[player_index]
        species = player.species_list[species_index]
        food_transfered = min(species.how_hungry(), self.stored_food)
        species.num_food_tokens += food_transfered
        self.stored_food -= food_transfered



    def get_name(self):
        return "Fat Tissue"

    def __eq__(self, other):
        return isinstance(other, FatTissueCard) and other.stored_food == self.stored_food and \
               TraitCard.__eq__(self, other)

    def __repr__(self):
        return "FatTissueCard({}, {})".format(self.num_tokens_as_food_card, self.stored_food)