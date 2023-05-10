import datetime
import matplotlib.pyplot as plt
import pandas as pd
import time

import cons


def get_plot_data(df, price_type, weekdays):
    window = 10
    window_std = 5
    buy_threshold = -1.0
    sell_threshold = 1.0
    risk_factor = 0.1
    stop_loss = 0.05

    dt = datetime.datetime.now()
    df = pd.read_csv(df)
    prices = df.loc[df['Type'] == price_type]
    prices_today = prices.loc[prices['Day'] == weekdays[dt.weekday()]]

    prices_offer = prices['Price'].loc[prices['Class'] == 'Opened']
    prices_sales = prices['Price'].loc[prices['Class'] == 'Closed']
    prices_today_prices = prices['Price'].loc[prices['Day'] == weekdays[dt.weekday()]]
    prices_total = prices['Price']

    roll_prices = prices['Price'].rolling(window).mean().fillna(method='bfill')
    roll_prices_today = prices_today['Price'].rolling(window).mean().fillna(method='bfill')

    std_prices = prices['Price'].rolling(window_std).std().fillna(method='bfill')
    std_prices_today = prices_today['Price'].rolling(window_std).std().fillna(method='bfill')

    z_score = (prices['Price'] - roll_prices) / std_prices

    volume_added = prices['Added'].div(prices.Time + 1, axis=0)
    volume_sold = prices['Sold'].div(prices.Time + 1, axis=0)

    volume_added_today = prices_today['Added'].div(prices_today.Time + 1, axis=0)
    volume_sold_today = prices_today['Sold'].div(prices_today.Time + 1, axis=0)

    total_volume = prices['Added'] + prices['Sold']
    roll_volume = total_volume.div(prices.Time + 1, axis=0)
    roll_volume = roll_volume.rolling(window).mean().fillna(method='bfill')

    return {
        'prices': prices,
        'prices_offer': prices_offer,
        'prices_sales': prices_sales,
        'prices_today': prices_today_prices,
        'prices_total': prices_total,
        'roll_prices': roll_prices,
        'roll_prices_today': roll_prices_today,
        'volume_added': volume_added,
        'volume_sold': volume_sold,
        'volume_added_today': volume_added_today,
        'volume_sold_today': volume_sold_today,
        'roll_volume': roll_volume,
        'std_prices_today': std_prices_today,
        'std_prices': std_prices,
        'z_score': z_score
    }
    #
    # for i in range(m, n):
    #     if z_score[i] < buy_threshold and portfolio > 0:
    #         entry_price = price[i]
    #         risk = portfolio * risk_factor
    #         position_size = int(risk / entry_price)
    #         if position_size > 0:
    #             positions = position_size
    #             cost = entry_price * positions
    #             portfolio -= cost
    #             print("Buy at:", entry_price, "with", positions, "shares")
    #     elif z_score[i] > sell_threshold and positions > 0:
    #         exit_price = price[i]
    #         pnl += (exit_price - entry_price) * positions
    #         portfolio += exit_price * positions
    #         positions = 0
    #         print("Sell at:", exit_price, "with P/L of", pnl)
    #     elif positions > 0 and price[i] < entry_price * (1 - stop_loss):
    #         exit_price = entry_price * (1 - stop_loss)
    #         pnl += (exit_price - entry_price) * positions
    #         portfolio += exit_price * positions
    #         positions = 0
    #         print("Stop-loss sell at:", exit_price, "with P/L of", pnl)
    # print("Final P/L:", pnl)


def make_plots():

    price_data_up = get_plot_data('prices_ask.csv', 'ask', cons.WEEKDAYS)
    price_data_down = get_plot_data('prices_bid.csv', 'bid', cons.WEEKDAYS)

    data_to_be_plotted = {
        1: price_data_up['roll_prices'],
        2: price_data_up['prices_today'],
        3: price_data_up['z_score'],
        4: price_data_up['volume_added'],
        5: price_data_up['volume_sold'],
        6: price_data_up['roll_volume'],
        7: price_data_down['roll_prices'],
        8: price_data_down['prices_today'],
        9: price_data_down['z_score'],
        10: price_data_down['volume_added'],
        11: price_data_down['volume_sold'],
        12: price_data_down['roll_volume'],
    }

    fig = plt.figure(figsize=(12.48, 10.8), dpi=100)

    titles = ['Prices Ask Rolling Average', 'Prices Ask Today', 'Prices Ask Z-Score',
              'Offer Volume Ask', 'Sales Volume Up', 'Total Volume Rolling Average Ask',
              'Prices Bid Rolling Average', 'Prices Bid Today', 'Prices Bid Z-Score',
              'Offer Volume Bid', 'Sales Volume Bid', 'Total Volume Rolling Average Bid',
              ]

    line_colors = ['blue', 'green', 'red',
                   'purple', 'orange', 'pink']

    for i in range(1, 13):
        ax = fig.add_subplot(4, 3, i)
        ax.set_title(titles[i - 1])
        ax.plot(data_to_be_plotted[i], color=line_colors[(i - 1) % 6])

    time.sleep(0.1)
    plt.tight_layout()
    plt.savefig(cons.FIGPATH)
    plt.close()


import pandas as pd
import numpy as np


# def calculate_rsi(data, time_period=14):
#     """
#     Calculates the Relative Strength Index (RSI) for a given stock using the historical price data.
#
#     Args:
#         data (pandas.DataFrame): Historical price data containing 'Open', 'High', 'Low', 'Close', and 'Volume' columns.
#         time_period (int): Number of days to use for RSI calculation (default is 14).
#
#     Returns:
#         pandas.DataFrame: The input data with an additional 'RSI' column.
#     """
#     # Calculate price change for each day
#     delta = data['Close'].diff()
#
#     # Get upward and downward price movements
#     gain = delta.where(delta > 0, 0)
#     loss = -delta.where(delta < 0, 0)
#
#     # Calculate the average gain and loss over the specified time period
#     avg_gain = gain.rolling(window=time_period).mean()
#     avg_loss = loss.rolling(window=time_period).mean()
#
#     # Calculate the relative strength (RS)
#     rs = avg_gain / avg_loss
#
#     # Calculate the RSI
#     rsi = 100 - (100 / (1 + rs))
#
#     # Add the RSI column to the data
#     data['RSI'] = rsi
#
#     return data

# def calculate_trade_threshold(volume_data, threshold_multiplier):
#     """
#     Calculates a trade volume threshold based on the average and standard deviation of the volume data.
#
#     Args:
#     - volume_data (list): A list of trade volume data.
#     - threshold_multiplier (float): A multiplier to adjust the threshold.
#
#     Returns:
#     - trade_threshold (float): A threshold value for big trades based on the trade volume.
#     """
#
#     # Calculate the mean and standard deviation of the volume data
#     volume_mean = sum(volume_data) / len(volume_data)
#     volume_std_dev = statistics.stdev(volume_data)
#
#     # Calculate the threshold based on the mean and standard deviation
#     trade_threshold = volume_mean + (threshold_multiplier * volume_std_dev)
#
#     return trade_threshold
# Here's an example of how you can use this function to calculate a trade threshold:
#
# yaml
# Copy code
# # Example usage
# volume_data = [1000, 2000, 3000, 4000, 5000]
# threshold_multiplier = 2.0
#
# trade_threshold = calculate_trade_threshold(volume_data, threshold_multiplier)
#
# print("Trade threshold:", trade_threshold)