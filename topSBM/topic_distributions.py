# CSV distributions of topics per year for further analysis

import pickle
import pandas
from scipy import stats as ss

# Filepaths for all the data files - run for all sims and levels.
VG_MISC = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_misc.pkl'
TV_MISC = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_misc.pkl'

# Document topic distribution files
tv_long_500_l0 = 'RESULTS/tv_longdesc_cluster_500topsbm_level_0_topic-dist.csv'
tv_long_500_l1 = 'RESULTS/tv_longdesc_cluster_500topsbm_level_1_topic-dist.csv'
tv_long_l0 = 'RESULTS/tv_longdesc_clustertopsbm_level_0_topic-dist.csv'
tv_long_l1 = 'RESULTS/tv_longdesc_clustertopsbm_level_1_topic-dist.csv'
tv_long_l2 = 'RESULTS/tv_longdesc_clustertopsbm_level_2_topic-dist.csv'
tv_original_500_l0 = 'RESULTS/tv_original_500topsbm_level_0_topic-dist.csv'
tv_original_500_l1 = 'RESULTS/tv_original_500topsbm_level_1_topic-dist.csv'
tv_original_500_l2 = 'RESULTS/tv_original_500topsbm_level_2_topic-dist.csv'
tv_original_l0 = 'RESULTS/tv_originaltopsbm_level_0_topic-dist.csv'
tv_original_l1 = 'RESULTS/tv_originaltopsbm_level_1_topic-dist.csv'
tv_original_l2 = 'RESULTS/tv_originaltopsbm_level_2_topic-dist.csv'
tv_related_500_l0 = 'RESULTS/tv_related_community_500topsbm_level_0_topic-dist.csv'
tv_related_l0 = 'RESULTS/tv_related_communitytopsbm_level_0_topic-dist.csv'
tv_short_500_l0 = 'RESULTS/tv_shortdesc_cluster_500topsbm_level_0_topic-dist.csv'
tv_short_500_l1 = 'RESULTS/tv_shortdesc_cluster_500topsbm_level_1_topic-dist.csv'
tv_short_l0 = 'RESULTS/tv_shortdesc_clustertopsbm_level_0_topic-dist.csv'
tv_short_l1 = 'RESULTS/tv_shortdesc_clustertopsbm_level_1_topic-dist.csv'
tv_short_l2 = 'RESULTS/tv_shortdesc_clustertopsbm_level_2_topic-dist.csv'

vg_long_500_l0 = 'RESULTS/vg_longdesc_cluster_500topsbm_level_0_topic-dist.csv'
vg_long_500_l1 = 'RESULTS/vg_longdesc_cluster_500topsbm_level_1_topic-dist.csv'
vg_long_l0 = 'RESULTS/vg_longdesc_clustertopsbm_level_0_topic-dist.csv'
vg_long_l1 = 'RESULTS/vg_longdesc_clustertopsbm_level_1_topic-dist.csv'
vg_long_l2 = 'RESULTS/vg_longdesc_clustertopsbm_level_2_topic-dist.csv'
vg_original_500_l0 = 'RESULTS/vg_original_500topsbm_level_0_topic-dist.csv'
vg_original_500_l1 = 'RESULTS/vg_original_500topsbm_level_1_topic-dist.csv'
vg_original_l0 = 'RESULTS/vg_originaltopsbm_level_0_topic-dist.csv'
vg_original_l1 = 'RESULTS/vg_originaltopsbm_level_1_topic-dist.csv'
vg_original_l2 = 'RESULTS/vg_originaltopsbm_level_2_topic-dist.csv'
vg_related_500_l0 = 'RESULTS/vg_related_community_500topsbm_level_0_topic-dist.csv'
vg_related_l0 = 'RESULTS/vg_related_communitytopsbm_level_0_topic-dist.csv'
vg_short_500_l0 = 'RESULTS/vg_shortdesc_cluster_500topsbm_level_0_topic-dist.csv'
vg_short_500_l1 = 'RESULTS/vg_shortdesc_cluster_500topsbm_level_1_topic-dist.csv'
vg_short_l0 = 'RESULTS/vg_shortdesc_clustertopsbm_level_0_topic-dist.csv'
vg_short_l1 = 'RESULTS/vg_shortdesc_clustertopsbm_level_1_topic-dist.csv'
vg_short_l2 = 'RESULTS/vg_shortdesc_clustertopsbm_level_2_topic-dist.csv'


