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
    loop_counter = run_control.check_previous('ask')['loop_counter']
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
            else:
                st_ask = st_ask.monitor_trades(pc_ask)

            pf = pf.update_performance_markers()

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
        run_control.dump_files('bid',offer_dict_bid)
        run_control.dump_files('ask', offer_dict_ask)


if __name__ == '__main__':
    run()

