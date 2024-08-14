
from django.db import models
# from django.utils import  get_object

# from zionvotes.models import PollOption


def parse_vote_selection(selection_string):
    from zionvotes.models import Choice
    votes = selection_string.split(',')
    output = list()
    try:
        for vote in votes:
            option = Choice.objects.get(slug=vote)
            output.append(option)
    except Choice.DoesNotExist:
        raise

    return output


class VoteSelectionField(models.TextField):
    description = "A selection of one or more votes"

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    def to_python(self, value):
        from zionvotes.models import Choice
        if isinstance(value, list):
            output = list()
            for v in value:
                if isinstance(v, Choice):
                    output.append(v)
                else:
                    output.append(Choice.objects.get(slug=v))
            return output

        if value is None:
            return None

        return parse_vote_selection(value)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value

        return parse_vote_selection(value)

    def value_from_object(self, obj):
        from zionvotes.models import Choice
        values = list()
        if isinstance(obj, list):
            for item in obj:
                if isinstance(item, Choice):
                    values.append(item.slug)
                else:
                    values.append(item)
        return ','.join(values)

    def get_db_prep_value(self, value, connection, prepared=False):
        from zionvotes.models import Choice
        output = list()
        for v in value:
            if isinstance(v, Choice):
                output.append(v.slug)
            else:
                output.append(v)
        return ','.join(output)