from scipy import stats as ss
import pickle
import pandas
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import random
from operator import itemgetter
from itertools import *

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


def kl_v2(document_topic_dists_file, tv_or_vg, run_name, run_number):
    print(str(run_number) + '/35: Analysing: ' + run_name)

    # Load the overall document distribution files (raw topsbm results)
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

    # get the dict of works for each year
    df2 = times_df[times_df['title'].isin(titles_with_topics)].groupby('start_year').apply(lambda x: list(x['title'].unique()))
    works_per_year = df2.to_dict()

    times_df2 = times_df[times_df['title'].isin(titles_with_topics)]

    years = [int(x) for x in list(set(times_df2['start_year'].tolist()))]
    missing_years = [x for x in range(min(years), max(years)) if x not in years]
    KL_over_multiple_years = [(x+1) for x in missing_years if (x+1) in years]

    # for each consecutive pair of years:
    prev_year_works = works_per_year[years[0]]

    kl_data = []
    kl_gaps_plot = []
    kl_gaps_plot_std = []

    for i in range(1, len(years)):
        current_year_works = works_per_year[years[i]]

        this_year_kl = []

        for j in range(1000):
            # Get topic distribution for a random work from both years

            work_index_y1 = random.randint(0, len(prev_year_works) - 1)
            prev_year_work = prev_year_works[work_index_y1]
            y1_work_topic_dist = df.loc[prev_year_work].replace(0, 10**(-9)).tolist()

            work_index_y2 = random.randint(0, len(current_year_works) - 1)
            current_year_work = current_year_works[work_index_y2]
            y2_work_topic_dist = df.loc[current_year_work].replace(0, 10**(-9)).tolist()

            assert(abs(1-sum(y1_work_topic_dist)) < 0.001)
            assert(abs(1-sum(y2_work_topic_dist)) < 0.001)

            # Calculate and safe the KL divergence between these distributions
            kl_divergence = ss.entropy(y1_work_topic_dist, y2_work_topic_dist)
            this_year_kl.append(kl_divergence)

        # Save the mean and standard deviation
        kl_mean = sum(this_year_kl) / len(this_year_kl)
        kl_std = np.std(this_year_kl)
        this_year_data = {'year': years[i], 'kl_mean': kl_mean, 'kl_std': kl_std}
        kl_data.append(this_year_data)

        # For gaps plot
        if (years[i] not in missing_years) and (years[i] not in KL_over_multiple_years):
            kl_gaps_plot.append(kl_mean)
            kl_gaps_plot_std.append(kl_std)
        else:
            kl_gaps_plot.append(None)
            kl_gaps_plot_std.append(None)

        prev_year_works = current_year_works


    # KL data
    kl_df = pandas.DataFrame(kl_data)
    filepath = 'TOPIC_DIST_ANALYSIS/' + run_name + '_klv2.csv'
    kl_df.to_csv(filepath)

    # Plot the mean KL with standard deviation
    plt.figure(figsize=(8,8))
    plt.plot(kl_df['year'], kl_df['kl_mean'])
    y_low_error = [kl_df['kl_mean'][i] - kl_df['kl_std'][i] for i in range(len(kl_df['year']))]
    y_high_error = [kl_df['kl_mean'][i] + kl_df['kl_std'][i] for i in range(len(kl_df['year']))]
    plt.fill_between(kl_df['year'], y_low_error, y_high_error, color='#bdfffd')
    plt.title('Mean novelty (KL divergence)')
    plt.xlabel('Year')
    plt.ylabel('Mean KL divergence')
    filename = 'TOPIC_DIST_ANALYSIS/' + run_name + '_KLv2.png'
    plt.savefig(filename)

    # Plot again with breaks in the time series if KL was calculated over
    # more than 1 year

    kl_gaps_plot_2 = []
    kl_gaps_plot_std_2 = []
    index_counter = 0
    for year in range(years[1], years[-1] + 1):
        if year in years:
            kl_gaps_plot_2.append(kl_gaps_plot[index_counter])
            kl_gaps_plot_std_2.append(kl_gaps_plot_std[index_counter])
            index_counter += 1
        else:
            kl_gaps_plot_2.append(None)
            kl_gaps_plot_std_2.append(None)


    years_to_plot = [year for year in range(years[1], years[-1] + 1)]
    plt.figure(figsize=(12, 10), dpi=80)
    plt.plot(years_to_plot, kl_gaps_plot_2)

    y_low_error = []
    y_high_error = []
    years_with_data = []

    for i in range(len(years_to_plot)):
        if kl_gaps_plot_2[i] is not None:
            y_low_error.append(kl_gaps_plot_2[i] - kl_gaps_plot_std_2[i])
            y_high_error.append(kl_gaps_plot_2[i] + kl_gaps_plot_std_2[i])
            years_with_data.append(years_to_plot[i])
        #else:
        #    y_low_error.append(None)
        #    y_high_error.append(None)

    groups = []
    for k, g in groupby(enumerate(years_with_data), lambda x: x[0]-x[1]):
        groups.append(list(map(itemgetter(1), g)))

    start_pos = 0
    for group in groups:
        end_pos = start_pos + len(group)
        plt.fill_between(group, y_low_error[start_pos:end_pos], y_high_error[start_pos:end_pos], color='#bdfffd')
        start_pos += len(group)

    # plt.fill_between(years_to_plot, y_low_error, y_high_error, color='#bdfffd')
    plt.xlabel('Year', fontsize=13)
    plt.ylabel('Mean novelty (KL divergence)', fontsize=13)
    plt.title('Mean novelty compared to previous year', fontsize=15)
    filename = 'TOPIC_DIST_ANALYSIS/' + run_name + '_KL_w_gaps_v2.png'
    plt.savefig(filename)


