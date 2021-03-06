"""'
Zoom/WebEx Auto joiner

"""

from utils.csv_utils import build_appointments_from_csv
from utils.log_utils import print_daily_message
from utils.session_utils import *
from utils.utils import get_meetings_day, time_until_end_of_day, prepare_appointments, get_time_to_next_meeting
from datetime import time as dt_time

__author__ = "Alex Peterson"
__copyright__ = "Copyright 2021"
__version__ = "1.0.0"
__maintainer__ = "Alex Peterson"
__email__ = "PetersonAlex99@gmail.com"
__status__ = "Prototype"

if __name__ == '__main__':
    appointments = build_appointments_from_csv()

    while True:
        # Each iteration is a new day
        print_daily_message()
        meetings_today = get_meetings_day(appointments)
        if not meetings_today:
            print("There are no meetings scheduled today. I am sleeping for the rest of the day. See you tomorrow! :)")
            t.sleep(time_until_end_of_day() + 1)
            continue

        sorted_appointments = prepare_appointments(meetings_today)
        for app in sorted_appointments:
            print(str(app.meeting_name) + " starts in " + str(get_time_to_next_meeting(app.get_meeting_start_time())))
            t.sleep(get_time_to_next_meeting(app.get_meeting_start_time()).seconds)

            # join meeting
            join_meeting(app)

            # meeting procedure
            act_in_meeting(app)

            # leave when necessary
            msg= ""
            if app.meeting_end_time != dt_time(0, 0, 0):
                # t.sleep(get_time_to_next_meeting(app.meeting_end_time).seconds - 1)
                # leave_meeting(app)
                msg = "You currently must leave sessions manually. This feature will be supported in the future."
                print(msg)
                log_event(msg)
                pass
            else:
                msg = "No End Time Specified. You must exit the meeting manually."
                log_event(msg)
                print(msg)
        print("All meetings for the day were completed. Check Back tomorrow.")
        t.sleep(time_until_end_of_day() + 1)
