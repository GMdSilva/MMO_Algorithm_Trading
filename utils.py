import keyboard
import numpy as np
import pandas as pd
import time
import win32api
import win32con
from datetime import datetime

import game
import vision as vs
import cons


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(np.random.uniform(0.1, 0.1))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(np.random.uniform(0.1, 0.1))


def right_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(np.random.uniform(0.1, 0.02))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def send_key(key):
    time.sleep(0.1)
    keyboard.press_and_release(key)


def sanitize_and_check_numbers(str_arr):
    nums = []
    for s in str_arr:
        # Remove non-numeric characters
        s = ''.join(filter(str.isdigit, s))
        # Convert to integer, skip iteration if not a valid integer within the range
        try:
            num = int(s)
            if cons.MIN_VAL < num < cons.MAX_VAL:
                nums.append(num)
        except:
            continue
    return nums


def sanitize_numbers(str_arr):
    nums = []
    for s in str_arr:
        # Remove non-numeric characters
        s = ''.join(filter(str.isdigit, s))
        # Convert to integer, skip iteration if not a valid integer within the range
        try:
            num = int(s)
            nums.append(num)
        except:
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
    for i, value in enumerate(arr):
        if cons.VAL in value:
            return i

def get_offer_list(offer_type):
    offer_list = vs.capture_text('market_location')
    index = find_index(offer_list)
    if offer_type == 'bid':
        offer_list = offer_list[index + 1:]
        offer_list = sanitize_and_check_numbers(offer_list)
    elif offer_type == 'ask':
        offer_list = offer_list[:index]
        offer_list = sanitize_and_check_numbers(offer_list)
    return offer_list

def get_price_data(offer_type):
    try:
        offer_list = get_offer_list(offer_type)
        if len(offer_list) < 5:
            offer_type = get_price_checks(offer_type)
            return offer_type
    except:
        offer_type = get_price_checks(offer_type)
        return offer_type
    return offer_list


# def get_price_data(arr, first_value_up_history, first_value_down_history):
#     try:
#         i = find_index(arr)
#         b = [0, 1, 2, 3]
#         c = [i + 1, i + 2, i + 3, i + 4]
#     except:
#         print(f"Didn't get a proper array with value")
#         get_price_checks(arr, first_value_up_history, first_value_down_history)
#     try:
#         up = [arr[i] for i in b]
#         down = [arr[i] for i in c]
#     except:
#         print(f"Didn't get a proper array")
#         get_price_checks(arr, first_value_up_history, first_value_down_history)
#     try:
#         up = sanitize_and_check_numbers(up)
#         down = sanitize_and_check_numbers(down)
#     except:
#         print(f"Can't sanitize numbers")
#         get_price_checks(arr, first_value_up_history, first_value_down_history)
#     try:
#         first_value_up_history.append(up[0])
#         first_value_down_history.append(down[0])
#     except:
#         print(f"Can't append arrays")
#         get_price_checks(arr, first_value_up_history, first_value_down_history)
#     return up, down,first_value_up_history,first_value_down_history

def validate_entity(to_be_validated, types, coords):
    reference = vs.capture_text(coords)
    if types == 'number':
        reference = sanitize_numbers(reference)
        try:
            num = int(reference[0])
        except:
            print('Reference is not a int')
    if to_be_validated == reference[0]:
        validation = True
    else:
        validation = False
    return validation

def send_offer_checks(types, value, shadow_mode):
    print('oferc ')
    if vs.check_if_image_on_screen(cons.THE_DEVIl_PATH):
        print('bb')
        game.bye_confirmation_box()
    if vs.check_if_image_on_screen(cons.OFFERS_PATH):
        print('cc')
        game.go_from_my_offers_to_market()
    game.click_item()
    game.timeout_prevention()
    if vs.check_if_image_on_screen(cons.ITEM_PATH):
        if types == 'bid':
            if vs.check_if_image_on_screen(cons.BUY_PATH):
                game.create_order(types, value, shadow_mode)
                print('creating order')
            else:
                click(cons.COORDS[types][0], cons.COORDS[types][1])
        elif types == 'ask':
            if vs.check_if_image_on_screen(cons.SELL_PATH):
                game.create_order(types, value, shadow_mode)
                print('creating order')
            else:
                click(cons.COORDS[types][0], cons.COORDS[types][1])
                time.sleep(0.1)
                game.create_order(types, value, shadow_mode)
                print('creating order')

    else:
        print('cant fix it')
        return -1

def get_price_checks(offer_type):
    print('pricec c')
    if vs.check_if_image_on_screen(cons.THE_DEVIl_PATH):
        print('bb')
        game.bye_confirmation_box()
    if vs.check_if_image_on_screen(cons.OFFERS_PATH):
        print('cc')
        game.go_from_my_offers_to_market()
    game.timeout_prevention()
    game.click_item()
    game.click_price_text_box()
    if vs.check_if_image_on_screen(cons.ITEM_PATH):
        print('getting_price data')
        offer_type = get_price_data(offer_type)
        return offer_type
    else:
        print('cant fix it')
        return -1

def get_resource_checks(resource):
    print('resource chce')
    if vs.check_if_image_on_screen(cons.THE_DEVIl_PATH):
        print('bb')
        game.bye_confirmation_box()
    if vs.check_if_image_on_screen(cons.OFFERS_PATH):
        print('cc')
        game.go_from_my_offers_to_market()
    game.timeout_prevention()
    game.click_item()
    game.click_price_text_box()
    if vs.check_if_image_on_screen(cons.ITEM_PATH):
        print('cjeclomg respirce')
        lines = vs.read_resources(resource)
        return lines
    else:
        print('cant fix it')
        return -1
    # try:
    #     if utils.validate_entity(value, 'number', 'price_box'):
    #         print('aa')
    #         all_good = True
    #         return all_good
    #     else:
    #         print('fffffff')
    # except: