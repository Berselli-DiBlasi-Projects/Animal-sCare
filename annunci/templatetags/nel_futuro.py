from datetime import datetime, timedelta, timezone
from django import template
register = template.Library()


@register.filter
def nel_futuro(value):
    now = datetime.now(timezone.utc) + timedelta(hours=2)
    return value > now
