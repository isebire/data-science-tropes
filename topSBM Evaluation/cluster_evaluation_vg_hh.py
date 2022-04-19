import pickle
import pandas
from sklearn.metrics.cluster import adjusted_rand_score, rand_score
import numpy as np
import sys
import matplotlib.pyplot as plt
import os
import seaborn as sns

sns.set('talk') # alternatively, poster <- presets for font size
sns.set_style('ticks')

cluster_file = '../topsbm/RESULTS/vg_original_500topsbm_level_0_clusters.csv'

vg_long_500_l0 = '../topsbm/RESULTS/vg_longdesc_cluster_500topsbm_level_0_clusters.csv'
vg_long_500_l1 = '../topsbm/RESULTS/vg_longdesc_cluster_500topsbm_level_1_clusters.csv'
vg_long_l0 = '../topsbm/RESULTS/vg_longdesc_clustertopsbm_level_0_clusters.csv'
vg_long_l1 = '../topsbm/RESULTS/vg_longdesc_clustertopsbm_level_1_clusters.csv'
vg_long_l2 = '../topsbm/RESULTS/vg_longdesc_clustertopsbm_level_2_clusters.csv'
vg_original_500_l0 = '../topsbm/RESULTS/vg_original_500topsbm_level_0_clusters.csv'
vg_original_500_l1 = '../topsbm/RESULTS/vg_original_500topsbm_level_1_clusters.csv'
vg_original_l0 = '../topsbm/RESULTS/vg_originaltopsbm_level_0_clusters.csv'
vg_original_l1 = '../topsbm/RESULTS/vg_originaltopsbm_level_1_clusters.csv'
vg_original_l2 = '../topsbm/RESULTS/vg_originaltopsbm_level_2_clusters.csv'
vg_related_500_l0 = '../topsbm/RESULTS/vg_related_community_500topsbm_level_0_clusters.csv'
vg_related_l0 = '../topsbm/RESULTS/vg_related_communitytopsbm_level_0_clusters.csv'
vg_short_500_l0 = '../topsbm/RESULTS/vg_shortdesc_cluster_500topsbm_level_0_clusters.csv'
vg_short_500_l1 = '../topsbm/RESULTS/vg_shortdesc_cluster_500topsbm_level_1_clusters.csv'
vg_short_l0 = '../topsbm/RESULTS/vg_shortdesc_clustertopsbm_level_0_clusters.csv'
vg_short_l1 = '../topsbm/RESULTS/vg_shortdesc_clustertopsbm_level_1_clusters.csv'
vg_short_l2 = '../topsbm/RESULTS/vg_shortdesc_clustertopsbm_level_2_clusters.csv'

