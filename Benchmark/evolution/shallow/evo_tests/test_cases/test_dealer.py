__author__ = 'Edwin Cowart, Kevin McDonough'

import unittest
from collections import deque

from evo_tests.examples import *
from executefeed1 import *
from evolution.player.player_feeding_choice import PlayerFeedVegetarian
from cardplay import ExchangeForBodySize, ExchangeForPopulation, \
    ExchangeForSpecies


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.ex_player_states = ExamplePlayerStates()
        self.ex_species = ExampleSpecies()
        self.ex_dealer = ExampleDealers()

    def test_feed1_all_veg(self):
        deque1 = deque([0, 1])
        dealer = self.ex_dealer.dealer_all_veg
        dealer.feed1(deque1)
        self.assertEqual(dealer.player_states[0],
                         self.ex_player_states.coop_fed)
        self.assertEqual(dealer.player_states[1], self.ex_player_states.fora)
        self.assertEqual(deque1, deque([1, 0]))

        dealer.feed1(deque1)
        self.assertEqual(dealer.player_states[0],
                         self.ex_player_states.coop_fed)
        self.assertEqual(dealer.player_states[1],
                         self.ex_player_states.fora_fed)
        self.assertEqual(deque1, deque([0, 1]))

        dealer.feed1(deque1)
        self.assertEqual(dealer.player_states[0],
                         self.ex_player_states.coop_fed)
        self.assertEqual(dealer.player_states[1],
                         self.ex_player_states.fora_fed)
        self.assertEqual(deque1, deque([1]))

        dealer.feed1(deque1)
        self.assertEqual(dealer.player_states[0],
                         self.ex_player_states.coop_fed)
        self.assertEqual(dealer.player_states[1],
                         self.ex_player_states.fora_fed)
        self.assertEqual(deque1, deque([]))

    def test_feed_1_carn_fat(self):
        deque1 = deque([0, 1])
        dealer = self.ex_dealer.dealer_carn_fat
        dealer.feed1(deque1)
        self.assertEqual(deque1, deque([1, 0]))
        # self.assertEqual(dealer.player_states[0], self.ex_player_states.carn_fat_attack)
        self.assertEqual(dealer.player_states[1],
                         self.ex_player_states.norm_pstart_2_attacked)

    def test_feed_1_fat_tissue(self):
        deque1 = deque([0])
        dealer = self.ex_dealer.dealer_burr_fat
        dealer.feed1(deque1)
        self.assertEqual(deque1, deque([0]))
        self.assertEqual(dealer.player_states[0],
                         self.ex_player_states.burr_and_fat_store)

    def test_feed_1_extinct(self):
        deque1 = deque([0, 1])
        dealer = self.ex_dealer.dealer_carn_extinct
        dealer.feed1(deque1)
        self.assertEqual(dealer.player_states[1], self.ex_player_states.default)
        self.ex_dealer.dealer_carn_extinct.feed1(deque1)
        self.assertEqual(deque1, deque([0]))
        self.ex_dealer.dealer_carn_extinct.feed1(deque1)
        self.assertEqual(deque1, deque([]))

    def test_feed_1_feed_veg(self):
        deque1 = deque([0, 1])
        dealer = self.ex_dealer.dealer_feed_veg
        dealer.feed1(deque1)
        player0 = dealer.player_states[0]
        scavenger = player0.species_list[0]
        carn_coop = player0.species_list[1]
        vegetarian = player0.species_list[2]
        self.assertEqual(0, scavenger.num_food_tokens)
        self.assertEqual(0, carn_coop.num_food_tokens)
        self.assertEqual(1, vegetarian.num_food_tokens)

    def test_feed_1_feed_order(self):
        deque1 = deque([0, 1])
        dealer = self.ex_dealer.dealer_feeding_order
        dealer.feed1(deque1)
        player0 = dealer.player_states[0]
        carn_scav = player0.species_list[0]
        carn_coop = player0.species_list[1]
        carn = player0.species_list[2]
        self.assertEqual(0, carn_scav.num_food_tokens)
        self.assertEqual(1, carn_coop.num_food_tokens)
        self.assertEqual(1, carn.num_food_tokens)

    def test_determine_choices_veg(self):
        dealer = self.ex_dealer.dealer_all_veg
        choice = dealer.determine_choices(0)
        self.assertEqual(choice, OneChoice(PlayerFeedVegetarian(0)))

    def test_determine_choices_mult(self):
        dealer = self.ex_dealer.dealer_burr_fat
        choice = dealer.determine_choices(0)
        self.assertEqual(choice, MultipleChoices())

    def test_determine_choices_no_choice(self):
        deque1 = deque([0, 1])
        dealer = self.ex_dealer.dealer_all_veg
        dealer.feed1(deque1)
        dealer.feed1(deque1)
        choice = dealer.determine_choices(0)
        self.assertEqual(choice, NoChoice())

    def test_step4_basic(self):
        dealer = self.ex_dealer.dealer_all_veg
        food_cards = [CarnivoreCard(3), ForagingCard(-2)]
        for player_state, food_card in zip(dealer.player_states, food_cards):
            player_state.hand = [food_card]
        to_feed = deque([0, 1])
        food_card_indices = [0, 0]
        dealer.step4(food_card_indices, [[], []], to_feed)

        coop_player = dealer.player_states[0]
        coop_spec = coop_player.species_list[0]
        fora_player = dealer.player_states[1]
        fora_spec = fora_player.species_list[0]

        self.assertEqual(dealer.wateringhole, 9)
        self.assertEqual(coop_spec.num_food_tokens, 1)
        self.assertEqual(fora_spec.num_food_tokens, 1)
        self.assertEqual(to_feed, deque([]))

    def test_step4_fert_long(self):
        dealer = self.ex_dealer.dealer_fert_long_fora
        food_cards = [CarnivoreCard(2), ForagingCard(-2)]
        for player_state, food_card in zip(dealer.player_states, food_cards):
            player_state.hand = [food_card]
        food_card_indices = [0, 0]
        to_feed = deque([0, 1])
        dealer.step4(food_card_indices, [[], []], to_feed)

        combo_player = dealer.player_states[0]
        combo_spec = combo_player.species_list[0]
        sad_player = dealer.player_states[1]
        sad_spec = sad_player.species_list[0]

        self.assertEqual(dealer.wateringhole, 0)
        self.assertEqual(combo_spec.num_food_tokens, 2)
        self.assertEqual(sad_spec.num_food_tokens, 0)
        self.assertEqual(to_feed, deque([0, 1]))

    def test_step4_with_cardplays(self):
        dealer = self.ex_dealer.dealer_all_veg
        dealer.player_states[0].hand = [CarnivoreCard(1), CarnivoreCard(2), FertileCard(1),
                                        LongNeckCard(-1), CarnivoreCard(-3)]
        dealer.player_states[1].hand = [ForagingCard(-1)]

        food_cards = [0, 0]
        card_plays0 = [ExchangeForSpecies(1, [2]),
                       ExchangeForPopulation(3, 1),
                       ExchangeForBodySize(4, 1)]
        card_plays = [card_plays0, []]
        to_feed = deque([0, 1])
        dealer.step4(food_cards, card_plays, to_feed)

        coop_player = dealer.player_states[0]
        coop_spec = coop_player.species_list[0]
        new_spec = coop_player.species_list[1]
        fora_player = dealer.player_states[1]
        fora_spec = fora_player.species_list[0]

        self.assertEqual(dealer.wateringhole, 5)
        self.assertEqual(coop_spec.num_food_tokens, 1)
        self.assertEqual(coop_spec.body_size, 0)
        self.assertEqual(coop_spec.population, 1)
        self.assertEqual(new_spec.num_food_tokens, 3)
        self.assertEqual(new_spec.body_size, 1)
        self.assertEqual(new_spec.population, 3)
        self.assertEqual(fora_spec.num_food_tokens, 1)
        self.assertEqual(fora_spec.body_size, 0)
        self.assertEqual(fora_spec.population, 1)

    def test_step4_1_in(self):
        dealer = self.ex_dealer.dealer_step4_1
        food_card_indices = [0, 0, 0]
        to_feed = deque([0, 1, 2])
        dealer.step4(food_card_indices, [[], [], []], to_feed)

        p0 = dealer.player_states[0]
        p1 = dealer.player_states[1]
        p2 = dealer.player_states[2]

        p0s0 = p0.species_list[0]
        p0s1 = p0.species_list[1]
        p0s2 = p0.species_list[2]
        p1s0 = p1.species_list[0]
        p2s0 = p2.species_list[0]

        all_species = [p0s0, p0s1, p0s2, p1s0, p2s0]

        self.assertEqual(dealer.wateringhole, 5)
        self.assertEqual(len(p0.species_list), 3)
        self.assertEqual(len(p1.species_list), 1)
        self.assertEqual(len(p2.species_list), 1)
        for species in all_species:
            self.assertEqual(species.num_food_tokens, 1)
            self.assertEqual(species.body_size, 3)
            self.assertEqual(species.population, 1)
        self.assertEqual(p0.hand, [ClimbingCard(2)])
        self.assertEqual(p1.hand, [ClimbingCard(-2)])
        self.assertEqual(p2.hand, [ClimbingCard(0)])

    def test_step4_fertile(self):
        dealer = self.ex_dealer.dealer_step4_1
        dealer.player_states[0].species_list.append(self.ex_species.fert_p7)
        food_card_indices = [0, 0, 0]
        to_feed = deque([0, 1, 2])
        dealer.step4(food_card_indices, [[], [], []], to_feed)

        self.assertEqual(dealer.player_states[0].species_list[-1].population, 7)

    def test_step4_fat_tissue(self):
        dealer = self.ex_dealer.dealer_step4_1
        dealer.player_states[0].species_list.append((self.ex_species.fat3))
        food_card_indices = [0, 0, 0]
        to_feed = deque([0, 1, 2])
        dealer.step4(food_card_indices, [[], [], []], to_feed)
        self.assertEqual(dealer.player_states[0].species_list[-1].get_fat_tissue_food(), 3)
        self.assertEqual(dealer.player_states[0].species_list[-1].num_food_tokens, 1)


    def test_step4_watering_hole(self):
        dealer = self.ex_dealer.dealer_step4_2
        food_card_indices = [0, 0, 0]
        to_feed = deque([0, 1, 2])
        dealer.step4(food_card_indices, [[], [], []], to_feed)
        self.assertEqual(dealer.wateringhole, 3)

    def test_run_turn(self):
        dealer = Dealer.make_dealer([self.ex_player_states.fat3,
                                     self.ex_player_states.fat5],
                                    Deck.make_deck(), 0)

        dealer.run_turn()
        ps0 = dealer.player_states[0]
        ps1 = dealer.player_states[1]
        self.assertEqual(1, ps1.food_bag)
        self.assertEqual(3, ps1.species_list[0].get_fat_tissue_food())
        self.assertEqual(3, ps1.species_list[0].body_size)
        self.assertEqual(1, ps1.species_list[0].population)
        self.assertEqual(0, ps1.species_list[0].num_food_tokens)
        self.assertEqual([BurrowingCard(-2), BurrowingCard(-1)], ps1.hand)
        self.assertEqual(1, ps0.food_bag)
        self.assertEqual(4, ps0.species_list[0].get_fat_tissue_food())
        self.assertEqual(6, ps0.species_list[0].body_size)
        self.assertEqual(1, ps0.species_list[0].population)
        self.assertEqual(0, ps0.species_list[0].num_food_tokens)
        self.assertEqual([BurrowingCard(0), BurrowingCard(1)], ps0.hand)
        self.assertEqual(110, len(dealer.deck.loc))

    def test_run_game_4p(self):
        dealer = Dealer([Player(), Player(), Player(), Player()],
                        Deck.make_deck())

        dealer.run_game()
        scores = dealer.get_sorted_scores()
        expected = [(2, 'player info', 13),
                    (1, 'player info', 12),
                    (4, 'player info', 12),
                    (3, 'player info', 12)]
        self.assertEqual(expected, scores)


if __name__ == '__main__':
    unittest.main()
