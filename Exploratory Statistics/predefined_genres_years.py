# Genres per year

import pickle
import pandas
import matplotlib.pyplot as plt

VG_MISC = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_misc.pkl'
TV_MISC = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_misc.pkl'
VG_GENRES = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_genres.pkl'
TV_GENRES = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_genres.pkl'

# Load the genres dataframe
tv_genres_df = pandas.read_pickle(TV_GENRES)
vg_genres_df = pandas.read_pickle(VG_GENRES)

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
# genre
list_for_df = []
vg_genres_list = vg_genres_df['genre'].unique().tolist()

for year in games_per_year.keys():
    current_year_games = games_per_year[year]
    current_year_games_w_genre = list(set(current_year_games).intersection(set(vg_genres_df['title'].unique().tolist())))
    number_games_year_with_genre = len(current_year_games_w_genre)

    this_year_data = {'year': year, 'total_games_w_genre': number_games_year_with_genre}
    for genre in vg_genres_list:
        this_year_data[genre] = 0

    for game_title in current_year_games_w_genre:
        genres = vg_genres_df.loc[vg_genres_df['title'] == game_title]['genre'].tolist()

        for genre in genres:
            this_year_data[genre] += 1

    list_for_df.append(this_year_data)

year_genre_counts_df = pandas.DataFrame(list_for_df)
print(year_genre_counts_df.head())
# move legend, add title and axis labels, remove total games with genre
# flip axis so counts on y axis and year on x
fig = year_genre_counts_df.drop(['total_games_w_genre'], axis=1).plot(x='year', ylabel='Number of Games', xlabel='Year', title='Number of games with RAWG.io genres per year', figsize=(8, 8)).get_figure()
fig.savefig('genre_counts_year_vg.png')

# From this can make % per year of each genre
year_genre_percentage_df = year_genre_counts_df
year_genre_percentage_df[vg_genres_list] = year_genre_counts_df[vg_genres_list].div(year_genre_counts_df.total_games_w_genre, axis=0)
print(year_genre_percentage_df.head())
ax = year_genre_percentage_df.drop(['total_games_w_genre'], axis=1).plot(x='year', ylabel='Percentage of Games', xlabel='Year', title='Percentage of games with RAWG.io genres per year', figsize=(8, 8))
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) #here is the magic
ax.plot()
ax.figure.savefig('genre_percentage_year_vg.png')

# with log scale
ax = year_genre_percentage_df.drop(['total_games_w_genre'], axis=1).plot(x='year', ylabel='Percentage of Games', xlabel='Year', title='Percentage of games with RAWG.io genres per year', figsize=(8, 8), logy=True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) #here is the magic
ax.plot()
ax.figure.savefig('genre_percentage_year_log_vg.png')

# tv: since 1980. vg: since 1990. highlight ones going up or down recently

year_genre_percentage_df = year_genre_percentage_df.drop(year_genre_percentage_df[year_genre_percentage_df.year < 1990].index)
up_overall = []
down_overall = []
same_overall = []
for genre in year_genre_percentage_df.columns[2:-2]:
    print(genre)
    genre_data = year_genre_percentage_df[genre].tolist()
    if genre_data[0] < genre_data[-1]:
        # increasing overall
        up_overall.append(genre)
    elif genre_data[0] > genre_data[-1]:
        # decreasing overall
        down_overall.append(genre)
    else:
        # same
        same_overall.append(genre)

# highlight the ones going down overall
plt.figure(figsize=(8,8))
for genre in up_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
for genre in down_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], label=genre)
for genre in same_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
plt.title('Percentage of games with RAWG.io genres per year')
plt.xlabel('Year')
plt.ylabel('Percentage of Games')
plt.legend()
plt.savefig('genre_percentage_year_down_vg.png')

# highlight the ones going up overall
plt.figure(figsize=(8,8))
for genre in up_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], label=genre)
for genre in down_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
for genre in same_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
plt.title('Percentage of games with RAWG.io genres per year')
plt.xlabel('Year')
plt.ylabel('Percentage of Games')
plt.legend()
plt.savefig('genre_percentage_year_up_vg.png')

# ones on average going up or down
up_overall = []
down_overall = []
same_overall = []
for genre in year_genre_percentage_df.columns[2:-2]:
    genre_data = year_genre_percentage_df[genre].tolist()
    up = 0
    down = 0
    for i in range(1, len(genre_data)):
        if genre_data[i] > genre_data[i-1]:
            up += 1
        else:
            down += 1
    if down < up:
        # increasing overall
        up_overall.append(genre)
    elif down > up:
        # decreasing overall
        down_overall.append(genre)
    else:
        # same
        same_overall.append(genre)

# highlight the ones going down overall
plt.figure(figsize=(8,8))
for genre in up_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
for genre in down_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], label=genre)
for genre in same_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
plt.title('Percentage of games with RAWG.io genres per year')
plt.xlabel('Year')
plt.ylabel('Percentage of Games')
plt.legend()
plt.savefig('genre_percentage_year_av_down_vg.png')

# highlight the ones going up overall
plt.figure(figsize=(8,8))
for genre in up_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], label=genre)
for genre in down_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
for genre in same_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
plt.title('Percentage of games with RAWG.io genres per year')
plt.xlabel('Year')
plt.ylabel('Percentage of Games')
plt.legend()
plt.savefig('genre_percentage_year_av_up_vg.png')

