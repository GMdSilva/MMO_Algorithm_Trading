PLATFORM = 'desktop'
AUDIO = r'C:\Users\gabri\Dropbox\tibia_market_bot\brasil.mp3'
VAL = 'Price'
DATASET = 'prices.csv'
THE_DEVIl_PATH = 'the_devil.jpg'
MARKET_PATH = 'market_open.JPG'
OFFERS_PATH = 'offers_open.JPG'
ITEMS_PATH = 'market_arae.JPG'
ITEM_PATH = 'coins.JPG'
LOCKER_PATH = 'locker.JPG'
BUY_PATH = 'buy.jpg'
SELL_PATH = 'sell.jpg'
DP_PATH = 'depot.JPG'
ITEMS = [0, 1]
ITEM = 0
WINDOW = 3
THRESH_UP = 97
THRESH_DOWN = 103
MIN_VAL = 10000
MAX_VAL = 30000
BUY_FEE = 0.02  # 2% fee per transaction
MIN_PROFIT_PERCENTAGE = 20  # minimum % profit required for trade to be worth it
OPERATIONS = 2
BATCH = 25
PLACEHOLDER = 0

if PLATFORM == 'desktop':
    FIGPATH = r'C:\Users\Gabriel\Dropbox\tibia_market_bot\tibia_market.png'
    AUDIO = r'C:\Users\Gabriel\Dropbox\tibia_market_bot\brasil.mp3'
    COORDS = {
        'market_location': (1305, 524, 58, 400),
        'item_swap': (945, 697),
        'item_query': (945, 739),
        # 'item_swap': (945, 807),
        # 'item_query': (945, 840),
        'close_market': (1623, 959),
        'open_market': (2525, 502),
        'key_coins': ['c', 'o', 'i', 'n'],
        # 'key_coins': ['s', 'p', 'e', 'a', 'r']
        'text_box': (1323, 889),
        'create_offer': (1609, 917),
        'ask': (1094, 853),
        'bid': (1095, 870),
        'my_offers': (1514, 958),
        'go_to_market': (1603, 960),
        'my_offers_ask_cancel': (1610, 479),
        'my_offers_bid_cancel': (1610, 713),
        'my_offers': (1517, 956),
        'offers': (1267, 528, 50, 281),
        'anon_box': (1506, 913),
        'price_box': (1277, 882, 43, 13),
        'gold_box': (959, 948, 79, 18),
        'coin_box': (1103, 948, 42, 18),
        'search_box': (961, 911, 37, 12),
    }

else:
    FIGPATH = r'tibia_market.png'
    AUDIO = r'brasil.mp3'
    COORDS = {
        'market_location': (994, 288, 100, 367),
        'item_swap': (541, 562),
        'item_query': (566, 597),
        'close_market': (1355, 830),
        'open_market': (1868, 590),
        'key_coins': ['c', 'o', 'i', 'n'],
        'text_box': (1030, 750),
        'create_offer': (1377, 777),
        'ask': (730, 700),
        'bid': (730, 726),
        'my_offers': (1263, 830),
        'go_to_market': (1356, 830),
        'my_offers_ask_cancel': (1365, 232),
        'my_offers_bid_cancel': (1365, 528),
        'offers': (908, 220, 98, 542),
        'anon_box': (1240, 777),
        'price_box': (956, 739, 60, 14),
        'gold_box': (571, 823, 52, 18),
        'coin_box': (734, 823, 56, 18),
        'search_box': (562, 733, 51, 55)
    }

WEEKDAYS = {
    0: 'Monday',
    1: 'Tuesday',
    2: 'Wednesday',
    3: 'Thursday',
    4: 'Friday',
    5: 'Saturday',
    6: 'Sunday'
}

DF_PRICES_COLS = {
    'Price': PLACEHOLDER,
    'Time': PLACEHOLDER,
    'Sold': PLACEHOLDER,
    'Added': PLACEHOLDER,
    'Percent Diff': PLACEHOLDER,
    'Item': PLACEHOLDER,
    'Class': PLACEHOLDER,
    'Type': PLACEHOLDER,
    'Day': PLACEHOLDER,
    'Hour': PLACEHOLDER,
    'Date': PLACEHOLDER,
}

ITEMS_DICT = {
    0: 'coin',
    1: 'spear'
}

# %%
