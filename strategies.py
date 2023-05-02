from playsound import playsound

import cons
import game
import utils
import vision
import vision as vs
from price_analysis import Price_analysis


class Strategies(Price_analysis):
    def __init__(self):
        self.profit = 0
        self.loss = 0

    class Arbitrage(Price_analysis):
        def __init__(self, pc, order_type):
            self.offer_list = 0  ## FIX THIS ##
            self.order_set = False
            self.index = False
            self.found = False
            self.offer_accepted = False
            self.index = 0
            self.price_new = 0
            self.success_counter = 0
            self.failure_counter = 0
            self.stale_counter = 0
            self.order_type = order_type

        def place_order(self, pc):
            """Places order on market at current price +/- 1.
            """
            if self.order_type == 'bid':
                self.price_new = pc.update_price(pc.current_price_bid, self.order_type)  # gets current price + 1 #
            if self.order_type == 'ask':
                self.price_new = pc.update_price(pc.current_price_ask, self.order_type)  # gets current price + 1 #
            # try:
            game.create_order(self.price_new, self.order_type)
            self.order_set = True  # order is set! (hopefully) #
            #  except:
            # print("Something went wrong when setting order")
            return self  # returns updated price + order status #

        def monitor_orders(self):
            """Monitors orders set by place_order.
            Checks if order exists and updates counter if not
            """
            self.found = False  # resets check condition #
            self.offer_list = vs.capture_text('market_location')
            self.offer_list = utils.sanitize_and_check_numbers(self.offer_list)
            for offer in self.offer_list:  # loops over current top 4 offers in market #
                print("Offers " + str(offer))
                if offer == self.price_new:  # if offer is within top 4, we're good #
                    self.index = offer  # gets where the offer is for future reasons #
                    print('found!')
                    self.found = True
                    return self

            def check_if_sold():
                """Does the actual checking.
                Only checks in your "offers" tab, we use the Vision module for the market tab.
                """
                game.go_to_offers()  # goes to my offers list #
                my_offers = vs.capture_text('offers')  # captures prices #
                self.offer_accepted = True  # ugly, but gets the job done #
                my_offers = utils.sanitize_and_check_numbers(my_offers)
                for offer in my_offers:  # check my offers line by line #
                    print(offer)
                    if offer == self.price_new:  # if we find our offer, turns out we didn't sell/buy :( #
                        self.offer_accepted = False
                game.go_to_market()  # returns to market #
                if self.offer_accepted:
                    self.order_set = False
                    self.success_counter += 1
                    print("Successes: " + str(self.success_counter))
                return self

            def check_offers_window():
                """Checks my offers tab to see if previous offer is there.
                Updates either the success or fail counter based on the above.
                """
                check_if_sold()  # see if offer sank or was sold #
                if not self.offer_accepted:
                    self.stale_timer += 1  # updates counter of staleness #
                    print("Failures "+str(self.stale.timer))
                return self

            if not self.found:
                check_offers_window()

            return self

        def cancel_specific_offer(self, offer_index):
            """Cancel stale offers and updates checks.
            """
            game.go_to_offers()
            game.cancel_offer(self.order_type)
            game.go_to_market()
            self.failure_counter += 1
            self.order_set = False

            return self

        def trade_flow(self, pc):
            """Sets trade flow so that orders are only created when necessary.
            Also controls all the monitoring and closing.
            """
            if pc.self_critique():
                if pc.calculate_total_profit() > cons.MIN_PROFIT_PERCENTAGE:
                    if not self.order_set:
                        self.place_order(pc)

                    elif self.order_set:  # if current offer is set, monitor it #
                        self.monitor_orders()  # 3 true outcomes #

                    if self.stale_counter > 50:  # if staleness counter is above threshold, cancel order and eat the loss #
                        self.cancel_order()
                else:
                    print("Bad market :(")
            else:
                print("Something is wrong with Vision module")
            return self

    class Opportunism:
        def __init__(self):
            self.played_sound = False

        def seek_opportunity(self, pc):
            if pc.self_critique():
                percent_up, percent_down = pc.get_percent_diff()
                if percent_up >= cons.THRESH_UP and self.played_sound is False:
                    playsound(cons.AUDIO)
                    self.played_sound = True
                if percent_down <= cons.THRESH_DOWN and self.played_sound is False:
                    playsound(cons.AUDIO)
                    self.played_sound = True
                if pc.counter % 50 == 0:
                    self.played_sound = False

    def trade_opportunism(self, pc):
        opp = self.Oportunism()
        return opp

