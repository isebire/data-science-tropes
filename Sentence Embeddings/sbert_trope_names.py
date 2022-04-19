import pickle

DATA_FILEPATH = 'trope_description_laconic_dict.pkl'

# Load the tropes description data
with open(DATA_FILEPATH, 'rb') as f:
    data = pickle.load(f)

trope_names = list(data.keys())

# Save
with open('trope_names_list.pkl', 'wb') as f:
    pickle.dump(trope_names, f)
