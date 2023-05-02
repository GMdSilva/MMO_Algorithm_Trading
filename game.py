import time

import cons
import utils


def click_boxes():
    utils.click(cons.COORDS['item_swap'][0], cons.COORDS['item_swap'][1])
    utils.click(cons.COORDS['item_query'][0], cons.COORDS['item_query'][1])
    time.sleep(1)


def timeout_prevention():
    utils.click(cons.COORDS['close_market'][0], cons.COORDS['close_market'][1])
    time.sleep(0.25)
    utils.right_click(cons.COORDS['open_market'][0], cons.COORDS['open_market'][1])
    time.sleep(0.25)
    for i in range(len(cons.COORDS['key_coins'])):
        time.sleep(0.25)
        utils.send_key(cons.COORDS['key_coins'][i])
        time.sleep(0.25)


def create_order(new_prices, type):
    ## Clicks sell or buy ##
    utils.click(cons.COORDS[type][0], cons.COORDS[type][1])
    time.sleep(0.2)
    ## Clicks text box ##
    utils.click(cons.COORDS['text_box'][0], cons.COORDS['text_box'][1])
    time.sleep(0.2)
    ## Fill in the price ##
    for number in str(new_prices):
        utils.send_key(number)
        time.sleep(0.2)
    utils.click(cons.COORDS['create_offer'][0],cons.COORDS['create_offer'][1])
    time.sleep(1)
    utils.send_key('enter')
    time.sleep(2)


def go_to_offers():
    utils.click(cons.COORDS['my_offers'][0], cons.COORDS['my_offers'][1])
    time.sleep(3)


def cancel_offer(order_type):
    if order_type == 'ask':
        # utils.click(cons.COORDS['my_offers_first_ask'][0], cons.COORDS['my_offers_first_ask'][1])
        # time.sleep(0.25)
        utils.click(cons.COORDS['my_offers_ask_cancel'][0], cons.COORDS['my_offers_ask_cancel'][1])
    elif order_type == 'bid':
        # utils.click(cons.COORDS['my_offers_first_bid'][0], cons.COORDS['my_offers_first_bid'][1])
        # time.sleep(0.25)
        utils.click(cons.COORDS['my_offers_bid_cancel'][0], cons.COORDS['my_offers_bid_cancel'][1])
    time.sleep(0.5)

def go_to_market():
    utils.click(cons.COORDS['go_to_market'][0], cons.COORDS['go_to_market'][1])
    time.sleep(0.5)
    for i in range(len(cons.COORDS['key_coins'])):
        time.sleep(0.2)
        utils.send_key(cons.COORDS['key_coins'][i])
        time.sleep(0.2)


