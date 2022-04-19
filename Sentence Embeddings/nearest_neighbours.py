# Sbert nearest neighbours

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
from sentence_transformers import SentenceTransformer, util
import pickle
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

with open('embeddings_laconic.pkl', 'rb') as f:
    laconic_embeddings = pickle.load(f)

with open('embeddings_long.pkl', 'rb') as f:
    long_embeddings = pickle.load(f)

tropes_only_long_desc = set(long_embeddings.keys()) - set(laconic_embeddings.keys())
tropes_short_desc = set(laconic_embeddings.keys())

# Load data with long descriptions

with open('trope_description_dict.pkl', 'rb') as f:
    trope_descriptions = pickle.load(f)

data_cleaned = {}
for trope, description in trope_descriptions.items():
    if trope in tropes_short_desc:
        data_cleaned[trope] = description

short_desc_tropes_ordered = list(data_cleaned.keys())
corpus = list(data_cleaned.values())

# Compute the corpus of long embeddings as a tensor, for the tropes with short descriptions

corpus_embeddings = model.encode(corpus, convert_to_tensor=True,
                                 show_progress_bar=True)

# Map tropes with only long description to the nearest neighbour with a
# short description based on long descriptions

nearest_neighbours = {}

for trope in tropes_only_long_desc:
    query_embedding = model.encode(trope_descriptions[trope],
                                      convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=1)

    for score, id in zip(top_results[0], top_results[1]):
        print('-----------')
        print(trope)
        print(short_desc_tropes_ordered[id], "(Score: {:.4f})".format(score))

    nearest_neighbours[trope] = short_desc_tropes_ordered[id]

# Save the results
with open('nearest_neighbours_dict.pkl', 'wb') as f:
    pickle.dump(nearest_neighbours, f)
