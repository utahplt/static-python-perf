from evolution.player.player_feeding_choice import PlayerForgoAttack

class Feed1Result:

    def execute_feed1(self, can_feed_deque, dealer, index):
        """
        Executes the feed1 method
        :param can_feed_deque: Indicies of the players
        :type can_feed_deque: [Nat, ...]
        :param players: List of players
        :type players: [Player, ...]
        :param player_states: List of player states
        :type player_states: [PlayerStates, ...]
        :return: None
        """
        raise NotImplementedError('Method not yet implemented')


    def verify_and_apply(self, feeding_choice, can_feed_deque, dealer, index):
        """
        Given a feeding choice, verifies it then
        applies the choice and appends index of
        the can_feed_deque
        :type feeding_choice: PlayerFeedingChoice
        :type dealer: Dealer
        :param index: Index of the current player
        :type index: Nat
        :return: None
        """
        player_states = dealer.player_states
        curr_player = player_states[index]
        if not feeding_choice.verify_self(player_states, curr_player):
            dealer.kick_player(curr_player)

        elif not isinstance(feeding_choice, PlayerForgoAttack):
            feeding_choice.apply_choice(index, dealer)
            can_feed_deque.append(index)


