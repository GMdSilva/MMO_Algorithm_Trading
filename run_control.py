import pickle

def dump_files(offer_type, offer_dict):
    file = open(offer_type+"_dump.txt", "wb")
    pickle.dump(offer_dict, file)
    file.close()

def check_previous(offer_type):
    with open(offer_type+'_dump.txt', 'rb') as handle:
        data = handle.read()
        previous_results = pickle.loads(data)
    return previous_results

offer_dict = {
    'price': 0,
    'successes' : [],
    'failures' : [],
    'order_set' : False
}