# Run for each simualation!

kl_v2(tv_long_500_l0, 'TV', 'tv_long_500_l0', 1)
kl_v2(tv_long_500_l1, 'TV', 'tv_long_500_l1', 2)
kl_v2(tv_long_l0, 'TV', 'tv_long_l0', 3)
kl_v2(tv_long_l1, 'TV', 'tv_long_l1', 4)
kl_v2(tv_long_l2, 'TV', 'tv_long_l2', 5)

kl_v2(tv_original_500_l0, 'TV', 'tv_original_500_l0', 6)
kl_v2(tv_original_500_l1, 'TV', 'tv_original_500_l1', 7)
kl_v2(tv_original_500_l2, 'TV', 'tv_original_500_l2', 8)
kl_v2(tv_original_l0, 'TV', 'tv_original_l0', 9)
kl_v2(tv_original_l1, 'TV', 'tv_original_l1', 10)
kl_v2(tv_original_l2, 'TV', 'tv_original_l2', 11)

kl_v2(tv_related_500_l0, 'TV', 'tv_related_500_l0', 12)
kl_v2(tv_related_l0, 'TV', 'tv_related_l0', 13)

kl_v2(tv_short_500_l0, 'TV', 'tv_short_500_l0', 14)
kl_v2(tv_short_500_l1, 'TV', 'tv_short_500_l1', 14)

kl_v2(tv_long_500_l1, 'TV', 'tv_long_500_l1', 15)
kl_v2(tv_short_l0, 'TV', 'tv_short_l0', 16)
kl_v2(tv_short_l1, 'TV', 'tv_short_l1', 17)
kl_v2(tv_short_l2, 'TV', 'tv_short_l2', 18)

kl_v2(vg_long_500_l0, 'VG', 'vg_long_500_l0', 19)
kl_v2(vg_long_500_l1, 'VG', 'vg_long_500_l1', 20)
kl_v2(vg_long_l0, 'VG', 'vg_long_l0', 21)
kl_v2(vg_long_l1, 'VG', 'vg_long_l1', 22)
kl_v2(vg_long_l2, 'VG', 'vg_long_l2', 23)

kl_v2(vg_original_500_l0, 'VG', 'vg_original_500_l0', 24)
kl_v2(vg_original_500_l1, 'VG', 'vg_original_500_l1', 25)
kl_v2(vg_original_l0, 'VG', 'vg_original_l0', 26)
kl_v2(vg_original_l1, 'VG', 'vg_original_l1', 27)
kl_v2(vg_original_l2, 'VG', 'vg_original_l2', 28)

kl_v2(vg_related_500_l0, 'VG', 'vg_related_500_l0', 29)
kl_v2(vg_related_l0, 'VG', 'vg_related_l0', 30)

kl_v2(vg_short_500_l0, 'VG', 'vg_short_500_l0', 31)
kl_v2(vg_short_500_l1, 'VG', 'vg_short_500_l1', 32)
kl_v2(vg_short_l0, 'VG', 'vg_short_l0', 33)
kl_v2(vg_short_l1, 'VG', 'vg_short_l1', 34)
kl_v2(vg_short_l2, 'VG', 'vg_short_l2', 35)
