tv_countries = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_countries.pkl'
TV_GENRES = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_genres.pkl'

vg_countries = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_countries.pkl'
VG_GENRES = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_genres.pkl'

import pickle
import pandas
import matplotlib.pyplot as plt
import numpy as np

# Load data
tv_genres_df = pandas.read_pickle(TV_GENRES)
tv_with_genre = tv_genres_df['title'].unique().tolist()
tv_genres_names = tv_genres_df['genre'].unique().tolist()

tv_countries_df = pandas.read_pickle(tv_countries)
tv_with_country = tv_countries_df['title'].unique().tolist()

df2 = tv_countries_df.groupby('country').apply(lambda x: list(x['title'].unique()))
tv_per_country_t = df2.to_dict()

tv_countries_list = ['US', 'JP', 'GB', "CA", 'FR', 'KR', 'AU', 'DE', 'CN', 'ES']
tv_per_country = {}
for k, v in tv_per_country_t.items():
    if k in tv_countries_list:
        tv_per_country[k] = v

heatmap_data = [[] for i in range(len(tv_genres_names))]

for country in tv_per_country.keys():
    shows = tv_per_country[country]
    country_genre_titles = [x for x in shows if x in tv_with_genre]

    genre_counts = {}

    for title in country_genre_titles:
        genres = tv_genres_df.loc[tv_genres_df['title'] == title]['genre'].tolist()

        for genre in genres:
            if genre in genre_counts.keys():
                genre_counts[genre] += 1
            else:
                genre_counts[genre] = 1

    genre_percentages = {}
    for genre, count in genre_counts.items():
        genre_percentage = (count/len(country_genre_titles)) * 100
        genre_percentages[genre] = genre_percentage

    for genre_number, genre in enumerate(tv_genres_names):
        if genre in genre_percentages.keys():
            heatmap_data[genre_number].append(genre_percentages[genre])
        else:
            heatmap_data[genre_number].append(0)

# Make heatmap

plt.figure(figsize=(20,20))
cmap = plt.cm.get_cmap('magma').copy()
plt.imshow(heatmap_data, origin='lower', aspect='auto',
           interpolation='none', cmap=cmap)
           # ,norm=colours.LogNorm())
plt.ylim(-0.5, len(tv_genres_names) - 0.5)
plt.title('Predefined Genres by Country', fontsize=25)
plt.xlabel('Country', fontsize=20)
plt.ylabel('Predefined Genres', fontsize=20)
plt.clim(0)
plt.colorbar()
plt.xticks(np.arange(len(tv_countries_list)), labels=[x for x in tv_countries_list])
plt.yticks(np.arange(len(tv_genres_names)), labels=[x for x in tv_genres_names])
filename = 'countries_genres_tv_plain.png'
plt.savefig(filename)


#################
#  Load data

vg_genres_df = pandas.read_pickle(VG_GENRES)
vg_with_genre = vg_genres_df['title'].unique().tolist()
vg_genres_names = vg_genres_df['genre'].unique().tolist()

vg_countries_df = pandas.read_pickle(vg_countries)
vg_with_country = vg_countries_df['title'].unique().tolist()

df2 = vg_countries_df.groupby('country').apply(lambda x: list(x['title'].unique()))
games_per_country_t = df2.to_dict()

vg_countries_list = ['US', 'JP', 'GB', "CA", 'FR', 'DE', 'CN', 'SE', 'SG']
games_per_country = {}
for k, v in games_per_country_t.items():
    if k in vg_countries_list:
        games_per_country[k] = v

heatmap_data = [[] for i in range(len(vg_genres_names))]

for country in games_per_country.keys():
    games = games_per_country[country]
    country_genre_titles = [x for x in games if x in vg_with_genre]

    genre_counts = {}

    if country == 'CN':
        print(games)

    for title in country_genre_titles:
        genres = vg_genres_df.loc[vg_genres_df['title'] == title]['genre'].tolist()

        for genre in genres:
            if genre in genre_counts.keys():
                genre_counts[genre] += 1
            else:
                genre_counts[genre] = 1

    genre_percentages = {}
    for genre, count in genre_counts.items():
        genre_percentage = (count/len(country_genre_titles)) * 100
        genre_percentages[genre] = genre_percentage

    for genre_number, genre in enumerate(vg_genres_names):
        if genre in genre_percentages.keys():
            heatmap_data[genre_number].append(genre_percentages[genre])
        else:
            heatmap_data[genre_number].append(0)

# Make heatmap

plt.figure(figsize=(20,20))
cmap = plt.cm.get_cmap('magma').copy()
plt.imshow(heatmap_data, origin='lower', aspect='auto',
           interpolation='none', cmap=cmap)
           # ,norm=colours.LogNorm())
plt.ylim(-0.5, len(vg_genres_names) - 0.5)
plt.title('Predefined Genres by Country', fontsize=25)
plt.xlabel('Countries', fontsize=20)
plt.ylabel('Predefined Genres', fontsize=20)
plt.clim(0)
plt.colorbar()
plt.xticks(np.arange(len(vg_countries_list)), labels=[x for x in vg_countries_list])
plt.yticks(np.arange(len(vg_genres_names)), labels=[x for x in vg_genres_names])
filename = 'countries_genres_vg_plain.png'
plt.savefig(filename)
