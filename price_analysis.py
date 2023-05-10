import numpy as np
import cons
from get_dataset import Get_dataset


class Price_analysis(Get_dataset):
    def __init__(self, gd, order_type):
        self.order_type = order_type
        self.counter = gd.counter
        self.current_price = gd.values[order_type][0]
        self.second_price = gd.values[order_type][1]
        if gd.counter > 0:
            self.previous_price = gd.first_value_history[order_type][gd.counter - 1]
        else:
            self.previous_price = gd.first_value_history[order_type][0]
        self.prices = np.array(gd.values[order_type])
        self.prices_mean = self.prices[1:2].mean()
        self.current_price_bid = gd.first_value_history['bid'][-1]
        self.current_price_ask = gd.first_value_history['ask'][-1]

    def self_critique(self):
        price_validity = True
        if self.order_type == 'ask':
            if self.current_price > self.second_price:
                print(f'Ask price ({self.current_price}) is higher than previous ask ({self.second_price}), DONT BUY')
                price_validity = False
            if self.prices_mean * 0.9 > self.current_price or \
                    self.prices_mean * 1.1 < self.current_price:
                print(f'Ask price ({self.current_price}) is too different from mean ({self.prices_mean}), DONT BUY')
                price_validity = False
        elif self.order_type == 'bid':
            if self.current_price < self.second_price:
                print(f'Bid price ({self.current_price}) is lower than previous bid ({self.second_price}), DONT BUY')
                price_validity = False
            if self.prices_mean * 0.9 > self.current_price or \
                    self.prices_mean * 1.1 < self.current_price:
                print(f'Bid price ({self.current_price}) is too different from mean ({self.prices_mean}), DONT BUY')
                price_validity = False
        return price_validity

    def get_percent_diff(self):
        percent = (self.previous_price / self.current_price) * 100
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
        profit = ((spread - fee) / fee) * 100
        if profit > cons.MIN_PROFIT_PERCENTAGE:
            # print(f'Income is {spread - fee}')
            # print(f'Total profit is {profit}%')
            self.market_change = False
            self.change_tracker = False
        return profit

    def update_price(self, current_price, order_type, shadow_mode):
        if not shadow_mode:
            if order_type == 'bid':
                return current_price + 1
            else:
                return current_price - 1
        else:
            return current_price
