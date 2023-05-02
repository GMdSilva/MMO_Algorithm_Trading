import pandas as pd
from datetime import datetime

import cons
import utils
import vision as vs


class Get_dataset():
    def __init__(self, arr, first_value_up_history, first_value_down_history, counter, df_prices,
                 sold_up, added_up, sold_down, added_down, dict):
        self.values_up = [0,0,0,0]
        self.values_down = [0,0,0,0]
        self.sold_up = sold_up
        self.added_up = added_up
        self.sold_down = sold_down
        self.added_down = added_down
        self.dict = dict
        self.arr = arr
        self.first_value_up_history = first_value_up_history
        self.first_value_down_history = first_value_down_history
        self.counter = counter
        self.df_prices = df_prices

    def update_counters(self, values, first_value_history, sold, added):
        transaction = None
        if self.counter == 0:
            transaction = 'Start'
        else:
            if values[0] != first_value_history[self.counter - 1]:
                if values[1] != first_value_history[self.counter - 1]:
                    sold += 1
                    transaction = 'Closed'
                else:
                    added += 1
                    transaction = 'Opened'
        return sold, added, transaction

    def update_dict(self, value, sold, added, transaction, market, df):

        dt, iso_str = utils.get_date()
        self.dict['Price'] = value
        self.dict['Time'] = self.counter+1
        self.dict['Sold'] = sold
        self.dict['Added'] = added
        self.dict['Item'] = cons.ITEMS_DICT[cons.ITEMS[cons.ITEM]]
        self.dict['Class'] = transaction
        self.dict['Type'] = market
        self.dict['Day'] = cons.WEEKDAYS[dt.weekday()]
        self.dict['Hour'] = dt.hour
        self.dict['Date'] = iso_str
        df_temp = pd.DataFrame(self.dict, index=[0])
        df = df.append(df_temp, ignore_index=True)
        return df

    def update_and_save(self, transaction, up, down):

        self.sold_up, self.added_up, transaction = self.update_counters(up, self.first_value_up_history,
                                                         self.sold_up, self.added_up)

        if transaction is not None:
            market = 'Up'
            self.df_prices = self.update_dict(up[0], self.sold_up, self.added_up,
                                    transaction, market, self.df_prices)

            self.df_prices.to_csv('prices.csv')


        self.sold_down, self.added_down, transaction = self.update_counters(down, self.first_value_down_history,
                                           self.sold_down, self.added_down)

        if transaction is not None:
            market = 'Down'
            self.df_prices = self.update_dict(down[0], self.sold_down, self.added_down,
                                              transaction, market, self.df_prices)

            self.df_prices.to_csv('prices.csv')

        return self

    def run(self, transaction):
        self.arr = vs.capture_text('market_location')
        self.values_up, self.values_down, self.first_value_up_history, self.first_value_down_history =\
            utils.get_price_data(self.arr, self.first_value_up_history, self.first_value_down_history)

        self.update_and_save(transaction, self.values_up, self.values_down)

        return self.df_prices, self.sold_up, self.added_up, self.sold_down, self.added_down,\
               self.first_value_up_history, self.first_value_down_history

