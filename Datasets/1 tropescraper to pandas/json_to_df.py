import pandas
import json
import pickle
import matplotlib.pyplot as plt

# VIDEOGAMES

with open('tvtropesvg.json') as json_file:
    vg_dict = json.load(json_file)  # this gives a dict
vg_df = pandas.DataFrame.from_dict(vg_dict, orient="index").sort_index().stack().reset_index(level=1, drop=True).reset_index()
vg_df.columns = ['title', 'trope']
vg_df['trope'] = vg_df['trope'].str.lower()
vg_df.to_pickle('vg_tropes.pkl')

# TV

with open('tvtropestv.json') as json_file:
    tv_dict = json.load(json_file)  # this gives a dict
tv_df = pandas.DataFrame.from_dict(tv_dict, orient="index").sort_index().stack().reset_index(level=1, drop=True).reset_index()
tv_df.columns = ['title', 'trope']
tv_df['trope'] = tv_df['trope'].str.lower()
tv_df.to_pickle('tv_tropes.pkl')

# get all the tropes
vg_tropes_set = set(vg_df['trope'])
tv_tropes_set = set(tv_df['trope'])
all_tropes = list(tv_tropes_set.union(vg_tropes_set))
print(len(all_tropes))
with open('trope_names.pkl', 'wb') as f:
    pickle.dump(all_tropes, f)
