import keyboard
import numpy as np
import pandas as pd
import time
import win32api
import win32con
from datetime import datetime

import cons


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(np.random.uniform(0.25, 0.1))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(np.random.uniform(0.1, 0.1))

def right_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(np.random.uniform(0.01, 0.02))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

def send_key(key):
    keyboard.press_and_release(key)

def sanitize_and_check_numbers(str_arr):
    nums = []
    for s in str_arr:
        # Remove non-numeric characters
        s = ''.join(filter(str.isdigit, s))
        # Convert to integer, skip iteration if not a valid integer within the range
        try:
            num = int(s)
            if num < cons.MIN_VAL or num > cons.MAX_VAL:
                continue
            nums.append(num)
        except ValueError:
            continue
    return nums

def get_date():
    dt = datetime.now()
    iso_str = dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return dt, iso_str

def load_dataset():
    df_prices = pd.read_csv(cons.DATASET, index_col=0)
    return df_prices

def find_index(arr):
    for i in range(len(arr)):
        if cons.VAL in arr[i]:
            return i
    return -1

def get_price_data(arr, first_value_up_history, first_value_down_history):
    i = find_index(arr)
    b = [0, 1, 2, 3]
    c = [i + 1, i + 2, i + 3, i + 4]
    try:
        up = [arr[i] for i in b]
        down = [arr[i] for i in c]
    except:
        print('failed at ' + str(arr))
        return -1

    up = sanitize_and_check_numbers(up)
    down = sanitize_and_check_numbers(down)

    first_value_up_history.append(up[0])
    first_value_down_history.append(down[0])

    return up, down,first_value_up_history,first_value_down_history

