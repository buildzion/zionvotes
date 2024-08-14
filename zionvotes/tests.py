from django.test import TestCase

from zionvotes import models, forms


class Poll(TestCase):
    def setUp(self):
        self.poll = models.Race.objects.create(
            title='Test poll',
            description='This is a poll',
            maximum_selections=1,
            slug=models.Race.get_random_slug(),
            open=True,
        )

        self.candidate1 = models.Choice.objects.create(
            poll=self.poll,
            slug=models.Choice.get_random_slug(),
            name="Candidate 1",
        )

        self.candidate2 = models.Choice.objects.create(
            poll=self.poll,
            slug=models.Choice.get_random_slug(),
            name="Candidate 2",
        )

        self.candidate3 = models.Choice.objects.create(
            poll=self.poll,
            slug=models.Choice.get_random_slug(),
            name="Candidate 3",
        )

        self.candidate4 = models.Choice.objects.create(
            poll=self.poll,
            slug=models.Choice.get_random_slug(),
            name="Candidate 4",
        )

    def test_ballot(self):
        selection = [self.candidate1, self.candidate2, self.candidate3]

        ballot = models.Ballot.objects.create(
            poll=self.poll,
            selection=selection,
        )

        loaded_ballot = models.Ballot.objects.get(pk=ballot.pk)

        self.assertEqual(loaded_ballot.selection, selection)

    def test_form_winner_takes_all(self):
        self.poll.maximum_selections = 1
        self.poll.save()

        ballot = models.Ballot(
            poll=self.poll,
        )

        form_data = {
            'selection': self.candidate1.slug,
        }

        form = forms.BallotForm(instance=ballot, data=form_data)
        form.is_valid()
        form.save()

        self.assertEquals(form.instance.selection, [self.candidate1])

    def test_form_winner_takes_all_too_many_votes(self):
        self.poll.maximum_selections = 1
        self.poll.save()

        ballot = models.Ballot(
            poll=self.poll,
        )

        form_data = {
            'selection': f"{self.candidate1.slug},{self.candidate2.slug}",
        }

        form = forms.BallotForm(instance=ballot, data=form_data)
        self.assertFalse(form.is_valid())

        self.assertIn("number of selections exceeded", form.errors['selection'][0])

    def test_form_ranked(self):
        self.poll.maximum_selections = 0
        self.poll.save()

        ballot = models.Ballot(
            poll=self.poll,
        )

        selection = [self.candidate3, self.candidate2, self.candidate4]

        form_data = {
            'selection': ','.join([s.slug for s in selection]),
        }

        form = forms.BallotForm(instance=ballot, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEquals(form.instance.selection, selection)


class Counters(TestCase):
    def setUp(self):
        pass
