import time as t
import webbrowser as wb

from datetime import datetime
import pyautogui as pyg

from appointment import Appointment
from utils.log_utils import log_event, screenshot_dir, initialize_logs
from utils.utils import get_image_dir
import cv2


def join_meeting(appointment: Appointment):
    print("Your meeting is being launched.")

    # zoom app related
    # webbrowser.register('firefox', None,
    #                     webbrowser.BackgroundBrowser("C://Program Files//Mozilla Firefox//firefox.exe"))
    wb.get().open(appointment.meeting_link, new=2)  # open zoom link in a new window
    log_event("Joined Session " + appointment.meeting_name + " at " + appointment.meeting_link)
    t.sleep(5)  # wait to make sure browser launched, and session started


def act_in_meeting(appointment: Appointment):
    take_screenshot(appointment)
    if appointment.meeting_type == "ZOOM":
        pass
    elif appointment.meeting_type == "WEBEX":
        pass
    else:
        pass
    # enter fullscreen window
    move_cursor("fullscreen.png")
    t.sleep(0.5)
    click_mouse()

    move_cursor("disable_webcam.png")
    t.sleep(0.5)
    click_mouse()
    t.sleep(0.25)

    move_cursor("mute.png")
    t.sleep(0.5)
    click_mouse()
    t.sleep(.025)

    move_cursor("chat.png")
    t.sleep(0.5)
    click_mouse()

    send_message("Hello :) How is everyone doing?")

    move_cursor("exit_fullscreen.png")
    t.sleep(0.5)
    click_mouse()

    move_cursor("minimize.png")
    t.sleep(0.5)
    click_mouse()


def leave_meeting(appointment: Appointment):
    move_cursor("exit_minimized.png")

    click_mouse()
    t.sleep(1)
    move_cursor("exit.png")
    t.sleep(0.5)
    click_mouse()
    log_event("Left Session " + appointment.meeting_name + "\n")


def move_cursor(image, confidence_measure=0.90):
    dir = get_image_dir()
    location = pyg.locateCenterOnScreen(dir + image, confidence=confidence_measure)
    log_event("Looked for " + dir + image)

    pyg.moveTo(location)
    log_event("Moved Mouse Cursor To " + str(location))


def click_mouse():
    pyg.click()


def take_screenshot(appointment: Appointment):
    initialize_logs()
    pyg.screenshot(screenshot_dir + (str(datetime.today().date()))+"__"+appointment.meeting_name + ".png")


def send_message(message):
    pyg.typewrite(message)
    pyg.press("enter")


