from evo_json.data_def import trait_dictionary

class Deck:
    """
    To represent a Deck of cards
    """
    def __init__(self, loc):
        """
        :param loc: List of cards
        :type loc: [TraitCards, ...]
        :return: None
        """
        self.loc = loc


    def get_n_cards(self, n):
        """
        Give the player n cards, if there are enough
        cards
        :param n: number of cards
        :type n: Nat
        :return: n cards
        :rtype: [TraitCard, ...]
        """
        loc = []
        for i in range(n):
            if self.has_next():
                loc.append(self.get_next())
        return loc


    def get_next(self):
        """
        Gets the next card in the deck
        :return: the next card
        :rtype: TraitCard
        """
        return self.loc.pop(0)

    def has_next(self):
        """
        Does this deck have anymore cards?
        :return: Returns true if there are more cards in the deck and false otherwise
        :rtype: Boolean
        """
        return len(self.loc) > 0

    @staticmethod
    def make_deck():
        """
        Creates a deck of cards
        :return: a deck of cards
        :rtype: Deck
        """
        deck_list = []
        for key in sorted(trait_dictionary):
            deck_list += (trait_dictionary[key].make_list_of_cards())
        return Deck(deck_list)

    def __eq__(self, other):
        if not isinstance(other, Deck):
            return False
        else:
            return self.loc == other.loc

    def __len__(self):
        return len(self.loc)