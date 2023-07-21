from executefeed1.feed1result import Feed1Result

class NoChoice(Feed1Result):

    def execute_feed1(self, can_feed_deque, dealer, index):
        pass

    def __eq__(self, other):
        return isinstance(other, NoChoice)