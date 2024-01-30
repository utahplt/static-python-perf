eq_comparator = lambda value_x, value_y: (value_x == value_y)
is_comparator = lambda value_x, value_y: (value_x is value_y)
type_comparator = lambda type_x, type_y: (type(type_x) is type(type_y))
of_type_comparator = lambda value_x, type_y: (type(value_x) is type_y)


def any_duplicates(list_a, equality_comparator=eq_comparator):
    """ Are their any duplicates in the given list where they equal according to the comparator
    :param list_a: The list being checked for duplicates
    :type list_a: [Any, ...]
    :param equality_comparator: The equality comparator which determines duplicates
    :type equality_comparator: Any, Any -> bool
    :return: True if any duplicates were found, False otherwise
    :rtype: bool
    """
    return any(any(equality_comparator(t_elem, list_a[j])
                   for j in range(i + 1, len(list_a)))
               for i, t_elem in enumerate(list_a))


def does_list_contain(list_a, value, equality_comparator=eq_comparator):
    """ Does the given list contain the given value according to the comparator
    :param list_a: The list being checked
    :type list_a: [Any, ...]
    :param value: The value being checked
    :type value: Any
    :param equality_comparator: The equality comparator
    :type equality_comparator: Any, Any -> bool
    :return: True if the list does contain, False otherwise
    :rtype: bool
    """
    return any(equality_comparator(t_elem, value) for t_elem in list_a)

def for_all_species(player_states, function):
    """
    Apply the given function to all the species in all the player states
    :param player_states: Player states whose species will have the function applied to
    :type player_states: [PlayerState, ...]
    :param function: Method to be called on each species (and the relevant context
    :type function: Species Nat PlayerState Nat [PlayserState, ...] -> X
    :return: None
    """
    for player_i, player_state in enumerate(player_states):
        species_list = player_state.species_list
        for species_i, species in enumerate(species_list):
            function(species, species_i, player_state, player_i, player_states)