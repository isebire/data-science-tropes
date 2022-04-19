# basic stats for later

import pickle
import pandas

tv_df = pandas.read_pickle('../* PRIMARY DATASETS/TROPES_WORKS_MAPPING/tv_tropes.pkl')
vg_df = pandas.read_pickle('../* PRIMARY DATASETS/TROPES_WORKS_MAPPING/vg_tropes.pkl')

# count the number of occurances per trope
combined = pandas.concat([tv_df, vg_df])
trope_counts = combined.groupby(by='trope').agg('count').sort_values(by='title', ascending=False)
top_tropes = trope_counts.head(n=200)

with open('../* PRIMARY DATASETS/TROPES_DATA/trope_description_laconic_dict.pkl', 'rb') as f:
    trope_short_description = pickle.load(f)

print('Top 200 tropes')

top_tropes_dict = top_tropes.to_dict()['title'].items()
for k, v in top_tropes_dict:
    print(k)
    if k in trope_short_description.keys():
        print(trope_short_description[k])
    print(v)
    print('\n')
