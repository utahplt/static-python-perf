from cardplay import *
from evolution.data_defs import is_natural, is_list_of_nat
from evo_json.data_def import ConvertPyJSONError

def convert_step4(py_json):
    """
    Converts a step4 pyjson into a list of food
    cards indices and a sequence of lists of card plays
    :param py_json: step4
    :type py_json: PyJSON
    :return: [[[CardPlay, ...], ...], [Nat, ...]]
    """
    list_of_food_card_indices = []
    lolocp = []
    for i, action4 in enumerate(py_json):
        [card, locp] = convert_action4(action4)
        list_of_food_card_indices.append(card)
        lolocp.append(locp)

    return [list_of_food_card_indices, lolocp]


def convert_action4(action4):
    """
    Converts an action4 pyjson in to
    a card index and a list of cardplays
    :param action4: Every natural number in an Action4
    represent an index into a sequence of species
    boards or cards. The first natural number
    specifies the card that a player is turning into food.
    :type action4: PYJSON
    :return: [idx, locp] where idx is the index of the food card and locp is
    the list of CardPlays
    :rtype: [Nat, [CardPlay, ...]]
    """
    if not(isinstance(action4, list) and len(action4) == 5):
        raise ConvertPyJSONError("Cannot convert Action4")
    [card_index, logp, logb, lobt, lort] = action4

    exchange_for_species = [convert_bt(bt) for bt in lobt]
    exchange_pop = [convert_gp(gp) for gp in logp]
    exchange_body = [convert_gb(gb) for gb in logb]
    replace_cards = [convert_rt(rt) for rt in lort]

    return [card_index,
            exchange_for_species + exchange_pop + exchange_body + replace_cards]


def convert_new_action4(action4):
    """
    Converts an action4 pyjson in to
    a card index and a list of cardplays
    :param action4: Every natural number in an Action4
    represent an index into a sequence of species
    boards or cards. The first natural number
    specifies the card that a player is turning into food.
    :type action4: PYJSON
    :return: [idx, locp] where idx is the index of the food card and locp is
    the list of CardPlays
    :rtype: [Nat, [CardPlay, ...]]
    """
    if not(isinstance(action4, list) and len(action4) == 5):
        raise ConvertPyJSONError("Cannot convert Action4")
    [card_index, logp, logb, lobt, lort] = action4

    exchange_for_species = [convert_bt(bt) for bt in lobt]
    exchange_pop = [new_convert_gp(gp) for gp in logp]
    exchange_body = [new_convert_gb(gb) for gb in logb]
    replace_cards = [convert_rt(rt) for rt in lort]

    return [card_index,
            exchange_for_species + exchange_pop + exchange_body + replace_cards]

def convert_g(g, g_key, class_name):
    """
    Converts a gb or gp to a CardPlay
    :param g:gb or gp
    :type gp: PYJSON
    :param g_key: string representing key
    in PYJSON
    :type g_key: String
    :param class_name: constructor of cardplay
    :type class_name: Nat Nat -> CardPlay
    :return: the corresponding CardPlay
    :rtype: CardPlay
    """
    [key, species_index, card_index] = g
    if key != g_key:
        raise ConvertPyJSONError("Wrong key")

    if not (is_natural(species_index) and is_natural(card_index)):
        raise ConvertPyJSONError("expected a natural number")

    return class_name(card_index, species_index)

def new_convert_g(g, class_name):
    """
    Converts a gb or gp to a CardPlay
    :param g:gb or gp
    :type gp: PYJSON
    :param g_key: string representing key
    in PYJSON
    :type g_key: String
    :param class_name: constructor of cardplay
    :type class_name: Nat Nat -> CardPlay
    :return: the corresponding CardPlay
    :rtype: CardPlay
    """
    [species_index, card_index] = g
    if not (is_natural(species_index) and is_natural(card_index)):
        raise ConvertPyJSONError("expected a natural number")

    return class_name(card_index, species_index)

def convert_gp(gp):
    """
    Converts a gp to a CardPlay
    :param gp: A ["population",i,j] array requests
    a trade of card j for a growth of the population
    of species board i by one.
    :type gp: PYJSON
    :return: the corresponding CardPlay
    :rtype: CardPlay
    """
    return convert_g(gp, "population", ExchangeForPopulation)

def convert_gb(gb):
    """
    Converts a gb to a CardPlay
    :param gp: A ["body",i,j] array requests a
    trade of card j for a growth of the body of
    species board i by one.
    :type gp: PYJSON
    :return: the corresponding CardPlay
    :rtype: CardPlay
    """
    return convert_g(gb, "body", ExchangeForBodySize)


def new_convert_gp(gp):
    """
    Converts a gp to a CardPlay
    :param gp: A ["population",i,j] array requests
    a trade of card j for a growth of the population
    of species board i by one.
    :type gp: PYJSON
    :return: the corresponding CardPlay
    :rtype: CardPlay
    """
    return new_convert_g(gp, ExchangeForPopulation)

def new_convert_gb(gb):
    """
    Converts a gb to a CardPlay
    :param gp: A ["body",i,j] array requests a
    trade of card j for a growth of the body of
    species board i by one.
    :type gp: PYJSON
    :return: the corresponding CardPlay
    :rtype: CardPlay
    """
    return new_convert_g(gb, ExchangeForBodySize)


def convert_bt(bt):
    """
    Converts a bt to a CardPlay
    :param bt: A BT represents a species board
    addition to the right of the existing sequence
    of boards for the corresponding player.
    Specifically, [i, j, ..., k] uses the first of
    the player’s cards (i) to "pay" for the
    new board and uses the remaining (up to three)
    cards (j, ..., k) as traits.
    :type bt: PYJSON
    :return: CardPlay
    """
    if not is_list_of_nat(bt) and 1 <= len(bt) <= 4:
        raise ConvertPyJSONError('Expected a list of natural numbers')
    exchanged_card = bt[0]

    return ExchangeForSpecies(exchanged_card, bt[1:])

def convert_rt(rt):
    """
    Converts a rt to a CardPlay
    :param rt: An RT represents a trait replacement
    for a species board. Specifically, [b, i, j]
    specifies that board b’s i’s trait card is replaced
    with the j’s card from the player’s card sequence.
    :type rt: PYJSON
    :return: CardPlay
    """
    if not is_list_of_nat(rt) and len(rt) == 3:
        raise ConvertPyJSONError('Error decoding RT')
    [species_index, replaced_card_index , new_card_index] = rt
    return ReplaceCards(new_card_index, species_index, replaced_card_index)
