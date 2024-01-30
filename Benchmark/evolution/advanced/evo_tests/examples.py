from copy import copy

from evolution.constants import *
from evolution.player.iplayer import IPlayer
from evolution.player.player import Player
from evolution.trait_cards import *
from dealer.dealer import Dealer
from dealer.deck import Deck
from evo_json.constants import *
from evolution.Species import Species

"""
A LOP+ is [Player+, ..., Player+].

A Player+ is one of
a regular Player

a Player with a "cards" field:
    [["id",Natural+],
     ["species",LOS],
     ["bag",Natural]
     ["cards",LOC]]

"""


class ExampleConfigurations:
    """
    To represent a configuration
    """

    def __init__(self):
        self.ex_loc = ExampleLOC()
        self.ex_p = ExamplePJPlayers()
        self.config = [[self.ex_p.player_coop, self.ex_p.player_fora], 10,
                       self.ex_loc.loc0]


class ExamplePJPlayers:
    def __init__(self):
        self.ex_species = ExamplePJSpecies()
        self.player_coop = [["id", 4],
                            ["species", [self.ex_species.coop_default]],
                            ["bag", 0]]

        self.player_fora = [["id", 13],
                            ["species", [self.ex_species.fora_default]],
                            ["bag", 0]]


class ExamplePJTraits:
    def __init__(self):
        self.carnivore = CARNIVORE_STR
        self.ambush = AMBUSH_STR
        self.burrowing = BURROWING_STR
        self.climbing = CLIMBING_STR
        self.cooperation = COOPERATION_STR
        self.fat_tissue = FAT_TISSUE_STR
        self.fertile = FERTILE_STR
        self.foraging = FORAGING_STR
        self.hard_shell = HARD_SHELL_STR
        self.herding = HERDING_STR
        self.horns = HORNS_STR
        self.long_neck = LONG_NECK_STR
        self.pack_hunting = PACK_HUNTING_STR
        self.scavenger = SCAVENGER_STR
        self.symbiosis = SYMBIOSIS_STR
        self.warning_call = WARNING_CALL_STR


class ExamplePJLOT:
    def __init__(self):
        self.ex_traits = ExampleTraits()
        self.ex_pj_traits = ExamplePJTraits()

        self.lot0 = []
        self.lot1 = [self.ex_pj_traits.carnivore]
        self.lot2 = [self.ex_pj_traits.carnivore, self.ex_pj_traits.ambush]
        self.lot3 = [self.ex_pj_traits.carnivore, self.ex_pj_traits.ambush,
                     self.ex_pj_traits.burrowing]
        self.lot4 = [self.ex_pj_traits.carnivore, self.ex_pj_traits.ambush,
                     self.ex_pj_traits.burrowing, self.ex_pj_traits.climbing]
        self.lot_dup = [self.ex_pj_traits.carnivore, self.ex_pj_traits.ambush,
                        self.ex_pj_traits.carnivore]


class ExampleLOC:
    def __init__(self):
        self.ex_cards = ExamplePJTraits()
        self.loc0 = []
        self.loc1 = [[1, self.ex_cards.ambush], [2, self.ex_cards.burrowing]]


class ExampleLOTC:
    """
    To represent a list of traitcards
    """

    def __init__(self):
        self.lotc1 = [AmbushCard(1), BurrowingCard(2)]


