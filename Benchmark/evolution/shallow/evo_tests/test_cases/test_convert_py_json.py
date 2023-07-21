__author__ = 'Edwin Cowart, Kevin McDonough'

import unittest
from evo_tests.examples import *
from evo_json.convert_py_json.convert_trait import *
from evo_json.convert_py_json.convert_species_fields import *
from evo_json.convert_py_json.convert_species import *


class TestConvertSituation(unittest.TestCase):

    def setUp(self):
        self.ex_pj_species = ExamplePJSpecies()
        self.ex_pj_traits = ExamplePJTraits()
        self.ex_traits = ExampleTraits()
        self.ex_py_lot = ExamplePJLOT()
        self.ex_lot = ExampleTraitList()
        self.ex_species = ExampleSpecies()

    def test_py_json_to_trait_card(self):
        self.assertTrue(is_pj_trait(self.ex_pj_traits.carnivore))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.ambush))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.burrowing))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.climbing))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.cooperation))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.fat_tissue))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.fertile))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.foraging))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.hard_shell))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.horns))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.long_neck))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.pack_hunting))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.scavenger))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.symbiosis))
        self.assertTrue(is_pj_trait(self.ex_pj_traits.warning_call))
        self.assertFalse(is_pj_trait("fafdsdf"))

        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.carnivore), self.ex_traits.carn)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.ambush), self.ex_traits.amb)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.burrowing), self.ex_traits.burr)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.climbing), self.ex_traits.climb)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.cooperation), self.ex_traits.coop)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.fat_tissue), self.ex_traits.fat)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.fertile), self.ex_traits.fert)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.foraging), self.ex_traits.fora)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.hard_shell), self.ex_traits.shell)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.horns), self.ex_traits.horn)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.long_neck), self.ex_traits.long)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.pack_hunting), self.ex_traits.pack)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.scavenger), self.ex_traits.scav)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.symbiosis), self.ex_traits.symb)
        self.assertEqual(convert_from_py_trait(self.ex_pj_traits.warning_call), self.ex_traits.warn)
        self.assertRaises(ValueError, convert_from_py_trait, "asdfds")

        self.assertEqual(convert_to_py_trait(self.ex_traits.carn), self.ex_pj_traits.carnivore)
        self.assertEqual(convert_to_py_trait(self.ex_traits.amb), self.ex_pj_traits.ambush)
        self.assertEqual(convert_to_py_trait(self.ex_traits.burr), self.ex_pj_traits.burrowing)
        self.assertEqual(convert_to_py_trait(self.ex_traits.climb), self.ex_pj_traits.climbing)
        self.assertEqual(convert_to_py_trait(self.ex_traits.coop), self.ex_pj_traits.cooperation)
        self.assertEqual(convert_to_py_trait(self.ex_traits.fat), self.ex_pj_traits.fat_tissue)
        self.assertEqual(convert_to_py_trait(self.ex_traits.fert), self.ex_pj_traits.fertile)
        self.assertEqual(convert_to_py_trait(self.ex_traits.fora), self.ex_pj_traits.foraging)
        self.assertEqual(convert_to_py_trait(self.ex_traits.shell), self.ex_pj_traits.hard_shell)
        self.assertEqual(convert_to_py_trait(self.ex_traits.horn), self.ex_pj_traits.horns)
        self.assertEqual(convert_to_py_trait(self.ex_traits.long), self.ex_pj_traits.long_neck)
        self.assertEqual(convert_to_py_trait(self.ex_traits.pack), self.ex_pj_traits.pack_hunting)
        self.assertEqual(convert_to_py_trait(self.ex_traits.scav), self.ex_pj_traits.scavenger)
        self.assertEqual(convert_to_py_trait(self.ex_traits.symb), self.ex_pj_traits.symbiosis)
        self.assertEqual(convert_to_py_trait(self.ex_traits.warn), self.ex_pj_traits.warning_call)
        self.assertRaises(ValueError, convert_from_py_trait, TraitCard)

        for card_name in trait_dictionary.keys():
            self.assertEqual(type(convert_from_py_trait(card_name)), trait_dictionary.get(card_name))

    def test_py_json_to_list_trait_card(self):

        self.assertTrue(is_pj_lot(self.ex_py_lot.lot0))
        self.assertTrue(is_pj_lot(self.ex_py_lot.lot1))
        self.assertTrue(is_pj_lot(self.ex_py_lot.lot2))
        self.assertTrue(is_pj_lot(self.ex_py_lot.lot3))
        self.assertFalse(is_pj_lot(self.ex_py_lot.lot3[:].append(["asdfdsaf"])))

        self.assertEqual(convert_from_pj_lot(self.ex_py_lot.lot0), self.ex_lot.lot0)
        self.assertEqual(convert_from_pj_lot(self.ex_py_lot.lot1), self.ex_lot.lot1)
        self.assertEqual(convert_from_pj_lot(self.ex_py_lot.lot2), self.ex_lot.lot2)
        self.assertEqual(convert_from_pj_lot(self.ex_py_lot.lot3), self.ex_lot.lot3)

        self.assertEqual(convert_to_pj_lot(self.ex_lot.lot0), self.ex_py_lot.lot0)
        self.assertEqual(convert_to_pj_lot(self.ex_lot.lot1), self.ex_py_lot.lot1)
        self.assertEqual(convert_to_pj_lot(self.ex_lot.lot2), self.ex_py_lot.lot2)
        self.assertEqual(convert_to_pj_lot(self.ex_lot.lot3), self.ex_py_lot.lot3)

    def test_pj_food(self):

        self.assertTrue(is_pj_food(self.ex_pj_species.food_0))
        self.assertTrue(is_pj_food(self.ex_pj_species.food_1))
        self.assertTrue(is_pj_food(self.ex_pj_species.food_10))
        self.assertFalse(is_pj_food(self.ex_pj_species.food_n1))
        self.assertFalse(is_pj_food(self.ex_pj_species.traits0))
        self.assertFalse(is_pj_food(self.ex_pj_species.body_0))

        self.assertEqual(convert_from_pj_food(self.ex_pj_species.food_0), 0)
        self.assertEqual(convert_from_pj_food(self.ex_pj_species.food_1), 1)
        self.assertEqual(convert_from_pj_food(self.ex_pj_species.food_10), 10)
        self.assertRaises(ValueError, convert_from_pj_food, self.ex_pj_species.food_n1)

        self.assertEqual(convert_to_pj_food(0), self.ex_pj_species.food_0)
        self.assertEqual(convert_to_pj_food(1), self.ex_pj_species.food_1)
        self.assertEqual(convert_to_pj_food(10), self.ex_pj_species.food_10)
        self.assertRaises(ValueError, convert_to_pj_food, -1)

    def test_pj_body(self):

        self.assertTrue(is_pj_body(self.ex_pj_species.body_0))
        self.assertTrue(is_pj_body(self.ex_pj_species.body_1))
        self.assertTrue(is_pj_body(self.ex_pj_species.body_10))
        self.assertFalse(is_pj_body(self.ex_pj_species.body_n1))
        self.assertFalse(is_pj_body(self.ex_pj_species.traits0))
        self.assertFalse(is_pj_body(self.ex_pj_species.pop_0))

        self.assertEqual(convert_from_pj_body(self.ex_pj_species.body_0), 0)
        self.assertEqual(convert_from_pj_body(self.ex_pj_species.body_1), 1)
        self.assertEqual(convert_from_pj_body(self.ex_pj_species.body_10), 10)
        self.assertRaises(ValueError, convert_from_pj_body, self.ex_pj_species.body_n1)

        self.assertEqual(convert_to_pj_body(0), self.ex_pj_species.body_0)
        self.assertEqual(convert_to_pj_body(1), self.ex_pj_species.body_1)
        self.assertEqual(convert_to_pj_body(10), self.ex_pj_species.body_10)
        self.assertRaises(ValueError, convert_to_pj_body, -1)

    def test_pj_pop(self):

        self.assertTrue(is_pj_pop(self.ex_pj_species.pop_0))
        self.assertTrue(is_pj_pop(self.ex_pj_species.pop_1))
        self.assertTrue(is_pj_pop(self.ex_pj_species.pop_10))
        self.assertFalse(is_pj_pop(self.ex_pj_species.pop_n1))
        self.assertFalse(is_pj_pop(self.ex_pj_species.traits0))
        self.assertFalse(is_pj_pop(self.ex_pj_species.body_0))

        self.assertEqual(convert_from_pj_pop(self.ex_pj_species.pop_0), 0)
        self.assertEqual(convert_from_pj_pop(self.ex_pj_species.pop_1), 1)
        self.assertEqual(convert_from_pj_pop(self.ex_pj_species.pop_10), 10)
        self.assertRaises(ValueError, convert_from_pj_pop, self.ex_pj_species.pop_n1)

        self.assertEqual(convert_to_pj_pop(0), self.ex_pj_species.pop_0)
        self.assertEqual(convert_to_pj_pop(1), self.ex_pj_species.pop_1)
        self.assertEqual(convert_to_pj_pop(10), self.ex_pj_species.pop_10)
        self.assertRaises(ValueError, convert_to_pj_pop, -1)

    def test_pj_traits(self):

        self.assertTrue(is_pj_traits(self.ex_pj_species.traits0))
        self.assertTrue(is_pj_traits(self.ex_pj_species.traits1))
        self.assertTrue(is_pj_traits(self.ex_pj_species.traits2))
        self.assertTrue(is_pj_traits(self.ex_pj_species.traits3))
        self.assertFalse(is_pj_traits(self.ex_pj_species.pop_0))
        self.assertFalse(is_pj_traits(self.ex_pj_species.body_0))

        self.assertEqual(convert_from_pj_traits(self.ex_pj_species.traits0), self.ex_lot.lot0)
        self.assertEqual(convert_from_pj_traits(self.ex_pj_species.traits1), self.ex_lot.lot1)
        self.assertEqual(convert_from_pj_traits(self.ex_pj_species.traits2), self.ex_lot.lot2)
        self.assertEqual(convert_from_pj_traits(self.ex_pj_species.traits3), self.ex_lot.lot3)
        self.assertRaises(ValueError, convert_from_pj_traits, self.ex_pj_species.pop_n1)

        self.assertEqual(convert_to_pj_traits(self.ex_lot.lot0), self.ex_pj_species.traits0)
        self.assertEqual(convert_to_pj_traits(self.ex_lot.lot1), self.ex_pj_species.traits1)
        self.assertEqual(convert_to_pj_traits(self.ex_lot.lot2), self.ex_pj_species.traits2)
        self.assertEqual(convert_to_pj_traits(self.ex_lot.lot3), self.ex_pj_species.traits3)
        self.assertRaises(ValueError, convert_to_pj_traits, -1)

    def test_pj_fat_food(self):

        self.assertTrue(is_pj_fat_food(self.ex_pj_species.fat_food_0))
        self.assertTrue(is_pj_fat_food(self.ex_pj_species.fat_food_1))
        self.assertTrue(is_pj_fat_food(self.ex_pj_species.fat_food_10))
        self.assertFalse(is_pj_fat_food(self.ex_pj_species.fat_food_n1))
        self.assertFalse(is_pj_fat_food(self.ex_pj_species.traits0))
        self.assertFalse(is_pj_fat_food(self.ex_pj_species.body_0))

        self.assertEqual(convert_from_pj_fat_food(self.ex_pj_species.fat_food_0), 0)
        self.assertEqual(convert_from_pj_fat_food(self.ex_pj_species.fat_food_1), 1)
        self.assertEqual(convert_from_pj_fat_food(self.ex_pj_species.fat_food_10), 10)
        self.assertRaises(ValueError, convert_from_pj_fat_food, self.ex_pj_species.fat_food_n1)

        self.assertEqual(convert_to_pj_fat_food(0), self.ex_pj_species.fat_food_0)
        self.assertEqual(convert_to_pj_fat_food(1), self.ex_pj_species.fat_food_1)
        self.assertEqual(convert_to_pj_fat_food(10), self.ex_pj_species.fat_food_10)
        self.assertRaises(ValueError, convert_to_pj_fat_food, -1)

    def test_pj_species(self):
        self.assertTrue(is_pj_species(self.ex_pj_species.spe_0))
        self.assertTrue(is_pj_species(self.ex_pj_species.spe_1))
        self.assertTrue(is_pj_species(self.ex_pj_species.spe_max))
        self.assertTrue(is_pj_species(self.ex_pj_species.spe_max_b1))
        self.assertTrue(is_pj_species(self.ex_pj_species.spe_max_p1))
        self.assertTrue(is_pj_species(self.ex_pj_species.spe_dup))
        self.assertFalse(is_pj_species(self.ex_traits.amb))

        self.assertEqual(convert_from_pj_species(self.ex_pj_species.spe_0), self.ex_species.spe_0)
        self.assertEqual(convert_from_pj_species(self.ex_pj_species.spe_1), self.ex_species.spe_1)
        self.assertEqual(convert_from_pj_species(self.ex_pj_species.spe_max), self.ex_species.spe_max)

        self.assertRaises(ValueError, convert_from_pj_species, self.ex_pj_species.spe_max_f1)

        self.assertRaises(ValueError, convert_from_pj_species, self.ex_pj_species.spe_max_b1)

        self.assertRaises(ValueError, convert_from_pj_species, self.ex_pj_species.spe_max_p1)

        self.assertRaises(ValueError, convert_from_pj_species, self.ex_pj_species.spe_dup)




if __name__ == '__main__':
    unittest.main()
