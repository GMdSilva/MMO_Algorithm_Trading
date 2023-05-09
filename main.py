# %%
import time
import game
import plotting
import config as c
import utils
from get_dataset import Get_dataset
from price_analysis import Price_analysis
from strategies import Strategies
from strategies import seek_opportunity
from performance import Performance
import run_control

def run():
    loop_counter = 0
    gd_bid = Get_dataset('bid')
    gd_ask = Get_dataset('ask')
    pc_bid = Price_analysis(gd_bid, 'bid')
    pc_ask = Price_analysis(gd_ask, 'ask')
    st_bid = Strategies.Arbitrage(pc_bid, 'bid', 'wild')
    st_ask = Strategies.Arbitrage(pc_ask, 'ask', 'wild')
    pf = Performance(st_bid, st_ask)
    pf = pf.calculate_profit(st_ask)
    pf = pf.update_performance_markers()
    time.sleep(2)

    try:

        while(1):

            game.run_action_safely(lambda: game.click_boxes())
            time.sleep(0.25)

            gd_ask = gd_ask.run('ask', loop_counter)
            gd_bid = gd_bid.run('bid', loop_counter)
            pc_bid = Price_analysis(gd_bid, 'bid')
            pc_ask = Price_analysis(gd_ask, 'ask')

            seek_opportunity(pc_bid, 'bid')
            seek_opportunity(pc_ask, 'ask')

            if not st_bid.order_set:
                if not pf.pause_buying:
                    c.image_can_appear = True
                    st_bid = st_bid.trade(pc_bid)
            else:
                st_bid = st_bid.monitor_trades(pc_bid)
                if not st_bid.order_set:
                    c.image_can_appear = False

            if not st_ask.order_set:
                if not pf.pause_selling:
                    st_ask = st_ask.trade(pc_ask)
            else:
                st_ask = st_ask.monitor_trades(pc_ask)

            pf = pf.update_performance_markers()

            if loop_counter > 10 and loop_counter % 10 == 0:
                pf = pf.calculate_profit(st_ask)
                game.timeout_prevention()
                print('Timeout Prevention')

            plotting.make_plots()
            loop_counter += 1
            #time.sleep(0.1)

    finally:
        offer_dict_ask = {
            'price': st_ask.price_new,
            'successes' : st_ask.successes,
            'failures' : st_ask.failures,
            'order_set' : st_ask.order_set,
            'staleness_counter': st_ask.staleness_counter
        }
        offer_dict_bid = {
            'price': st_bid.price_new,
            'successes' : st_bid.successes,
            'failures' : st_bid.failures,
            'order_set' : st_bid.order_set,
            'staleness_counter': st_bid.staleness_counter
        }
        run_control.dump_files('bid',offer_dict_bid)
        run_control.dump_files('ask', offer_dict_ask)

#
#
# class MonitorClass(threading.Thread):
#     def __init__(self, image_appeared_event, can_image_appear):
#         threading.Thread.__init__(self)
#         self.image_appeared_event = image_appeared_event
#         self.can_image_appear = can_image_appear
#         self.running = True
#
#     def run(self, image_path=cons.THE_DEVIl_PATH):
#         while self.running:
#             try:
#                 self.can_image_appear.wait()
#                 image = pyautogui.locateOnScreen(image_path)
#
#                 # Check the boolean variable before checking for the image:
#                 if pyautogui.locateOnScreen(image_path, region=image, confidence=.9) is not None:
#                     print('Image found!')
#                     # Image found, update the boolean variable and clear the event
#                     self.image_appeared_event.set()
#                     self.can_image_appear.clear()
#                     game.bye_confirmation_box()
#                     self.image_appeared_event.clear()
#
#                 time.sleep(0.1)
#
#             except KeyboardInterrupt:
#                 self.running = False


if __name__ == '__main__':
    run()
    # # Create the shared boolean
    # image_appeared_event = threading.Event()
    # image_appeared_event.clear()
    # # Create the threads
    # program_thread = ProgramClass(image_appeared_event)
    # monitor_thread = MonitorClass(image_appeared_event)
    # # Start the threads
    # program_thread.start()
    # monitor_thread.start()

    # try:
    #     # Wait for the threads to finish
    #     # program_thread.join()
    #     # monitor_thread.join()
    # except KeyboardInterrupt:
        # Set the running flag to False to terminate the threads
        # program_thread.running = False
        # monitor_thread.running = False
        # Wait for the threads to finish
        # program_thread.join()
        # monitor_thread.join()

# %%
