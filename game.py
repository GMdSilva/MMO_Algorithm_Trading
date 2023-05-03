import time

import cons
import utils


def click_boxes():
    bye_confirmation_box()
    utils.click(cons.COORDS['item_swap'][0], cons.COORDS['item_swap'][1])
    bye_confirmation_box()
    utils.click(cons.COORDS['item_query'][0], cons.COORDS['item_query'][1])
    bye_confirmation_box()


def timeout_prevention():
    bye_confirmation_box()
    utils.click(cons.COORDS['close_market'][0], cons.COORDS['close_market'][1])
    bye_confirmation_box()
    utils.right_click(cons.COORDS['open_market'][0], cons.COORDS['open_market'][1])
    bye_confirmation_box()
    for i in range(len(cons.COORDS['key_coins'])):
        bye_confirmation_box()
        utils.send_key(cons.COORDS['key_coins'][i])
        bye_confirmation_box()


def create_order(new_prices, type):
    ## Clicks sell or buy ##
    bye_confirmation_box()
    utils.click(cons.COORDS[type][0], cons.COORDS[type][1])
    time.sleep(0.2)
    ## Clicks text box ##
    bye_confirmation_box()
    utils.click(cons.COORDS['text_box'][0], cons.COORDS['text_box'][1])
    time.sleep(0.2)
    ## Fill in the price ##
    for number in str(new_prices):
        bye_confirmation_box()
        utils.send_key(number)
    bye_confirmation_box()
    utils.click(cons.COORDS['create_offer'][0], cons.COORDS['create_offer'][1])
    time.sleep(1)
    bye_confirmation_box()


def create_order(new_prices, type, shadow_mode):
    ## Clicks sell or buy ##
    bye_confirmation_box()
    utils.click(cons.COORDS[type][0], cons.COORDS[type][1])
    time.sleep(0.2)
    ## Clicks text box ##
    bye_confirmation_box()
    utils.click(cons.COORDS['text_box'][0], cons.COORDS['text_box'][1])
    time.sleep(0.2)
    ## Fill in the price ##
    for number in str(new_prices):
        bye_confirmation_box()
        utils.send_key(number)
    bye_confirmation_box()
    if utils.validate_entity(new_prices, 'number', 'price_box'):
        if not shadow_mode:
            utils.click(cons.COORDS['create_offer'][0], cons.COORDS['create_offer'][1])
        time.sleep(1)
    else:
        print('price validation failed!!!!!!!!!!')
        # TODO IMPLEMENT PROPER EXCEPTION HERE

    bye_confirmation_box()


def go_to_offers():
    bye_confirmation_box()
    utils.click(cons.COORDS['my_offers'][0], cons.COORDS['my_offers'][1])
    time.sleep(1)


def cancel_offer(order_type):
    if order_type == 'ask':
        # utils.click(cons.COORDS['my_offers_first_ask'][0], cons.COORDS['my_offers_first_ask'][1])
        bye_confirmation_box()
        utils.click(cons.COORDS['my_offers_ask_cancel'][0], cons.COORDS['my_offers_ask_cancel'][1])
    elif order_type == 'bid':
        # utils.click(cons.COORDS['my_offers_first_bid'][0], cons.COORDS['my_offers_first_bid'][1])
        bye_confirmation_box()
        utils.click(cons.COORDS['my_offers_bid_cancel'][0], cons.COORDS['my_offers_bid_cancel'][1])
    time.sleep(0.2)


def bye_confirmation_box():
    time.sleep(0.1)
    utils.send_key('enter')
    time.sleep(0.1)


def go_to_market():
    bye_confirmation_box()
    utils.click(cons.COORDS['go_to_market'][0], cons.COORDS['go_to_market'][1])
    time.sleep(0.5)
    for i in range(len(cons.COORDS['key_coins'])):
        bye_confirmation_box()
        utils.send_key(cons.COORDS['key_coins'][i])
    bye_confirmation_box()
    if utils.validate_entity('coin', 'text', 'search_box'):
        print('search validated!')
    else:
        print('search validation failed!!!!!!!!!!')
        # TODO IMPLEMENT PROPER EXCEPTION HERE

def anon_order():
    bye_confirmation_box()
    utils.click(cons.COORDS['anon_box'][0], cons.COORDS['anon_box'][1])
