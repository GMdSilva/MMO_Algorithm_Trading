from playsound import playsound
import run_control
import cons
import game
import utils
import vision as vs
from price_analysis import Price_analysis


class Strategies(Price_analysis):
    def __init__(self, pc, order_type, method):
        self.arb = self.Arbitrage(pc, order_type, method)
        self.opp = self.Opportunism()

    class Arbitrage(Price_analysis):
        def __init__(self, pc, order_type, method):
            self.offer_list = 0  ## FIX THIS ##
            self.order_set = run_control.check_previous(order_type)['order_set']
            self.index = False
            self.found = False
            self.offer_accepted = False
            self.market_bad = False
            self.index = 0
            self.price_new = run_control.check_previous(order_type)['price']
            self.successes = run_control.check_previous(order_type)['successes']
            self.failures = run_control.check_previous(order_type)['failures']
            self.staleness_counter = run_control.check_previous(order_type)['staleness_counter']
            self.is_order_stale = False
            self.order_type = order_type
            self.market_timer = 0
            self.timer = 0
            self.trade_method = method
            self.duplicate_checker = 0
            if self.trade_method == 'wild':
                self.staleness_threshold = 30
            if self.trade_method == 'simulation':
                self.shadow_mode = True
            else:
                self.shadow_mode = False

        def place_order(self, pc):
            """Places order on market at current price +/- 1.
            """
            if self.order_type == 'bid':
                self.price_new = pc.update_price(pc.current_price_bid,
                                                 self.order_type, self.shadow_mode)  # gets current price + 1 #
            if self.order_type == 'ask':
                self.price_new = pc.update_price(pc.current_price_ask,
                                                 self.order_type, self.shadow_mode)  # gets current price + 1 #
            self.order_set = game.create_order(self.price_new, self.order_type, self.shadow_mode)
            return self  # returns updated price + order status #

        def monitor_orders(self):
            """Monitors orders set by place_order.
            Checks if order exists and updates counter if not
            """
            self.index = 0
            if self.duplicate_checker > 1:
                # TODO # IMPLEMENT THE DANGER ZONE
                print('Welcome to the danger zone')
            self.found = False  # resets check condition #
            self.duplicate_checker = 0
            self.offer_list = utils.get_price_data(self.order_type)
            for i, offer in enumerate(self.offer_list):  # loops over current top 4 offers in market #
                if offer == self.price_new:  # if offer is within top 4, we're good #
                    self.duplicate_checker += 1
                    self.index = i
                    self.staleness_counter += 1
                    if self.market_timer >= 5 and self.market_timer % 5 == 0:
                        print(f'{self.order_type} Offer is at index {self.index}!')
                    if self.index < 3:
                        self.found = True
                        return self

            def check_if_sold():
                """Does the actual checking.
                Only checks in your "offers" tab, we use the Vision module for the market tab.
                """
                game.run_action_safely(game.go_to_offers())  # goes to my offers list #
                my_offers = game.run_action_safely(lambda: vs.capture_text('offers'))  # captures prices #
                self.offer_accepted = True  # ugly, but gets the job done #
                my_offers = utils.sanitize_and_check_numbers(my_offers)
                for offer in my_offers:  # check my offers line by line #
                    if offer == self.price_new:  # if we find our offer, turns out we didn't sell/buy :( #
                        self.offer_accepted = False
                game.run_action_safely(lambda: game.go_from_my_offers_to_market())  # returns to market #

            def check_offers_window():
                """Checks my offers tab to see if previous offer is there.
                Updates either the success or fail counter based on the above.
                """
                check_if_sold()  # see if offer sank or was sold #
                if not self.offer_accepted:
                    if self.staleness_counter > self.staleness_threshold:
                        self.is_order_stale = True
                        self.staleness_counter = 0  # updates counter of staleness #
                return self

            def update_success():
                if self.offer_accepted:
                    self.order_set = False
                    self.successes.append(self.price_new)
                    print(f"Offer for {self.order_type} at price {self.price_new} closed!"
                          f" Successes at {self.order_type}: {len(self.successes)}")
                return self

            if not self.found:
                if self.trade_method is 'wild' or self.trade_method is 'simulation':
                    if self.index >= 3 or self.staleness_counter > self.staleness_threshold:
                        self.is_order_stale = True
                        self.staleness_counter = 0
                    else:
                        self.offer_accepted = True
                        update_success()
                else:
                    check_offers_window()

            return self

        def cancel_specific_offer(self):
            """Cancel stale offers and updates checks.
            """
            game.run_action_safely(lambda: game.go_to_offers())
            game.cancel_offer(self.order_type)
            game.run_action_safely(lambda: game.go_from_my_offers_to_market())
            self.failures.append(self.price_new)
            self.order_set = False
            self.is_order_stale = False

            return self

        def trade(self, pc):
            if pc.self_critique():
                if not self.order_set:
                    if pc.calculate_total_profit() > cons.MIN_PROFIT_PERCENTAGE:
                        if self.market_bad:
                            self.market_bad = False
                            print(f"Market is good for arbitrage, profit/trade: {pc.calculate_total_profit()}")
                        self.place_order(pc)
                        if self.order_set:
                            print(f"Set {self.order_type} offer at price {self.price_new},"
                                  f" monitoring with strategy: {self.trade_method}")
                    else:
                        if not self.market_bad:
                            self.market_bad = True
                            print(f"Market is not good for arbitrage, profit/trade: {pc.calculate_total_profit()}")
            self.market_timer += 1
            return self

        def monitor_trades(self, pc):
            """Sets trade flow so that orders are only created when necessary.
            Also controls all the monitoring and closing.
            """
            if self.order_set:  # if current offer is set, monitor it #
                self.monitor_orders()  # 3 true outcomes #

                if self.is_order_stale:  # if staleness counter is above threshold, cancel order and eat the loss #
                    self.cancel_specific_offer()
                    print(f"Offer for {self.order_type} at price {self.price_new} stale, canceling"
                          f" Failures at {self.order_type} {self.failures[-1]}")

            self.market_timer += 1
            return self

    class Opportunism:
        def __init__(self):
            self.played_sound = False

def seek_opportunity(pc, order_type):
    played_sound = False
    percent = pc.get_percent_diff()
    if order_type == 'bid' and percent <= cons.THRESH_DOWN and played_sound is False:
        print(percent)
        playsound(cons.AUDIO)
        played_sound = False
    if order_type == 'ask' and percent >= cons.THRESH_UP and played_sound is False:
        print(percent)
        playsound(cons.AUDIO)
        played_sound = False
    # if pc.counter %  == 0:
    #     self.played_sound = False
