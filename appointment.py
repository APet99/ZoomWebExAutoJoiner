from datetime import time


class Appointment:
    def __init__(self, name: str, link: str, days: str, start_time_str: str, end_time_str: str = "", id: str = None,
                 password: str = None, message: str = None):
        self.meeting_name = name.strip()
        self.meeting_link = link
        self.meeting_days = convert_days_to_int(days)
        self.meeting_start_time = to_time_object(start_time_str)
        self.meeting_end_time = to_time_object(end_time_str)
        self.meeting_id = id
        self.meeting_password = password
        self.custom_message = message
        self.meeting_type = self.get_meeting_type()

    def get_meeting_name(self):
        return self.meeting_name

    def get_meeting_link(self):
        return self.meeting_link

    def get_meeting_days(self):
        return self.meeting_days

    def get_meeting_start_time(self):
        return self.meeting_start_time

    def get_meeting_end_time(self):
        return self.meeting_end_time

    def get_meeting_id(self):
        return self.meeting_id

    def get_meeting_password(self):
        return self.meeting_password

    def get_custom_message(self):
        return self.custom_message

    def get_meeting_type(self):
        if "ZOOM" in self.meeting_link.upper():
            return "ZOOM"
        elif "WEBEX" in self.meeting_link.upper():
            return "WEBEX"
        else:
            return None

    def to_string(self):
        return 'Meeting Name: {}\n' \
               'Link:{}\n' \
               'Days: {}\n' \
               'Start Time: {}\n' \
               'End Time: {}\n' \
               'ID: {}\n' \
               'Password: {}\n' \
               'Message {}\n'.format(self.meeting_name, self.meeting_link, self.meeting_days,
                                     self.meeting_start_time, self.meeting_end_time, self.meeting_id,
                                     self.meeting_password, str(self.custom_message))


map_days = {'M': (1, 'Monday'), 'T': (2, 'Tuesday'), 'W': (3, 'Wednesday'), 'R': (4, 'Thursday'), 'F': (5, 'Friday'),
            'S': (6, 'Saturday'), 'U': (7, 'Sunday')}


def convert_days_to_int(days):
    number_representation_of_days = 0
    digit_shift = 1

    for day in reversed(days):

        if day.upper() in map_days.keys():
            number_representation_of_days += (digit_shift * map_days.get(day.upper())[0])
            digit_shift *= 10
    return number_representation_of_days


def to_time_object(time_str: str):
    if not time_str:
        return time(0, 0)
    time_list = format_time(time_str)
    return time(hour=time_list[0], minute=time_list[1], second=time_list[2])


def format_time(x):
    t = x.split(sep="-")
    return list(map(int, t))