class ExamplePJSpecies:
    def __init__(self):
        self.ex_pj_traits = ExamplePJTraits()
        self.ex_pj_lot = ExamplePJLOT()

        self.food_n1 = [FOOD_STR, -1]
        self.food_0 = [FOOD_STR, 0]
        self.food_1 = [FOOD_STR, 1]
        self.food_max = [FOOD_STR, SPECIES_MAX_POP]
        self.food_max_p1 = [FOOD_STR, SPECIES_MAX_POP + 1]
        self.food_10 = [FOOD_STR, 10]

        self.body_n1 = [BODY_STR, -1]
        self.body_0 = [BODY_STR, 0]
        self.body_1 = [BODY_STR, 1]
        self.body_max = [BODY_STR, SPECIES_MAX_BODY_SIZE]
        self.body_max_p1 = [BODY_STR, SPECIES_MAX_BODY_SIZE + 1]
        self.body_10 = [BODY_STR, 10]

        self.pop_n1 = [POP_STR, -1]
        self.pop_0 = [POP_STR, 0]
        self.pop_1 = [POP_STR, 1]
        self.pop_max = [POP_STR, SPECIES_MAX_POP]
        self.pop_max_p1 = [POP_STR, SPECIES_MAX_POP + 1]
        self.pop_10 = [POP_STR, 10]

        self.traits0 = [TRAITS_STR, self.ex_pj_lot.lot0]
        self.traits1 = [TRAITS_STR, self.ex_pj_lot.lot1]
        self.traits2 = [TRAITS_STR, self.ex_pj_lot.lot2]
        self.traits3 = [TRAITS_STR, self.ex_pj_lot.lot3]
        self.traits4 = [TRAITS_STR, self.ex_pj_lot.lot4]
        self.traits_dup = [TRAITS_STR, self.ex_pj_lot.lot_dup]

        self.fat_food_n1 = [FAT_FOOD_STR, -1]
        self.fat_food_0 = [FAT_FOOD_STR, 0]
        self.fat_food_1 = [FAT_FOOD_STR, 1]
        self.fat_food_max = [FAT_FOOD_STR, SPECIES_MAX_POP]
        self.fat_food_max_p1 = [FAT_FOOD_STR, SPECIES_MAX_POP + 1]
        self.fat_food_10 = [FAT_FOOD_STR, 10]

        self.spe_0 = [self.food_0, self.body_0, self.pop_0, self.traits0]
        self.spe_1 = [self.food_1, self.body_1, self.pop_1, self.traits1]
        self.spe_max = [self.food_max, self.body_max, self.pop_max,
                        self.traits3]
        self.spe_max_f1 = [self.food_max_p1, self.body_max, self.pop_max,
                           self.traits3]
        self.spe_max_b1 = [self.food_max, self.body_max_p1, self.pop_max,
                           self.traits3]
        self.spe_max_p1 = [self.food_max, self.body_max, self.pop_max_p1,
                           self.traits3]
        self.spe_dup = [self.food_0, self.body_0, self.pop_0, self.traits_dup]
        self.spe_t4 = [self.food_0, self.body_0, self.pop_0, self.traits4]

        self.coop_default = [["food", 0],
                             ["body", 0],
                             ["population", 1],
                             ["traits", [self.ex_pj_traits.cooperation]]]

        self.fora_default = [["food", 0],
                             ["body", 0],
                             ["population", 1],
                             ["traits", [self.ex_pj_traits.foraging]]]


class ExampleTraitTypes:
    def __init__(self):
        self.horn_type = HornCard
        self.carn_type = CarnivoreCard
        self.amb_type = AmbushCard
        self.burr_type = BurrowingCard
        self.climb_type = ClimbingCard
        self.shell_type = HardShellCard
        self.herd_type = HerdingCard
        self.symb_type = SymbiosisCard
        self.warn_type = WarningCallCard
        self.coop_type = CooperationCard
        self.fat_type = FatTissueCard
        self.fert_type = FertileCard
        self.fora_type = ForagingCard
        self.long_type = LongNeckCard
        self.pack_type = PackHuntingCard
        self.scav_type = ScavengerCard

        self.all_trait_types = [self.horn_type,
                                self.carn_type,
                                self.amb_type,
                                self.burr_type,
                                self.climb_type,
                                self.shell_type,
                                self.herd_type,
                                self.symb_type,
                                self.warn_type,
                                self.coop_type,
                                self.fat_type,
                                self.fert_type,
                                self.fora_type,
                                self.long_type,
                                self.pack_type,
                                self.scav_type]


