import logging
from urllib.parse import urlencode

from django import template

log = logging.getLogger(__name__)
register = template.Library()


@register.simple_tag(takes_context=True)
def with_get_args(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def unsnake(value):
    return value.replace('_', ' ').title()


@register.filter
def format_timestamp(value):
    if value:
        return value.strftime('%Y-%m-%dT%H:%M')
    return ''


@register.simple_tag(takes_context=True)
def time_select_options(context, selected_time):
    times = dict()
    for i in range(0, 24*60, 30):
        minute = i % 60
        hour = i // 60
        times[time(hour=hour, minute=minute)] = False

    if selected_time:
        times[selected_time] = True
    return sorted(times.items())

