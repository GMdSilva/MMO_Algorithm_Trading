import keyboard
import numpy as np
import pandas as pd
import time
import win32api
import win32con
from datetime import datetime
import pickle
import game
import vision as vs
import cons
import config

def open_dump_files(offer_type, offer_dict):
    file = open(offer_type+"_dump.txt", "wb")
    pickle.dump(offer_dict, file)
    file.close()

def check_previous(offer_type):
    with open(offer_type+'_dump.txt', 'rb') as handle:
        data = handle.read()
        d = pickle.loads(data)
    return d

def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(np.random.uniform(0.1, 0.02))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    time.sleep(np.random.uniform(0.1, 0.02))


def right_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(np.random.uniform(0.1, 0.02))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)


def send_key(key):
    time.sleep(0.05)
    keyboard.press_and_release(key)


def select_all():
    time.sleep(0.05)
    keyboard.press_and_release('ctrl+a')


def delete():
    time.sleep(0.05)
    keyboard.press_and_release('backspace')


def sanitize_and_check_numbers(str_arr):
    nums = []
    for s in str_arr:
        # Remove non-numeric characters
        s = ''.join(filter(str.isdigit, s))
        # Convert to integer, skip iteration if not a valid integer within the range
        try:
            num = int(s)
            if cons.MIN_VAL >= num or num >= cons.MAX_VAL:
                raise ValueError
            else:
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


def load_dataset(order_type):
    df_prices = pd.read_csv('prices_'+order_type+'.csv', index_col=0)
    return df_prices


def find_index(arr):
    for i, value in enumerate(arr):
        if cons.VAL in value:
            return i


def get_offer_list(offer_type):
    offer_list = game.run_action_safely(lambda: vs.capture_text('market_location'))
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
            print('Something is wrong with prices, they exist but are too few')
            offer_list = get_price_checks(offer_type)
            return offer_list
        #except:
        else:
            return offer_list
    except:
        offer_list = get_price_checks(offer_type)
        return offer_list
   #return offer_list

def validate_entity(to_be_validated, types, coords):
    reference = game.run_action_safely(lambda: vs.capture_text(coords))
    if types == 'number':
        reference = sanitize_numbers(reference)
        try:
            num = int(reference[0])
        except ValueError:
            print('Reference is not a int')
    if to_be_validated == reference[0]:
        validation = True
    else:
        validation = False
    return validation

def validate_order_type(types):
    if game.run_action_safely(lambda: vs.check_if_image_on_screen(cons.ITEM_PATH)):
        if types == 'bid':
            if not game.run_action_safely(lambda: vs.check_if_image_on_screen(cons.BUY_PATH)):
                print("Order was set to ask when it should be bid, check code")
                game.run_action_safely(lambda: click(cons.COORDS[types][0], cons.COORDS[types][1]))
                #time.sleep(0.1)
        elif types == 'ask':
            if not game.run_action_safely(lambda: vs.check_if_image_on_screen(cons.SELL_PATH)):
                print("Order was set to bid when it should be ask, check code")
                game.run_action_safely(lambda: click(cons.COORDS[types][0], cons.COORDS[types][1]))
                #time.sleep(0.1)


def send_offer_checks(types, value, shadow_mode):
    print('Something triggered checking offers')
    if vs.check_if_image_on_screen(cons.THE_DEVIL_PATH):
        game.bye_confirmation_box()
        config.image_can_appear = False
    if vs.check_if_image_on_screen(cons.OFFERS_PATH):
        game.run_action_safely(lambda: game.go_from_my_offers_to_market())
    game.run_action_safely(lambda: game.click_item())
    game.timeout_prevention()
    if game.run_action_safely(lambda: vs.check_if_image_on_screen(cons.ITEM_PATH)):
        if types == 'bid':
            if game.run_action_safely(lambda: vs.check_if_image_on_screen(cons.BUY_PATH)):
                game.create_order(types, value, shadow_mode)
                print('creating order bid')
            else:
                game.run_action_safely(lambda: click(cons.COORDS[types][0], cons.COORDS[types][1]))
                #time.sleep(0.1)
                game.create_order(types, value, shadow_mode)
        elif types == 'ask':
            if game.run_action_safely(lambda: vs.check_if_image_on_screen(cons.SELL_PATH)):
                game.run_action_safely(lambda: game.create_order(types, value, shadow_mode))
                print('creating order ask')
            else:
                game.run_action_safely(lambda: click(cons.COORDS[types][0], cons.COORDS[types][1]))
                #time.sleep(0.1)
                game.create_order(types, value, shadow_mode)
                print('creating order')

    else:
        print('cant fix it')
        raise BaseException


def get_price_checks(offer_type):
    print('Something triggered checking prices')
    if vs.check_if_image_on_screen(cons.THE_DEVIL_PATH):
        game.bye_confirmation_box()
        config.image_can_appear = False
    if game.run_action_safely(lambda: vs.check_if_image_on_screen(cons.OFFERS_PATH)):
        game.run_action_safely(lambda: game.go_from_my_offers_to_market())
    game.timeout_prevention()
    game.run_action_safely(lambda: game.click_item())
    game.run_action_safely(lambda: game.click_price_text_box())
    if game.run_action_safely(lambda: vs.check_if_image_on_screen(cons.ITEM_PATH)):
        offer_lists = get_price_data(offer_type)
        return offer_lists
    else:
        print('cant fix it')
        raise BaseException


def get_resource_checks(resource):
    print('Something triggered checking resources')
    if vs.check_if_image_on_screen(cons.THE_DEVIL_PATH):
        print('bb')
        game.bye_confirmation_box()
    if game.run_action_safely(lambda: vs.check_if_image_on_screen(cons.OFFERS_PATH)):
        print('cc')
        game.run_action_safely(lambda: game.go_from_my_offers_to_market())
    game.timeout_prevention()
    game.run_action_safely(lambda: game.click_item())
    game.run_action_safely(lambda: game.click_price_text_box())
    if game.run_action_safely(lambda: vs.check_if_image_on_screen(cons.ITEM_PATH)):
        lines = game.run_action_safely(lambda: vs.read_resources(resource))
        return lines
    else:
        print('cant fix it')
        raise BaseException
    # try:
    #     if utils.validate_entity(value, 'number', 'price_box'):
    #         print('aa')
    #         all_good = True
    #         return all_good
    #     else:
    #         print('fffffff')
    # except:
