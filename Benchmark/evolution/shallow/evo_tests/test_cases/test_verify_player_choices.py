import unittest
from evo_tests.examples import ExamplePlayerStates
from cardplay import *
from evolution.player.player_feeding_choice import *

class TestTraitCards(unittest.TestCase):
    def setUp(self):
        self.ex_player_states = ExamplePlayerStates()

    def test_verify_card_choices(self):
        ps = self.ex_player_states.step4_2_p2
        ps2 = self.ex_player_states.step4_2_p3
        assert ps.verify_card_choices((0, [ExchangeForBodySize(1, 0)]))
        assert ps2.verify_card_choices((0, [ExchangeForSpecies(1, [2])]))
        assert ps2.verify_card_choices((0, [ExchangeForPopulation(1, 0)]))

        assert not ps.verify_card_choices((0, [ExchangeForSpecies(0, [0])]))
        assert not ps.verify_card_choices((1, [ExchangeForSpecies(10, [1, 1, 1])]))
        assert not ps.verify_card_choices((1, [ExchangeForPopulation(0, 1), ExchangeForPopulation(0, 1)]))
        assert not ps.verify_card_choices((1, [ExchangeForSpecies(0, [1, 1]), ExchangeForPopulation(0, 1)]))
        assert not ps.verify_card_choices((1, [ExchangeForBodySize(0, 1), ExchangeForPopulation(0, 1)]))

    def test_verify_feed_choices(self):
        ps1 = self.ex_player_states.fat5
        ps2 = self.ex_player_states.fat3
        ps3 = self.ex_player_states.burr_veg
        ps4 = self.ex_player_states.carn
        ps5 = self.ex_player_states.norm

        assert PlayerFeedVegetarian(0).verify_self([ps4, ps3], ps5)
        assert PlayerStoreFat(0, 1).verify_self([], ps1)
        assert PlayerAttackWithCarnivore(0, 0, 0).verify_self([ps2], ps4)
        assert not PlayerFeedVegetarian(0).verify_self([ps2], ps3)
        assert not PlayerStoreFat(0, 100).verify_self([ps3], ps2)
        assert not PlayerStoreFat(100, 1).verify_self([ps3], ps2)
        assert not PlayerAttackWithCarnivore(0, 0, 1).verify_self([ps2], ps4)
        assert not PlayerAttackWithCarnivore(10, 0, 20).verify_self([ps2], ps4)

if __name__ == '__main__':
    main()
