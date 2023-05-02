import vision as vs
from strategies import Strategy

class Performance(Strategy):
    def __init__(self, st):
        self.cycles = 0
        self.starting_gold = 0
        self.starting_coin = 0
        self.current_gold = 0
        self.current_coin = 0
        self.n_sus_transcations = st.n_sus_transactions
        self.n_failed_transactions = st.n_failed_transactions

    def update_resources(self):
        if cycles == 0:
            self.starting_gold = vs.get_resources('gold')
            self.starting_coin = vs.get_resources('coins')
        else:
            self.current_gold = vs.get_resources('gold')
            self.current_coin = vs.get_resources('coins')
        return self

    def calculate_performance(self, current_resource, starting_resource):
        perf_resource = current_resource - starting_resource
        return perf_resource

    def set_update_frequency():


