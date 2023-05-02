import numpy as np
import random
import time

import cons
import game
import utils
from get_dataset import Get_dataset


class Price_analysis(Get_dataset):
    def __init__(self, gd, ):
        self.counter = gd.counter
        self.current_price_bid = gd.values_down[0]
        self.current_price_ask = gd.values_up[0]
        self.second_price_ask = gd.values_up[1]
        self.second_price_bid = gd.values_down[1]
        self.previous_price_bid = gd.first_value_down_history[gd.counter - 1]
        self.previous_price_ask = gd.first_value_up_history[gd.counter - 1]
        self.bid_prices = np.array(gd.values_down)
        self.ask_prices = np.array(gd.values_up)
        self.ask_prices_mean = self.bid_prices[1:2].mean()
        self.bid_prices_mean = self.ask_prices[1:2].mean()

    def self_critique(self):
        price_validity = True
        if self.current_price_ask > self.second_price_ask:
            print('Ask price is higher than previous ask, DONT BUY')
            price_validity = False
        if self.current_price_bid < self.second_price_bid:
            print('Bid price is lower than previous bid, DONT BUY')
            price_validity = False
        if self.ask_prices_mean * 0.9 > self.current_price_ask or \
                self.ask_prices_mean * 1.1 < self.current_price_ask:
            print('Ask price is too different from mean, DONT BUY')
            price_validity = False
        if self.bid_prices_mean * 0.9 > self.current_price_bid or \
                self.bid_prices_mean * 1.1 < self.current_price_bid:
            print('Bid price is too different from mean, DONT BUY')
            price_validity = False
        return price_validity

    def get_percent_diff(self):
        percent_up = (self.previous_price_ask/self.current_price_ask) * 100
        percent_down = (self.previous_price_bid/self.current_price_bid) * 100
        return percent_up, percent_down

    def calculate_spread(self):
        return (self.current_price_ask * cons.BATCH) - (self.current_price_bid * cons.BATCH)

    def calculate_fee(self):
        fee = ((self.current_price_ask * cons.BATCH) * cons.BUY_FEE) + \
              ((self.current_price_bid * cons.BATCH) * cons.BUY_FEE)
        return fee

    def calculate_total_profit(self):
        spread = self.calculate_spread()
        fee = self.calculate_fee()
        profit = ((spread - fee) / (fee)) * 100
        return profit

    def update_price(self, current_price, order_type):
        if order_type == 'bid':
            return current_price + 1
        else:
            return current_price - 1
