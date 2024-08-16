
from .constants import METHOD_CSSD


class BaseCounter:
    method = None
    def __init__(self, race):
        self.race = race
        assert self.race.counting_method == self.method
        self.setup_accumulator()

    def setup_accumulator(self):
        pass

    def count(self, vote_qs):
        pass

    def report_result(self):
        pass


class CSSDCounter(BaseCounter):
    class Accumulator:
        def __init__(self, choices):
            self.choices = list(choices)
            self.counts = dict()
            self.ties = list()
            self.winners = list()
            for current in choices:
                choices.remove(current)
                for choice in choices:
                    self.counts[(current, choice)] = 0
                    self.counts[(choice, current)] = 0

        def count(self, selection):

            for current in selection:
                selection.remove(current)
                for choice in selection:
                    self.counts[(current.slug, choice.slug)] += 1

        def report_result(self):
            choices = list(self.choices)
            for current in choices:
                choices.remove(current)
                for choice in choices:
                    if self.counts[(current, choice)] == self.counts[(choice, current)]:
                        tied_count = self.counts[(choice, current)]
                        self.ties.append(((current, choice), tied_count))
                        self.ties.append(((choice, current), tied_count))
                    elif self.counts[(current, choice)] > self.counts[(choice, current)]:
                        winner_count = (self.counts[(current, choice)], self.counts[(choice, current)])
                        self.winners.append(((current, choice), winner_count))
                    elif self.counts[(choice, current)] > self.counts[(current, choice)]:
                        winner_count = (self.counts[(choice, current)], self.counts[(current, choice)])
                        self.winners.append(((choice, current), winner_count))

    method = METHOD_CSSD

    def setup_accumulator(self):
        choices = list(self.race.choice_set.all().values_list('slug', flat=True))
        self.accumulator = self.Accumulator(choices)

    def count(self, vote_qs):
        votes = vote_qs.values_list('selection', flat=True)

        for vote in votes:
            self.accumulator.count(vote)

    def report_result(self):
        self.accumulator.report_result()
        choices = {c.slug: c for c in self.race.choice_set.all()}

        result = ""
        if self.accumulator.ties:
            result += f"{len(self.accumulator.ties)//2} ties in pairwise elections:\n"
        for candidates, count in self.accumulator.ties:
            candidate0 = choices[candidates[0]]
            candidate1 = choices[candidates[1]]
            result += f"{candidate0.name}, {candidate1.name}: {count}\n"

        result += f"\n\nPairwise election winners:\n"
        for winners, counts in self.accumulator.winners:
            winner = choices[winners[0]]
            loser = choices[winners[1]]
            high, low = counts
            result += f"{winner.name} beat {loser.name}, {high} to {low}\n"

        return result


def counter_for_race(race):
    if race.counting_method == METHOD_CSSD:
        return CSSDCounter(race)

    assert False, f"counter_for_race() doesn't handle {race.counting_method_name} yet."
