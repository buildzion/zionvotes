
from django import forms
from django.core.exceptions import ValidationError

from zionvotes import models


class PollSelectionField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        self.race = kwargs.pop('race')
        super(PollSelectionField, self).__init__(*args, **kwargs)
    def prepare_value(self, value):
        if value is None:
            return None
        output = list()
        for item in value:
            output.extend(item.split(','))
        return super().prepare_value(output)

    def clean(self, value):
        # slugs = value.split(',')
        slugs = self.prepare_value(value)
        if not self.to_field_name:
            self.to_field_name = 'slug'

        qs = super().clean(slugs)
        objects = {po.slug: po for po in qs}

        output = list()
        bad_slugs = list()
        races = set()
        race = None
        for slug in slugs:
            if slug not in objects:
                bad_slugs.append(slug)
            else:
                output.append(objects[slug])
                race = objects[slug].race
                races.add(race.title)

        if bad_slugs:
            raise ValidationError(f"Invalid poll options: {', '.join(bad_slugs)}")
        if len(races) > 1:
            raise ValidationError(f"Selection included candidates from different polls! {', '.join(races)}")
        if race.maximum_selections and len(output) > race.maximum_selections:
            raise ValidationError(f"Maxumum number of selections exceeded! max: {race.maximum_selections}, selections: {value}")

        return output


class PollForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.poll = kwargs.pop('poll')
        super().__init__(*args, **kwargs)
        self.poll_fields = list()
        for race in self.poll.race_set.all().order_by('poll_priority', 'created_at'):
            self.fields[race.slug] = PollSelectionField(race=race, queryset=race.choice_set.all())
            # Provide an interable that maintains order
            self.poll_fields.append((race, self.fields[race.slug]))


# class BallotForm(forms.ModelForm):
#     class Meta:
#         model = models.Ballot
#         fields = [
#             'selection',
#         ]
#
#     selection = PollSelectionField(queryset=None, required=True, to_field_name='slug')
#
#     def __init__(self, *args, **kwargs):
#         self.poll = kwargs.pop('poll', None)
#         super().__init__(*args, **kwargs)
#
#         if not self.poll and self.instance:
#             self.poll = self.instance.poll
#
#         self.fields['selection'].queryset = self.poll.choice_set.all()
#
#     def clean_selection(self):
#         selection = self.cleaned_data['selection']
#         return selection


class RaceForm(forms.ModelForm):
    class Meta:
        model = models.Race

        fields = [
            'title',
            'description',
            'maximum_selections',
            'counting_method',
        ]
