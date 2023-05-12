# %%
import time
import game
import plotting
import config as c
from get_dataset import Get_dataset
from price_analysis import Price_analysis
from strategies import Strategies
from strategies import seek_opportunity
from performance import Performance
import run_control

def run():
    items = ['coin']
    gd_bids = []
    gd_asks = []
    pc_bids = []
    pc_asks = []
    st_bids = []
    st_asks = []

    for item in items:
        loop_counter = run_control.check_previous('ask')['loop_counter'] #TODO add item as argument
        # game.run_action_safely(lambda: go_to_item(item)) # TODO: IMPLEMENT
        gd_bid = Get_dataset('bid') # TODO add item as argument
        gd_ask = Get_dataset('ask')  # TODO add item as argument
        pc_bid = Price_analysis(gd_bid, 'bid')  # TODO add item as argument
        pc_ask = Price_analysis(gd_ask, 'ask') # TODO add item as argument
        st_bid = Strategies.Arbitrage(pc_bid, 'bid', 'wild')  # TODO add item as argument
        st_ask = Strategies.Arbitrage(pc_ask, 'ask', 'wild')  # TODO add item as argument
        pf = Performance(st_bid, st_ask)
        pf = pf.calculate_profit(st_ask)
        pf = pf.update_performance_markers(st_bid.successes, st_ask.successes)
        time.sleep(2)

    try:

        while(1):
            # for item in items:
            #
            #     for index, value in enumerate(items):
            #         game.run_action_safely(lambda: go_to_item(item))
            #         gd_ask[index] = gd_ask[index].run('ask', loop_counter)
            #         gd_bid[index] = gd_bid[index].run('bid', loop_counter)
            #         pc_bid[index] = Price_analysis(gd_bid[index], 'bid')
            #         pc_ask[index] = Price_analysis(gd_ask[index], 'ask')
            #         seek_opportunity(pc_bid[index], 'bid')
            #         seek_opportunity(pc_ask[index], 'ask')
            #         if not st_bid[index].order_set:
            #             if not pf[index].pause_buying:
            #                 st_bid[index] = st_bid[index].trade(pc_bid[index])
            #                 if st_bid[index].order_set:
            #                     c.image_can_appear = True
            #         else:
            #             st_bid[index] = st_bid[index].monitor_trades(pc_bid[index])
            #             if not st_bid[index].order_set:
            #                 c.image_can_appear = False # TODO REMOVE
            #
            #         if not st_ask[index].order_set:
            #             if not pf[index].pause_selling:
            #                 st_ask[index] = st_ask[index].trade(pc_ask[index])
            #         else:
            #             st_ask[index] = st_ask[index].monitor_trades(pc_ask[index])
            #
            #         pf[index] = pf[index].update_performance_markers()
            #
            #         if loop_counter > 10 and loop_counter % 10 == 0:
            #             pf[index] = pf[index].calculate_profit(st_ask[index])
            #             game.timeout_prevention()
            #             print('Timeout Prevention')
            #
            #         plotting[index].make_plots(value)
            #         loop_counter += 1
            #
            #
            game.run_action_safely(lambda: game.click_boxes())  # TODO replace this to swap between items
            #game.run_action_safely(lambda: go_to_item(item)) # TODO: IMPLEMENT
            time.sleep(0.25)

            gd_ask = gd_ask.run('ask', loop_counter)
            gd_bid = gd_bid.run('bid', loop_counter)
            pc_bid = Price_analysis(gd_bid, 'bid')
            pc_ask = Price_analysis(gd_ask, 'ask')

            if not st_bid.order_set:
                if not pf.pause_buying:
                    st_bid = st_bid.trade(pc_bid)
                    if st_bid.order_set:
                        c.image_can_appear = True
            else:
                st_bid = st_bid.monitor_trades(pc_bid)
                if not st_bid.order_set:
                    c.image_can_appear = False

            if not st_ask.order_set:
                if not pf.pause_selling:
                    st_ask = st_ask.trade(pc_ask)
                    c.image_can_appear = True
            else:
                st_ask = st_ask.monitor_trades(pc_ask)

            pf = pf.update_performance_markers(st_bid.successes, st_ask.successes)

            if loop_counter > 10 and loop_counter % 10 == 0:
                pf = pf.calculate_profit(st_ask)
                game.timeout_prevention()
                print('Timeout Prevention')

            plotting.make_plots()
            loop_counter += 1

    finally:
        offer_dict_ask = {
            'price': st_ask.price_new,
            'successes' : st_ask.successes,
            'failures' : st_ask.failures,
            'order_set' : st_ask.order_set,
            'staleness_counter': st_ask.staleness_counter,
            'loop_counter': loop_counter,
            'opened': gd_ask.added,
            'closed': gd_ask.sold
        }
        offer_dict_bid = {
            'price': st_bid.price_new,
            'successes' : st_bid.successes,
            'failures' : st_bid.failures,
            'order_set' : st_bid.order_set,
            'staleness_counter': st_bid.staleness_counter,
            'loop_counter': loop_counter,
            'opened': gd_bid.added,
            'closed': gd_bid.sold

        }
        run_control.dump_files('bid', offer_dict_bid)
        run_control.dump_files('ask', offer_dict_ask)


if __name__ == '__main__':
    run()

