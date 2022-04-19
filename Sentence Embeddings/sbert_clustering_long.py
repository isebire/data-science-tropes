import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
from sentence_transformers import SentenceTransformer, util
import pickle
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import time

DATA_FILEPATH = 'trope_description_dict.pkl'

model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the tropes description data
with open(DATA_FILEPATH, 'rb') as f:
    data = pickle.load(f)

trope_names = list(data.keys())
trope_descriptions = list(data.values())

# Compute encodings
trope_embeddings = model.encode(trope_descriptions, show_progress_bar=True)

embeddings_dict = {}
for trope, embedding in zip(trope_names, trope_embeddings):
    embeddings_dict[trope] = embedding

# Save the embeddings
with open('embeddings_long.pkl', 'wb') as f:
    pickle.dump(embeddings_dict, f)

print('Embeddings done')

# Perform agglomerative (hierarchical) clustering as in agglomerative.py
# (from documentation)

print('Started agglomerative clustering:')

# Normalize the embeddings to unit length
trope_embeddings_agg = trope_embeddings / np.linalg.norm(trope_embeddings, axis=1, keepdims=True)

# Perform kmean clustering
clustering_model = AgglomerativeClustering(n_clusters=None, distance_threshold=1.5) #, affinity='cosine', linkage='average', distance_threshold=0.4)
clustering_model.fit(trope_embeddings_agg)
cluster_assignment = clustering_model.labels_

clustered_tropes_desc = {}
clustered_tropes = {}
for trope_id, cluster_id in enumerate(cluster_assignment):
    if cluster_id not in clustered_tropes_desc:
        clustered_tropes_desc[cluster_id] = []
        clustered_tropes[cluster_id] = []

    clustered_tropes_desc[cluster_id].append(trope_descriptions[trope_id])
    clustered_tropes[cluster_id].append(trope_names[trope_id])

# Save the results
with open('embeddings_long_cluster_agg_MODEL_RESULTS.pkl', 'wb') as f:
    pickle.dump(clustering_model, f)

with open('embeddings_long_cluster_agg.pkl', 'wb') as f:
    pickle.dump(clustered_tropes, f)

with open('embeddings_long_cluster_agg_descs.pkl', 'wb') as f:
    pickle.dump(clustered_tropes_desc, f)

for i, cluster in clustered_tropes.items():
    print("Cluster ", i+1)
    print(cluster)
    print("")

print(len(clustered_tropes.items()))

# Perform clustering as in fast_clustering.py
print("Start fast clustering")
start_time = time.time()

# Two parameters to tune:
# min_cluster_size: Only consider cluster that have at least 25 elements
# threshold: Consider sentence pairs with a cosine-similarity larger than threshold as similar
clusters = util.community_detection(trope_embeddings, min_community_size=3, threshold=0.5)

# ^ format - list of lists of trope ids

print("Clustering done after {:.2f} sec".format(time.time() - start_time))

# Print for all clusters the top 3 and bottom 3 elements
for i, cluster in enumerate(clusters):
    print("\nCluster {}, #{} Elements ".format(i+1, len(cluster)))
    for sentence_id in cluster[0:3]:
        print("\t", trope_names[sentence_id])
    print("\t", "...")
    for sentence_id in cluster[-3:]:
        print("\t", trope_names[sentence_id])

clustered_tropes = {}
for i, cluster in enumerate(clusters):
    names_cluster = []
    for trope_id in cluster:
        names_cluster.append(trope_names[trope_id])
    clustered_tropes[i] = names_cluster

print(clustered_tropes)

# Save the results
with open('embeddings_long_cluster_fast.pkl', 'wb') as f:
    pickle.dump(clustered_tropes, f)
