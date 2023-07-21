from evolution.player.player_feeding_choice import PlayerForgoAttack
from evolution.timeout import TimeoutError
from evo_json.data_def import ConvertPyJSONError
from executefeed1.feed1result import Feed1Result


class MultipleChoices(Feed1Result):
    """
    To represent multiple evolution choices for the player
    """

    def execute_feed1(self, can_feed_deque, dealer, index):
        """
        Executes a evolution when evolution choices > 2
        """
        player_state = dealer.player_states[index]
        try:
            feeding_choice = player_state.choose_feeding(dealer.wateringhole, dealer.player_states)
            self.verify_and_apply(feeding_choice, can_feed_deque, dealer, index)

        except (TimeoutError, ConvertPyJSONError):
            dealer.kick_player(player_state)

    def __eq__(self, other):
        return isinstance(other, MultipleChoices)