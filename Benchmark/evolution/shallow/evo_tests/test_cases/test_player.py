__author__ = 'Edwin Cowart, Kevin McDonough'

import unittest

from evo_tests.examples import *
from evolution.player.player_feeding_choice import *
from cardplay import *



class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.ex_player_states = ExamplePlayerStates()
        self.ex_species = ExampleSpecies()
        self.player = Player()

    def test_choose_fat_veg_carn(self):
        # Choosing Fat Species before Vegetarian
        player_fat_veg = self.ex_player_states.burr_and_fat
        self.assertEqual(self.player.choose_feeding(1, [self.ex_player_states.burr_veg,
                                                        self.ex_player_states.carn_fat,
                                                        self.ex_player_states.fora],
                                                    player_fat_veg),
                         PlayerStoreFat(1, 1))

        # Choosing Fat Species before Carnivore
        player_fat_carn = self.ex_player_states.carn_coop_and_fat
        self.assertEqual(self.player.choose_feeding(2, [self.ex_player_states.burr_veg,
                                                        self.ex_player_states.carn_fat,
                                                        self.ex_player_states.fora],
                                                    player_fat_carn),
                         PlayerStoreFat(1, 2))

        # Choosing Fat Species before Carnivore and before Full Fat
        player_carn_fat_fat = self.ex_player_states.carn_coop_and_fat_and_fat
        self.assertEqual(self.player.choose_feeding(10, [self.ex_player_states.burr_veg,
                                                         self.ex_player_states.carn_fat,
                                                         self.ex_player_states.fora],
                                                    player_carn_fat_fat),
                         PlayerStoreFat(2, SPECIES_MAX_BODY_SIZE))

        # Choosing Fat Species before Carnivore and Vegetarian
        player_fat_carn_veg = self.ex_player_states.fat_and_carn_and_shell_veg
        self.assertEqual(self.player.choose_feeding(10, [self.ex_player_states.burr_veg,
                                                         self.ex_player_states.carn_fat,
                                                         self.ex_player_states.fora],
                                                    player_fat_carn_veg),
                         PlayerStoreFat(1, SPECIES_MAX_BODY_SIZE))

        # Choosing Vegetarian before Carnivore
        player_carn_veg = self.ex_player_states.carn_coop_and_warn
        self.assertEqual(self.player.choose_feeding(6, [self.ex_player_states.burr_veg,
                                                        self.ex_player_states.carn_fat,
                                                        self.ex_player_states.fora],
                                                    player_carn_veg),
                         PlayerFeedVegetarian(1))

    def test_fat_ordering(self):
        # Test that the species with more fat tissue space is picked  5 - 3 > 6 - 5
        player_diff_fat_space = IPlayer(Player(), 1, [self.ex_species.fat5_fed1_b6,
                                                          self.ex_species.fat3_fed2_b5])
        self.assertEqual(self.player.choose_feeding(3, [self.ex_player_states.carn], player_diff_fat_space),
                         PlayerStoreFat(1, 2))

        # Choose the Fat Species with the greater Population
        player_diff_fat_pop = IPlayer(Player(), 1, [self.ex_species.fat3_bd4_popmax_food1,
                                                        self.ex_species.fat3_bd4_pop4_food1])
        self.assertEqual(self.player.choose_feeding(1, [self.ex_player_states.burr_veg,
                                                        self.ex_player_states.carn_fat,
                                                        self.ex_player_states.fora],
                                                    player_diff_fat_pop),
                         PlayerStoreFat(0, 1))

        # Choose the Fat Species with the greater food already fed
        player_diff_fat_food = IPlayer(Player(), 1, [self.ex_species.fat3_bd4_pop4_food1,
                                                         self.ex_species.fat3_bd4_pop4_food3])
        self.assertEqual(self.player.choose_feeding(1, [self.ex_player_states.burr_veg,
                                                        self.ex_player_states.carn_fat,
                                                        self.ex_player_states.fora],
                                                    player_diff_fat_food),
                         PlayerStoreFat(1, 1))

        # Choose the Fat Species with the greater body size
        player_diff_fat_body = IPlayer(Player(), 1, [self.ex_species.fat5_bd6_popmax_food1,
                                                         self.ex_species.fat3_bd4_popmax_food1])
        self.assertEqual(self.player.choose_feeding(1, [self.ex_player_states.burr_veg,
                                                        self.ex_player_states.carn_fat,
                                                        self.ex_player_states.fora],
                                                    player_diff_fat_body),
                         PlayerStoreFat(0, 1))

        # If species are identical, choose the first one
        player_fat_identical = IPlayer(Player(), 1, [self.ex_species.fat3_fed2_b5,
                                                         self.ex_species.fat3_fed2_b5])
        self.assertEqual(self.player.choose_feeding(2, [self.ex_player_states.default],
                                                    player_fat_identical),
                         PlayerStoreFat(0, 2))

    def test_choose_veg(self):
        # Choose the vegetarian with the largest population
        player_veg_diff_pop = IPlayer(Player(), 1, [self.ex_species.norm_pstart2, self.ex_species.norm_bstart3])
        self.assertEqual(self.player.choose_feeding(2, [self.ex_player_states.default],
                                                    player_veg_diff_pop),
                         PlayerFeedVegetarian(0))

        # With same population, choose the vegetarian with the largest number of food tokens
        player_veg_diff_food = IPlayer(Player(), 2, [self.ex_species.norm_fed1_p2,
                                                         self.ex_species.norm_fed3_p4])
        self.assertEqual(self.player.choose_feeding(2, [self.ex_player_states.default],
                                                    player_veg_diff_food),
                         PlayerFeedVegetarian(1))

        # With same population and food tokens, choose the vegetarian with the largest body size
        player_veg_diff_body_size = IPlayer(Player(), 3, [self.ex_species.norm_bstart3,
                                                              self.ex_species.norm_bstart4])
        self.assertEqual(self.player.choose_feeding(2, [self.ex_player_states.default],
                                                    player_veg_diff_body_size),
                         PlayerFeedVegetarian(1))

        # With identical vegetarians, choose the first one
        player_veg_identical = IPlayer(Player(), 4, [self.ex_species.norm_default,
                                                         self.ex_species.norm_default])
        self.assertEqual(self.player.choose_feeding(2, [self.ex_player_states.default],
                                                    player_veg_identical),
                         PlayerFeedVegetarian(0))

    def test_choose_carn(self):
        # If all carnivores can attack, largest is picked to attack only target
        player_card_order_varied = IPlayer(Player(), 1, [self.ex_species.carn_pstart1,
                                                             self.ex_species.carn_default,
                                                             self.ex_species.carn_pstart1_bstart3])
        self.assertEqual(self.player.choose_feeding(3, [self.ex_player_states.carn],
                                                    player_card_order_varied),
                         PlayerAttackWithCarnivore(2, 0, 0))

        # If 2 carnivores come in same place in order, pick first in list
        player_carn_order_match = IPlayer(Player(), 2, [self.ex_species.carn_pstart1,
                                                            self.ex_species.carn_default,
                                                            self.ex_species.carn_pstart1])
        self.assertEqual(self.player.choose_feeding(3, [self.ex_player_states.carn],
                                                    player_carn_order_match),
                         PlayerAttackWithCarnivore(0, 0, 0))

        # If some can't attack, pick largest that can attack
        player_carn_can_attack = IPlayer(Player(), 3, [self.ex_species.carn_pstart1_bstart3,
                                                           self.ex_species.carnamb_default,
                                                           self.ex_species.carnamb_pstart2])
        player_double_warn = IPlayer(Player(), 4, [self.ex_species.warn_default,
                                                       self.ex_species.warn_default2])
        self.assertEqual(self.player.choose_feeding(3, [player_double_warn],
                                                    player_carn_can_attack),
                         PlayerAttackWithCarnivore(2, 0, 0))

        # Make sure the carnivore attacks the largest of the attackable species
        player_carn_basic = IPlayer(Player(), 5, [self.ex_species.carn_default])
        player_some_warned = IPlayer(Player(), 6, [self.ex_species.warn_default,
                                                       self.ex_species.norm_pstart2,
                                                       self.ex_species.norm_bstart3])
        self.assertEqual(self.player.choose_feeding(3, [player_some_warned],
                                                    player_carn_basic),
                         PlayerAttackWithCarnivore(0, 0, 2))

        # If two species could equally be chosen, favor earlier player
        self.assertEqual(self.player.choose_feeding(3, [self.ex_player_states.fat_default,
                                                        self.ex_player_states.carn],
                                                    player_carn_basic),
                         PlayerAttackWithCarnivore(0, 0, 0))

        # Within player, with two equal species, attacks first
        player_equiv_defs = IPlayer(Player(), 7, [self.ex_species.norm_default,
                                                      self.ex_species.carn_default])
        self.assertEqual(self.player.choose_feeding(3, [player_equiv_defs],
                                                    player_carn_basic),
                         PlayerAttackWithCarnivore(0, 0, 0))

        # Test the new index result instead of id
        player_equiv_defs = IPlayer(Player(), 8, [self.ex_species.carn_default])
        self.assertEqual(self.player.choose_feeding(3, [self.ex_player_states.burr_veg,
                                                        self.ex_player_states.carn,
                                                        self.ex_player_states.carn,
                                                        self.ex_player_states.player_state_with_4],
                                                    player_equiv_defs),
                         PlayerAttackWithCarnivore(0, 3, 3))

    def test_get_card_choices_json_1(self):
        silly_player = Player()
        silly_player.start(self.ex_player_states.silly_choice_json_1, 0)
        choices = silly_player.get_card_choices([self.ex_player_states.burr_and_fat],
                                                [self.ex_player_states.carn_coop])
        self.assertEqual((0, [ExchangeForSpecies(1, [2])]), choices)

    def test_get_card_choices_json_3(self):
        silly_player = Player()
        silly_player.start(self.ex_player_states.silly_choice_json_3, 0)
        choices = silly_player.get_card_choices([self.ex_player_states.burr_and_fat],
                                                [self.ex_player_states.carn_coop])
        self.assertEqual((0, [ExchangeForSpecies(1, [2]),
                              ExchangeForPopulation(3, 2),
                              ExchangeForBodySize(4, 2),
                              ReplaceCards(5, 2, 0)]), choices)


    def test_carnivore_attack(self):
        ex = self.ex_player_states
        lop = [ex.attack_carnivore2, ex.attack_carnivore3, ex.attack_carnivore4, ex.attack_carnivore1]
        choice = ex.attack_carnivore3.choose_feeding(3, lop)

        self.assertEquals(choice, PlayerAttackWithCarnivore(1, 0, 1))




if __name__ == '__main__':
    unittest.main()
