__author__ = 'Edwin Cowart, Kevin McDonough'
from evolution.Species import Species
from evolution.species_types import is_extant_carnivore


class Situation:

    def __init__(self, defender, attacker, defender_left_neighbor=None, defender_right_neighbor=None):
        """
        Construct a Situation
        :param defender: The defender in the Situation
        :type defender: Species
        :param attacker: The attacker in the Situation
        :type attacker: Species
        :param defender_left_neighbor: The left neighbor of the defender
        :type defender_left_neighbor: Species or None
        :param defender_right_neighbor: The right neighbor of the defender
        :type defender_right_neighbor: Species or None
        :return: None
        """
        if not Species.is_extant_species(defender):
            raise ValueError("Situation - __init__: Invalid Extant Species as defender")
        elif not is_extant_carnivore(attacker):
            raise ValueError("Situation - __init__: Invalid Extant Carnivore as attacker")
        elif not Species.is_opt_extant_species(defender_left_neighbor):
            raise ValueError("Situation - __init__: Invalid Optional Extant Species as defender_left_neighbor")
        elif not Species.is_opt_extant_species(defender_right_neighbor):
            raise ValueError("Situation - __init__: Invalid Optional Extant Species as defender_right_neighbor")

        self.defender = defender                               # type: Species
        self.attacker = attacker                               # type: Carnivore
        self.defender_left_neighbor = defender_left_neighbor   # type: Optional[Species]
        self.defender_right_neighbor = defender_right_neighbor # type: Optional[Species]


    def is_defender_attackable(self):
        """
        Is the Situation defender attackable by attacker given the defender's neighbors?
        :return: True if the defender is attackable, False otherwise
        :rtype: bool
        """
        return self.defender.is_attackable(self.attacker, self.defender_left_neighbor, self.defender_right_neighbor)


