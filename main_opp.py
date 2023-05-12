# %%
import time
import game
import plotting
from get_dataset import Get_dataset
from price_analysis import Price_analysis
from strategies import seek_opportunity
import run_control

def run():
    items = ['coin']
    for item in items:
        loop_counter = run_control.check_previous('ask')['loop_counter'] #TODO add item as argument
        # game.run_action_safely(lambda: go_to_item(item)) # TODO: IMPLEMENT
        gd_bid = Get_dataset('bid') # TODO add item as argument
        gd_ask = Get_dataset('ask')  # TODO add item as argument
        time.sleep(2)

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
        gd_ask = gd_ask.run('ask', loop_counter)
        gd_bid = gd_bid.run('bid', loop_counter)
        bid_pct, bid_previous_price, bid_crt_price = gd_bid.get_percent_diff('bid')
        ask_pct, ask_previous_price, ask_crt_price = gd_bid.get_percent_diff('bid')
        seek_opportunity(bid_pct, bid_previous_price, bid_crt_price, 'bid')
        seek_opportunity(ask_pct, ask_previous_price, ask_crt_price, 'ask')

        if loop_counter > 100 and loop_counter % 100 == 0:
            game.timeout_prevention()
            print('Timeout Prevention')

        plotting.make_plots()
        loop_counter += 1

if __name__ == '__main__':
    run()

