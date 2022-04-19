# Genres per year

import pickle
import pandas
import numpy as np
import matplotlib.pyplot as plt

VG_MISC = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_misc.pkl'
TV_MISC = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_misc.pkl'

VG_FILEPATH = '../data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/vg_tropes.pkl'
TV_FILEPATH = '../data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/tv_tropes.pkl'

# Load the tropes-works dataframe
tv_df = pandas.read_pickle(TV_FILEPATH)
vg_df = pandas.read_pickle(VG_FILEPATH)

# Load the years dataframe and format correctly (into years)
vg_times = pandas.read_pickle(VG_MISC).drop(['metacritic', 'number_ratings'], axis=1)
vg_times['release_date'] = pandas.DatetimeIndex(vg_times['release_date']).year
vg_times = vg_times.rename(columns={'release_date': 'start_year'})
vg_times = vg_times.dropna()
tv_times = pandas.read_pickle(TV_MISC).drop(['imdb_title', 'number_episodes', 'end_year', 'rating', 'rating_count'], axis=1)
tv_times = tv_times.dropna()

# VIDEOGAMES

# Make a dict of with years as key, and list of games as value
print('Getting data for games per year...')
df2 = vg_times.groupby('start_year').apply(lambda x: list(x['title'].unique()))
games_per_year = df2.to_dict()

# For each title in this list of titles, get its tropes
list_for_df = []

for year in games_per_year.keys():
    current_year_games = games_per_year[year]

    this_year_data = {'year': year, 'total_number_works': len(current_year_games)}

    unique_tropes = set()
    total_tropes = 0
    raw_tropes_per_work_count_year = []

    for game_title in current_year_games:
        tropes = vg_df.loc[vg_df['title'] == game_title]['trope'].tolist()

        for trope in tropes:
            total_tropes += 1
            unique_tropes.add(trope)

        raw_tropes_per_work_count_year.append(len(tropes))

    this_year_data['unique_tropes_used'] = len(unique_tropes)
    this_year_data['tropes_used'] = total_tropes
    this_year_data['standard_deviation'] = np.std(raw_tropes_per_work_count_year)

    list_for_df.append(this_year_data)

year_trope_counts_vg = pandas.DataFrame(list_for_df)


# Plot unique tropes used, tropes used, and average tropes per work (tropes_used/total_number_games)
# plot total number of works

print('Plotting...')

year_trope_counts_vg['mean_tropes_per_work'] = year_trope_counts_vg['tropes_used'] / year_trope_counts_vg['total_number_works']

print(year_trope_counts_vg.head())


# TV SHOWS

# Make a dict of with years as key, and list of games as value
print('Getting data for tropes per year...')
df2 = tv_times.groupby('start_year').apply(lambda x: list(x['title'].unique()))
tv_per_year = df2.to_dict()

# For each title in this list of titles, get its tropes
list_for_df = []

for year in tv_per_year.keys():
    current_year_tv = tv_per_year[year]

    this_year_data = {'year': year, 'total_number_works': len(current_year_tv)}

    unique_tropes = set()
    total_tropes = 0
    raw_tropes_per_work_count_year = []

    for tv_title in current_year_tv:
        tropes = tv_df.loc[tv_df['title'] == tv_title]['trope'].tolist()

        for trope in tropes:
            total_tropes += 1
            unique_tropes.add(trope)

        raw_tropes_per_work_count_year.append(len(tropes))

    this_year_data['unique_tropes_used'] = len(unique_tropes)
    this_year_data['tropes_used'] = total_tropes
    this_year_data['standard_deviation'] = np.std(raw_tropes_per_work_count_year)

    list_for_df.append(this_year_data)

year_trope_counts_tv = pandas.DataFrame(list_for_df)


# Plot unique tropes used, tropes used, and average tropes per work (tropes_used/total_number_games)
# plot total number of works

print('Plotting..')

year_trope_counts_tv['mean_tropes_per_work'] = year_trope_counts_tv['tropes_used'] / year_trope_counts_tv['total_number_works']

print(year_trope_counts_tv.head())

plt.figure(figsize=(8,8))
plt.plot(year_trope_counts_tv['year'], year_trope_counts_tv['total_number_works'], label='TV Shows')
plt.plot(year_trope_counts_vg['year'], year_trope_counts_vg['total_number_works'], label='Video Games')
plt.title('Number of TV Shows and Video Games per Year')
plt.xlabel('Year')
plt.ylabel('Number of Works')
plt.legend()
plt.savefig('tv_vg_year.png')

plt.figure(figsize=(8,8))
plt.plot(year_trope_counts_tv['year'], year_trope_counts_tv['tropes_used'], label='TV Shows')
plt.plot(year_trope_counts_vg['year'], year_trope_counts_vg['tropes_used'], label='Video Games')
plt.title('Number of Trope Usages per Year')
plt.xlabel('Year')
plt.ylabel('Number of Tropes')
plt.legend()
plt.savefig('tv_vg_year_tropes.png')
