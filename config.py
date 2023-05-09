import pickle

def get_configs():
    with open('config.txt', 'rb') as handle:
        data = handle.read()
        previous_results = pickle.loads(data)
    return previous_results

image_can_appear = False
char_name = 'tibia'
coords = get_configs()

