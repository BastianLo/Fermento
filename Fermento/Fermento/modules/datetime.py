from django import template
register = template.Library()
from django.utils.translation import gettext as _

@register.filter
def duration(td):


    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    label_day = _("day") if days == 1 else _("days")
    label_hour = _("hour") if days == 1 else _("hours")
    label_minute = _("minute") if days == 1 else _("minutes")

    days_str = f'{days} {label_day} ' if days else ''
    hours_str = f'{hours} {label_hour} ' if hours else ''
    minutes_str = f'{minutes} {label_minute} ' if minutes else ''

    return f'{days_str}{hours_str}{minutes_str}'