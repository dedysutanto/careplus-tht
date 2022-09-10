from datetime import date
from django.utils.timezone import now


def calculate_age(dob):
    today = date.today()
    try:
        age = (today.year - dob.year) \
              - ((today.month, today.day) < (dob.month, dob.day))
    except ValueError:
        age = 0
    return age


def time_different(datetime):
    delta = datetime - now()
    t_secs = delta.total_seconds()
    t_hours = int(t_secs / (60 * 60))

    if delta.days > 1:
        result_txt = '{} days'.format(delta.days)
    elif delta.days > 0:
        result_txt = '{} day'.format(delta.days)
    elif t_hours > 0:
        result_txt = '{} hour'.format(t_hours)
    elif t_secs > 0:
        result_txt = 'Now'
    else:
        result_txt= 'Expired'

    return result_txt
