import time
import cons
import utils

def click_item():
    time.sleep(0.1)
    utils.click(cons.COORDS['item_query'][0], cons.COORDS['item_query'][1])
    time.sleep(0.1)

def click_boxes():
    time.sleep(0.1)
    utils.click(cons.COORDS['item_swap'][0], cons.COORDS['item_swap'][1])
    time.sleep(0.1)
    utils.click(cons.COORDS['item_query'][0], cons.COORDS['item_query'][1])
    time.sleep(0.1)

def close_market():
    time.sleep(0.1)
    utils.click(cons.COORDS['close_market'][0], cons.COORDS['close_market'][1])

def open_market():
    time.sleep(0.1)
    utils.right_click(cons.COORDS['open_market'][0], cons.COORDS['open_market'][1])

def click_price_text_box():
    time.sleep(0.1)
    utils.click(cons.COORDS['text_box'][0], cons.COORDS['text_box'][1])

def click_create_offer():
    time.sleep(0.1)
    utils.click(cons.COORDS['create_offer'][0], cons.COORDS['create_offer'][1])

def go_to_offers():
    time.sleep(0.1)
    utils.click(cons.COORDS['my_offers'][0], cons.COORDS['my_offers'][1])

def bye_confirmation_box():
    time.sleep(0.1)
    utils.send_key('enter')

def go_from_my_offers_to_market():
    time.sleep(0.1)
    utils.click(cons.COORDS['go_to_market'][0], cons.COORDS['go_to_market'][1])

def anon_order():
    time.sleep(0.1)
    utils.click(cons.COORDS['anon_box'][0], cons.COORDS['anon_box'][1])

def send_gold(new_prices):
    for number in str(new_prices):
        time.sleep(0.1)
        utils.send_key(number)
    click_item()

def send_item_name_and_validate():
    for i in range(len(cons.COORDS['key_coins'])):
        time.sleep(0.1)
        utils.send_key(cons.COORDS['key_coins'][i])
    # TODO REPLACE THIS #

def cancel_offer(order_type):
    if order_type == 'ask':
        # utils.click(cons.COORDS['my_offers_first_ask'][0], cons.COORDS['my_offers_first_ask'][1])
        time.sleep(0.1)
        utils.click(cons.COORDS['my_offers_ask_cancel'][0], cons.COORDS['my_offers_ask_cancel'][1])
    elif order_type == 'bid':
        # utils.click(cons.COORDS['my_offers_first_bid'][0], cons.COORDS['my_offers_first_bid'][1])
        time.sleep(0.1)
        utils.click(cons.COORDS['my_offers_bid_cancel'][0], cons.COORDS['my_offers_bid_cancel'][1])

############ COMPLEX FUNCTIONS ##########################

def go_to_market_and_search():
    go_from_my_offers_to_market()
    send_item_name_and_validate()

def timeout_prevention():
    close_market()
    open_market()
    send_item_name_and_validate()

def create_order(new_prices, types, shadow_mode):
    ## Clicks sell or buy ##
    time.sleep(0.1)
    utils.click(cons.COORDS[types][0], cons.COORDS[types][1])
    time.sleep(0.1)
    ## Click price text box #
    click_price_text_box()
    ## Fill in the price ##
    send_gold(new_prices)
    # anonymize it #
    anon_order()
    if not shadow_mode:
        try:
            if utils.validate_entity(new_prices, 'number', 'price_box'):
                click_create_offer()
            else:
                utils.send_offer_checks(types, new_prices, shadow_mode)
        except:
            utils.send_offer_checks(types, new_prices, shadow_mode)

    anon_order()
    time.sleep(0.1)