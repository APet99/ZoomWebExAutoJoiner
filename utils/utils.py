import os
from datetime import datetime, time
from operator import attrgetter
# from sys import platform
import platform
from pathlib import Path
from appointment import Appointment, map_days


def get_meetings_day(appointments, day=datetime.today().weekday() + 1):
    appointments_on_day = []
    for a in appointments:
        if str(day) in str(a.get_meeting_days()):
            appointments_on_day.append(a)
    return appointments_on_day


def remove_passed_appointments(appointments: list):
    reduced_appointments = []

    for app in appointments:

        if datetime.now().time() < app.meeting_start_time:
            reduced_appointments.append(app)
    return reduced_appointments


def time_until_end_of_day(dt=None):
    if dt is None:
        dt = datetime.now()
    return ((24 - dt.hour - 1) * 60 * 60) + ((60 - dt.minute - 1) * 60) + (60 - dt.second)


def sort_appointments_by_time(appointments):
    sorted_appointments = sorted(appointments, key=attrgetter('meeting_start_time'))
    return sorted_appointments


def prepare_appointments(appointments: list) -> list:
    sorted_appointments = sort_appointments_by_time(appointments)
    return remove_passed_appointments(sorted_appointments)


def get_time_to_next_meeting(meeting_time: datetime.time, current_time=datetime.now().time()):
    now = datetime.combine(datetime.today(), current_time)
    app = datetime.combine(datetime.today(), meeting_time)
    return app - now


def get_time_to_meeting(appointment: Appointment, current_time=datetime.now().time()):
    now = datetime.combine(datetime.today(), current_time)
    app = datetime.combine(datetime.today(), appointment.meeting_start_time)
    return app - now


def get_day(day: int):
    if day < 1 or day > 7:
        raise ValueError("Attempted to get an invalid day.")

    for value in map_days.values():
        if value[0] is day:
            return value[1]


def format_date(x):
    date = x.split(sep="-")
    return list(map(int, date))


def given_datetime(date, t):
    # YY, MM, DD, HH, MM
    return datetime(date[2], date[1], date[0], t[0], t[1], t[2])


def get_image_dir():
    return Path(f'images')
