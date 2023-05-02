PLATFORM = 'desktop'
AUDIO = r'C:\Users\gabri\Dropbox\tibia_market_bot\brasil.mp3'
VAL = 'Price'
DATASET = 'prices.csv'
ITEMS = [0, 1]
ITEM = 0
WINDOW = 3
THRESH_UP = 97
THRESH_DOWN = 103
MIN_VAL = 10000
MAX_VAL = 20000
BUY_FEE = 0.02  # 2% fee per transaction
MIN_PROFIT_PERCENTAGE = -100  # minimum % profit required for trade to be worth it
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
        'open_market': (2525, 675),
        'key_coins': ['c', 'o', 'i', 'n'],
        # 'key_coins': ['s', 'p', 'e', 'a', 'r']
        'text_box': (1323, 889),
        'create_offer': (1609, 917),
        'ask': (1094, 853),
        'bid': (1095, 870),
        'my_offers': (1514, 958),
        'go_to_market': (1603, 960),
        'my_ofers_ask_cancel': (1610, 479),
        'my_offers_bid_cancel': (1610, 713),
        'my_offers': (1517, 956),
        'offers': (1267, 528, 50, 281)
    }

else:
    FIGPATH = r'C:\Users\gabri\Dropbox\Aplicativos\My.DropPages\tibiamarkets.droppages.net\Public\tibia_market.png'
    AUDIO = r'C:\Users\gabri\Dropbox\tibia_market_bot\brasil.mp3'
    COORDS = {
        'market_location': (994, 288, 72, 368),
        'item_swap': (608, 512),
        'item_query': (608, 560),
        'close_market': (1355, 830),
        'open_market': (1873, 590),
        'key_coins': ['c', 'o', 'i', 'n']
        # 'text_box' : (1323,889)
        # 'create_offer': (1609, 917)
        #  'sell_button' : (1094, 853)
        #  'buy_button' : (1095, 870)
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
    0: 'Coin',
    1: 'Spear'
}
