import pandas as pd
from datetime import datetime
import typing
import cons
import utils
import vision as vs


class Get_dataset():
    def __init__(self, order_type,counter):
        self.values = [0,0,0,0]
        self.sold = 0
        self.added = 0
        self.dict = cons.DF_PRICES_COLS
        self.arr = 0
        self.first_value_history = [0,0]
        self.values_up = [0,0,0,0]
        self.values_down = [0,0,0,0]
        self.first_value_up_history = []
        self.first_value_down_history = []
        self.counter = counter
        self.df_prices = utils.load_dataset()
        self.order_type = order_type
        self.transaction = None

    def update_counters(self):
        self.transaction = None
        if self.counter == 0:
            self.transaction = 'Start'
        else:
            if self.values[0] != self.first_value_history[self.counter - 1]:
                if self.values[1] != self.first_value_history[self.counter - 1]:
                    self.sold += 1
                    self.transaction = 'Closed'
                else:
                    self.added += 1
                    self.transaction = 'Opened'
        return self

    def update_dict(self):
        dt, iso_str = utils.get_date()
        self.dict['Price'] = self.values[0]
        self.dict['Time'] = self.counter+1
        self.dict['Sold'] = self.sold
        self.dict['Added'] = self.added
        self.dict['Item'] = cons.ITEMS_DICT[cons.ITEMS[cons.ITEM]]
        self.dict['Class'] = self.transaction
        self.dict['Type'] = self.order_type
        self.dict['Day'] = cons.WEEKDAYS[dt.weekday()]
        self.dict['Hour'] = dt.hour
        self.dict['Date'] = iso_str
        df_temp = pd.DataFrame(self.dict, index=[0])
        self.df_prices = self.df_prices.append(df_temp, ignore_index=True)
        return self

    def update_and_save(self):
        self.update_counters()
        if self.transaction is not None:
            self.update_dict()
            self.df_prices.to_csv('prices.csv')
        return self

    def run(self, order_type, counter):
        raw_values = vs.capture_text('market_location')
        self.values_up, self.values_down, self.first_value_up_history, self.first_value_down_history =\
            utils.get_price_data(raw_values, self.first_value_up_history, self.first_value_down_history)

        if order_type == 'bid':
            self.values = self.values_down
            self.first_value_history = self.first_value_down_history
        elif order_type == 'ask':
            self.values = self.values_up
            self.first_value_history = self.first_value_up_history
        self.counter = counter

        self.update_and_save()

        return self