class ExampleTraits:
    def __init__(self):
        self.ex_trait_types = ExampleTraitTypes()

        """
        Creates a new set of example TraitCards
        """
        self.horn = self.ex_trait_types.horn_type()
        self.carn = self.ex_trait_types.carn_type()
        self.amb = self.ex_trait_types.amb_type()
        self.burr = self.ex_trait_types.burr_type()
        self.climb = self.ex_trait_types.climb_type()
        self.shell = self.ex_trait_types.shell_type()
        self.herd = self.ex_trait_types.herd_type()
        self.symb = self.ex_trait_types.symb_type()
        self.warn = self.ex_trait_types.warn_type()
        self.coop = self.ex_trait_types.coop_type()
        self.fat = self.ex_trait_types.fat_type()
        self.fat_min = self.ex_trait_types.fat_type(
            stored_food=SPECIES_MIN_BODY_SIZE)
        self.fat3 = self.ex_trait_types.fat_type(stored_food=3)
        self.fat5 = self.ex_trait_types.fat_type(stored_food=5)
        self.fat6 = self.ex_trait_types.fat_type(stored_food=6)
        self.fat_max = self.ex_trait_types.fat_type(
            stored_food=SPECIES_MAX_BODY_SIZE)
        self.fert = self.ex_trait_types.fert_type()
        self.fora = self.ex_trait_types.fora_type()
        self.long = self.ex_trait_types.long_type()
        self.pack = self.ex_trait_types.pack_type()
        self.scav = self.ex_trait_types.scav_type()

        self.all_trait_classes = [CarnivoreCard, AmbushCard, BurrowingCard,
                                  ClimbingCard,
                                  HardShellCard, HerdingCard,
                                  SymbiosisCard, WarningCallCard,
                                  CooperationCard, FatTissueCard,
                                  FertileCard,
                                  ForagingCard, LongNeckCard, PackHuntingCard,
                                  ScavengerCard]
        self.classes_with_default_food_points = [x for x in
                                                 self.all_trait_classes if
                                                 x != CarnivoreCard]
        self.classes_with_generic_atk_body_size = [x for x in
                                                   self.all_trait_classes if
                                                   x != PackHuntingCard]
        self.classes_block_attacks = [BurrowingCard, ClimbingCard,
                                      HardShellCard, HerdingCard,
                                      SymbiosisCard,
                                      WarningCallCard]
        self.classes_cant_block_attacks = [x for x in self.all_trait_classes if
                                           x not in self.classes_block_attacks]


class ExampleTraitList:
    def __init__(self):
        self.ex_traits = ExampleTraits()

        self.lot0 = []
        self.lot1 = [self.ex_traits.carn]
        self.lot2 = [self.ex_traits.carn, self.ex_traits.amb]
        self.lot3 = [self.ex_traits.carn, self.ex_traits.amb,
                     self.ex_traits.burr]
        self.lot4 = [self.ex_traits.carn, self.ex_traits.amb,
                     self.ex_traits.burr, self.ex_traits.climb]


