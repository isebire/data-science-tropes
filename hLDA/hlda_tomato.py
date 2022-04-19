import tomotopy as tp
import pandas
import pickle
import sys
from tomotopy.utils import Corpus

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

    # Create the model
    model = tp.HLDAModel(depth=depth)

    # Format the data
    print('Formatting data as documents....')
    texts = []
    for title in titles:
        tropes = df.loc[df['title'] == title]['trope'].tolist()
        texts.append(tropes)
        model.add_doc(tropes)

    # Train (fit) the model
    '''
    for i in range(0, 100, 10):
        model.train(10)
        print('Iteration: {}\tLog-likelihood: {}'.format(i, model.ll_per_word))
    '''

    print('Training...', file=sys.stderr, flush=True)
    for _ in range(0, 1000, 10):
        model.train(7)
        model.train(3, freeze_topics=True)
        print('Iteration: {:05}\tll per word: {:.5f}\tNum. of topics: {}'.format(model.global_step, model.ll_per_word, model.live_k))

    for _ in range(0, 100, 10):
        model.train(10, freeze_topics=True)
        print('Iteration: {:05}\tll per word: {:.5f}\tNum. of topics: {}'.format(model.global_step, model.ll_per_word, model.live_k))


    # Results (analyse)
    print('Number of live topics: ' + str(model.live_k))

    for level in range(depth):
        print('Analysing at level ' + str(level))
        df = pandas.DataFrame()

        current_level_topics = [k for k in range(model.k) if model.level(k) == level]
        print('Topics at level:')
        print(current_level_topics)

        # Analyse each topic at this level
        for k in current_level_topics:
            print('Topic' + str(k))
            print(model.children_topics(k))
            print(model.parent_topic(k))

            # Weight of each word in the topic
            topic_words = model.get_topic_words(k, top_n=-1)
            df['Topic ' + str(k)] = [(i + '/' + str(j)) for (i,j) in topic_words]

        df.to_csv(run_name + '_level_' + str(level) + '_topics.csv')

    model.summary()

    # how to choose level? this is so mysterious
    # I think it might say the path through the topic tree, so which topic on
    # which level. so if 3 levels, it is 3 long
    for text in texts:
        test_result, ll = model.infer(model.make_doc(text))
        print(test_result)

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
