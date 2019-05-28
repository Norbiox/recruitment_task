from datetime import date, datetime
from django.conf import settings


def date_to_string(date_object):
    if date_object is None:
        return None
    if type(date_object) not in [date, datetime]:
        raise TypeError("date_to_string converts only date or datetime types")
    return date_object.strftime(settings.DATE_FORMAT)


def string_to_date(date_string):
    if date_string is None:
        return None
    return datetime.strptime(date_string, settings.DATE_FORMAT).date()