class ExampleSpecies:
    def __init__(self):
        """ Creates a new ExampleSpecies with all of the example species initialized
        """
        self.ex_traits = ExampleTraits()

        self.spe_0 = Species(0, 0, 0, [])
        self.spe_1 = Species(1, 1, 1, [CarnivoreCard(0)])
        self.spe_max = Species(7, 7, 7, [CarnivoreCard(0), AmbushCard(0),
                                         BurrowingCard(0)])

        # Normal (trait-less) species
        self.norm_default = Species()
        self.norm_bstart3 = Species(body_size=(3 + SPECIES_START_BODY_SIZE))
        self.norm_bstart3_f1 = Species(body_size=(3 + SPECIES_START_BODY_SIZE),
                                       num_food_tokens=1)
        self.norm_bstart4 = Species(body_size=(4 + SPECIES_START_BODY_SIZE))
        self.norm_bstartshell = Species(
            body_size=(HARD_SHELL_OFFSET + SPECIES_START_BODY_SIZE))
        self.norm_bmax = Species(body_size=SPECIES_MAX_BODY_SIZE)
        self.norm_pstart2 = Species(population=(2 + SPECIES_START_POP))
        self.norm_bstart3_pstart2 = Species(
            body_size=(3 + SPECIES_START_BODY_SIZE),
            population=(2 + SPECIES_START_POP))
        self.norm_fed1_p2 = Species(num_food_tokens=1, population=2)
        self.norm_fed3_p4 = Species(num_food_tokens=3, population=4)

        # Carnivore species
        self.carn_default = Species(played_cards=[self.ex_traits.carn])
        self.carn_pstart1 = Species(population=1 + SPECIES_START_POP,
                                    played_cards=[self.ex_traits.carn])
        self.carn_pstart1_bstart3 = Species(population=1 + SPECIES_START_POP,
                                            body_size=3 + SPECIES_START_BODY_SIZE,
                                            played_cards=[self.ex_traits.carn])
        self.carn_bstart3 = Species(body_size=3 + SPECIES_START_BODY_SIZE,
                                    played_cards=[self.ex_traits.carn])
        self.carnamb_default = Species(
            played_cards=[self.ex_traits.carn, self.ex_traits.amb])
        self.carnamb_pstart2 = Species(population=2 + SPECIES_START_POP,
                                       played_cards=[self.ex_traits.carn,
                                                     self.ex_traits.amb])
        self.carn_scav = Species(
            played_cards=[self.ex_traits.carn, self.ex_traits.scav])
        self.carn_coop_pstart1 = Species(
            population=1 + SPECIES_START_POP,
            played_cards=[self.ex_traits.carn, self.ex_traits.coop])

        # Burrowing species
        self.burr_fstart_pstart = Species(num_food_tokens=SPECIES_START_FOOD,
                                          population=SPECIES_START_POP,
                                          played_cards=[self.ex_traits.burr])
        self.burr_fstart1_pstart = Species(
            num_food_tokens=1 + SPECIES_START_FOOD,
            population=SPECIES_START_POP,
            played_cards=[self.ex_traits.burr])
        self.burr_fstart2_pstart2 = Species(
            num_food_tokens=2 + SPECIES_START_FOOD,
            population=2 + SPECIES_START_POP,
            played_cards=[self.ex_traits.burr])
        self.burr_fstart3_pstart2 = Species(
            num_food_tokens=3 + SPECIES_START_FOOD,
            population=2 + SPECIES_START_POP,
            played_cards=[self.ex_traits.burr])

        # Climbing species
        self.climb_default = Species(played_cards=[self.ex_traits.climb])
        self.climb_default_2 = Species(played_cards=[self.ex_traits.climb])
        self.climb_bstart3 = Species(body_size=3 + SPECIES_START_BODY_SIZE,
                                     played_cards=[self.ex_traits.climb])

        # Cooperation Species
        self.coop_default = Species(played_cards=[self.ex_traits.coop])
        self.carn_coop_default = Species(
            played_cards=[self.ex_traits.carn, self.ex_traits.coop])

        # Fat Tissue Species
        self.fat_default = Species(played_cards=[self.ex_traits.fat])
        self.fat_min = Species(body_size=4,
                               played_cards=[self.ex_traits.fat_min])
        self.fat3 = Species(body_size=3, played_cards=[self.ex_traits.fat3])
        self.fat5 = Species(body_size=6, played_cards=[self.ex_traits.fat5])
        self.fat_max = Species(body_size=SPECIES_MAX_BODY_SIZE,
                               played_cards=[self.ex_traits.fat_max])
        self.carn_fat_default = Species(
            played_cards=[self.ex_traits.carn, self.ex_traits.fat])
        self.carn_fat_coop_default = Species(
            played_cards=[self.ex_traits.carn, self.ex_traits.fat,
                          self.ex_traits.coop])

        # Fef Fat Tissue Species
        self.fat5_fed1_b6 = Species(body_size=6, population=SPECIES_MAX_POP,
                                    played_cards=[self.ex_traits.fat5],
                                    num_food_tokens=1)

        self.fat6_fed1_b6 = Species(body_size=6,
                                    population=SPECIES_MAX_POP,
                                    played_cards=[self.ex_traits.fat6],
                                    num_food_tokens=1)

        self.fat3_fed2_b5 = Species(body_size=5, population=SPECIES_MAX_POP,
                                    played_cards=[self.ex_traits.fat3],
                                    num_food_tokens=2)
        self.fat_min_fedmax_bmax = Species(body_size=SPECIES_MAX_BODY_SIZE,
                                           population=SPECIES_MAX_POP,
                                           played_cards=[
                                               self.ex_traits.fat_min],
                                           num_food_tokens=SPECIES_MAX_BODY_SIZE)
        self.fat_max_fed0_bmax = Species(body_size=SPECIES_MAX_BODY_SIZE,
                                         population=SPECIES_MAX_POP,
                                         played_cards=[self.ex_traits.fat_max],
                                         num_food_tokens=SPECIES_MAX_BODY_SIZE)

        # Fat Species with the same Body - Fat already store
        self.fat5_bd6_popmax_food1 = Species(body_size=6,
                                             population=SPECIES_MAX_POP,
                                             played_cards=[self.ex_traits.fat5],
                                             num_food_tokens=1)
        self.fat3_bd4_popmax_food1 = Species(body_size=4,
                                             population=SPECIES_MAX_POP,
                                             played_cards=[self.ex_traits.fat3],
                                             num_food_tokens=1)
        self.fat3_bd4_pop4_food1 = Species(body_size=4,
                                           population=4,
                                           played_cards=[self.ex_traits.fat3],
                                           num_food_tokens=1)
        self.fat3_bd4_pop4_food3 = Species(body_size=4,
                                           population=4,
                                           played_cards=[self.ex_traits.fat3],
                                           num_food_tokens=3)

        # Foraging Species
        self.fora_default = Species(played_cards=[self.ex_traits.fora])
        self.carn_fora_default = Species(
            played_cards=[self.ex_traits.carn, self.ex_traits.fora])

        # Hard Shell species
        self.shell_default = Species(played_cards=[self.ex_traits.shell])
        self.shell_bstart3 = Species(body_size=3 + SPECIES_START_BODY_SIZE,
                                     played_cards=[self.ex_traits.shell])

        # Herding species
        self.herd_default = Species(played_cards=[self.ex_traits.herd])
        self.herd_pstart1 = Species(population=1 + SPECIES_START_POP,
                                    played_cards=[self.ex_traits.herd])
        self.herd_pstart2 = Species(population=2 + SPECIES_START_POP,
                                    played_cards=[self.ex_traits.herd])

        # Scavanger species
        self.scav_default = Species(played_cards=[self.ex_traits.scav])

        # Symbiosis species
        self.symb_default = Species(played_cards=[self.ex_traits.symb])
        self.symb_bstart3 = Species(body_size=3 + SPECIES_START_BODY_SIZE,
                                    played_cards=[self.ex_traits.symb])

        # Warning call
        self.warn_default = Species(played_cards=[self.ex_traits.warn])
        self.warn_default2 = Species(played_cards=[self.ex_traits.warn])

        # Pack Hunting species
        self.pack_bstart_pstart = Species(body_size=SPECIES_START_BODY_SIZE,
                                          population=SPECIES_START_POP,
                                          played_cards=[self.ex_traits.pack])
        self.pack_bstart_pstart2 = Species(body_size=SPECIES_START_BODY_SIZE,
                                           population=SPECIES_START_POP + 2,
                                           played_cards=[self.ex_traits.pack])
        self.pack_bstart3_pstart2 = Species(
            body_size=SPECIES_START_BODY_SIZE + 3,
            population=SPECIES_START_POP + 2,
            played_cards=[self.ex_traits.pack])


        # Fertile species
        self.fert_p7 = Species(population=7, played_cards=[self.ex_traits.fert])

        # Combination species
        self.fert_long_fora = Species(played_cards=[self.ex_traits.long,
                                                    self.ex_traits.fert,
                                                    self.ex_traits.fora])

        # fed species
        self.coop_default_fed = Species(played_cards=[self.ex_traits.coop],
                                        num_food_tokens=1 + SPECIES_START_FOOD)
        self.fora_default_fed = Species(played_cards=[self.ex_traits.fora],
                                        num_food_tokens=1 + SPECIES_START_FOOD)
        self.carn_fat_default_attack = Species(
            played_cards=[self.ex_traits.carn, self.ex_traits.fat],
            num_food_tokens=1 + SPECIES_START_FOOD)

        self.norm_pstart2_fed = Species(population=(1 + SPECIES_START_POP),
                                        num_food_tokens=1 + SPECIES_START_FOOD)

        # attacked species
        self.norm_pstart2_attacked = Species(population=(1 + SPECIES_START_POP))

        # test fest
        self.test1_species1 = Species(body_size=1,
                                      played_cards=[self.ex_traits.coop])
        self.test1_species2 = Species(body_size=1,
                                      played_cards=[self.ex_traits.horn,
                                                    self.ex_traits.coop])
        self.test1_species3 = Species(body_size=1)


