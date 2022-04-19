# topSBM Model

import pickle
import pandas
import pylab as plt
from sbmtm import sbmtm
import graph_tool.all as gt
import numpy as np

# need to do conda activate gt   first then   conda deactivate   after

# Filepaths for all the data files
VG_FILEPATH = '../data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/vg_tropes.pkl'
TV_FILEPATH = '../data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/tv_tropes.pkl'
#VG_FILEPATH = 'vg_tropes.pkl'
#TV_FILEPATH = 'tv_tropes.pkl'

TV_RELATED_TROPES = 'Clustered_datasets/tv_tropes_communities.pkl'
TV_LONG_DESC = 'Clustered_datasets/tv_tropes_long_cluster.pkl'
TV_SHORT_DESC = 'Clustered_datasets/tv_tropes_short_neighbour_cluster.pkl'
VG_RELATED_TROPES = 'Clustered_datasets/vg_tropes_communities.pkl'
VG_LONG_DESC = 'Clustered_datasets/vg_tropes_long_cluster.pkl'
VG_SHORT_DESC = 'Clustered_datasets/vg_tropes_short_neighbour_cluster.pkl'


def sbm_topic_model(data_file, run_name, titles, plot_dists):
    print('Running topSBM for: ' + run_name)

    # Read the file
    df = pandas.read_pickle(data_file)

    # Format the data
    print('Formatting data as documents....')
    texts = []
    for title in titles:
        tropes = df.loc[df['title'] == title]['trope'].tolist()
        texts.append(tropes)

    # Initialise and fit the model
    print('Initialising and fitting topSBM model...')
    sbmtm_model = sbmtm()
    sbmtm_model.make_graph(texts, documents=titles)
    gt.seed_rng(32)
    sbmtm_model.fit()

    # Plot the model
    print('Saving plot of the model')
    filename_sbmtm_plot = run_name + '_sbmtm_plot.png'
    sbmtm_model.plot(nedges=10000, filename=filename_sbmtm_plot)

    levels = sbmtm_model.L

    # Analyse at each level
    for level in range(levels):
        print('Analysing at level ' + str(level))

        # Note: for non-overlapping, each document belongs to one group
        # with prob 1. but document is still dist over multiple
        # topics. overlapping case doesn't work anyway causes seg fault
        # print_topics saves topics, topic-distributions, document clusters
        # to file. edited so that weights of tropes in the topic are also saved
        # and that plots the topic dists for each document also in this
        # function as that is an expensive operation
        sbmtm_model.print_topics(l=level, filename_prefix=run_name,
                                 plot_dists=plot_dists)

        # Save the model to pickle
        model_filename = run_name + '_model.pkl'
        with open(model_filename, 'wb') as f:
            pickle.dump(sbmtm_model, f)


print('Packages loaded.')

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

# Run the simulations
sbm_topic_model(TV_RELATED_TROPES, 'tv_related_community_500', top_500_tv, True)
sbm_topic_model(VG_RELATED_TROPES, 'vg_related_community_500', top_500_vg, True)
sbm_topic_model(VG_SHORT_DESC, 'vg_shortdesc_cluster_500', top_500_vg, True)
sbm_topic_model(TV_SHORT_DESC, 'tv_shortdesc_cluster_500', top_500_tv, True)
sbm_topic_model(VG_LONG_DESC, 'vg_longdesc_cluster_500', top_500_vg, True)
sbm_topic_model(TV_LONG_DESC, 'tv_longdesc_cluster_500', top_500_tv, True)
sbm_topic_model(TV_FILEPATH, 'tv_original_500', top_500_tv, True)
sbm_topic_model(VG_FILEPATH, 'vg_original_500', top_500_vg, True)

sbm_topic_model(TV_RELATED_TROPES, 'tv_related_community', all_tv, False)
sbm_topic_model(VG_RELATED_TROPES, 'vg_related_community', all_vg, False)
sbm_topic_model(VG_SHORT_DESC, 'vg_shortdesc_cluster', all_vg, False)
sbm_topic_model(TV_SHORT_DESC, 'tv_shortdesc_cluster', all_tv, False)
sbm_topic_model(VG_LONG_DESC, 'vg_longdesc_cluster', all_vg, False)
sbm_topic_model(TV_LONG_DESC, 'tv_longdesc_cluster', all_tv, False)
sbm_topic_model(TV_FILEPATH, 'tv_original', all_tv, False)
sbm_topic_model(VG_FILEPATH, 'vg_original', all_vg, False)
