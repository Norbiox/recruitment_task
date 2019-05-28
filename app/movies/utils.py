from datetime import date, datetime
from django.conf import settings
from django.http import HttpResponse


def date_to_string(date_object):
    if date_object is None or date_object == "N/A":
        return None
    if type(date_object) not in [date, datetime]:
        raise TypeError("date_to_string converts only date or datetime types")
    return date_object.strftime(settings.DATE_FORMAT)


def string_to_date(date_string):
    if date_string is None or date_string == "N/A":
        return None
    return datetime.strptime(date_string, settings.DATE_FORMAT).date()


def get_parameter_or_400(request_query_dict, parameter_name):
    try:
        return request_query_dict.get(parameter_name)
    except KeyError as e:
        return HttpResponse(f"{parameter_name} field is required", 400)