class ExamplePlayerStates:
    def __init__(self):
        self.ex_species = ExampleSpecies()

        self.default = IPlayer(Player(), 1)
        self.burr_veg = IPlayer(Player(), 2, [self.ex_species.burr_fstart1_pstart])
        self.carn = IPlayer(Player(), 3, [self.ex_species.carn_default])
        self.coop = IPlayer(Player(), 4, [self.ex_species.coop_default])
        self.carn_coop = IPlayer(Player(), 5, [self.ex_species.carn_coop_default])
        self.fat_default = IPlayer(Player(), 6, [self.ex_species.fat_default])
        self.fat_min = IPlayer(Player(), 7, [self.ex_species.fat_min])
        self.fat3 = IPlayer(Player(), 8, [self.ex_species.fat3])
        self.fat5 = IPlayer(Player(), 9, [self.ex_species.fat5])
        self.fat_max = IPlayer(Player(), 10, [self.ex_species.fat_max])
        self.carn_fat = IPlayer(Player(), 11, [self.ex_species.carn_fat_default])
        self.carn_fat_coop = IPlayer(Player(), 12, [
            self.ex_species.carn_fat_coop_default])
        self.fora = IPlayer(Player(), 13, [self.ex_species.fora_default])
        self.carn_fora = IPlayer(Player(), 14, [self.ex_species.carn_fora_default])

        self.burr_and_fat = IPlayer(Player(),
                                        15,
                                        [self.ex_species.burr_fstart1_pstart,
                                         self.ex_species.fat5_fed1_b6])
        self.carn_coop_and_fat = IPlayer(Player(),
                                             16,
                                             [self.ex_species.carn_coop_default,
                                              self.ex_species.fat3_fed2_b5])
        self.carn_coop_and_fat_and_fat = IPlayer(Player(),
                                                     17, [
                                                         self.ex_species.carn_coop_default,
                                                         self.ex_species.fat_max_fed0_bmax,
                                                         self.ex_species.fat_min_fedmax_bmax])
        self.fat_and_carn_and_shell_veg = IPlayer(Player(),
                                                      18, [
                                                          self.ex_species.carn_coop_default,
                                                          self.ex_species.fat_min_fedmax_bmax,
                                                          self.ex_species.norm_bstartshell])
        self.carn_coop_and_warn = IPlayer(Player(),
                                              19,
                                              [
                                                  self.ex_species.carn_coop_default,
                                                  self.ex_species.warn_default])

        self.scav_and_carn_coop_and_veg = IPlayer(
            Player(),
            2,
            [
                self.ex_species.scav_default,
                self.ex_species.carn_coop_default,
                self.ex_species.norm_bstart3])

        self.carn_scav_and_carn_coop_and_carn = IPlayer(
            Player(),
            2,
            [
                self.ex_species.carn_scav,
                self.ex_species.carn_coop_pstart1,
                self.ex_species.carn_default
            ]
        )

        self.player_state_with_4 = IPlayer(
            Player(),
            21,
            [self.ex_species.norm_default,
             self.ex_species.norm_bstart3,
             self.ex_species.norm_bstart4,
             self.ex_species.norm_fed3_p4])

        self.norm = IPlayer(Player(), 1, [self.ex_species.norm_default])

        self.norm_pstart_2 = IPlayer(Player(), 1, [self.ex_species.norm_pstart2])

        self.fert_long_fora = IPlayer(Player(), 3, [self.ex_species.fert_long_fora])

        # player states after evolution
        self.coop_fed = IPlayer(Player(), 4, [self.ex_species.coop_default_fed])
        self.fora_fed = IPlayer(Player(), 13, [self.ex_species.fora_default_fed])
        self.burr_and_fat_store = IPlayer(Player(), 15,
                                              [
                                                  self.ex_species.burr_fstart1_pstart,
                                                  self.ex_species.fat6_fed1_b6])

        # Player states after attacking
        self.carn_fat_attack = IPlayer(Player(), 11, [
            self.ex_species.carn_fat_default_attack])

        # player states after being attacked
        self.norm_pstart_2_attacked = IPlayer(Player(), 1, [
            self.ex_species.norm_pstart2_attacked])

        # player states with hand
        self.player_state_with_hand = IPlayer(Player(), 21,
                                                  [self.ex_species.carn_default,
                                                   self.ex_species.norm_bstart3],
                                                  hand=[CarnivoreCard(1),
                                                        CooperationCard(2)])

        self.silly_choice_json_1 = IPlayer(Player(), 123,
                                                    [self.ex_species.carn_default,
                                                     self.ex_species.norm_bstart3],
                                                    hand=[AmbushCard(-3),
                                                          BurrowingCard(2),
                                                          CarnivoreCard(3)])

        self.silly_choice_json_3 = IPlayer(Player(), 34,
                                                    [self.ex_species.carn_default,
                                                     self.ex_species.norm_bstart3],
                                                    hand=[AmbushCard(-3),
                                                          BurrowingCard(2),
                                                          CarnivoreCard(3),
                                                          HornCard(0),
                                                          PackHuntingCard(1),
                                                          PackHuntingCard(2),
                                                          PackHuntingCard(3)], )

        # test fest
        self.test1_player1 = IPlayer(Player(),
                                         1,
                                         [self.ex_species.test1_species1,
                                          self.ex_species.test1_species2,
                                          self.ex_species.test1_species3])

        self.step4_1_p1 = IPlayer(Player(),
                                      1,
                                      [self.ex_species.norm_bstart3,
                                       self.ex_species.norm_bstart3_f1,
                                       self.ex_species.carn_bstart3],
                                      hand=[CarnivoreCard(3),
                                            ClimbingCard(2)])

        self.step4_1_p2 = IPlayer(Player(),
                                      2,
                                      [copy(self.ex_species.norm_bstart3),
                                       self.ex_species.climb_bstart3],
                                      hand=[CarnivoreCard(-3),
                                            ClimbingCard(-2)])
        self.step4_1_p3 = IPlayer(Player(),
                                      3,
                                      [copy(self.ex_species.norm_bstart3_f1)],
                                      hand=[CarnivoreCard(0),
                                            ClimbingCard(0)])

        self.step4_2_p1 = IPlayer(Player(),
                                      1,
                                      [self.ex_species.coop_default_fed],
                                      hand=[CarnivoreCard(-3),
                                            ClimbingCard(2)])

        self.step4_2_p2 = IPlayer(Player(),
                                      2,
                                      [self.ex_species.fora_default_fed],
                                      hand=[CarnivoreCard(-4),
                                            ClimbingCard(-2)])
        self.step4_2_p3 = IPlayer(Player(),
                                      3,
                                      [self.ex_species.fora_default_fed],
                                      hand=[CarnivoreCard(3),
                                            ClimbingCard(0)])

        self.step4_2_p3 = IPlayer(Player(),
                                      3,
                                      [self.ex_species.fora_default_fed],
                                      hand=[CarnivoreCard(3),
                                            ClimbingCard(0),
                                            HornCard(3)])

        self.attack_carnivore2 = IPlayer(Player(), 2,
                                         [Species(1,0,1,[AmbushCard(3)]), Species(1,0,2,[CarnivoreCard(-4)])])
        self.attack_carnivore3 = IPlayer(Player(), 3,
                                         [Species(1,0,1,[]), Species(0,0,1,[CarnivoreCard(0)])])

        self.attack_carnivore4 = IPlayer(Player(), 4,
                                          [Species(1,0,1,[]), Species(0,0,2,[CarnivoreCard(4)])])
        self.attack_carnivore1 = IPlayer(Player(), 1,
                                          [Species(1,0,1,[AmbushCard(-1)]), Species(0,0,2,[CarnivoreCard(8)])])


