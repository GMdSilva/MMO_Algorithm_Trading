import datetime
import matplotlib.pyplot as plt
import pandas as pd
import time
from IPython.display import clear_output

import cons


def get_plot_data(df, price_type, weekdays, window):
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

    volume_added = prices['Added'].div(prices.Time, axis=0)
    volume_sold = prices['Sold'].div(prices.Time, axis=0)

    volume_added_today = prices_today['Added'].div(prices_today.Time, axis=0)
    volume_sold_today = prices_today['Sold'].div(prices_today.Time, axis=0)

    total_volume = prices['Added'] + prices['Sold']
    roll_volume = total_volume.div(prices.Time, axis=0)
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
        'roll_volume': roll_volume
    }


def make_plots():
    price_data_up = get_plot_data(cons.DATASET, 'Up', cons.WEEKDAYS, cons.WINDOW)
    price_data_down = get_plot_data(cons.DATASET, 'Down', cons.WEEKDAYS, cons.WINDOW)

    data_to_be_plotted = {
        1: price_data_up['prices_total'],
        2: price_data_up['prices_today'],
        3: price_data_up['roll_prices'],
        4: price_data_up['volume_added_today'],
        5: price_data_up['volume_sold_today'],
        6: price_data_up['roll_volume'],
        7: price_data_down['prices_total'],
        8: price_data_down['prices_today'],
        9: price_data_down['roll_prices'],
        10: price_data_down['volume_added_today'],
        11: price_data_down['volume_sold_today'],
        12: price_data_down['roll_volume'],
    }

    fig = plt.figure(figsize=(12.48, 10.8), dpi=100)

    titles = ['Prices Ask', 'Prices Ask Today', 'Prices Ask Rolling Average',
              'Offer Volume Ask', 'Sales Volume Up', 'Total Volume Rolling Average Ask',
              'Prices Bid', 'Prices Bid Today', 'Prices Bid Rolling Average',
              'Offer Volume Bid', 'Sales Volume Bid', 'Total Volume Rolling Average Bid',
              ]

    line_colors = ['blue', 'green', 'red',
                   'purple', 'orange', 'pink']

    for i in range(1, 13):
        ax = fig.add_subplot(4, 3, i)
        ax.set_title(titles[i - 1])
        lines, = ax.plot(data_to_be_plotted[i], color=line_colors[(i - 1) % 6])

    time.sleep(0.1)
    plt.tight_layout()
    plt.savefig(cons.FIGPATH)
    plt.close()
