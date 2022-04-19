import pickle
from sklearn.metrics.cluster import adjusted_rand_score, rand_score
import os
from sklearn.metrics import silhouette_score
import numpy as np

# can probs make more efficient

# Load the trope names
#with open('trope_names_list.pkl', 'rb') as f:
#    trope_names_list = pickle.load(f)

# Load the clusters
with open('embeddings_laconic_cluster_agg.pkl', 'rb') as f:
    short_agg = pickle.load(f)

with open('embeddings_laconic_cluster_fast.pkl', 'rb') as f:
    short_fast = pickle.load(f)

with open('embeddings_long_cluster_agg.pkl', 'rb') as f:
    long_agg = pickle.load(f)

with open('embeddings_long_cluster_fast.pkl', 'rb') as f:
    long_fast = pickle.load(f)

# Load embeddings

with open('embeddings_laconic.pkl', 'rb') as f:
    embeddings_laconic_dict = pickle.load(f)

with open('embeddings_long.pkl', 'rb') as f:
    embeddings_long_dict = pickle.load(f)

# Find the cluster assignment of each trope
short_agg_flip = {}
for cluster, tropes in short_agg.items():
    for trope in tropes:
        short_agg_flip[trope] = cluster

short_fast_flip = {}
for cluster, tropes in short_fast.items():
    for trope in tropes:
        short_fast_flip[trope] = cluster

long_agg_flip = {}
for cluster, tropes in long_agg.items():
    for trope in tropes:
        long_agg_flip[trope] = cluster

long_fast_flip = {}
for cluster, tropes in long_fast.items():
    for trope in tropes:
        long_fast_flip[trope] = cluster


# Load tropes with laconic entries
os.chdir('..')
with open('data_new/* PRIMARY DATASETS/TROPES_DATA/trope_description_laconic_dict.pkl', 'rb') as f:
    laconic_dict = pickle.load(f)

tropes_names_list = []
for trope, description in laconic_dict.items():
    if description != '/':
        tropes_names_list.append(trope)

# Save a list of cluster assignments
long_agg_clusters_list = []
long_fast_clusters_list = []
short_agg_clusters_list = []
short_fast_clusters_list = []
embeddings_laconic_list = []

# Find the cluster assignment of these tropes
max_short_fast = max(short_fast.keys())
max_long_fast = max(long_fast.keys())

for trope in tropes_names_list:
    long_agg_clusters_list.append(long_agg_flip[trope])
    short_agg_clusters_list.append(short_agg_flip[trope])
    embeddings_laconic_list.append(embeddings_laconic_dict[trope])

    # Note that for fast clustering, not every trope is assigned a cluster. So
    # if it's not in a cluster, label as a singleton.

    if trope in short_fast_flip.keys():
        short_fast_clusters_list.append(short_fast_flip[trope])
    else:
        max_short_fast += 1
        short_fast_clusters_list.append(max_short_fast)

    if trope in long_fast_flip.keys():
        long_fast_clusters_list.append(long_fast_flip[trope])
    else:
        max_long_fast += 1
        long_fast_clusters_list.append(max_long_fast)

# input(adjusted_rand_score([1,1,2,2], [2,2,4,4]))

# Now the data is in the right format to begin computing ARI Scores
# Note the labels used don't need to match for the clusters to match
print('ARI Scores of how well they match: 1 best 0 low')
print('Short agg and short fast')
print(adjusted_rand_score(short_agg_clusters_list, short_fast_clusters_list))
print('Short agg and long agg')
print(adjusted_rand_score(short_agg_clusters_list, long_agg_clusters_list))
print('Short agg and long fast')
print(adjusted_rand_score(short_agg_clusters_list, long_fast_clusters_list))
print('Short fast and long agg')
print(adjusted_rand_score(short_fast_clusters_list, long_agg_clusters_list))
print('Short fast and long fast')
print(adjusted_rand_score(short_fast_clusters_list, long_fast_clusters_list))
print('Long agg and Long fast')
print(adjusted_rand_score(long_agg_clusters_list, long_fast_clusters_list))

print('RI Scores of how well they match: 1 best 0 low')
print('Short agg and short fast')
print(rand_score(short_agg_clusters_list, short_fast_clusters_list))
print('Short agg and long agg')
print(rand_score(short_agg_clusters_list, long_agg_clusters_list))
print('Short agg and long fast')
print(rand_score(short_agg_clusters_list, long_fast_clusters_list))
print('Short fast and long agg')
print(rand_score(short_fast_clusters_list, long_agg_clusters_list))
print('Short fast and long fast')
print(rand_score(short_fast_clusters_list, long_fast_clusters_list))
print('Long agg and Long fast')
print(rand_score(long_agg_clusters_list, long_fast_clusters_list))


# Silhouette

# For silhouette scores for long descriptions, do for all tropes
long_agg_clusters_list_full = []
long_fast_clusters_list_full = []
embeddings_long_list = []

max_long_fast = max(long_fast.keys())
for trope in laconic_dict.keys():  # all tropes
    long_agg_clusters_list_full.append(long_agg_flip[trope])
    embeddings_long_list.append(embeddings_long_dict[trope])

    if trope in long_fast_flip.keys():
        long_fast_clusters_list_full.append(long_fast_flip[trope])
    else:
        max_long_fast += 1
        long_fast_clusters_list_full.append(max_long_fast)

# Calculate

print('Silhouette score short fast')
print(silhouette_score(embeddings_laconic_list, short_fast_clusters_list, metric='euclidean'))
print('Silhouette score long fast')
print(silhouette_score(embeddings_long_list, long_fast_clusters_list_full, metric='euclidean'))

embeddings_laconic_list = embeddings_laconic_list / np.linalg.norm(embeddings_laconic_list, axis=1, keepdims=True)
print('Silhouette score short agg')
print(silhouette_score(embeddings_laconic_list, short_agg_clusters_list, metric='euclidean'))
print('Silhouette score long agg')
print(silhouette_score(embeddings_long_list, long_agg_clusters_list_full, metric='euclidean'))
