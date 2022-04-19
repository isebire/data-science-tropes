import pickle

with open('rawg_data_dict_combined.pkl', 'rb') as f:
    rawg_data = pickle.load(f)

developers = set()

for game in rawg_data.values():
    for developer in game['developers']:
        developers.add(developer)

developers = list(developers)

with open('developers.txt', 'w') as f:
    for developer in developers:
        f.write(developer + '\n')
