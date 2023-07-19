import unittest

from evolution.constants import *
from evolution.player.player_feeding_choice import PlayerForgoAttack
from evolution.situation_flag import SituationFlag
from evolution.Species import Species
from evo_tests.examples import ExampleSpecies, ExampleTraits, \
    ExampleTraitTypes, ExampleDealers

__author__ = 'Edwin Cowart, Kevin McDonough'


class TestSpecies(unittest.TestCase):
    def setUp(self):
        self.ex_species = ExampleSpecies()
        self.ex_traits = ExampleTraits()
        self.ex_trait_types = ExampleTraitTypes()
        self.ex_dealers = ExampleDealers()

    def test_get_population(self):
        self.assertEqual(self.ex_species.norm_default.get_population(),
                         SPECIES_START_POP)
        self.assertEqual(self.ex_species.norm_pstart2.get_population(),
                         2 + SPECIES_START_POP)
        self.assertEqual(self.ex_species.pack_bstart_pstart2.get_population(),
                         2 + SPECIES_START_POP)


    def test_set_population(self):
        self.ex_species.norm_default.set_population(SPECIES_EXTINCTION_POP)
        self.assertEqual(self.ex_species.norm_default.get_population(), SPECIES_EXTINCTION_POP)
        self.ex_species.norm_default.set_population(SPECIES_MAX_POP)
        self.assertEqual(self.ex_species.norm_default.get_population(), SPECIES_MAX_POP)

        self.ex_species.shell_default.set_population(2 + SPECIES_START_POP)
        self.assertEqual(self.ex_species.shell_default.get_population(), 2 + SPECIES_START_POP)

        self.assertRaises(ValueError,
                          self.ex_species.norm_default.set_population, -1 + SPECIES_EXTINCTION_POP)
        self.assertRaises(ValueError,
                          self.ex_species.norm_default.set_population, 1 + SPECIES_MAX_POP)

    def test_get_body_size(self):
        self.assertEqual(self.ex_species.burr_fstart1_pstart.get_body_size(), 0)
        self.assertEqual(self.ex_species.burr_fstart1_pstart.get_body_size(SituationFlag.ATTACKER), 0)
        self.assertEqual(self.ex_species.burr_fstart1_pstart.get_body_size(SituationFlag.ATTACKER), 0)
        self.assertEqual(self.ex_species.burr_fstart1_pstart.get_body_size(SituationFlag.DEFENDER_R_NEIGHBOR), 0)
        self.assertEqual(self.ex_species.burr_fstart1_pstart.get_body_size(SituationFlag.DEFENDER_L_NEIGHBOR), 0)

        self.assertEqual(self.ex_species.pack_bstart3_pstart2.get_body_size(), 3)
        self.assertEqual(self.ex_species.pack_bstart3_pstart2.get_body_size(SituationFlag.DEFENDER), 3)
        self.assertEqual(self.ex_species.pack_bstart3_pstart2.get_body_size(SituationFlag.ATTACKER), 5 +
                         SPECIES_START_POP)
        self.assertEqual(self.ex_species.pack_bstart3_pstart2.get_body_size(SituationFlag.ATTACKER), 5 +
                         SPECIES_START_POP)
        self.assertEqual(self.ex_species.pack_bstart3_pstart2.get_body_size(SituationFlag.DEFENDER_R_NEIGHBOR), 3)
        self.assertEqual(self.ex_species.pack_bstart3_pstart2.get_body_size(SituationFlag.DEFENDER_L_NEIGHBOR), 3)


    def test_is_attackable(self):
        # Can't Attack Self
        self.assertEqual(self.ex_species.carn_default.is_attackable(self.ex_species.carn_default), False)
        self.assertEqual(self.ex_species.carn_default.is_attackable(self.ex_species.carn_default,
                                                                    self.ex_species.carn_default,
                                                                    self.ex_species.carn_default), False)
        # Can be attacked by random Carnivore
        self.assertEqual(self.ex_species.norm_default.is_attackable(self.ex_species.carn_default), True)
        self.assertEqual(self.ex_species.norm_default.is_attackable(self.ex_species.carn_default,
                                                                    self.ex_species.carn_default,
                                                                    self.ex_species.carn_default), True)

        # Can be attacked by random Species
        self.assertEqual(self.ex_species.norm_default.is_attackable(self.ex_species.norm_bmax), True)
        self.assertEqual(self.ex_species.norm_default.is_attackable(self.ex_species.norm_bmax,
                                                                    self.ex_species.norm_bmax,
                                                                    self.ex_species.norm_bmax), True)

        # Burrowing defender
        self.assertEqual(self.ex_species.burr_fstart_pstart.is_attackable(self.ex_species.carn_default), True)
        self.assertEqual(self.ex_species.burr_fstart1_pstart.is_attackable(self.ex_species.carn_default), False)
        self.assertEqual(self.ex_species.burr_fstart2_pstart2.is_attackable(self.ex_species.carn_default), True)
        self.assertEqual(self.ex_species.burr_fstart3_pstart2.is_attackable(self.ex_species.carn_default), False)

    def test_attacks_blocker(self):
        pass


    def test_any_traits_block_attacks(self):
        pass


    def test_get_owner_species(self):
        attacker = self.ex_species.carn_fat_default
        defender = self.ex_species.symb_default
        defender_left = self.ex_species.burr_fstart1_pstart
        defender_right = self.ex_species.carn_coop_default

        self.assertTrue(Species.get_owner_species(defender, attacker, defender_left, defender_right) is None)
        self.assertTrue(Species.get_owner_species(defender, attacker, defender_left, defender_right,
                                                  SituationFlag.ATTACKER), attacker)
        self.assertTrue(Species.get_owner_species(defender, attacker, defender_left, defender_right,
                                                  SituationFlag.DEFENDER) is defender)
        self.assertTrue(Species.get_owner_species(defender, attacker, defender_left, defender_right,
                                                  SituationFlag.DEFENDER_L_NEIGHBOR) is defender_left)
        self.assertTrue(Species.get_owner_species(defender, attacker, defender_left, defender_right,
                                                  SituationFlag.DEFENDER_R_NEIGHBOR) is defender_right)

    def test_has_trait(self):
        self.assertTrue(self.ex_species.burr_fstart1_pstart.has_trait(self.ex_trait_types.burr_type))
        self.assertFalse(self.ex_species.burr_fstart1_pstart.has_trait(self.ex_trait_types.scav_type))

        self.assertTrue(self.ex_species.carn_fat_default.has_trait(self.ex_trait_types.carn_type))
        self.assertFalse(self.ex_species.carn_fat_default.has_trait(self.ex_trait_types.burr_type))

        trait_types = self.ex_trait_types.all_trait_types
        for index, trait_type in enumerate(trait_types):
            species = Species(played_cards=[trait_type()])
            self.assertTrue(species.has_trait(trait_type))
            if index + 1 >= len(trait_types):
                for other_trait in trait_types[index + 1:]:
                    self.assertFalse(species.has_trait(other_trait))

    def test_attack_body_size(self):
        norm_species = self.ex_species.norm_default
        norm_body_size = norm_species.body_size
        self.assertEqual(norm_species.get_body_size(), norm_body_size)
        self.assertEqual(norm_species.get_body_size(SituationFlag.DEFENDER), norm_body_size)
        self.assertEqual(norm_species.get_body_size(SituationFlag.ATTACKER), norm_body_size)
        self.assertEqual(norm_species.get_body_size(SituationFlag.DEFENDER_L_NEIGHBOR), norm_body_size)
        self.assertEqual(norm_species.get_body_size(SituationFlag.DEFENDER_R_NEIGHBOR), norm_body_size)


        pack_species = self.ex_species.pack_bstart3_pstart2
        pack_body_size = pack_species.body_size
        pack_atk_body_size = pack_body_size + pack_species.population
        self.assertEqual(pack_species.get_body_size(), pack_body_size)
        self.assertEqual(pack_species.get_body_size(SituationFlag.DEFENDER), pack_body_size)
        self.assertEqual(pack_species.get_body_size(SituationFlag.ATTACKER), pack_atk_body_size)
        self.assertEqual(pack_species.get_body_size(SituationFlag.ATTACKER), pack_atk_body_size)
        self.assertEqual(pack_species.get_body_size(SituationFlag.ATTACKER), pack_atk_body_size)
        self.assertEqual(pack_species.get_body_size(SituationFlag.ATTACKER), pack_atk_body_size)
        self.assertEqual(pack_species.get_body_size(SituationFlag.DEFENDER_L_NEIGHBOR), pack_body_size)
        self.assertEqual(pack_species.get_body_size(SituationFlag.DEFENDER_R_NEIGHBOR), pack_body_size)
        self.assertEqual(pack_species.body_size, pack_body_size)

    def test_get_carnivore_choices_forgo(self):
        species = self.ex_species.carn_coop_default
        dealer = self.ex_dealers.dealer_forgo_friends
        self.assertIn(PlayerForgoAttack(), species.get_carnivore_choices(dealer, 0))



if __name__ == '__main__':
    unittest.main()