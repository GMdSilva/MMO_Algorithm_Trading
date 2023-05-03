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
from performance import Performance
## TODO: FIGURE OUT WAY TO GET RID OF ANNOYING BOX ##


counter = 0

gd_bid = Get_dataset('bid', counter)
gd_ask = Get_dataset('ask', counter)
pc_bid = Price_analysis(gd_bid, 'bid')
pc_ask = Price_analysis(gd_ask, 'ask')
st_bid = Strategies.Arbitrage(pc_bid, 'bid', 'simulation')
st_ask = Strategies.Arbitrage(pc_ask, 'ask', 'simulation')
pf = Performance(st_bid, st_ask)
pf = pf.calculate_profit(st_ask)
pf = pf.update_performance_markers()
time.sleep(2)


while 1:

    game.click_boxes()
    gd_ask = gd_ask.run('ask', counter)
    gd_bid = gd_bid.run('bid', counter)

    pc_bid = Price_analysis(gd_bid, 'bid')
    pc_ask = Price_analysis(gd_ask, 'ask')
    if not pf.pause_buying:
        st_bid = st_bid.trade_flow(pc_bid)
    game.click_boxes()
    if not pf.pause_selling:
        st_ask = st_ask.trade_flow(pc_ask)

    pf = pf.update_performance_markers()

    if counter > 3 and counter % 3 == 0:
        pf = pf(st_bid, st_ask).calculate_profit()
        print(pf.combined_profit,pf.coin_profit,pf.gold_profit)
        game.timeout_prevention()

    plotting.make_plots()
    counter += 1
    time.sleep(0.5)






































