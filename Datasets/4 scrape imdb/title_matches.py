import pickle

title_matches = {}

for i in range(12):
    filename = 'title_matches_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_dict = pickle.load(f)
        title_matches.update(chunk_dict)

removal_total = []

for i in range(12):
    filename = 'remove_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_list = pickle.load(f)
        removal_total = removal_total + chunk_list

for title in removal_total:
    try:
        title_matches.pop(title)
    except:
        pass

with open('title_matches.pkl', 'wb') as f:
    pickle.dump(title_matches, f)
