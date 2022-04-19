# rawg investigation

import pickle

with open('games_names.pkl', 'rb') as f:
    games_names = pickle.load(f)

with open('rawg_data_dict.pkl', 'rb') as f:
    rawg_data = pickle.load(f)

with open('rawg_data_dict_manual_ones.pkl', 'rb') as f:
    rawg_data_2 = pickle.load(f)

rawg_data.update(rawg_data_2)

with open('rawg_data_dict_combined.pkl', 'wb') as f:
    pickle.dump(rawg_data, f)

not_included = [game for game in games_names if game not in rawg_data.keys()]
included = [game for game in games_names if game in rawg_data.keys()]

print(len(not_included))
print(len(included))
print(len(games_names))
print(not_included)

"""
with open('not_included.txt', 'w') as f:
    for game in not_included:
        f.write(game + '\n')

print('done')
"""
