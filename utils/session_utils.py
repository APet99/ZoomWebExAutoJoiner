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

    # webbrowser.register('firefox', None,
    #                     webbrowser.BackgroundBrowser("C://Program Files//Mozilla Firefox//firefox.exe"))
    wb.get().open(appointment.meeting_link, new=2)  # open link in a new window
    log_event("Joined Session " + appointment.meeting_name + " at " + appointment.meeting_link)
    t.sleep(7.5)  # wait to make sure browser launched, and session started


def act_in_meeting(appointment: Appointment):
    take_screenshot(appointment)
    if appointment.meeting_type == "ZOOM":
        # check if muted
        t.sleep(2)

        if move_cursor("..\\zoom\\stop_video.png"):
            click_mouse()
            t.sleep(1.5)

        if move_cursor("..\\zoom\\mute.png"):
            t.sleep(0.25)
            click_mouse()
            t.sleep(1.5)

        # message in chat
        if appointment.custom_message and move_cursor("..\\zoom\\chat.png"):
            click_mouse()
            t.sleep(0.25)
            send_message(appointment.custom_message)
            log_event("Sent message " + str(appointment.custom_message))

        if move_cursor("..\\zoom\\end.png"):
            click_mouse()
            t.sleep(0.25)

        if move_cursor("..\\zoom\\end_meeting_for_all.png"):
            click_mouse()
            t.sleep(0.25)

        # take screenshot for proof of class
        take_screenshot(appointment)
        log_event("Took Screenshot of session " + appointment.meeting_name)
    elif appointment.meeting_type == "WEBEX":
        print("Webex is not yet supported")
        log_event("Attempted to act in a WEBEX session. This feature is currently not supported.")
    else:
        print("Attempted to join an unsupported Link.")
        log_event("Join link is not ZOOM or WEBEX")
        pass


def move_cursor(image, confidence_measure=0.90):
    dir_loc = get_image_dir()
    location = pyg.locateCenterOnScreen(dir_loc + image, confidence=confidence_measure)
    log_event("Looked for " + dir_loc + image)

    pyg.moveTo(location)
    log_event("Moved Mouse Cursor To " + str(location))
    return location


def click_mouse():
    pyg.click(clicks=1)
    log_event("Clicked")


def take_screenshot(appointment: Appointment):
    initialize_logs()
    pyg.screenshot(screenshot_dir + (str(datetime.today().date())) + "__" + appointment.meeting_name + ".png")


def send_message(message):
    pyg.typewrite(message)
    pyg.press("enter")


def leave_meeting(appointment: Appointment):
    # if we can see fullscreen icon, we are not currently in full screen.
    if move_cursor("..\\zoom\\exit_minimized.png"):
        click_mouse()

    if move_cursor("..\\zoom\\end.png"):
        click_mouse()

    if move_cursor("..\\zoom\\end_meeting_for_all.png"):
        click_mouse()
    log_event("Left Session " + appointment.meeting_name + "\n")
