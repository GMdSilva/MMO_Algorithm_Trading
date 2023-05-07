# %%
import pyautogui
import time
import cons
import game
import plotting
import utils
import config as c
from get_dataset import Get_dataset
from price_analysis import Price_analysis
from strategies import Strategies
from performance import Performance
import threading


class ProgramClass(threading.Thread):
    def __init__(self, image_appeared_event, can_image_appear):
        threading.Thread.__init__(self)
        self.image_appeared_event = image_appeared_event
        self.can_image_appear = can_image_appear
        self.running = True

    def run(self):
        counter = 0
        gd_bid = Get_dataset('bid', counter)
        gd_ask = Get_dataset('ask', counter)
        pc_bid = Price_analysis(gd_bid, 'bid')
        pc_ask = Price_analysis(gd_ask, 'ask')
        st_bid = Strategies.Arbitrage(pc_bid, 'bid', 'wild')
        st_ask = Strategies.Arbitrage(pc_ask, 'ask', 'wild')
        pf = Performance(st_bid, st_ask)
        pf = pf.calculate_profit(st_ask)
        pf = pf.update_performance_markers()
        time.sleep(2)

        while self.running:
            try:
                if self.can_image_appear == True:
                    self.image_appeared_event.wait()
                game.click_boxes()

                gd_ask = gd_ask.run('ask', counter)

                gd_bid = gd_bid.run('bid', counter)

                pc_bid = Price_analysis(gd_bid, 'bid')

                pc_ask = Price_analysis(gd_ask, 'ask')

                # if not pf.pause_buying:
                if st_bid.order_set == False:
                    st_bid = st_bid.trade(pc_bid)
                    self.can_image_appear.set()
                else:
                    st_bid = st_bid.monitor_trades(pc_bid)
                    if st_bid.order_set == False:
                        self.can_image_appear.clear()

                game.click_boxes()

                if st_ask.order_set == False:
                    st_ask = st_ask.trade(pc_ask)
                else:
                    st_ask = st_ask.monitor_trades(pc_ask)

                pf = pf.update_performance_markers()

                if counter > 10 and counter % 10 == 0:
                    pf = pf.calculate_profit(st_ask)
                    game.timeout_prevention()

                plotting.make_plots()
                counter += 1
                time.sleep(0.5)

                if self.can_image_appear == True:
                    self.image_appeared_event.wait()

            except KeyboardInterrupt:
                self.running = False


class MonitorClass(threading.Thread):
    def __init__(self, image_appeared_event, can_image_appear):
        threading.Thread.__init__(self)
        self.image_appeared_event = image_appeared_event
        self.can_image_appear = can_image_appear
        self.running = True

    def run(self, image_path=cons.THE_DEVIl_PATH):
        while self.running:
            try:
                self.can_image_appear.wait()
                image = pyautogui.locateOnScreen(image_path)

                # Check the boolean variable before checking for the image:
                if pyautogui.locateOnScreen(image_path, region=image, confidence=.9) is not None:
                    print('Image found!')
                    # Image found, update the boolean variable and clear the event
                    self.image_appeared_event.set()
                    self.can_image_appear.clear()
                    utils.send_key('enter')
                    game.bye_confirmation_box()
                    self.image_appeared_event.clear()

                time.sleep(0.1)

            except KeyboardInterrupt:
                self.running = False


if __name__ == '__main__':
    # Create the shared boolean
    image_appeared_event = threading.Event()
    image_appeared_event.clear()
    can_image_appear = threading.Event()
    can_image_appear.clear()
    # Create the threads
    program_thread = ProgramClass(image_appeared_event, can_image_appear)
    monitor_thread = MonitorClass(image_appeared_event, can_image_appear)
    # Start the threads
    program_thread.start()
    monitor_thread.start()

    try:
        # Wait for the threads to finish
        program_thread.join()
        monitor_thread.join()
    except KeyboardInterrupt:
        # Set the running flag to False to terminate the threads
        program_thread.running = False
        monitor_thread.running = False
        # Wait for the threads to finish
        program_thread.join()
        monitor_thread.join()

# %%
