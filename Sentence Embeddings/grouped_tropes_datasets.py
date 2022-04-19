# New vers of datasets clustered

import pickle
from sklearn.metrics.cluster import adjusted_rand_score, rand_score
import os
import numpy as np
import pandas

# Load the clusters
with open('embeddings_laconic_cluster_agg.pkl', 'rb') as f:
    short_agg = pickle.load(f)

with open('embeddings_long_cluster_agg.pkl', 'rb') as f:
    long_agg = pickle.load(f)

with open('nearest_neighbours_dict.pkl', 'rb') as f:
    nearest_neighbours = pickle.load(f)

# Find the cluster assignment of each trope
short_agg_flip = {}
for cluster, tropes in short_agg.items():
    for trope in tropes:
        short_agg_flip[trope] = cluster

long_agg_flip = {}
for cluster, tropes in long_agg.items():
    for trope in tropes:
        long_agg_flip[trope] = cluster

short_agg_flip_neighbours = short_agg_flip.copy()
for trope in nearest_neighbours:
    neighbour_trope = nearest_neighbours[trope]
    short_agg_flip_neighbours[trope] = short_agg_flip_neighbours[neighbour_trope]

# Find ARI for neighbours + short and long desc
long_agg_list = []
short_agg_list = []

for trope in long_agg_flip.keys():
    long_agg_list.append(long_agg_flip[trope])
    short_agg_list.append(short_agg_flip_neighbours[trope])

# Now the data is in the right format to begin computing ARI Scores
# Note the labels used don't need to match for the clusters to match
print('ARI')
print(adjusted_rand_score(long_agg_list, short_agg_list))
print('RI')
print(rand_score(long_agg_list, short_agg_list))

# Load communities
os.chdir('../community detection related')
with open('tropes_communities_dict.pkl', 'rb') as f:
    communities_dict = pickle.load(f)

# SEE CODE FOR REPLACING ALT TROPES NAMES BASED ON DICT
os.chdir('..')

main_df_folder = 'data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/'

# small investigation
'''
vg_df = pandas.read_pickle(main_df_folder + 'vg_tropes.pkl')
tv_df = pandas.read_pickle(main_df_folder + 'tv_tropes.pkl')
missing_tropes = list((set(vg_df['trope'].unique()).union(set(tv_df['trope'].unique())).difference(set(long_agg_flip.keys()))).union(set(vg_df['trope'].unique()).union(set(tv_df['trope'].unique())).difference(set(communities_dict.keys()))))
input(missing_tropes)
input('audiencealienatingending' in list(set(vg_df['trope'].unique()).union(set(tv_df['trope'].unique()))))
with open('missing_tropes.pkl', 'wb') as f:
    pickle.dump(missing_tropes, f)
input('fish')
'''

# Stats on trope coverage
vg_df = pandas.read_pickle(main_df_folder + 'vg_tropes.pkl')
vg_tropes = vg_df['trope'].unique()
print(len(vg_tropes)) # how many tropes in og dataset
print(len(set(long_agg_flip.keys()).intersection(set(vg_tropes))))  # how many of these
print(len(set(short_agg_flip_neighbours.keys()).intersection(set(vg_tropes))))
print(len(set(communities_dict.keys()).intersection(set(vg_tropes))))

tv_df = pandas.read_pickle(main_df_folder + 'tv_tropes.pkl')
tv_tropes = tv_df['trope'].unique()
print(len(tv_tropes)) # how many tropes in og dataset
print(len(set(long_agg_flip.keys()).intersection(set(tv_tropes)))) # how many of these
print(len(set(short_agg_flip_neighbours.keys()).intersection(set(tv_tropes))))
print(len(set(communities_dict.keys()).intersection(set(tv_tropes))))

# Make the datasets
print('VG - Long...')
vg_df = pandas.read_pickle(main_df_folder + 'vg_tropes.pkl')
vg_df['trope'].replace(long_agg_flip, inplace=True)
vg_df = vg_df[vg_df['trope'].isin(long_agg_flip.values())]
vg_df = vg_df.drop_duplicates()
print(set(vg_df['trope'].unique()))
vg_df.to_pickle('vg_tropes_long_cluster.pkl')

print('VG - Short + neighbours...')
vg_df = pandas.read_pickle(main_df_folder + 'vg_tropes.pkl')
vg_df['trope'].replace(short_agg_flip_neighbours, inplace=True)
vg_df = vg_df[vg_df['trope'].isin(short_agg_flip_neighbours.values())]
vg_df = vg_df.drop_duplicates()
print(set(vg_df['trope'].unique()))
vg_df.to_pickle('vg_tropes_short_neighbour_cluster.pkl')

print('VG - Communities...')
vg_df = pandas.read_pickle(main_df_folder + 'vg_tropes.pkl')
vg_df['trope'].replace(communities_dict, inplace=True)
vg_df = vg_df[vg_df['trope'].isin(communities_dict.values())]
vg_df = vg_df.drop_duplicates()
print(set(vg_df['trope'].unique()))
vg_df.to_pickle('vg_tropes_communities.pkl')

print('TV - Long...')
tv_df = pandas.read_pickle(main_df_folder + 'tv_tropes.pkl')
tv_df['trope'].replace(long_agg_flip, inplace=True)
tv_df = tv_df[tv_df['trope'].isin(long_agg_flip.values())]
tv_df = tv_df.drop_duplicates()
print(set(tv_df['trope'].unique()))
tv_df.to_pickle('tv_tropes_long_cluster.pkl')

print('TV - Short + neighbours...')
tv_df = pandas.read_pickle(main_df_folder + 'tv_tropes.pkl')
tv_df['trope'].replace(short_agg_flip_neighbours, inplace=True)
tv_df = tv_df[tv_df['trope'].isin(short_agg_flip_neighbours.values())]
tv_df = tv_df.drop_duplicates()
print(set(tv_df['trope'].unique()))
tv_df.to_pickle('tv_tropes_short_neighbour_cluster.pkl')

print('TV - Communities ...')
tv_df = pandas.read_pickle(main_df_folder + 'tv_tropes.pkl')
tv_df['trope'].replace(communities_dict, inplace=True)
tv_df = tv_df[tv_df['trope'].isin(communities_dict.values())]
tv_df = tv_df.drop_duplicates()
print(set(tv_df['trope'].unique()))
tv_df.to_pickle('tv_tropes_communities.pkl')
