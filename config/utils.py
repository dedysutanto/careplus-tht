from datetime import date


def calculate_age(dob):
    today = date.today()
    try:
        age = (today.year - dob.year) \
              - ((today.month, today.day) < (dob.month, dob.day))
    except ValueError:
        age = 0
    return age
