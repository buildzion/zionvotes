
from zionvotes.constants import METHOD_WINNER_TAKES_ALL, METHOD_IRV, METHOD_CSSD


class BaseVoteCounter:
    def __init__(self, race):
        self.race = race

    def add_vote(self, selection_slugs):
        pass

    def evaluate_winner(self):
        pass
