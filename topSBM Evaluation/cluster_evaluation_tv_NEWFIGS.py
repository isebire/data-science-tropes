import pickle
import pandas
from sklearn.metrics.cluster import adjusted_rand_score, rand_score
import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy import stats as ss
import seaborn as sns

sns.set('talk') # alternatively, poster <- presets for font size
sns.set_style('ticks')

tv_long_l0 = '../topsbm/RESULTS/tv_longdesc_clustertopsbm_level_0_clusters.csv'
tv_long_l1 = '../topsbm/RESULTS/tv_longdesc_clustertopsbm_level_1_clusters.csv'
tv_original_l0 = '../topsbm/RESULTS/tv_originaltopsbm_level_0_clusters.csv'
tv_original_l1 = '../topsbm/RESULTS/tv_originaltopsbm_level_1_clusters.csv'
tv_short_l0 = '../topsbm/RESULTS/tv_shortdesc_clustertopsbm_level_0_clusters.csv'
tv_short_l1 = '../topsbm/RESULTS/tv_shortdesc_clustertopsbm_level_1_clusters.csv'


def analyse_clusters(cluster_file, run_name):
    print(run_name)

    filename = 'CLUSTER_ANALYSIS/' + run_name + '_cluster_analysis.txt'

    df = pandas.read_csv(cluster_file)

    clusters = []

    for col in df.columns:
        current_cluster = df[col].tolist()
        current_cluster_cleaned = [x for x in current_cluster if str(x) != 'nan']
        clusters.append(current_cluster_cleaned)

    print('Number of clusters: ')
    print(len(clusters))

    clusters_with_100_genre = set()
    heatmap_data = [[] for i in range(len(tv_genres_names))]
    eni_dict = {}
    hh_dict = {}

    # Analyse each cluster
    for cluster_count, cluster in enumerate(clusters):
        print('\n#### CLUSTER ' + str(cluster_count + 1) + ' ####')
        print('Items in cluster: ' + str(len(cluster)))

        # Get the genre distribution
        cluster_genre_titles = [x for x in cluster if x in tv_with_genre]
        print('Items with predefined genre: ' + str(len(cluster_genre_titles)))

        cluster_description = ''

        genre_counts = {}

        for title in cluster_genre_titles:
            genres = tv_genres_df.loc[tv_genres_df['title'] == title]['genre'].tolist()

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

        for genre_number, genre in enumerate(tv_genres_names):
            if genre in genre_percentages.keys():
                heatmap_data[genre_number].append(genre_percentages[genre])
            else:
                heatmap_data[genre_number].append(0)

        cluster_description += 'shows '

        # ENI
        entropy = ss.entropy(list(genre_percentages.values()))
        eni = 2**entropy
        eni_dict[cluster_count + 1] = eni

        # Get the country distrubution?
        cluster_country_titles = [x for x in cluster if x in tv_with_country]
        print('Items with country: ' + str(len(cluster_country_titles)))

        country_counts = {}

        for title in cluster_country_titles:
            countries = tv_countries_df.loc[tv_countries_df['title'] == title]['country'].unique().tolist()

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
               # ,norm=colours.LogNorm())
    plt.ylim(-0.5, len(tv_genres_names) - 0.5)
    plt.title('Predefined Genres in TopSBM Derived Clusters', fontsize=30)
    plt.xlabel('TopSBM Derived Clusters', fontsize=30)
    plt.ylabel('Predefined Genres', fontsize=30)
    plt.clim(0)
    plt.colorbar()
    plt.xticks(np.arange(len(clusters)), labels=[(x+1) for x in range(len(clusters))], fontsize=20)
    plt.yticks(np.arange(len(tv_genres_names)), labels=[x for x in tv_genres_names], fontsize=20)
    if run_name.endswith('l0'):
        ax = plt.gca()
        ax.set_xticks(ax.get_xticks()[9::10])
    filename = run_name + '_clusters_genres_heatmap.png'
    plt.savefig(filename, bbox_inches='tight')

    # Analyse wrt the imdb related tropes community detection
    with open('tv_communities_dict.pkl', 'rb') as f:
        tv_communities = pickle.load(f)

    # FORMAT FOR (A)RI
    # input(adjusted_rand_score([1,1,2,2], [2,2,4,4]))

    # Get list of titles in both
    titles_with_cluster = [title for cluster in clusters for title in cluster]
    titles_with_community = tv_communities.keys()
    titles_to_analyse = [x for x in titles_with_cluster if x in titles_with_community]
    print('\n')
    print(str(len(titles_to_analyse)) + ' titles being analysed wrt imdb communities')

    cluster_ri_format = []
    community_ri_format = []

    for title in titles_to_analyse:

        title_cluster = [i for i in range(len(clusters)) if title in clusters[i]][0]
        cluster_ri_format.append(title_cluster)

        community_ri_format.append(tv_communities[title])

    print('(A)RI Scores of how well they match: 1 best 0 low')
    print('ARI:')
    print(adjusted_rand_score(cluster_ri_format, community_ri_format))
    print('RI:')
    print(rand_score(cluster_ri_format, community_ri_format))


# Load data
tv_genres = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_genres.pkl'
tv_countries = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_countries.pkl'

tv_genres_df = pandas.read_pickle(tv_genres)
tv_with_genre = tv_genres_df['title'].unique().tolist()
tv_genres_names = tv_genres_df['genre'].unique().tolist()

tv_countries_df = pandas.read_pickle(tv_countries)
tv_with_country = tv_countries_df['title'].unique().tolist()

# Run for each clustering
analyse_clusters(tv_long_l0, 'tv_long_l0')
analyse_clusters(tv_long_l1, 'tv_long_l1')
analyse_clusters(tv_original_l0, 'tv_original_l0')
analyse_clusters(tv_original_l1, 'tv_original_l1')
analyse_clusters(tv_short_l0, 'tv_short_l0')
analyse_clusters(tv_short_l1, 'tv_short_l1')
