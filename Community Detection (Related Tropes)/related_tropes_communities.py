# Related tropes communities

import pandas
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.community as nx_comm
from community import community_louvain

DATA_FILE = '../data_new/* PRIMARY DATASETS/TROPES_DATA/related_tropes_dict.pkl'

with open(DATA_FILE, 'rb') as f:
    related_tropes_dict = pickle.load(f)

print('Constructing graph...')
tropes_graph = nx.Graph(related_tropes_dict)

# Run Louvain Alg for community detection
print('Running Louvain community detection...')
communities = community_louvain.best_partition(tropes_graph)

# Save the assignments for the best communities
#with open('tropes_communities_dict.pkl', 'wb') as f:
#    pickle.dump(communities, f)

print(max(communities.values()))

dendrogram = community_louvain.generate_dendrogram(tropes_graph)

for level in range(len(dendrogram)):  # removed - 1
    print('Partition at level ' + str(level))
    current_level_partition = community_louvain.partition_at_level(dendrogram,
                                                                   level)
    max_community_number = max(current_level_partition.values())

    print(len(current_level_partition))
    input(str(max_community_number + 1) + ' communities')

    # Need to convert results into a list of sets of nodes for each community
    # results dict with tropes (nodes) as keys & clusters (integers) as values
    communities_partition = [set() for i in range(max_community_number + 1)]
    for trope, community_number in current_level_partition.items():
        communities_partition[community_number].add(trope)

    # Evaluation
    modularity = nx_comm.quality.modularity(tropes_graph,
                                            communities_partition)
    print('Modularity is ' + str(modularity))

    quality = nx_comm.quality.partition_quality(tropes_graph,
                                                communities_partition)
    print('Quality (coverage, performance) is ' + str(quality))

# Write graph to gephi
nx.write_gexf(tropes_graph, 'related_tropes.gexf')