def analyse_clusters(cluster_file, run_name):

    filename = 'CLUSTER_ANALYSIS/' + run_name + '_cluster_analysis.txt'
    #sys.stdout = open(filename, 'w')

    df = pandas.read_csv(cluster_file)

    clusters = []

    for col in df.columns:
        current_cluster = df[col].tolist()
        current_cluster_cleaned = [x for x in current_cluster if str(x) != 'nan']
        clusters.append(current_cluster_cleaned)

    print('Number of clusters: ')
    print(len(clusters))

    clusters_with_100_genre = set()
    heatmap_data = [[] for i in range(len(vg_genres_names))]

    # Analyse each cluster
    for cluster_count, cluster in enumerate(clusters):
        print('\n#### CLUSTER ' + str(cluster_count + 1) + ' ####')
        print('Items in cluster: ' + str(len(cluster)))

        # Get the genre distribution
        cluster_genre_titles = [x for x in cluster if x in vg_with_genre]
        print('Items with predefined genre: ' + str(len(cluster_genre_titles)))

        cluster_description = ''

        genre_counts = {}

        for title in cluster_genre_titles:
            genres = vg_genres_df.loc[vg_genres_df['title'] == title]['genre'].tolist()

            for genre in genres:
                if genre in genre_counts.keys():
                    genre_counts[genre] += 1
                else:
                    genre_counts[genre] = 1

        genre_percentages = {}
        for genre, count in genre_counts.items():
            genre_percentage = (count/len(cluster_genre_titles)) * 100
            genre_percentages[genre] = genre_percentage
            if genre_percentage == 100:
                clusters_with_100_genre.add(cluster_count/100)
                cluster_description += genre + ' '
            print(genre + ' : ' + str(count) + ' (' + str(genre_percentage) + ' %)')

        for genre_number, genre in enumerate(vg_genres_names):
            if genre in genre_percentages.keys():
                heatmap_data[genre_number].append(genre_percentages[genre])
            else:
                heatmap_data[genre_number].append(0)

        cluster_description += 'shows '

        # Get the country distrubution?
        cluster_country_titles = [x for x in cluster if x in vg_with_country]
        print('Items with country: ' + str(len(cluster_country_titles)))

        country_counts = {}

        for title in cluster_country_titles:
            countries = vg_countries_df.loc[vg_countries_df['title'] == title]['country'].unique().tolist()

            for country in countries:
                if country in country_counts.keys():
                    country_counts[country] += 1
                else:
                    country_counts[country] = 1

        added_country = False

        for country, count in country_counts.items():
            country_percentage = (count/len(cluster_country_titles)) * 100
            if country_percentage == 100:
                if added_country is False:
                    cluster_description += 'from '
                    added_country = True
                cluster_description += country + ' '
            print(country + ' : ' + str(count) + ' (' + str(country_percentage) + ' %)')

        print(cluster_description)

    print('\n')
    print(str(len(clusters_with_100_genre)) + ' clusters have characterstic genre (' +
          str(len(clusters_with_100_genre)/len(clusters)*100) + '%)')

    # Make heatmap

    plt.figure(figsize=(20,20))
    cmap = plt.cm.get_cmap('magma').copy()
    plt.imshow(heatmap_data, origin='lower', aspect='auto',
               interpolation='none', cmap=cmap)
    plt.ylim(-0.5, len(vg_genres_names) - 0.5)
    plt.title('Predefined Genres in TopSBM Derived Clusters', fontsize=25)
    plt.xlabel('TopSBM Derived Clusters', fontsize=20)
    plt.ylabel('Predefined Genres', fontsize=20)
    plt.clim(0)
    plt.colorbar()
    plt.xticks(np.arange(len(clusters)), labels=[(x+1) for x in range(len(clusters))], rotation=90)
    plt.yticks(np.arange(len(vg_genres_names)), labels=[x for x in vg_genres_names])
    filename = 'CLUSTER_ANALYSIS/' + run_name + '_clusters_genres_heatmap.png'
    plt.savefig(filename)

    # Analsye wrt the sequels

    # Read in the sequels file (list of lists)
    with open('vg_sequels_list.pkl', 'rb') as f:
        sequels_list = pickle.load(f)

    # Find intersection between games in the sequels file and games in the topsbm
    # dataset
    series_titles = [title for series in sequels_list for title in series]
    titles_with_cluster = [title for cluster in clusters for title in cluster]
    titles_to_analyse = [x for x in titles_with_cluster if x in series_titles]

    sequels_filtered = []
    for series in sequels_list:
        series_filtered = []
        for title in series:
            if title in titles_to_analyse:
                series_filtered.append(title)
        if len(series_filtered) > 1:
            sequels_filtered.append(series_filtered)

    print('\n')
    print(str(len(titles_to_analyse)) + ' titles being analysed wrt series')
    print(str(len(sequels_filtered)) + ' series included')

    total = 0

    hh_indices = []
    mean_hh = 0

    for series in sequels_filtered:
        series_name = os.path.commonprefix(series)

        num_works_in_series = len(series)

        clusters_represented = {}

        # Get the topSBM cluster assignment for each item in the series
        for title in series:
            title_cluster = [i for i in range(len(clusters)) if title in clusters[i]][0]
            if title_cluster in clusters_represented.keys():
                clusters_represented[title_cluster] += 1
            else:
                clusters_represented[title_cluster] = 1

        hh_index = 0
        for cluster, num_works in clusters_represented.items():
            proportion_in_cluster = num_works / num_works_in_series
            hh_index += proportion_in_cluster ** 2

        num_clusters_represented = len(clusters_represented)

        print(str(num_works_in_series) + ' games in series out of ' +
              str(len(titles_with_cluster)) + ' titles in topSBM clusters: ' +
              '( ' + str((num_works_in_series/len(titles_with_cluster))*100) +
              '%)')
        print(str(num_clusters_represented) + ' clusters represented out of ' +
              str(len(clusters)) + ': (' +
              str((num_clusters_represented/len(clusters))*100) + '%)')

        print('!! Herfindahl-Hirschman Index: ' + str(hh_index))

        hh_indices.append({'series': series_name, 'HH_index': hh_index,
                           'works_in_series': num_works_in_series})
        mean_hh += hh_index

    mean_hh = mean_hh / len(sequels_filtered)
    print(run_name)
    input(mean_hh)

    hh_df = pandas.DataFrame(hh_indices)
    filename = 'CLUSTER_ANALYSIS/' + run_name + '_hh_index.csv'
    hh_df.to_csv(filename)



    # Plot the distribution of HH index

    plt.figure(figsize=(20,20))
    cm = plt.cm.get_cmap('magma')
    plt.hist(hh_df['HH_index'], color=cm(0.5))
    plt.xlim(0, 1)
    plt.title('Distribution of Herfindahl-Hirschman Index', fontsize=25)
    plt.xlabel('Herfindahl-Hirschman Index', fontsize=20)
    plt.ylabel('Frequency', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    filename = 'CLUSTER_ANALYSIS/' + run_name + '_hh_index_dist.png'
    plt.savefig(filename)

    # HH index vs games in series
    plt.figure(figsize=(20,20))
    plt.scatter(hh_df['works_in_series'], hh_df['HH_index'], color=cm(0.5))
    z = np.polyfit(hh_df['works_in_series'], hh_df['HH_index'], 1)
    p = np.poly1d(z)
    plt.plot(hh_df['works_in_series'], p(hh_df['works_in_series']), "r--")
    plt.title('Herfindahl-Hirschman Index and Number of Games in Series', fontsize=25)
    plt.ylabel('Herfindahl-Hirschman Index', fontsize=20)
    plt.xlabel('Number of Games in Series', fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    filename = 'CLUSTER_ANALYSIS/' + run_name + '_hh_index_num_games.png'
    plt.savefig(filename)

    # sys.stdout.close()


# Load data
vg_genres = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_genres.pkl'
vg_countries = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_countries.pkl'

vg_genres_df = pandas.read_pickle(vg_genres)
vg_with_genre = vg_genres_df['title'].unique().tolist()
vg_genres_names = vg_genres_df['genre'].unique().tolist()

vg_countries_df = pandas.read_pickle(vg_countries)
vg_with_country = vg_countries_df['title'].unique().tolist()

# Run for each clustering
analyse_clusters(vg_long_500_l0, 'vg_long_500_l0')
analyse_clusters(vg_long_500_l1, 'vg_long_500_l1')
analyse_clusters(vg_long_l0, 'vg_long_l0')
analyse_clusters(vg_long_l1, 'vg_long_l1')
analyse_clusters(vg_long_l2, 'vg_long_l2')
analyse_clusters(vg_original_500_l0, 'vg_original_500_l0')
analyse_clusters(vg_original_500_l1, 'vg_original_500_l1')
analyse_clusters(vg_original_l0, 'vg_original_l0')
analyse_clusters(vg_original_l1, 'vg_original_l1')
analyse_clusters(vg_original_l2, 'vg_original_l2')
analyse_clusters(vg_related_500_l0, 'vg_related_500_l0')
analyse_clusters(vg_related_l0, 'vg_related_l0')
analyse_clusters(vg_short_500_l0, 'vg_short_500_l0')
analyse_clusters(vg_short_500_l1, 'vg_short_500_l1')
analyse_clusters(vg_short_l0, 'vg_short_l0')
analyse_clusters(vg_short_l1, 'vg_short_l1')
analyse_clusters(vg_short_l2, 'vg_short_l2')
