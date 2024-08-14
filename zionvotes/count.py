
from .constants import METHOD_CSSD


class BaseCounter:
    method = None
    def __init__(self, race):
        self.race = race
        assert self.race.counting_method == self.method
        self.accumulator = None


    def setup_accumulator(self):
        pass

    def count(self, vote_qs):
        pass


class CSSDCounter(BaseCounter):
    class Accumulator:
        def __init__(self, choices):
            self.counts = dict()
            for current in choices:
                choices.remove(current)
                for choice in choices:
                    self.counts[(current, choice)] = 0
                    self.counts[(choice, current)] = 0

        def count(self, selection):

            for current in selection:
                selection.pop()
            pass


    method = METHOD_CSSD

    def setup_accumulator(self):
        choices = list(self.race.choice_set.all().values_list('slug', flat=True))
        self.accumulator = self.Accumulator(choices)

    def count(self, vote_qs):
        votes = vote_qs.values_list('selection', flat=True)

        for vote in votes:
            self.accumulator.count(vote)

