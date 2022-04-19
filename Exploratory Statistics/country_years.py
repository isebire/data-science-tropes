# countries per year

import pickle
import pandas
import matplotlib.pyplot as plt

VG_MISC = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_misc.pkl'
TV_MISC = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_misc.pkl'
VG_COUNTRIES = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_countries.pkl'
TV_COUNTRIES = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_countries.pkl'

# Load the countries dataframe
tv_countries_df = pandas.read_pickle(TV_COUNTRIES)
vg_countries_df = pandas.read_pickle(VG_COUNTRIES)

# Load the years dataframe and format correctly (into years)
vg_times = pandas.read_pickle(VG_MISC).drop(['metacritic', 'number_ratings'], axis=1)
vg_times['release_date'] = pandas.DatetimeIndex(vg_times['release_date']).year
vg_times = vg_times.rename(columns={'release_date': 'start_year'})
vg_times = vg_times.dropna()
tv_times = pandas.read_pickle(TV_MISC).drop(['imdb_title', 'number_episodes', 'end_year', 'rating', 'rating_count'], axis=1)
tv_times = tv_times.dropna()

# VIDEOGAMES

# Make a dict of with years as key, and list of games as value
df2 = vg_times.groupby('start_year').apply(lambda x: list(x['title'].unique()))
games_per_year = df2.to_dict()

# For each title in this list of titles, append to a dictionary counts for each
# country
list_for_df = []
vg_countries_list = ['US', 'JP', 'GB', "CA", 'FR', 'DE', 'CN', 'SE', 'SG']

for year in games_per_year.keys():
    current_year_games = games_per_year[year]
    current_year_games_w_country = list(set(current_year_games).intersection(set(vg_countries_df['title'].unique().tolist())))
    number_games_year_with_country = len(current_year_games_w_country)

    this_year_data = {'year': year, 'total_games_w_country': number_games_year_with_country}
    for country in vg_countries_list:
        this_year_data[country] = 0

    for game_title in current_year_games_w_country:
        countries = vg_countries_df.loc[vg_countries_df['title'] == game_title]['country'].tolist()

        for country in countries:
            if country in vg_countries_list:
                this_year_data[country] += 1

    list_for_df.append(this_year_data)

year_country_counts_df = pandas.DataFrame(list_for_df)
print(year_country_counts_df.head())
# move legend, add title and axis labels, remove total games with country
# flip axis so counts on y axis and year on x
fig = year_country_counts_df.drop(['total_games_w_country'], axis=1).plot(x='year', ylabel='Number of Games', xlabel='Year', title='Number of games with RAWG.io countries per year', figsize=(8, 8)).get_figure()
fig.savefig('country_counts_year_vg.png')

# From this can make % per year of each country
year_country_percentage_df = year_country_counts_df
year_country_percentage_df[vg_countries_list] = year_country_counts_df[vg_countries_list].div(year_country_counts_df.total_games_w_country, axis=0)
print(year_country_percentage_df.head())
ax = year_country_percentage_df.drop(['total_games_w_country'], axis=1).plot(x='year', ylabel='Percentage of Games', xlabel='Year', title='Percentage of games with RAWG.io countries per year', figsize=(8, 8))
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) #here is the magic
ax.plot()
ax.figure.savefig('country_percentage_year_vg.png')

# with log scale
ax = year_country_percentage_df.drop(['total_games_w_country'], axis=1).plot(x='year', ylabel='Percentage of Games', xlabel='Year', title='Percentage of games with RAWG.io countries per year', figsize=(8, 8), logy=True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) #here is the magic
ax.plot()
ax.figure.savefig('country_percentage_year_log_vg.png')




# TV SHOWS

# Make a dict of with years as key, and list of games as value
df2 = tv_times.groupby('start_year').apply(lambda x: list(x['title'].unique()))
tv_per_year = df2.to_dict()

# For each title in this list of titles, append to a dictionary counts for each
# country
list_for_df = []
tv_countries_list = ['US', 'JP', 'GB', "CA", 'FR', 'KR', 'AU', 'DE', 'CN', 'ES']

for year in tv_per_year.keys():
    current_year_tv = tv_per_year[year]
    current_year_tv_w_country = list(set(current_year_tv).intersection(set(tv_countries_df['title'].unique().tolist())))
    number_tv_year_with_country = len(current_year_tv_w_country)

    this_year_data = {'year': year, 'total_tv_w_country': number_tv_year_with_country}
    for country in tv_countries_list:
        this_year_data[country] = 0

    for tv_title in current_year_tv_w_country:
        countries = tv_countries_df.loc[tv_countries_df['title'] == tv_title]['country'].tolist()

        for country in countries:
            if country in tv_countries_list:
                this_year_data[country] += 1

    list_for_df.append(this_year_data)

year_country_counts_df = pandas.DataFrame(list_for_df)
print(year_country_counts_df.head())
fig = year_country_counts_df.drop(['total_tv_w_country'], axis=1).plot(x='year', ylabel='Number of TV Shows', xlabel='Year', title='Number of TV shows with IMDB countries per year', figsize=(8, 8)).get_figure()
fig.savefig('country_counts_year_tv.png')

# From this can make % per year of each country
year_country_percentage_df = year_country_counts_df
year_country_percentage_df[tv_countries_list] = year_country_counts_df[tv_countries_list].div(year_country_counts_df.total_tv_w_country, axis=0)
print(year_country_percentage_df.head())
ax = year_country_percentage_df.drop(['total_tv_w_country'], axis=1).plot(x='year', ylabel='Percentage of TV Shows', xlabel='Year', title='Percentage of TV shows with IMDB countries per year', figsize=(8, 8))
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) #here is the magic
ax.plot()
ax.figure.savefig('country_percentage_year_tv.png')

# with log scale
ax = year_country_percentage_df.drop(['total_tv_w_country'], axis=1).plot(x='year', ylabel='Percentage of TV Shows', xlabel='Year', title='Percentage of TV shows with IMDB countries per year', figsize=(8, 8), logy=True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) #here is the magic
ax.plot()
ax.figure.savefig('country_percentage_year_log_tv.png')