def yearly_topic_dists(document_topic_dists_file, tv_or_vg, run_name, run_number):
    print(str(run_number) + '/35: Analysing: ' + run_name)

    # Read the topic distributions from topSBM into dataframe and format
    df = pandas.read_csv(document_topic_dists_file).drop(['i_doc'], axis=1)
    df = df.rename(columns={'doc': 'title'})
    titles_with_topics = df['title'].unique().tolist()
    df = df.set_index('title')
    number_topics = int(list(df.columns)[-1].split(' ')[1])

    # Load the years dataframes and format correctly (into years)
    if tv_or_vg == 'VG':
        times_df = pandas.read_pickle(VG_MISC).drop(['metacritic', 'number_ratings'], axis=1)
        times_df['release_date'] = pandas.DatetimeIndex(times_df['release_date']).year
        times_df = times_df.rename(columns={'release_date': 'start_year'})
        times_df = times_df.dropna()
    elif tv_or_vg == 'TV':
        times_df = pandas.read_pickle(TV_MISC).drop(['imdb_title', 'number_episodes', 'end_year', 'rating', 'rating_count'], axis=1)
        times_df = times_df.dropna()

    # Make a dict of with years as key, and list of works that year as value
    df2 = times_df[times_df['title'].isin(titles_with_topics)].groupby('start_year').apply(lambda x: list(x['title'].unique()))
    works_per_year = df2.to_dict()

    # For each year, sum the weights of each topic for each work and record the
    # total number of works for that year
    list_for_df = []

    for year in works_per_year.keys():
        # Get the works for this year
        current_year_works = works_per_year[year]

        # Initialise the data dictionary
        number_works_year_w_topics = len(current_year_works)
        this_year_data = {'year': year, 'total_works': number_works_year_w_topics}
        for topic_number in range(1, number_topics + 1):
            key = 'topic_' + str(topic_number)
            this_year_data[key] = 0

        # Get the topic weights for each game
        for title in current_year_works:

            topic_weights = df.loc[title].tolist()

            for topic_number, topic_weight in enumerate(topic_weights):
                key = 'topic_' + str(topic_number + 1)
                this_year_data[key] += topic_weight

        # Save the data for this year
        list_for_df.append(this_year_data)

    # Make the data for all years into a dataframe
    year_topic_weights_df = pandas.DataFrame(list_for_df)

    # Calculate the stats for all time
    all_time_dist = year_topic_weights_df.sum(axis=0).to_dict()
    all_time_dist.pop('year', None)
    for topic_number in range(1, number_topics + 1):
        key = 'topic_' + str(topic_number)
        all_time_dist[key] = all_time_dist[key] / all_time_dist['total_works']

    # Save
    filename = 'TOPIC_DISTS/' + run_name + '_all_time_topic_dist_dict.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(all_time_dist, f)

    # For each year, divide by total number of works column for distribution
    for topic_number in range(1, number_topics + 1):
        key = 'topic_' + str(topic_number)
        year_topic_weights_df[key] = year_topic_weights_df[key] / year_topic_weights_df['total_works']

    # Save
    filename = 'TOPIC_DISTS/' + run_name + '_yearly_topic_dist_df.csv'
    year_topic_weights_df.to_csv(filename)


# Run for each simualation!

yearly_topic_dists(tv_long_500_l0, 'TV', 'tv_long_500_l0', 1)
yearly_topic_dists(tv_long_500_l1, 'TV', 'tv_long_500_l1', 2)
yearly_topic_dists(tv_long_l0, 'TV', 'tv_long_l0', 3)
yearly_topic_dists(tv_long_l1, 'TV', 'tv_long_l1', 4)
yearly_topic_dists(tv_long_l2, 'TV', 'tv_long_l2', 5)

yearly_topic_dists(tv_original_500_l0, 'TV', 'tv_original_500_l0', 6)
yearly_topic_dists(tv_original_500_l1, 'TV', 'tv_original_500_l1', 7)
yearly_topic_dists(tv_original_500_l2, 'TV', 'tv_original_500_l2', 8)
yearly_topic_dists(tv_original_l0, 'TV', 'tv_original_l0', 9)
yearly_topic_dists(tv_original_l1, 'TV', 'tv_original_l1', 10)
yearly_topic_dists(tv_original_l2, 'TV', 'tv_original_l2', 11)

yearly_topic_dists(tv_related_500_l0, 'TV', 'tv_related_500_l0', 12)
yearly_topic_dists(tv_related_l0, 'TV', 'tv_related_l0', 13)

yearly_topic_dists(tv_short_500_l0, 'TV', 'tv_short_500_l0', 14)
yearly_topic_dists(tv_short_500_l1, 'TV', 'tv_short_500_l1', 14)

yearly_topic_dists(tv_long_500_l1, 'TV', 'tv_long_500_l1', 15)
yearly_topic_dists(tv_short_l0, 'TV', 'tv_short_l0', 16)
yearly_topic_dists(tv_short_l1, 'TV', 'tv_short_l1', 17)
yearly_topic_dists(tv_short_l2, 'TV', 'tv_short_l2', 18)

yearly_topic_dists(vg_long_500_l0, 'VG', 'vg_long_500_l0', 19)
yearly_topic_dists(vg_long_500_l1, 'VG', 'vg_long_500_l1', 20)
yearly_topic_dists(vg_long_l0, 'VG', 'vg_long_l0', 21)
yearly_topic_dists(vg_long_l1, 'VG', 'vg_long_l1', 22)
yearly_topic_dists(vg_long_l2, 'VG', 'vg_long_l2', 23)

yearly_topic_dists(vg_original_500_l0, 'VG', 'vg_original_500_l0', 24)
yearly_topic_dists(vg_original_500_l1, 'VG', 'vg_original_500_l1', 25)
yearly_topic_dists(vg_original_l0, 'VG', 'vg_original_l0', 26)
yearly_topic_dists(vg_original_l1, 'VG', 'vg_original_l1', 27)
yearly_topic_dists(vg_original_l2, 'VG', 'vg_original_l2', 28)

yearly_topic_dists(vg_related_500_l0, 'VG', 'vg_related_500_l0', 29)
yearly_topic_dists(vg_related_l0, 'VG', 'vg_related_l0', 30)

yearly_topic_dists(vg_short_500_l0, 'VG', 'vg_short_500_l0', 31)
yearly_topic_dists(vg_short_500_l1, 'VG', 'vg_short_500_l1', 32)
yearly_topic_dists(vg_short_l0, 'VG', 'vg_short_l0', 33)
yearly_topic_dists(vg_short_l1, 'VG', 'vg_short_l1', 34)
yearly_topic_dists(vg_short_l2, 'VG', 'vg_short_l2', 35)
