import unittest
from evo_tests.examples import ExampleLOC, ExampleLOTC, ExampleConfigurations, ExampleDealers
from evo_json.convert_py_json.convert_trait import convert_from_pj_loc
from evo_json.process_json.process_configuration import convert_config_to_dealer, convert_dealer_to_config

class TestConvert(unittest.TestCase):

    def setUp(self):
        self.ex_loc = ExampleLOC()
        self.ex_lotc = ExampleLOTC()
        self.ex_config = ExampleConfigurations()
        self.ex_dealer = ExampleDealers()

    def test_convert_loc(self):
        self.assertEqual(convert_from_pj_loc(self.ex_loc.loc1), self.ex_lotc.lotc1)

    def test_convert_to_config(self):
        self.assertEqual(convert_dealer_to_config(self.ex_dealer.dealer_all_veg), self.ex_config.config)

    def test_convert_from_config(self):
        self.assertEqual(convert_config_to_dealer(self.ex_config.config), self.ex_dealer.dealer_all_veg)