# TV SHOWS

# Make a dict of with years as key, and list of games as value
df2 = tv_times.groupby('start_year').apply(lambda x: list(x['title'].unique()))
tv_per_year = df2.to_dict()

# For each title in this list of titles, append to a dictionary counts for each
# genre
list_for_df = []
tv_genres_list = tv_genres_df['genre'].unique().tolist()

for year in tv_per_year.keys():
    current_year_tv = tv_per_year[year]
    current_year_tv_w_genre = list(set(current_year_tv).intersection(set(tv_genres_df['title'].unique().tolist())))
    number_tv_year_with_genre = len(current_year_tv_w_genre)

    this_year_data = {'year': year, 'total_tv_w_genre': number_tv_year_with_genre}
    for genre in tv_genres_list:
        this_year_data[genre] = 0

    for tv_title in current_year_tv_w_genre:
        genres = tv_genres_df.loc[tv_genres_df['title'] == tv_title]['genre'].tolist()

        for genre in genres:
            this_year_data[genre] += 1

    list_for_df.append(this_year_data)

year_genre_counts_df = pandas.DataFrame(list_for_df)
print(year_genre_counts_df.head())
fig = year_genre_counts_df.drop(['total_tv_w_genre'], axis=1).plot(x='year', ylabel='Number of TV Shows', xlabel='Year', title='Number of TV shows with IMDB genres per year', figsize=(8, 8)).get_figure()
fig.savefig('genre_counts_year_tv.png')

# From this can make % per year of each genre
year_genre_percentage_df = year_genre_counts_df
year_genre_percentage_df[tv_genres_list] = year_genre_counts_df[tv_genres_list].div(year_genre_counts_df.total_tv_w_genre, axis=0)
print(year_genre_percentage_df.head())
ax = year_genre_percentage_df.drop(['total_tv_w_genre'], axis=1).plot(x='year', ylabel='Percentage of TV Shows', xlabel='Year', title='Percentage of TV shows with IMDB genres per year', figsize=(8, 8))
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) #here is the magic
ax.plot()
ax.figure.savefig('genre_percentage_year_tv.png')

# with log scale
ax = year_genre_percentage_df.drop(['total_tv_w_genre'], axis=1).plot(x='year', ylabel='Percentage of TV Shows', xlabel='Year', title='Percentage of TV shows with IMDB genres per year', figsize=(8, 8), logy=True)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])
ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5)) #here is the magic
ax.plot()
ax.figure.savefig('genre_percentage_year_log_tv.png')

# tv: since 1980. vg: since 1990. highlight ones going up or down recently

year_genre_percentage_df = year_genre_percentage_df.drop(year_genre_percentage_df[year_genre_percentage_df.year < 1980].index)
up_overall = []
down_overall = []
same_overall = []
for genre in year_genre_percentage_df.columns[2:-2]:
    print(genre)
    genre_data = year_genre_percentage_df[genre].tolist()
    if genre_data[0] < genre_data[-1]:
        # increasing overall
        up_overall.append(genre)
    elif genre_data[0] > genre_data[-1]:
        # decreasing overall
        down_overall.append(genre)
    else:
        # same
        same_overall.append(genre)

# highlight the ones going down overall
plt.figure(figsize=(8,8))
for genre in up_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
for genre in down_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], label=genre)
for genre in same_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
plt.title('Percentage of TV shows with IMDB genres per year')
plt.xlabel('Year')
plt.ylabel('Percentage of TV Shows')
plt.legend()
plt.savefig('genre_percentage_year_down_tv.png')

# highlight the ones going up overall
plt.figure(figsize=(8,8))
for genre in up_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], label=genre)
for genre in down_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
for genre in same_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
plt.title('Percentage of TV shows with IMDB genres per year')
plt.xlabel('Year')
plt.ylabel('Percentage of TV Shows')
plt.legend()
plt.savefig('genre_percentage_year_up_tv.png')

# ones on average going up or down
up_overall = []
down_overall = []
same_overall = []
for genre in year_genre_percentage_df.columns[2:-2]:
    genre_data = year_genre_percentage_df[genre].tolist()
    up = 0
    down = 0
    for i in range(1, len(genre_data)):
        if genre_data[i] > genre_data[i-1]:
            up += 1
        else:
            down += 1
    if down < up:
        # increasing overall
        up_overall.append(genre)
    elif down > up:
        # decreasing overall
        down_overall.append(genre)
    else:
        # same
        same_overall.append(genre)

# highlight the ones going down overall
plt.figure(figsize=(8,8))
for genre in up_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
for genre in down_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], label=genre)
for genre in same_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
plt.title('Percentage of TV shows with IMDB genres per year')
plt.xlabel('Year')
plt.ylabel('Percentage of TV Shows')
plt.legend()
plt.savefig('genre_percentage_year_av_down_tv.png')

# highlight the ones going up overall
plt.figure(figsize=(8,8))
for genre in up_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], label=genre)
for genre in down_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
for genre in same_overall:
    plt.plot(year_genre_percentage_df['year'], year_genre_percentage_df[genre], color='#d9d9d9', label=genre)
plt.title('Percentage of TV shows with IMDB genres per year')
plt.xlabel('Year')
plt.ylabel('Percentage of TV Shows')
plt.legend()
plt.savefig('genre_percentage_year_av_up_tv.png')
