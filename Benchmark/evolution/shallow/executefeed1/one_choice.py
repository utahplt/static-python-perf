from executefeed1.feed1result import Feed1Result

class OneChoice(Feed1Result):

    def __init__(self, feeding_choice):
        """
        :param feeding_choice: The evolution choice to be made
        :type feeding_choice: PlayerFeedingChoice
        :return: None
        """
        self.feeding_choice = feeding_choice

    def execute_feed1(self, can_feed_deque, dealer, index):
        self.verify_and_apply(self.feeding_choice, can_feed_deque, dealer, index)

    def __eq__(self, other):
        return isinstance(other, OneChoice) and\
            self.feeding_choice == other.feeding_choice
