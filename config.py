import pickle

def get_configs():
    with open('config.txt', 'rb') as handle:
        data = handle.read()
        previous_results = pickle.loads(data)
    return previous_results

image_can_appear = False
char_name = 'tibia - dorivall intermedlo'
coords = get_configs()

def initialize():
    for filename in ['bid_dump.txt', 'ask_dump.txt']:
        dict = {
            'order_set': False,
            'price': 0,
            'successes': [],
            'failures': [],
            'staleness_counter': 0,
            'loop_counter': 0,
            'opened': 0,
            'closed': 0
        }

        file = open(filename, "wb")
        pickle.dump(dict, file)
        file.close()