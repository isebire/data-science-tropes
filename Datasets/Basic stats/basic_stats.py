# basic stats for later

import pickle
import pandas
import matplotlib.pyplot as plt
import numpy as np

tv_df = pandas.read_pickle('../* PRIMARY DATASETS/TROPES_WORKS_MAPPING/tv_tropes.pkl')
vg_df = pandas.read_pickle('../* PRIMARY DATASETS/TROPES_WORKS_MAPPING/vg_tropes.pkl')

# number of works
number_tv = tv_df['title'].nunique()
number_games = vg_df['title'].nunique()
print('TV total works: ' + str(number_tv))
print('Games total works: ' + str(number_games))

# number of unique tropes
number_tropes_tv = tv_df['trope'].nunique()
number_tropes_games = vg_df['trope'].nunique()
print('TV total number of tropes: ' + str(number_tropes_tv))
print('Games total number of tropes: ' + str(number_tropes_games))

# number of tropes per media -> graph
idk_what = tv_df.groupby('title').count()
# print(idk_what.head())
fig, ax = plt.subplots()
idk_what.hist('trope', ax=ax)
ax.set_yscale('log')
plt.title('Number of Tropes per TV Show')
plt.xlabel('Number of Tropes')
plt.ylabel('Frequency')
fig.savefig('tropes_per_media_tv_log.png')

idk_2 = vg_df.groupby('title').count()
# print(idk_what.head())
fig, ax = plt.subplots()
idk_2.hist('trope', ax=ax)
ax.set_yscale('log')
plt.title('Number of Tropes per Video Game')
plt.xlabel('Number of Tropes')
plt.ylabel('Frequency')
fig.savefig('tropes_per_media_games_log.png')

# avg number of tropes per media: sum of trope occurances / number of media
mean_tropes_per_tv_show = tv_df.shape[0] / number_tv
mean_tropes_per_game = vg_df.shape[0] / number_games
print('Mean number of tropes per tv show: ' + str(mean_tropes_per_tv_show))
print('Mean number of tropes per game: ' + str(mean_tropes_per_game))

# Counting the frequency of each trope -> graph
total_counts = pandas.DataFrame(tv_df['trope'].value_counts()).reset_index()
total_counts.columns = ['trope', 'counts']
# print(total_counts.head())
fig, ax = plt.subplots()
total_counts.hist('counts', ax=ax)
ax.set_yscale('log')
plt.title('Number of Occurances per Trope (TV Shows)')
plt.xlabel('Number of Occurances')
plt.ylabel('Frequency')
fig.savefig('occurances_per_trope_tv_log.png')

total_counts2 = pandas.DataFrame(vg_df['trope'].value_counts()).reset_index()
total_counts2.columns = ['trope', 'counts']
# print(total_counts.head())
fig, ax = plt.subplots()
total_counts2.hist('counts', ax=ax)
ax.set_yscale('log')
plt.title('Number of Occurances per Trope (Video Games)')
plt.xlabel('Number of Occurances')
plt.ylabel('Frequency')
fig.savefig('occurances_per_trope_games_log.png')

# Avg number of occurances per trope: number of trope occurances / number of tropes
mean_occurances_per_trope_tv = tv_df.shape[0] / number_tropes_tv
mean_occurances_per_trope_games = vg_df.shape[0] / number_tropes_games
print('Mean number of occurances per trope (tv): ' + str(mean_occurances_per_trope_tv))
print('Mean number of occurances per trope (games): ' + str(mean_occurances_per_trope_games))

# get the tropes in a specific media
# print(tv_trope_df.loc[tv_trope_df['title'] == 'Person Of Interest'])

# get the media for a specific trope
# print(tv_trope_df.loc[tv_trope_df['trope'] == 'Conlang'])
