import time
import win32api
import win32gui
from win_interface import Windows_Interface
import keyboard
#from vision import Vision
import pickle
import config
#vision = Vision()

class Setup(Windows_Interface):
    def __init__(self):
        super().__init__()
        self.test_points = ['item_query', 'x_button', 'open_market', 'bid', 'my_offers']
        self.click_coords = config.coords #{
        #     'item_swap': (945, 697),
        #     'item_query': (945, 739),
        #     'x_button': (1070, 915),
        #     'close_market': (1623, 959),
        #     'open_market': (2525, 502),
        #     'text_box': (1323, 889),
        #     'create_offer': (1609, 917),
        #     'ask': (1094, 853),
        #     'bid': (1095, 870),
        #     'go_to_market': (1603, 960),
        #     'my_offers_ask_cancel': (1610, 479),
        #     'my_offers_bid_cancel': (1610, 713),
        #     'my_offers': (1517, 956),
        #     'anon_box': (1506, 913),
        # }
        # self.ss_coordinates = {
        # 'offers': (1267, 528, 50, 281),
        # 'price_box': (1277, 882, 43, 13),
        # 'gold_box': (959, 948, 79, 18),
        # 'coin_box': (1103, 948, 42, 18),
        # 'search_box': (961, 911, 37, 12),
        # 'market_location': (1305, 500, 58, 300),
        # }
        # self.item_letters = {
        #     'key_coins': ['c', 'o', 'i', 'n'],
        # }
        self.update_specific = ['accept_box_bid', 'accept_box_ask']
    def get_4_points(self, key):
        self.mouse_over_element(key)
        x1, y1 = win32api.GetCursorPos()
        self.mouse_out(key)
        coords1 = win32gui.ScreenToClient(self.hwnd, (x1, y1))
        self.mouse_over_element(key)
        x2, y2 = win32api.GetCursorPos()
        self.mouse_out(key)
        coords2 = win32gui.ScreenToClient(self.hwnd, (x2, y2))
        x, y = coords1[0], coords1[1]
        h = coords2[1] - y
        w = coords2[0] - x
        coords = [x,y,w,h]
        print(coords)
        return coords

    def wait_for_user(self):
        result = False
        while True:
            if keyboard.is_pressed('1'):
                keyboard.release('1')
                time.sleep(0.1)
                result = True
                return result
            elif keyboard.is_pressed('2'):
                keyboard.release('2')
                time.sleep(0.111)
                return result

    def mouse_over_element(self, key):
        print(f"Put Mouse over {key}")
        print("Press Enter When Ready")
        self.wait_for_user()

    def mouse_out(self, key):
        print(f"Position of {key} set")

    def get_location(self, key):
        self.mouse_over_element(key)
        x, y = win32api.GetCursorPos()
        self.mouse_out(key)
        coords = win32gui.ScreenToClient(self.hwnd, (x, y))
        return coords11

    def update_coords(self):
        for key in self.update_specific:
            print(f"Now setting {key}")
            coords = self.get_location(key)
            self.click_coords.update({key: coords})
            time.sleep(1)

    def update_4_coords(self):
        for key in self.update_specific:
            print(f"Now setting {key}")
            coords = self.get_4_points(key)
            self.click_coords.update({key: coords})
            time.sleep(1)

    def run_item_query_test(self):
        print('Testing market swap/reload')
        time.sleep(1)
        self.left_click(self.click_coords['item_query'])
        time.sleep(1)
        self.left_click(self.click_coords['item_swap'])
        time.sleep(1)
        print("Did the market swap indexes?")
        print("Send Enter if yes, press any other key if no")
        result = self.wait_for_user()
        if result:
            print("Testing market swap successful, moving on")
        else:
            time.sleep(0.5)
            print("Testing failed, would you like to test again?")
            print("Press enter to try again, press any other key to re-do setup")
            result = self.wait_for_user()
            if result:
                time.sleep(0.5)
                self.run_item_query_test()
            else:
                time.sleep(0.5)
                print('Re-doing item query/item swap coordinate selection')
                failed_tests = ['item_swap', 'item_query']
                for key in failed_tests:
                    print(f"Now setting {key}")
                    coords = self.get_location(key)
                    self.click_coords.update({key: coords})
                    time.sleep(1)
                self.run_item_query_test()
                time.sleep(0.5)

    def run_x_test(self):
        print('Testing clear button')
        time.sleep(1)
        print('Write something on search box, then press "Q"')
        result = self.wait_for_user()
        if result:
            time.sleep(1)
            self.left_click(self.click_coords['x_button'])
            time.sleep(1)
            print("Did the text clear? Press 'Q' if so, 'T' if no")
            result = self.wait_for_user()
            if result:
                print('Testing clear button successful, moving on')
            else:
                print("Testing failed, would you like to test again?")
                print("Press enter to try again, press any other key to re-do setup")
                result = self.wait_for_user()
                time.sleep(0.5)
                if result:
                    time.sleep(0.5)
                    self.run_x_test()
                else:
                    time.sleep(0.5)
                    print('Re-doing clear box coordinate selection')
                    failed_tests = ['x_button']
                    for key in failed_tests:
                        print(f"Now setting {key}")
                        coords = self.get_location(key)
                        self.click_coords.update({key: coords})
                        time.sleep(1)
                    self.run_x_test()
                    time.sleep(0.5)

    def run_market_test(self):
        print('Testing market open/close')
        time.sleep(1)
        self.left_click(self.click_coords['close_market'])
        time.sleep(1)
        self.right_click(self.click_coords['open_market'])
        time.sleep(1)
        print("Did the market close and open?")
        print("Send Enter if yes, press any other key if no")
        result = self.wait_for_user()
        if result:
            print("Testing market close and open")
        else:
            time.sleep(0.5)
            print("Testing failed, would you like to test again?")
            print("Press enter to try again, press any other key to re-do setup")
            result = self.wait_for_user()
            if result:
                time.sleep(0.5)
                self.run_market_test()
            else:
                time.sleep(0.5)
                print('Re-doing market open/market_close coordinate selection')
                failed_tests = ['close_market', 'open_market']
                for key in failed_tests:
                    print(f"Now setting {key}")
                    coords = self.get_location(key)
                    self.click_coords.update({key: coords})
                    time.sleep(1)
                self.run_market_test()
                time.sleep(0.5)

    def run_ask_bid_test(self):
        print('Testing ask/bid buttons')
        time.sleep(1)
        self.left_click(self.click_coords['text_box'])
        time.sleep(1)
        self.left_click(self.click_coords['bid'])
        time.sleep(1)
        self.left_click(self.click_coords['ask'])
        time.sleep(1)
        print("Did the market price box, ask and bid buttons worked?")
        print("Send Enter if yes, press any other key if no")
        result = self.wait_for_user()
        if result:
            print("Testing market close and open")
        else:
            time.sleep(0.5)
            print("Testing failed, would you like to test again?")
            print("Press enter to try again, press any other key to re-do setup")
            result = self.wait_for_user()
            if result:
                time.sleep(0.5)
                self.run_ask_bid_test()
            else:
                time.sleep(0.5)
                print('Re-doing market open/market_close coordinate selection')
                failed_tests = ['test_box', 'bid', 'ask']
                for key in failed_tests:
                    print(f"Now setting {key}")
                    coords = self.get_location(key)
                    self.click_coords.update({key: coords})
                    time.sleep(1)
                self.run_ask_bid_test()
                time.sleep(0.5)



def main():

    st = Setup()
    st.update_coords()
    #st.update_4_coords()
    print(st.click_coords)
    file = open('config.txt', 'wb')
    pickle.dump(st.click_coords, file)
    file.close()
