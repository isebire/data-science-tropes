import pickle
import pandas
import json

with open('rawg_data_dict_combined_MISALIGNED.pkl', 'rb') as f:
    games_data_old = pickle.load(f)

new_dict = {}
flag1 = False

for i in range(len(list(games_data_old.keys()))):
    if list(games_data_old.keys())[i] == 'castlevania-rondo-of-blood':
        flag1 = True
    if list(games_data_old.keys())[i] == 'tale-spin-capcom':
        new_dict['tale-spin-sega'] = list(games_data_old.values())[i]
        flag1 = False
        continue
    if not flag1:
        new_dict[list(games_data_old.keys())[i]] = list(games_data_old.values())[i]
    else:
        new_dict[list(games_data_old.keys())[i+1]] = list(games_data_old.values())[i]


with open('rawg_data_dict_combined_maybealign.pkl', 'wb') as f:
    pickle.dump(new_dict, f)
