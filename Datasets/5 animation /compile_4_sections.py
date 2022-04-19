# compile

import pickle
import pandas

# Compile the 4 dataframes

df_anime = pandas.read_pickle('tv_tropes_anime_cleaned.pkl')
df_aa = pandas.read_pickle('tv_tropes_asiananimation_cleaned.pkl')
df_eea = pandas.read_pickle('tv_tropes_easterneur_cleaned2.pkl')
df_wa = pandas.read_pickle('tv_tropes_westernani_cleaned.pkl')

# etc to determine conflicts
'''
anime_titles = list(dict.fromkeys(df_anime['title']))
input(set(anime_titles).isdisjoint(set(wa_titles))) # not disjoint
print(set(anime_titles).intersection(set(wa_titles))) # not disjoint
'''

frames = [df_anime, df_aa, df_eea, df_wa]
df_animation = pandas.concat(frames)
df_animation = df_animation.drop_duplicates()
print(df_animation.head())
print(len(list(dict.fromkeys(df_animation['title']))))
df_animation.to_pickle('tv_tropes_animation.pkl')

# Compile the 4 imdb data

with open('imdb_data_dict_anime_cleaned.pkl', 'rb') as f:
    imdb_data_dict_anime = pickle.load(f)

with open('imdb_data_dict_compiled_aa.pkl', 'rb') as f:
    imdb_data_dict_asianani = pickle.load(f)

with open('imdb_data_dict_compiled_eea.pkl', 'rb') as f:
    imdb_data_dict_eea = pickle.load(f)

with open('imdb_data_dict_westernani_cleaned.pkl', 'rb') as f:
    imdb_data_dict_westernani = pickle.load(f)

imdb_data_dict = {}
imdb_data_dict.update(imdb_data_dict_anime)
imdb_data_dict.update(imdb_data_dict_asianani)
imdb_data_dict.update(imdb_data_dict_eea)
imdb_data_dict.update(imdb_data_dict_westernani)

with open('imdb_data_dict_ANIMATION.pkl', 'wb') as f:
    pickle.dump(imdb_data_dict, f)

# Compile the 4 title matches

with open('title_matches_anime_cleaned.pkl', 'rb') as f:
    title_matches_anime = pickle.load(f)

with open('title_matches_compiled_aa.pkl', 'rb') as f:
    title_matches_aa = pickle.load(f)

with open('title_matches_compiled_eea.pkl', 'rb') as f:
    title_matches_eea = pickle.load(f)

with open('title_matches_westernani_cleaned.pkl', 'rb') as f:
    title_matches_wa = pickle.load(f)

title_matches = {}
title_matches.update(title_matches_anime)
title_matches.update(title_matches_aa)
title_matches.update(title_matches_eea)
title_matches.update(title_matches_wa)

with open('title_matches_ANIMATION.pkl', 'wb') as f:
    pickle.dump(title_matches, f)

# Replace the related ones to match the names in TVTropes dataset rather
# than native imdb

replacements = dict((v, k) for k, v in title_matches.items())

for title, data in imdb_data_dict.items():
    if 'similar_titles' in data.keys():
        new_related = []
        for related_title in data['similar_titles']:
            if related_title.lower() in replacements.keys():
                new_related.append(replacements[related_title.lower()].lower())
        data['similar_titles'] = new_related

# Save this dict
with open('imdb_data_dict_ANIMATION_related_matched.pkl', 'wb') as f:
    pickle.dump(imdb_data_dict, f)


# Make into dataframes
df_misc_data = []
df_genre_data = []
df_country_data = []
df_related_data = []

for title, data in imdb_data_dict.items():

    misc_data_current = {'title': title, 'imdb_title': data['imdb_title']}

    if 'number_episodes' in data.keys():
        misc_data_current['number_episodes'] = data['number_episodes']

    if 'start_year' in data.keys():
        misc_data_current['start_year'] = data['start_year']

    if 'end_year' in data.keys():
        misc_data_current['end_year'] = data['end_year']

    if 'rating' in data.keys():
        misc_data_current['rating'] = data['rating']

    if 'rating_count' in data.keys():
        misc_data_current['rating_count'] = data['rating_count']

    df_misc_data.append(misc_data_current)

    if 'genres' in data.keys():
        for genre in data['genres']:
            df_genre_data.append({'title': title, 'genre': genre})

    if 'countries' in data.keys():
        for country in data['countries']:
            df_country_data.append({'title': title, 'country': country})

    if 'similar_titles' in data.keys():
        for related_title in data['similar_titles']:
            df_related_data.append({'title': title,
                                    'similar_title': related_title})

# Save the dataframes

tv_misc_df = pandas.DataFrame(df_misc_data)
# There was an issue of repeated casing
tv_misc_df['title'] = tv_misc_df['title'].str.lower()
tv_misc_df = tv_misc_df.drop_duplicates()
print(tv_misc_df.head())
tv_misc_df.to_pickle('tv_misc_df.pkl')
number_titles_covered = len(list(dict.fromkeys(tv_misc_df['title'])))
print('Have data for ' + str(number_titles_covered))

tv_countries_df = pandas.DataFrame(df_country_data)
tv_countries_df['title'] = tv_countries_df['title'].str.lower()
tv_countries_df = tv_countries_df.drop_duplicates()
print(tv_countries_df.head())
tv_countries_df.to_pickle('tv_countries_df.pkl')
number_titles_covered = len(list(dict.fromkeys(tv_countries_df['title'])))
print('Have data for ' + str(number_titles_covered))

tv_genres_df = pandas.DataFrame(df_genre_data)
tv_genres_df['title'] = tv_genres_df['title'].str.lower()
tv_genres_df = tv_genres_df.drop_duplicates()
print(tv_genres_df.head())
tv_genres_df.to_pickle('tv_genres_df.pkl')
number_titles_covered = len(list(dict.fromkeys(tv_genres_df['title'])))
print('Have data for ' + str(number_titles_covered))

tv_similar_df = pandas.DataFrame(df_related_data)
tv_similar_df['title'] = tv_similar_df['title'].str.lower()
tv_similar_df = tv_similar_df.drop_duplicates()
print(tv_similar_df.head())
tv_similar_df.to_pickle('tv_similar_df.pkl')
number_titles_covered = len(list(dict.fromkeys(tv_similar_df['title'])))
print('Have data for ' + str(number_titles_covered))
