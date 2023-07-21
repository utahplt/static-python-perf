__author__ = 'Edwin Cowart, Kevin McDonough'

import unittest
from evolution.situation_flag import *

class TestSituationFlag(unittest.TestCase):
    def test_situation_flag(self):
        self.assertFalse(SituationFlag.ATTACKER is SituationFlag.DEFENDER)
        self.assertTrue(SituationFlag.ATTACKER is SituationFlag.ATTACKER)
        self.assertFalse(SituationFlag.ATTACKER is SituationFlag.DEFENDER_L_NEIGHBOR)
        self.assertFalse(SituationFlag.ATTACKER is SituationFlag.DEFENDER_R_NEIGHBOR)

        self.assertTrue(SituationFlag.DEFENDER is SituationFlag.DEFENDER)
        self.assertFalse(SituationFlag.DEFENDER is SituationFlag.ATTACKER)
        self.assertFalse(SituationFlag.DEFENDER is SituationFlag.DEFENDER_L_NEIGHBOR)
        self.assertFalse(SituationFlag.DEFENDER is SituationFlag.DEFENDER_R_NEIGHBOR)

        self.assertFalse(SituationFlag.DEFENDER_L_NEIGHBOR is SituationFlag.DEFENDER)
        self.assertFalse(SituationFlag.DEFENDER_L_NEIGHBOR is SituationFlag.ATTACKER)
        self.assertTrue(SituationFlag.DEFENDER_L_NEIGHBOR is SituationFlag.DEFENDER_L_NEIGHBOR)
        self.assertFalse(SituationFlag.DEFENDER_L_NEIGHBOR is SituationFlag.DEFENDER_R_NEIGHBOR)

        self.assertFalse(SituationFlag.DEFENDER_R_NEIGHBOR is SituationFlag.DEFENDER)
        self.assertFalse(SituationFlag.DEFENDER_R_NEIGHBOR is SituationFlag.ATTACKER)
        self.assertFalse(SituationFlag.DEFENDER_R_NEIGHBOR is SituationFlag.DEFENDER_L_NEIGHBOR)
        self.assertTrue(SituationFlag.DEFENDER_R_NEIGHBOR is SituationFlag.DEFENDER_R_NEIGHBOR)

    def test_is_belligerent(self):
        self.assertTrue(SituationFlag.is_belligerent(SituationFlag.DEFENDER))
        self.assertTrue(SituationFlag.is_belligerent(SituationFlag.ATTACKER))
        self.assertFalse(SituationFlag.is_belligerent(SituationFlag.DEFENDER_L_NEIGHBOR))
        self.assertFalse(SituationFlag.is_belligerent(SituationFlag.DEFENDER_R_NEIGHBOR))

    def test_is_defender(self):
        self.assertTrue(SituationFlag.is_defender(SituationFlag.DEFENDER))
        self.assertFalse(SituationFlag.is_defender(SituationFlag.ATTACKER))
        self.assertFalse(SituationFlag.is_defender(SituationFlag.DEFENDER_L_NEIGHBOR))
        self.assertFalse(SituationFlag.is_defender(SituationFlag.DEFENDER_R_NEIGHBOR))

    def test_is_attacker(self):
        self.assertFalse(SituationFlag.is_attacker(SituationFlag.DEFENDER))
        self.assertTrue(SituationFlag.is_attacker(SituationFlag.ATTACKER))
        self.assertFalse(SituationFlag.is_attacker(SituationFlag.DEFENDER_L_NEIGHBOR))
        self.assertFalse(SituationFlag.is_attacker(SituationFlag.DEFENDER_R_NEIGHBOR))

    def test_is_defender_neighbor(self):
        self.assertFalse(SituationFlag.is_defender_neighbor(SituationFlag.DEFENDER))
        self.assertFalse(SituationFlag.is_defender_neighbor(SituationFlag.ATTACKER))
        self.assertTrue(SituationFlag.is_defender_neighbor(SituationFlag.DEFENDER_L_NEIGHBOR))
        self.assertTrue(SituationFlag.is_defender_neighbor(SituationFlag.DEFENDER_R_NEIGHBOR))

    def test_is_defender_l_neighbor(self):
        self.assertFalse(SituationFlag.is_defender_left_neighbor(SituationFlag.DEFENDER))
        self.assertFalse(SituationFlag.is_defender_left_neighbor(SituationFlag.ATTACKER))
        self.assertTrue(SituationFlag.is_defender_left_neighbor(SituationFlag.DEFENDER_L_NEIGHBOR))
        self.assertFalse(SituationFlag.is_defender_left_neighbor(SituationFlag.DEFENDER_R_NEIGHBOR))

    def test_is_defender_r_neighbor(self):
        self.assertFalse(SituationFlag.is_defender_right_neighbor(SituationFlag.DEFENDER))
        self.assertFalse(SituationFlag.is_defender_right_neighbor(SituationFlag.ATTACKER))
        self.assertFalse(SituationFlag.is_defender_right_neighbor(SituationFlag.DEFENDER_L_NEIGHBOR))
        self.assertTrue(SituationFlag.is_defender_right_neighbor(SituationFlag.DEFENDER_R_NEIGHBOR))


if __name__ == '__main__':
    unittest.main()