class ExampleDealers:
    def __init__(self):
        self.player_states = ExamplePlayerStates()
        self.players = [Player(), Player(), Player(), Player()]

        self.dealer_all_veg = ExampleDealers.make_dealer(self.players[:2],
                                                         [self.player_states.coop,
                                                          self.player_states.fora],
                                                         Deck([]),
                                                         wateringhole=10)

        self.dealer_carn_fat = ExampleDealers.make_dealer(self.players[:2],
                                                          [self.player_states.carn_fat,
                                                           self.player_states.norm_pstart_2],
                                                          Deck([]),
                                                          wateringhole=10)

        self.dealer_burr_fat = ExampleDealers.make_dealer(self.players[:1],
                                                          [self.player_states.burr_and_fat],
                                                          Deck([]),
                                                          wateringhole=10)

        self.dealer_carn_extinct = ExampleDealers.make_dealer(self.players[:2],
                                                              [self.player_states.carn_fat,
                                                               self.player_states.norm],
                                                              Deck([]),
                                                              wateringhole=10)

        self.dealer_feed_veg = ExampleDealers.make_dealer(
            self.players[:2],
            [
                self.player_states.scav_and_carn_coop_and_veg,
                self.player_states.norm],
            Deck([]),
            wateringhole=2)

        self.dealer_feeding_order = ExampleDealers.make_dealer(
            self.players[:2],
            [
                self.player_states.carn_scav_and_carn_coop_and_carn,
                self.player_states.norm],
            Deck([]),
            wateringhole=2)

        self.dealer_fert_long_fora = ExampleDealers.make_dealer(
            self.players[:2],
            [
                self.player_states.fert_long_fora,
                self.player_states.norm
            ],
            Deck([]),
            2
        )

        # Test fest
        self.test1_dealer = ExampleDealers.make_dealer(self.players[:3],
                                                       [self.player_states.test1_player1,
                                                        self.player_states.default,
                                                        self.player_states.default],
                                                       Deck([]),
                                                       7)

        self.dealer_forgo_friends = ExampleDealers.make_dealer(self.players[:2],
                                                               [
                                                                   self.player_states.carn_coop_and_warn,
                                                                   self.player_states.burr_veg],
                                                               Deck([]),
                                                               3)

        self.dealer_step4_1 = ExampleDealers.make_dealer(self.players[:3],
                                                         [self.player_states.step4_1_p1,
                                                          self.player_states.step4_1_p2,
                                                          self.player_states.step4_1_p3],
                                                         Deck([]),
                                                         9)


        self.dealer_step4_2 = ExampleDealers.make_dealer(self.players[:3],
                                                         [self.player_states.step4_2_p1,
                                                          self.player_states.step4_2_p2,
                                                          self.player_states.step4_2_p3],
                                                         Deck([]),
                                                         0)

    @staticmethod
    def make_dealer(players, player_states, deck, wateringhole):
        dealer = Dealer(players, deck, wateringhole)
        dealer.player_states = player_states
        return dealer
