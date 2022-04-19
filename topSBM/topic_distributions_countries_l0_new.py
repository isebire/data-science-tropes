# CSV distributions of topics per year for further analysis

import pickle
import pandas
from scipy import stats as ss
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set('talk') # alternatively, poster <- presets for font size
sns.set_style('ticks')

# Filepaths for all the data files - run for all sims and levels.
VG_COUNTRIES = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_countries.pkl'
TV_COUNTRIES = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_countries.pkl'

# Document topic distribution files
tv_original_l0 = 'RESULTS/tv_originaltopsbm_level_0_topic-dist.csv'
vg_original_l0 = 'RESULTS/vg_originaltopsbm_level_0_topic-dist.csv'

def yearly_topic_dists(document_topic_dists_file, tv_or_vg, run_name, run_number):
    print(str(run_number) + '/35: Analysing: ' + run_name)

    # Read the topic distributions from topSBM into dataframe and format
    df = pandas.read_csv(document_topic_dists_file).drop(['i_doc'], axis=1)
    df = df.rename(columns={'doc': 'title'})
    titles_with_topics = df['title'].unique().tolist()
    df = df.set_index('title')
    number_topics = int(list(df.columns)[-1].split(' ')[1])

    # Load the country dataframes
    if tv_or_vg == 'VG':
        countries_df = pandas.read_pickle(VG_COUNTRIES)
    elif tv_or_vg == 'TV':
        countries_df = pandas.read_pickle(TV_COUNTRIES)

    # Make a dict of with countries as key, and list of works that year as value
    # Note that a country can be part for multiple different countries

    df2 = countries_df[countries_df['title'].isin(titles_with_topics)].groupby('country').apply(lambda x: list(x['title'].unique()))
    works_per_country_sorted = dict(sorted(df2.to_dict().items(), key=lambda i: -len(i[1])))

    # For countries which comprise more than 1% of the dataset
    works_per_country = {}
    for k, v in works_per_country_sorted.items():
        if len(v) > len(titles_with_topics)/100:
            works_per_country[k] = v

    # For each year, sum the weights of each topic for each work and record the
    # total number of works for that year
    list_for_df = []

    for country in works_per_country.keys():
        # Get the works for this year
        current_country_works = works_per_country[country]

        # Initialise the data dictionary
        number_works_country_w_topics = len(current_country_works)
        this_country_data = {'country': country, 'total_works': number_works_country_w_topics}
        for topic_number in range(1, number_topics + 1):
            key = 'topic_' + str(topic_number)
            this_country_data[key] = 0

        # Get the topic weights for each game
        for title in current_country_works:

            topic_weights = df.loc[title].tolist()

            for topic_number, topic_weight in enumerate(topic_weights):
                key = 'topic_' + str(topic_number + 1)
                this_country_data[key] += topic_weight

        # Save the data for this year
        list_for_df.append(this_country_data)

    # Make the data for all years into a dataframe
    country_topic_weights_df = pandas.DataFrame(list_for_df)

    heatmap_data = []

    # For each year, divide by total number of works column for distribution
    for topic_number in range(1, number_topics + 1):
        key = 'topic_' + str(topic_number)
        country_topic_weights_df[key] = country_topic_weights_df[key] / country_topic_weights_df['total_works']
        heatmap_data.append(country_topic_weights_df[key].to_list())

    # Heatmap
    plt.figure(figsize=(20,20))
    cmap = plt.cm.get_cmap('gist_rainbow').copy()
    cmap.set_over(color='#ffccf2')
    plt.imshow(heatmap_data, origin='lower', aspect='auto',
               interpolation='none', cmap=cmap)
    plt.ylim(-0.5, number_topics - 0.5)
    plt.title('Topic distribution per country', fontsize=30)
    plt.xlabel('Country', fontsize=30)
    plt.ylabel('Topics', fontsize=30)
    plt.clim(0, 0.15)
    plt.colorbar()
    plt.xticks(np.arange(len(works_per_country.keys())),
               labels=[x + '\n (' + str(len(works_per_country[x])) + ')' for x in
               works_per_country.keys()], fontsize=20)
    plt.yticks(np.arange(number_topics), labels=[i for i in range(1, number_topics + 1)])
    #plt.yticks([], [])   # for no y ticks
    ax = plt.gca()
    ax.set_yticks(ax.get_yticks()[9::10])
    filename = run_name + '_topics_countries_heatmap_2.png'
    plt.savefig(filename, bbox_inches='tight')


yearly_topic_dists(tv_original_l0, 'TV', 'tv_original_l0', 9)
yearly_topic_dists(vg_original_l0, 'VG', 'vg_original_l0', 26)
