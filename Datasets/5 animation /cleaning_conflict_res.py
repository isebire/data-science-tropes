import pickle
import pandas

#remove Astroboy from western animation

# remove the films etc from the dataframe
df = pandas.read_pickle('tv_tropes_westernani_removedknownfilms_c1.pkl')
remove_list = ['Astroboy']
df = df[~df['title'].isin(remove_list)]
df.to_pickle('tv_tropes_westernani_cleaned.pkl')

# remove non tv and ones to replace from imdb_data_dict.pkl
with open('imdb_data_dict_westernani_compiled.pkl', 'rb') as f:
    imdb_data_dict = pickle.load(f)

data_new = {}

for key, value in imdb_data_dict.items():
    if key not in remove_list:
        data_new[key] = value

with open('imdb_data_dict_westernani_cleaned.pkl', 'wb') as f:
    pickle.dump(data_new, f)

# remove non tv and ones to replace from title matches

with open('title_matches_westernani_compiled.pkl', 'rb') as f:
    title_matches = pickle.load(f)

data_new = {}

for key, value in title_matches.items():
    if key not in remove_list:
        data_new[key] = value

with open('title_matches_westernani_cleaned.pkl', 'wb') as f:
    pickle.dump(data_new, f)

#remove SylvanianFamilies from anime

# remove the films etc from the dataframe
df = pandas.read_pickle('tv_tropes_anime_wmanga_removedknownfilms_c1.pkl')
remove_list = ['SylvanianFamilies']
df = df[~df['title'].isin(remove_list)]
df.to_pickle('tv_tropes_anime_cleaned.pkl')

# remove non tv and ones to replace from imdb_data_dict.pkl
with open('imdb_data_dict_animem_compiled.pkl', 'rb') as f:
    imdb_data_dict = pickle.load(f)

data_new = {}

for key, value in imdb_data_dict.items():
    if key not in remove_list:
        data_new[key] = value

with open('imdb_data_dict_anime_cleaned.pkl', 'wb') as f:
    pickle.dump(data_new, f)

# remove non tv and ones to replace from title matches

with open('title_matches_animem_compiled.pkl', 'rb') as f:
    title_matches = pickle.load(f)

data_new = {}

for key, value in title_matches.items():
    if key not in remove_list:
        data_new[key] = value

with open('title_matches_anime_cleaned.pkl', 'wb') as f:
    pickle.dump(data_new, f)
