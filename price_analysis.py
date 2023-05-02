import numpy as np
import random
import time
import cons
import game
import utils
from get_dataset import Get_dataset

class Price_analysis(Get_dataset):
    def __init__(self, gd, order_type):
        self.counter = gd.counter
        self.current_price = gd.values[0]
        self.second_price = gd.values[1]
        self.previous_price = gd.first_value_history[gd.counter - 1]
        self.prices = np.array(gd.values)
        self.prices_mean = self.prices[1:2].mean()
        self.current_price_bid = gd.values_down[0]
        self.current_price_ask = gd.values_up[0]
        self.order_type = order_type

    def self_critique(self):
        price_validity = True
        if self.order_type == 'ask':
            if self.current_price > self.second_price:
                print('Ask price is higher than previous ask, DONT BUY')
                price_validity = False
            if self.prices_mean * 0.9 > self.current_price or \
                    self.prices_mean * 1.1 < self.current_price:
                print('Ask price is too different from mean, DONT BUY')
                price_validity = False
        elif self.order_type == 'bid':
            if self.current_price < self.second_price:
                print('Bid price is lower than previous bid, DONT BUY')
                price_validity = False
            if self.prices_mean * 0.9 > self.current_price or \
                    self.prices_mean * 1.1 < self.current_price:
                print('Bid price is too different from mean, DONT BUY')
                price_validity = False
        return price_validity

    def get_percent_diff(self):
        percent = (self.previous_price/self.current_price) * 100
        return percent

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
            return current_price + 0
        else:
            return current_price - 0
