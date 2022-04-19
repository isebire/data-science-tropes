from imdbpie import Imdb
import pickle
import pandas

df = pandas.read_pickle('tv_tropes_easterneur_cleaned1.pkl')

remove_names = ['AdventuresOfMowgli', 'CaptainPronin']

df = df[~df['title'].isin(remove_names)]

print(list(dict.fromkeys(df['title'])))

df.to_pickle('tv_tropes_easterneur_cleaned2.pkl')

with open('imdb_data_dict_easterneur.pkl', 'rb') as f:
    imdb_data_dict = pickle.load(f)

remove_imdb_old = ['AdventuresOfMowgli', 'CaptainPronin', 'HungarianFolkTales', 'MezgaCsalad', 'NuPogodi', 'ThirtyEightParrots']

for k in remove_imdb_old:
    imdb_data_dict.pop(k, None)

with open('imdb_data_dict_manual.pkl', 'rb') as f:
    imdb_data_dict_manual = pickle.load(f)
    imdb_data_dict.update(imdb_data_dict_manual)

print(imdb_data_dict.keys())

with open('imdb_data_dict_compiled.pkl', 'wb') as f:
    pickle.dump(imdb_data_dict, f)

with open('title_matches_easterneur.pkl', 'rb') as f:
    title_matches = pickle.load(f)

for k in remove_imdb_old:
    title_matches.pop(k, None)

with open('title_matches_manual.pkl', 'rb') as f:
    title_matches_manual = pickle.load(f)
    title_matches.update(title_matches_manual)

with open('title_matches_compiled.pkl', 'wb') as f:
    pickle.dump(title_matches, f)
