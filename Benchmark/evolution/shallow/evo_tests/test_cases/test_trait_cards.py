import unittest

import evolution.Species
from evolution.trait_cards.burrowing import BurrowingCard
import evolution.trait_cards.cards
from evo_tests.examples import ExampleSpecies
from evolution.constants import *
from evolution.trait_cards.pack_hunting import PackHuntingCard
from evolution.trait_cards.carnivore import CarnivoreCard
from evolution.trait_cards.climbing import ClimbingCard
from evolution.trait_cards.fat_tissue import FatTissueCard
from evolution.trait_cards.long_neck import LongNeckCard
from evolution.trait_cards.foraging import ForagingCard
from evolution.trait_cards.scavenger import ScavengerCard
from evolution.trait_cards.cooperation import CooperationCard
from evolution.trait_cards.hard_shell import HardShellCard
from evolution.trait_cards.herding import HerdingCard
from evolution.trait_cards.fertile import FertileCard
from evolution.trait_cards.symbiosis import SymbiosisCard
from evolution.trait_cards.warning import WarningCallCard
from evolution.trait_cards.ambush import AmbushCard
from evolution.situation_flag import SituationFlag

__author__ = 'Edwin Cowart, Kevin McDonough'


class TestTraitCards(unittest.TestCase):
    def setUp(self):
        self.all_trait_classes = [CarnivoreCard, AmbushCard, BurrowingCard, ClimbingCard,
                                  HardShellCard, HerdingCard, SymbiosisCard, WarningCallCard,
                                  CooperationCard, FatTissueCard, FertileCard, ForagingCard,
                                  LongNeckCard, PackHuntingCard, ScavengerCard]
        self.classes_with_default_food_points = [x for x in self.all_trait_classes if
                                                 x != CarnivoreCard]
        self.classes_with_generic_atk_body_size = [x for x in self.all_trait_classes if
                                                   x != PackHuntingCard]
        self.classes_block_attacks = [BurrowingCard, ClimbingCard, HardShellCard, HerdingCard,
                                      SymbiosisCard,
                                      WarningCallCard]
        self.classes_cant_block_attacks = [x for x in self.all_trait_classes if
                                           x not in self.classes_block_attacks]

        self.ex_species = ExampleSpecies()

    def test_carnivore_constructor(self):
        for food_tokens in range(CARNIVORE_MIN_FOOD_TOKENS, CARNIVORE_MAX_FOOD_TOKENS + 1):
            carnivore = CarnivoreCard(food_tokens)
            self.assertEqual(carnivore.num_tokens_as_food_card, food_tokens,
                             "Carnivore " + str(food_tokens) + ": constructor-food_tokens")
            self.assertEqual(carnivore.description,
                             "CarnivoreCard must attack to eat during the evolution stage.")

    def test_rest_trait_card_constructors(self):
        for trait_class in self.classes_with_default_food_points:
            self._test_generic_trait_card_constructor(trait_class)

    def _test_generic_trait_card_constructor(self, trait_class):
        for food_tokens in range(TRAIT_CARD_MIN_FOOD_TOKENS, TRAIT_CARD_MAX_FOOD_TOKENS + 1):
            card = trait_class(food_tokens)  # type: TraitCard
            self.assertEqual(card.num_tokens_as_food_card, food_tokens)

        self.assertRaises(ValueError, trait_class, TRAIT_CARD_MAX_FOOD_TOKENS + 1)
        self.assertRaises(ValueError, trait_class, TRAIT_CARD_MIN_FOOD_TOKENS - 1)

    def test_default_blocks_attacks(self):
        for trait_class in self.classes_cant_block_attacks:
            trait_card1 = trait_class(0)  # type: TraitCard
            attacker = evolution.Species.Species(played_cards=[CarnivoreCard(0)])
            defender = evolution.Species.Species(played_cards=[trait_card1])
            self.assertEqual(trait_card1.blocks_attack(defender, attacker,
                                                       owner_flag=SituationFlag.DEFENDER), False)

    def test_burrowing_blocks_attacks(self):
        b_card = BurrowingCard(0)
        attacker = evolution.Species.Species(played_cards=[CarnivoreCard(0)])
        defender_1 = evolution.Species.Species(num_food_tokens=0, population=1, played_cards=[b_card])
        defender_2 = evolution.Species.Species(num_food_tokens=1, population=1, played_cards=[b_card])
        defender_3 = evolution.Species.Species(num_food_tokens=2, population=3, played_cards=[b_card])
        defender_4 = evolution.Species.Species(num_food_tokens=3, population=3, played_cards=[b_card])

        self.assertEqual(b_card.blocks_attack(self.ex_species.burr_fstart_pstart, attacker,
                                              owner_flag=SituationFlag.DEFENDER),
                         SPECIES_START_FOOD == SPECIES_START_POP)
        self.assertEqual(b_card.blocks_attack(self.ex_species.burr_fstart1_pstart, attacker,
                                              owner_flag=SituationFlag.DEFENDER),
                         1 + SPECIES_START_FOOD == SPECIES_START_POP)
        self.assertEqual(b_card.blocks_attack(self.ex_species.burr_fstart2_pstart2, attacker,
                                              owner_flag=SituationFlag.DEFENDER),
                         2 + SPECIES_START_FOOD == 2 + SPECIES_START_POP)
        self.assertEqual(b_card.blocks_attack(self.ex_species.burr_fstart3_pstart2, attacker,
                                              owner_flag=SituationFlag.DEFENDER),
                         3 + SPECIES_START_FOOD == 2 + SPECIES_START_POP)

    def test_climbing_blocks_attacks(self):
        c_card0 = ClimbingCard(0)
        c_card1 = ClimbingCard(1)

        self.assertEqual(c_card1.blocks_attack(self.ex_species.climb_default,
                                               self.ex_species.climb_default_2,
                                               owner_flag=SituationFlag.DEFENDER),
                         False)
        self.assertEqual(c_card1.blocks_attack(self.ex_species.climb_default,
                                               self.ex_species.norm_default,
                                               owner_flag=SituationFlag.DEFENDER),
                         True)

    def test_hard_shell_blocks_attacks(self):
        hs_card = HardShellCard(0)
        attacker_0 = evolution.Species.Species(body_size=0, played_cards=[CarnivoreCard(0)])
        attacker_3 = evolution.Species.Species(body_size=3, played_cards=[CarnivoreCard(0)])
        attacker_4 = evolution.Species.Species(body_size=4, played_cards=[CarnivoreCard(0)])
        attacker_7 = evolution.Species.Species(body_size=7, played_cards=[CarnivoreCard(0)])
        defender_0 = evolution.Species.Species(body_size=0, played_cards=[hs_card])
        defender_4 = evolution.Species.Species(body_size=4, played_cards=[hs_card])

        self.assertEqual(hs_card.blocks_attack(self.ex_species.shell_default,
                                               self.ex_species.norm_default,
                                               owner_flag=SituationFlag.DEFENDER), True)
        # MAGIC CONSTANT TEST
        self.assertEqual(hs_card.blocks_attack(self.ex_species.shell_default,
                                               self.ex_species.norm_bstart3,
                                               owner_flag=SituationFlag.DEFENDER), True)

        self.assertEqual(hs_card.blocks_attack(self.ex_species.shell_default,
                                               self.ex_species.norm_bstartshell,
                                               owner_flag=SituationFlag.DEFENDER), False)

        self.assertEqual(hs_card.blocks_attack(self.ex_species.shell_default,
                                               self.ex_species.norm_bmax,
                                               owner_flag=SituationFlag.DEFENDER),
                         HARD_SHELL_OFFSET > SPECIES_MAX_POP - SPECIES_START_POP)

        self.assertEqual(hs_card.blocks_attack(self.ex_species.shell_bstart3,
                                               self.ex_species.norm_default,
                                               owner_flag=SituationFlag.DEFENDER), True)

    def test_herding_blocks_attacks(self):
        h_card = HerdingCard(0)
        self.assertEqual(h_card.blocks_attack(self.ex_species.herd_default,
                                              self.ex_species.carn_default,
                                              owner_flag=SituationFlag.DEFENDER), True)
        self.assertEqual(h_card.blocks_attack(self.ex_species.herd_default,
                                              self.ex_species.carn_pstart1,
                                              owner_flag=SituationFlag.DEFENDER), False)
        self.assertEqual(h_card.blocks_attack(self.ex_species.herd_pstart1,
                                              self.ex_species.carn_pstart1,
                                              owner_flag=SituationFlag.DEFENDER), True)
        self.assertEqual(h_card.blocks_attack(self.ex_species.herd_pstart2,
                                              self.ex_species.carn_pstart1,
                                              owner_flag=SituationFlag.DEFENDER), True)

    def test_symbiosis_blocks_attacks(self):
        card = SymbiosisCard(0)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_default,
                                            self.ex_species.carn_default,
                                            None, self.ex_species.norm_default,
                                            owner_flag=SituationFlag.DEFENDER),
                         False)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_default,
                                            self.ex_species.carn_default,
                                            None, self.ex_species.norm_bstart3,
                                            owner_flag=SituationFlag.DEFENDER),
                         True)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_bstart3,
                                            self.ex_species.carn_default,
                                            None, self.ex_species.norm_bstart3,
                                            owner_flag=SituationFlag.DEFENDER),
                         False)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_bstart3,
                                            self.ex_species.carn_default,
                                            None, self.ex_species.norm_bstart4,
                                            owner_flag=SituationFlag.DEFENDER),
                         True)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_bstart3,
                                            self.ex_species.carn_default,
                                            None, self.ex_species.norm_default,
                                            owner_flag=SituationFlag.DEFENDER),
                         False)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_bstart3,
                                            self.ex_species.carn_default,
                                            self.ex_species.norm_bstart4, None,
                                            owner_flag=SituationFlag.DEFENDER),
                         False)
        self.assertEqual(card.blocks_attack(self.ex_species.symb_bstart3,
                                            self.ex_species.carn_default,
                                            self.ex_species.norm_default, None,
                                            owner_flag=SituationFlag.DEFENDER),
                         False)

    def test_warning_call_blocks_attacks(self):
        warn_card = WarningCallCard(0)

        # Warn doesn't protect defender
        self.assertEqual(warn_card.blocks_attack(self.ex_species.warn_default,
                                                 self.ex_species.carn_default,
                                                 owner_flag=SituationFlag.DEFENDER), False)
        # Left defense
        self.assertEqual(warn_card.blocks_attack(self.ex_species.norm_default,
                                                 self.ex_species.carn_default,
                                                 self.ex_species.warn_default, None,
                                                 SituationFlag.DEFENDER_L_NEIGHBOR),
                         True)
        # Right defense
        self.assertEqual(warn_card.blocks_attack(self.ex_species.norm_default,
                                                 self.ex_species.carn_default,
                                                 None, self.ex_species.warn_default,
                                                 SituationFlag.DEFENDER_R_NEIGHBOR),
                         True)
        # Left defense ambushed
        self.assertEqual(warn_card.blocks_attack(self.ex_species.norm_default,
                                                 self.ex_species.carnamb_default,
                                                 self.ex_species.warn_default, None,
                                                 SituationFlag.DEFENDER_L_NEIGHBOR),
                         False)
        # Right defense ambushed
        self.assertEqual(warn_card.blocks_attack(self.ex_species.norm_default,
                                                 self.ex_species.carnamb_default,
                                                 None, self.ex_species.warn_default,
                                                 SituationFlag.DEFENDER_R_NEIGHBOR),
                         False)



if __name__ == '__main__':
    unittest.main()
