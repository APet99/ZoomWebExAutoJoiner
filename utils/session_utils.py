import subprocess
import time as t
import webbrowser

from datetime import datetime
import pyautogui as pyg
import cv2
import platform
from pathlib import Path
from appointment import Appointment
from utils.log_utils import log_event, screenshot_dir, initialize_logs
from utils.utils import get_image_dir

def join_meeting(appointment: Appointment):
    print('Your meeting is being launched.')

    os = platform.system()
    p = subprocess
    if os == 'Windows':
        p.Popen(f'start {appointment.meeting_link}', shell=True)

    elif os == 'Darwin':
        p.Popen(f'open -a {appointment.meeting_link}', shell=True)

    else:
        raise EnvironmentError(f'ERROR: Unsupported OS. {os}')
    log_event(f'Joined Session {appointment.meeting_name} at {appointment.meeting_link}.')
    t.sleep(7.5)  # wait to make sure browser launched, and session started


def act_in_meeting(appointment: Appointment):
    take_screenshot(appointment)
    if appointment.meeting_type == 'ZOOM' or appointment.meeting_type == 'WEBEX':
        t.sleep(2)

        if move_cursor(folder=appointment.meeting_type, image='stop_video', theme='light') or \
                move_cursor(folder=appointment.meeting_type, image='stop_video', theme='dark'):
            click_mouse()
            t.sleep(1.5)

        if move_cursor(folder=appointment.meeting_type, image='mute', theme='light') or \
                move_cursor(folder=appointment.meeting_type, image='mute', theme='dark'):
            t.sleep(0.25)
            click_mouse()
            t.sleep(1.5)

        if appointment.meeting_type == 'WEBEX':
            if move_cursor(folder=appointment.meeting_type, image='join_meeting', theme='light') or \
                    move_cursor(folder=appointment.meeting_type, image='join_meeting', theme='dark'):
                click_mouse()
                t.sleep(1.5)
        # message in chat
        if appointment.custom_message and (move_cursor(folder=appointment.meeting_type, image='chat', theme='light') or
                                           move_cursor(folder=appointment.meeting_type, image='chat', theme='dark')):
            click_mouse()
            t.sleep(0.25)

            if appointment.meeting_type == 'WEBEX' and ((move_cursor(folder=appointment.meeting_type, image='please_select', theme='light') or
                                           move_cursor(folder=appointment.meeting_type, image='please_select', theme='dark'))):
                click_mouse()
                t.sleep(0.25)

                if (move_cursor(folder=appointment.meeting_type, image='everyone', theme='light') or move_cursor(folder=appointment.meeting_type, image='everyone', theme='dark')):
                    click_mouse()
                    t.sleep(0.25)

            send_message(appointment.custom_message)
            log_event(f'Sent message {str(appointment.custom_message)}')

        # take screenshot for proof of class
        take_screenshot(appointment)
        log_event(f'Took Screenshot of session {appointment.meeting_name}')

    else:
        print('Attempted to join an unsupported Link.')
        log_event(f'ERROR: Meeting link \"{appointment.meeting_link}\" is not ZOOM or WEBEX link.')


def move_cursor(folder: str, image: str, theme='light', confidence_measure=0.90):
    img_dir = get_image_dir()
    img_path = img_dir
    if folder.upper() == 'ZOOM' or folder.upper() == 'WEBEX':
        img_path = Path(f'{img_path}\\{folder}\\{image}_{theme}.png')
    else:
        img_path = Path(f'{img_path}\\os\\{folder}\\{image}.png')
    try:
        log_event(f'Looked for: {str(img_path)}')
        location = pyg.locateCenterOnScreen(str(img_path), confidence=confidence_measure)
        pyg.moveTo(location)
        log_event(f'Moved Mouse Cursor To {str(location)}')
        return location
    except Exception:
        pass

    return None


def click_mouse():
    pyg.click(clicks=1)
    log_event('Clicked')


def take_screenshot(appointment: Appointment):
    initialize_logs()
    pyg.screenshot(screenshot_dir + (str(datetime.today().date())) + "__" + appointment.meeting_name + '.png')


def send_message(message):
    pyg.typewrite(message)
    pyg.press("enter")


def leave_meeting(appointment: Appointment):
    if appointment.meeting_type == 'ZOOM':
        if move_cursor(folder='zoom', image='leave', theme='light') or move_cursor(folder='zoom', image='leave', theme='dark'):
            click_mouse()

        if move_cursor(folder='zoom', image='leave_meeting', theme='light') or move_cursor(folder='zoom', image='leave_meeting_red', theme='light') or \
                move_cursor(folder='zoom', image='leave_meeting', theme='dark') or move_cursor(folder='zoom', image='leave_meeting_red', theme='dark'):
            click_mouse()

        log_event(f'Left Session {appointment.meeting_name}\n')

    elif appointment.meeting_type == 'WEBEX':
        if move_cursor(folder='webex', image='end_meeting', theme='light') or move_cursor(folder='webex', image='end_meeting', theme='dark'):
            click_mouse()

        if move_cursor(folder='webex', image='end_meeting_text', theme='light') or move_cursor(folder='webex', image='end_meeting_text', theme='dark'):
            click_mouse()

        log_event(f'Left Session {appointment.meeting_name}\n')
    else:
        err = f'ERROR: Attempting to close unknown session: {appointment.meeting_id} at {appointment.meeting_link}.'
        print(err)
        log_event(err)
