# hlda


import pandas
import pickle
import sys
from hlda.sampler import HierarchicalLDA

# Filepaths for all the data files
VG_FILEPATH = '../data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/vg_tropes.pkl'
TV_FILEPATH = '../data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/tv_tropes.pkl'

TV_RELATED_TROPES = '../topsbm tests/Clustered_datasets/tv_tropes_communities.pkl'
TV_LONG_DESC = '../topsbm tests/Clustered_datasets/tv_tropes_long_cluster.pkl'
TV_SHORT_DESC = '../topsbm tests/Clustered_datasets/tv_tropes_short_neighbour_cluster.pkl'
VG_RELATED_TROPES = '../topsbm tests/Clustered_datasets/vg_tropes_communities.pkl'
VG_LONG_DESC = '../topsbm tests/Clustered_datasets/vg_tropes_long_cluster.pkl'
VG_SHORT_DESC = '../topsbm tests/Clustered_datasets/vg_tropes_short_neighbour_cluster.pkl'


def run_hlda(data_file, run_name, titles, depth):
    print('Running hLDA for: ' + run_name)

    # Read the file
    df = pandas.read_pickle(data_file)

    vocab = set()


    # Format the data
    print('Formatting data as documents....')
    corpus = []
    for title in titles:
        tropes = df.loc[df['title'] == title]['trope'].tolist()
        corpus.append(tropes)
        vocab.update(tropes)

    vocab = sorted(list(vocab))
    vocab_index = {}
    for i, w in enumerate(vocab):
        vocab_index[w] = i

    new_corpus = []
    for doc in corpus:
        new_doc = []
        for word in doc:
            word_idx = vocab_index[word]
            new_doc.append(word_idx)
        new_corpus.append(new_doc)

    hlda = HierarchicalLDA(new_corpus, vocab, alpha=10, gamma=1, eta=0.1, num_levels=3)
    hlda.estimate(500, display_topics=50, n_words=5, with_weights=True)


print('Extracting work titles...')

# Load main tv and vg dataframes
vg_df = pandas.read_pickle(VG_FILEPATH)
tv_df = pandas.read_pickle(TV_FILEPATH)

# Get a list of all titles
all_vg = vg_df['title'].unique().tolist()
all_tv = tv_df['title'].unique().tolist()

# Get a list of the top 500 titles from main datasets for vg and tv
top_500_vg = vg_df.groupby(by='title').agg('count').sort_values(by='trope', ascending=False).head(n=500).reset_index()
top_500_vg = top_500_vg['title'].tolist()
top_500_tv = tv_df.groupby(by='title').agg('count').sort_values(by='trope', ascending=False).head(n=500).reset_index()
top_500_tv = top_500_tv['title'].tolist()

# Run the simulations - ADD THE REST
run_hlda(VG_FILEPATH, 'vg_original', all_vg, 3)  # depth same as topSBM inferred
