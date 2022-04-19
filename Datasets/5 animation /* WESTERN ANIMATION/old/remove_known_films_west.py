# removes known films

import pickle
import pandas

# remove the films etc from the dataframe

with open('western_animated_film_locators.pkl', 'rb') as f:
    known_films = pickle.load(f)

df = pandas.read_pickle('tv_tropes_anime_wmanga.pkl')

print(len(list(dict.fromkeys(df['title']))))
df = df[~df['title'].isin(known_films)]

with open('remove_anime.txt', 'r') as f:
    remove_list = f.read().splitlines()

df = df[~df['title'].isin(remove_list)]

print(len(list(dict.fromkeys(df['title']))))

with open('anime_locators.pkl', 'rb') as f:
    anime_locators = pickle.load(f)

df = df[df['title'].isin(anime_locators)]

print(len(list(dict.fromkeys(df['title']))))

for item in list(dict.fromkeys(df['title'])):
    print(item)

df.to_pickle('tv_tropes_anime_wmanga_removedknownfilms.pkl')

'''
# imdb data dict
with open('imdb_data_dict_westernani.pkl', 'rb') as f:
    imdb_data_dict = pickle.load(f)

print(len(imdb_data_dict))

data_new = {}

for key, value in imdb_data_dict.items():
    if key not in known_films:
        data_new[key] = value

print(len(data_new))

with open('imdb_data_dict_westernani_removedknownfilms.pkl', 'wb') as f:
    pickle.dump(data_new, f)

# title matches
with open('title_matches_westernani.pkl', 'rb') as f:
    matches_data = pickle.load(f)

print(len(matches_data))

data_new = {}

for key, value in matches_data.items():
    if key not in known_films:
        data_new[key] = value

print(len(data_new))

with open('title_matches_westernani_removedknownfilms.pkl', 'wb') as f:
    pickle.dump(data_new, f)


# manual checks
with open('manual_checks_westernani.pkl', 'rb') as f:
    manual_data = pickle.load(f)

print(len(manual_data))

data_new = {}

for key, value in manual_data.items():
    if key not in known_films:
        data_new[key] = value

print(len(data_new))

with open('manual_checks_westernani_removedknownfilms.pkl', 'wb') as f:
    pickle.dump(data_new, f)
'''
