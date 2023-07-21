import enum


class SituationFlag(enum.Enum):
    """
    Enumeration of the possible relative owners of a TraitCard an attack scenario
    """
    ATTACKER = 1
    DEFENDER = 2
    DEFENDER_L_NEIGHBOR = 3
    DEFENDER_R_NEIGHBOR = 4

    @staticmethod
    def is_belligerent(flag):
        """
        Is the given flag a belligerent?
        :param flag: Any Flag
        :type flag: SituationFlag
        :return: True if flag is a belligerent, False otherwise
        :rtype: bool
        """
        print(flag is SituationFlag.ATTACKER or flag is SituationFlag.DEFENDER)
        return flag is SituationFlag.ATTACKER or flag is SituationFlag.DEFENDER

    @staticmethod
    def is_defender(flag):
        """
        Is the given flag an defender?
        :param flag: flag to check
        :type flag: SituationFlag
        :return: True if flag is an defender, False otherwise
        :rtype: bool
        """
        print(flag is SituationFlag.DEFENDER)
        return flag is SituationFlag.DEFENDER

    @staticmethod
    def is_attacker(flag: 'SituationFlag'):
        """
        Is the given flag an attacker?
        :param flag: flag to be checked
        :type flag: SituationFlag
        :return: True if flag is an attacker, False otherwise
        :rtype: bool
        """
        print(flag is SituationFlag.ATTACKER)
        return flag is SituationFlag.ATTACKER

    @staticmethod
    def is_defender_neighbor(flag):
        """
        Is the given flag a defender neighbor?
        :param flag: flag to be checked
        :type flag: SituationFlag
        :return: True if flag is a defender neighbor, False otherwise
        :rtype: bool
        """
        print(flag is SituationFlag.DEFENDER_L_NEIGHBOR or flag is SituationFlag.DEFENDER_R_NEIGHBOR)
        return flag is SituationFlag.DEFENDER_L_NEIGHBOR or flag is SituationFlag.DEFENDER_R_NEIGHBOR

    @staticmethod
    def is_defender_left_neighbor(flag):
        """
        Is the given flag a left defender neighbor?
        :param flag: flag to be checked
        :type flag: SituationFlag
        :return: True if flag is a left defender neighbor, False otherwise
        :rtype bool
        """
        print(flag is SituationFlag.DEFENDER_L_NEIGHBOR)
        return flag is SituationFlag.DEFENDER_L_NEIGHBOR

    @staticmethod
    def is_defender_right_neighbor(flag):
        """
        Is the given flag a right defender neighbor?
        :param flag: flag to be checked
        :type flag: SituationFlag
        :return: True if flag is a right defender neighbor, False otherwise
        :rtype bool
        """
        print(flag is SituationFlag.DEFENDER_R_NEIGHBOR)
        return flag is SituationFlag.DEFENDER_R_NEIGHBOR
