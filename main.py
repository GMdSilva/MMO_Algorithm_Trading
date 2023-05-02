# %%
import cv2
import imutils
import keyboard
import locale
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyautogui
import pytesseract
import time
import win32api
import win32con
from datetime import datetime
from playsound import playsound

import cons
import game
import plotting
import utils
import vision
from get_dataset import Get_dataset
from price_analysis import Price_analysis
from strategies import Strategies

## TODO: FIGURE OUT WAY TO GET RID OF ANNOYING BOX ##
## TODO: TURN PRICE_ANALYSIS INTO A BETTER CLASS ##
## EVENTUALLY DO THAT TO GET_DATASET TOO ##




locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
dict = cons.DF_PRICES_COLS
played = False
arr = []


(
    added_down,
    sold_down,
    added_up,
    sold_up,
    counter,
) = (0, 0, 0, 0, 0)

(
    value,
    sold,
    added,
    percent,
    market,
    roll,
    transaction,
    dt,
    iso_str,
    value_up_prev,
    value_down_prev,
    percent_diff_down,
    percent_diff_up,
    placeholder,
) = (None, None, None, None, None, None, None, None, None, None, None, None, None, None)


first_value_up_history = [0,0]
first_value_down_history = [0,0]

time.sleep(2)

df_prices = utils.load_dataset()
gd = Get_dataset(arr, first_value_up_history, first_value_down_history, counter, df_prices, sold_up, added_up,
                  sold_down, added_down, dict)


pc = Price_analysis(gd)

bid = Strategies.Arbitrage(pc, 'bid')
ask = Strategies.Arbitrage(pc, 'ask')
first_value_up_history = []
first_value_down_history = []

while 1:
    utils.send_key("enter")
    
    game.click_boxes()

    gd = Get_dataset(arr, first_value_up_history, first_value_down_history, counter, df_prices, sold_up, added_up,
                  sold_down, added_down, dict)

    df_prices, sold_up, added_up, sold_down, added_down, first_value_up_history, first_value_down_history =\
        gd.run(transaction)

    pc = Price_analysis(gd)

    #bid = bid.trade_flow(pc)
    ask = ask.trade_flow(pc)

    if counter % 50 == 0:
        game.timeout_prevention()

    plotting.make_plots()
    counter += 1

    time.sleep(0.5)















