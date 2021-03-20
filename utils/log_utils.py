import os
from datetime import datetime

from utils.utils import get_day

log_dir = "logs"
screenshot_dir = os.path.join(log_dir, "screenshot proof")
log_file = "task.log"


def log_event(event: str):
    initialize_logs()
    event_to_log = str(datetime.now().date()) + "\t" + str(
        datetime.now().time().replace(microsecond=0)) + "\t\t" + event + "\n"
    with open(log_dir + log_file, "a+") as file:
        file.write(event_to_log)


def log_whitespace():
    with open(log_dir + log_file, "a+") as file:
        file.write("\n")


def initialize_logs():
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)

    if not os.path.isdir(screenshot_dir):
        os.mkdir(screenshot_dir)


def print_daily_message():
    print("Today is " + get_day(datetime.today().weekday() + 1) + ". Have a great day!")


def print_joined_message(app_name, app_link):
    print("Joined " + str(app_name) + " at " + str(datetime.now().time().hour) + ":" + str(
        datetime.now().time().minute) + " " + str(app_link))
    print()


def print_left_message(app_name):
    print("Left " + str(app_name) + " at " + str(datetime.now().time().hour) + ":" + str(
        datetime.now().time().minute))
    print()
