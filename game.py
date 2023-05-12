import time
import cons
import config
import utils
import vision as vs

def run_action_safely(fun):
    # if not config.image_can_appear:
    #     return fun()
    # else:
    # if vs.Vision.check_if_image_on_screen(cons.THE_DEVIL_PATH, threshold=0.9):
        #print('Image found!')
        #config.image_can_appear = False # TODO REMOVE
    bye_confirmation_box()
    return fun()


def click_item():
    utils.click(cons.COORDS['item_query'][0], cons.COORDS['item_query'][1]) # TODO UPDATE TO ITEM POSITION ?
    #time.sleep(0.1)

def click_accept(order_type):
    if order_type == 'bid':
        utils.click(cons.COORDS['accept_box_bid'][0],(cons.COORDS['accept_box_bid'][1]))
    if order_type == 'ask':
        utils.click(cons.COORDS['accept_box_ask'][0], (cons.COORDS['accept_box_ask'][1]))

def click_boxes():
    utils.click(cons.COORDS['item_swap'][0], cons.COORDS['item_swap'][1])
    utils.click(cons.COORDS['item_query'][0], cons.COORDS['item_query'][1])
    time.sleep(0.2)

def close_market():
    utils.click(cons.COORDS['close_market'][0], cons.COORDS['close_market'][1])
    #time.sleep(0.1)

def open_market():
    utils.right_click(cons.COORDS['open_market'][0], cons.COORDS['open_market'][1])
    #time.sleep(0.1)

def click_price_text_box():
    utils.click(cons.COORDS['text_box'][0], cons.COORDS['text_box'][1])
    #time.sleep(0.1)

def click_create_offer():
    utils.click(cons.COORDS['create_offer'][0], cons.COORDS['create_offer'][1])
    time.sleep(0.1)

def go_to_offers():
    utils.click(cons.COORDS['my_offers'][0], cons.COORDS['my_offers'][1])
    #time.sleep(0.1)

def bye_confirmation_box():
    time.sleep(0.1)
    utils.send_enter()

def go_from_my_offers_to_market():
    utils.click(cons.COORDS['go_to_market'][0], cons.COORDS['go_to_market'][1])
    #time.sleep(0.1)

def anon_order():
    utils.click(cons.COORDS['anon_box'][0], cons.COORDS['anon_box'][1])
    #time.sleep(0.1)

def click_x():
    utils.click(cons.COORDS['x_button'][0], cons.COORDS['x_button'][1])
    #time.sleep(0.1)

def send_gold(new_prices):
    try:
        new_prices = int(new_prices)
    except ValueError:
        print('Price is not integer, recheck image capture')
   #run_action_safely(lambda: utils.select_all())
    run_action_safely(lambda: utils.delete())
    #for number in str(new_prices):
    run_action_safely(lambda: utils.send_key(str(new_prices)))

def check_if_enough_resources(offer_type):
    # TODO
    pass

def send_item_name():
    run_action_safely(lambda: click_x())
    run_action_safely(lambda: click_item())
    time.sleep(0.1)
    #or i in range(len(cons.COORDS['key_coins'])):
    run_action_safely(lambda: utils.send_key(cons.COORDS['key_coins'])) # TODO IMPLEMENT CORRECT NAME


def cancel_offer(order_type):
    if order_type == 'ask':
        # utils.click(cons.COORDS['my_offers_first_ask'][0], cons.COORDS['my_offers_first_ask'][1]) # TODO IMPLEMENT
        time.sleep(0.1)
        run_action_safely(lambda: utils.click(cons.COORDS['my_offers_ask_cancel'][0], cons.COORDS['my_offers_ask_cancel'][1]))
    elif order_type == 'bid':
        # utils.click(cons.COORDS['my_offers_first_bid'][0], cons.COORDS['my_offers_first_bid'][1]) # TODO IMPLEMENT
        time.sleep(0.1)
        run_action_safely(lambda: utils.click(cons.COORDS['my_offers_bid_cancel'][0], cons.COORDS['my_offers_bid_cancel'][1]))


############ COMPLEX FUNCTIONS ##########################

# def go_to_market_and_search():
#     run_action_safely(lambda: go_from_my_offers_to_market())
#     send_item_name()


def timeout_prevention():
    run_action_safely(lambda: close_market())
    run_action_safely(lambda: open_market())
    send_item_name() # TODO REMOVE


def create_order(new_prices, types, shadow_mode):
    ## Clicks sell or buy ##
    #time.sleep(0.1)
    run_action_safely(lambda: utils.click(cons.COORDS[types][0], cons.COORDS[types][1]))
    #time.sleep(0.1)
    ## Click price text box #
    run_action_safely(lambda: click_price_text_box())
    ## Fill in the price ##
    send_gold(new_prices)
    # anonymize it #
    if not shadow_mode:
        if utils.validate_entity(new_prices, 'number', 'price_box'):
            if utils.validate_order_type(types):
                run_action_safely(lambda: anon_order())
                run_action_safely(lambda: click_create_offer())
                run_action_safely(lambda: anon_order())
                return True
            else:
                print('cant validate money')
                return False
        else:
            print('cant validate prices')
            utils.send_offer_checks(new_prices, types, shadow_mode)
    else:
        return True
