import vision as vs
import game


class Performance:
    def __init__(self, arb_bids, arb_asks):
        self.cycles = 0
        self.starting_gold = 0
        self.starting_coin = 0
        self.current_gold = 0
        self.current_coin = 0
        self.gold_profit = 0
        self.coin_profit = 0
        self.coin_price = 0
        self.combined_profit = 0
        self.bids_successes = arb_bids.successes
        self.asks_successes = arb_asks.successes

        self.bids_failed = arb_bids.failures
        self.asks_failed = arb_bids.failures

        self.checked_performance = False

        self.success_diff = 0
        self.failure_diff = 0

        self.pause_selling = False
        self.pause_buying = False

    def get_coin_price(self, new_price):
        self.coin_price = new_price
        return self

    def update_resources(self):
        if self.cycles == 0:
            self.starting_gold = game.run_action_safely(lambda: vs.read_resources('gold_box'))
            print(f'Starting gold is: {self.starting_gold}')
            self.starting_coin = game.run_action_safely(lambda: vs.read_resources('coin_box'))
            print(f'Starting coin is {self.starting_coin}')
            self.cycles += 1
        else:
            self.current_gold = game.run_action_safely(lambda: vs.read_resources('gold_box'))
            self.current_coin = game.run_action_safely(lambda: vs.read_resources('coin_box'))
            self.cycles += 1
        return self

    def calculate_profit(self, arb_asks):
        self.update_resources()
        self.get_coin_price(arb_asks.price_new)
        self.gold_profit = self.current_gold - self.starting_gold
        self.coin_profit = (self.current_gold - self.starting_gold) * self.coin_price
        self.combined_profit = self.gold_profit + self.coin_profit
        return self

    def calculates_sale_offset(self):
        self.success_diff = len(self.bids_successes) - len(self.asks_successes)
        self.failure_diff = len(self.bids_successes) - len(self.asks_successes)
        return self

    def update_performance_markers(self):
        self.calculates_sale_offset()
        if not self.checked_performance:
            if self.success_diff > 2:
                print(f'We are buying more than selling, slow down the buying!')
                self.checked_performance = True
                self.pause_buying = True
            elif self.success_diff < -2:
                print(f'We are selling more than we are buying, slow down the selling! {self.success_diff}')
                self.checked_performance = True
                self.pause_selling = True
            elif self.failure_diff > 2:
                print(f'We are cancelling a lot of sales, slow down the selling!')
                self.checked_performance = True
                self.pause_selling = True
            elif self.failure_diff < -2:
                print(f'We are cancelling a lot of bids, slow down the buying!')
                self.checked_performance = True
                self.pause_buying = True
            else:
                self.pause_selling = False
                self.pause_buying = False
                self.checked_performance = False
        return self

        # def calculate_income(self, type):
        #     if type == 'successful_trades':
        #         revenue = cons.BATCH * (self.consummated_asks[-1] - self.consummated_bids[-1])
        #         fees = cons.BATCH * cons.BUY_FEE * (self.consummated_asks[-1] + self.consummated_bids[-1])
        #     else:
        #         revenue = 0
        #         fees = cons.BATCH * cons.BUY_FEE * (self.canceled_asks[-1] + self.canceled_bids[-1])
        #     income = revenue - fees
        #     return income
        #
        # def calculate_profit(self):
        #     profit = self.calculate_income('success')
        #     self.total_profit += self.total_profit
        #     return self
        #
        # def calculate_loss(self):
        #     profit = self.calculate_income('failure')
        #     self.total_loss += profit
        #     return self
        #
        # def get_outcome(self):
        #     if self.new_value == True:
        #         self.calculate_profit()
        #         print(self.total_profit, self.total_loss)
        #     if self.new_value == True:
        #         self.calculate_loss()
        #     self.outcome = self.total_profit + self.total_loss

# def calculate_performance(self, current_resource, starting_resource):
#     perf_resource = current_resource - starting_resource
#     return perf_resource
#
# def set_update_frequency(self):
#     ## TODO ##
#
#     print(total_profit)
