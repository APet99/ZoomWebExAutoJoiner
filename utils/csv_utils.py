import numpy as np
import pandas as pd

from appointment import Appointment


def build_appointments_from_csv(csv_path: str = 'schedule.csv'):
    data = load_csv(csv_path)
    data = remove_null_rows(data)
    data = data.replace(np.nan, '', regex=True)
    data_list = data.values.tolist()
    return map_list_of_data_to_appointment_list(data_list)


def load_csv(file_location: str):
    return pd.read_csv(file_location)


def remove_null_rows(data):
    return data[data['Meeting Link'].notna()]


def map_list_of_data_to_appointment_list(data_list: list):
    appointments = []
    for row in data_list:
        appointment = Appointment(*row)
        appointments.append(appointment)
    return appointments
