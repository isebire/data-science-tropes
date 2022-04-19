# Supplementary data basic stats

import pickle
import pandas
import matplotlib.pyplot as plt
import numpy as np
import pygal

pandas.set_option('display.max_rows', 100)


def countries_stats(countries_df, media):
    # Number and proportion for each country
    number_of_shows = countries_df['title'].nunique()

    countries = countries_df.groupby('country').count().sort_values(by='title', ascending=False)
    country_data = countries.to_dict()['title'].items()

    print('COUNTRIES ' + media)

    for k, v in country_data:
        print(k + ': total number of works ' + str(v))
        percentage = (v / number_of_shows) * 100
        print('Percentage in dataset: ' + str(percentage))

    worldmap = pygal.maps.world.World()
    worldmap.title = media + ' per country (logarithmic scale)'
    map_data = dict((k.lower(), np.log(v)) for k, v in country_data)  # changed for log?
    worldmap.add('Data', map_data)
    filename = media + '_countries.svg'
    worldmap.render_to_file(filename)

    # Number and proportion having more than 1 country

    country_collab = countries_df.groupby(['title']).size().reset_index(name='counts')
    country_collab_multiple = country_collab.loc[country_collab['counts'] > 1]
    print('Number of works involving multiple countries: ' + str(country_collab_multiple.shape[0]))
    country_collab = country_collab.groupby(['counts']).size().reset_index(name='num_works')
    print('Distribution of number of genres')
    print(country_collab)
    ax = country_collab.plot.bar(x='counts', y='num_works', rot=0, legend=False)
    fig = ax.get_figure()
    if media == 'TV':
        title = 'Number of Countries per TV Show'
    else:
        title = 'Number of Countries per Video Game'
    plt.title(title)
    plt.xlabel('Number of Countries')
    plt.ylabel('Frequency')
    filename = 'countries_per_' + media + '.png'
    fig.savefig(filename)


def genre_stats(genres_df, media):
    number_of_shows = genres_df['title'].nunique()
    genres = genres_df.groupby(['genre']).count().sort_values(by='title', ascending=False)
    genre_data = genres.to_dict()['title'].items()

    print('GENRES ' + media)

    for k, v in genre_data:
        print(k + ': total number of works ' + str(v))
        percentage = (v / number_of_shows) * 100
        print('Percentage in dataset: ' + str(percentage))

    # Mean genres per work
    mean_genres_per_tv_show = genres_df.shape[0] / number_of_shows
    print('Mean number of genres per tv show: ' + str(mean_genres_per_tv_show))

    # Distibution of genres
    genres_dist = genres_df.groupby(['title']).size().reset_index(name='counts').groupby(['counts']).size().reset_index(name='num_works')
    print(genres_dist.head(n=100))
    ax = genres_dist.plot.bar(x='counts', y='num_works', rot=0, legend=False)
    fig = ax.get_figure()
    if media == 'TV':
        title = 'Number of Genres per TV Show'
    else:
        title = 'Number of Genres per Video Game'
    plt.title(title)
    plt.xlabel('Number of Genres')
    plt.ylabel('Frequency')
    filename = 'genres_per_' + media + '.png'
    fig.savefig(filename)

    # Titles with the most genres
    genre_titles = genres_df.groupby(['title']).count().sort_values(by='genre', ascending=False).head(n=5).reset_index()
    many_genre_works = genre_titles['title'].tolist()
    many_genre_works_df = genres_df[genres_df.title.isin(many_genre_works)]
    print('Genres for the 5 works with the most genres')
    print(many_genre_works_df)

def year_stats(year_df, media):
    print('YEARS ' + media)
    years = year_df.groupby(['start_year']).size().reset_index(name='counts')
    print(years)
    ax = years.plot.line(x='start_year', y='counts', legend=False)
    fig = ax.get_figure()
    if media == 'TV':
        title = 'Number of TV Shows per Year'
    else:
        title = 'Number of Video Games per Year'
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Number of Works')
    filename = media + '_per_year.png'
    fig.savefig(filename)


# main

# TV
tv_countries_df = pandas.read_pickle('../* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_countries.pkl')
countries_stats(tv_countries_df, 'TV')

tv_genres_df = pandas.read_pickle('../* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_genres.pkl')
genre_stats(tv_genres_df, 'TV')

tv_misc_df = pandas.read_pickle('../* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_misc.pkl')
tv_misc_df = tv_misc_df.drop(['imdb_title', 'number_episodes', 'end_year', 'rating', 'rating_count'], axis=1)
year_stats(tv_misc_df, 'TV')

# VG
vg_countries_df = pandas.read_pickle('../* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_countries.pkl')
vg_countries_df = vg_countries_df.drop(['developer'], axis=1)
vg_countries_df = vg_countries_df.drop_duplicates()
countries_stats(vg_countries_df, 'VG')

vg_genres_df = pandas.read_pickle('../* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_genres.pkl')
genre_stats(vg_genres_df, 'VG')

vg_misc_df = pandas.read_pickle('../* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_misc.pkl')
vg_misc_df = vg_misc_df.drop(['metacritic', 'number_ratings'], axis=1)
vg_misc_df['release_date'] = pandas.DatetimeIndex(vg_misc_df['release_date']).year
vg_misc_df = vg_misc_df.rename(columns={'release_date': 'start_year'})
year_stats(vg_misc_df, 'VG')
