# Related tropes communities

import pandas
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.community as nx_comm
from community import community_louvain

DATA_FILE = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_similar.pkl'

print('Loading data...')
tv_related_df = pandas.read_pickle(DATA_FILE)

print('Constructing graph...')
related_graph = nx.convert_matrix.from_pandas_edgelist(tv_related_df, source='title', target='similar_title')

# Run Louvain Alg for community detection to find the best communities
print('Running Louvain community detection...')
communities = community_louvain.best_partition(related_graph)

# Save the assignments for the best communities
with open('tv_communities_dict.pkl', 'wb') as f:
    pickle.dump(communities, f)

max_community_number = max(communities.values())

print(len(communities))
print(str(max_community_number + 1) + ' communities')

# Need to convert results into a list of sets of nodes for each community
# results dict with tropes (nodes) as keys & clusters (integers) as values
communities_partition = [set() for i in range(max_community_number + 1)]
for show, community_number in communities.items():
    communities_partition[community_number].add(show)

# Evaluation
modularity = nx_comm.quality.modularity(related_graph,
                                        communities_partition)
print('Modularity is ' + str(modularity))

quality = nx_comm.quality.partition_quality(related_graph,
                                            communities_partition)
print('Quality (coverage, performance) is ' + str(quality))

# Write graph to gephi
nx.write_gexf(related_graph, 'related_tropes.gexf')
