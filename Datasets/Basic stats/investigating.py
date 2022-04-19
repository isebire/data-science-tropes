# basic stats for later

import pickle
import pandas

tv_df = pandas.read_pickle('* PRIMARY DATASETS/TROPES_WORKS_MAPPING/tv_tropes.pkl')
vg_df = pandas.read_pickle('* PRIMARY DATASETS/TROPES_WORKS_MAPPING/vg_tropes.pkl')


# print the top 100 media with the most tropes
pandas.set_option('display.max_rows', 100)
print(tv_df.groupby(by='title').agg('count').sort_values(by='trope', ascending=False).head(n=100))

# count the number of occurances per trope
combined = pandas.concat([tv_df, vg_df])
trope_counts = combined.groupby(by='trope').agg('count').sort_values(by='title', ascending=False)

top_tropes = trope_counts.head(n=100)
bottom_tropes = trope_counts.tail(n=100)

with open('* PRIMARY DATASETS/TROPES_DATA/trope_description_laconic_dict.pkl', 'rb') as f:
    trope_short_description = pickle.load(f)

print('Top 100 tropes')

top_tropes_dict = top_tropes.to_dict()['title'].items()
for k, v in top_tropes_dict:
    print(k)
    if k in trope_short_description.keys():
        print(trope_short_description[k])
    print(v)
    print('\n')

print('Bottom 100 tropes')

bottom_tropes_dict = bottom_tropes.to_dict()['title'].items()
for k, v in bottom_tropes_dict:
    print(k)
    if k in trope_short_description.keys():
        print(trope_short_description[k])
    print(v)
    print('\n')

# Which videogames have 33 countries
vg_countries_df = pandas.read_pickle('* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_countries.pkl')
countries = vg_countries_df.drop(['developer'], axis=1).drop_duplicates().groupby('title').count().sort_values(by='country', ascending=False).head(n=13).reset_index()
print(countries)
thirtythree_games = countries['title'].tolist()
thirtythree_games_df = vg_countries_df[vg_countries_df.title.isin(thirtythree_games)]
print(list(set(thirtythree_games_df['developer'].tolist())))
big_devs = vg_countries_df.drop(['title'], axis=1).drop_duplicates().groupby('developer').count().sort_values(by='country', ascending=False).head(n=10).reset_index()
print(big_devs)

# get the tropes in a specific media
# print(tv_df.loc[tv_df['title'] == 'ThreeThousandWhysOfBlueCat'])

# get the media for a specific trope
# print(tv_trope_df.loc[tv_trope_df['trope'] == 'Conlang'])
