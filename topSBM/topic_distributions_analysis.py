from scipy import stats as ss
import pickle
import pandas
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np


def analyse_yearly_topic_dists(run_name):
    print('Running for: ' + run_name)

    # Read data
    yearly_topic_dist_file = 'TOPIC_DISTS/' + run_name + '_yearly_topic_dist_df.csv'
    yearly_topic_dist_df = pandas.read_csv(yearly_topic_dist_file, index_col=0)

    number_topics = int(list(yearly_topic_dist_df.columns)[-1].split('_')[1])
    years = [int(x) for x in yearly_topic_dist_df['year'].tolist()]

    # Plot the frequency of each topic (genre) per year as line chart
    ax = yearly_topic_dist_df.drop(['total_works'], axis=1).plot(x='year', ylabel='Frequency of topic', xlabel='Year', title='Frequency of topSBM derived topics per year', figsize=(8, 8))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
    ax.legend(ncol=2, loc='center left', bbox_to_anchor=(1.0, 0.5))
    ax.plot()
    filename = 'TOPIC_DIST_ANALYSIS/' + run_name + '_topics_line.png'
    ax.figure.savefig(filename)

    # Plot the frequency of each topic (genre) per year as heatmap
    # Including dealing with the missing years

    heatmap_data = [[] for i in range(number_topics)]

    for year in range(min(years), max(years) + 1):
        if year in years:
            year_dist = yearly_topic_dist_df.loc[yearly_topic_dist_df['year'] == year].iloc[0].tolist()[2:]
        else:
            # missing year
            year_dist = [-1 for i in range(number_topics)]
        for i in range(number_topics):
            heatmap_data[i].append(year_dist[i])

    plt.figure(figsize=(20,20))
    cmap = plt.cm.get_cmap('gist_rainbow').copy()
    cmap.set_under(color='white')
    plt.imshow(heatmap_data, origin='lower', aspect='auto',
               interpolation='none', cmap=cmap)
               # ,norm=colours.LogNorm())
    plt.ylim(-0.5, number_topics - 0.5)
    plt.title('Topic distribution per year', fontsize=25)
    plt.xlabel('Year', fontsize=20)
    plt.ylabel('Topics', fontsize=20)
    plt.clim(0, 1)
    plt.colorbar()
    plt.xticks(np.arange(len(range(min(years), max(years) + 1))), labels=[x for x in range(min(years), max(years) + 1)], rotation=90)
    plt.yticks(np.arange(number_topics), labels=[i for i in range(1, number_topics + 1)])
    filename = 'TOPIC_DIST_ANALYSIS/' + run_name + '_topics_heatmap.png'
    plt.savefig(filename)

    # Calculate effective number of issues for each year
    number_of_years = yearly_topic_dist_df.shape[0]
    eni_list = []

    for i in range(number_of_years):
        year_dist = yearly_topic_dist_df.iloc[i].tolist()[2:]
        entropy = ss.entropy(year_dist)
        eni = 2**entropy
        eni_list.append(eni)

    yearly_topic_dist_df['ENI'] = eni_list

    fig = yearly_topic_dist_df.plot(colormap='spring', x='year', y='ENI', ylabel='Effective Number of Genres', xlabel='Year', title='Effective number of genres per year', figsize=(8, 8)).get_figure()
    filename = 'TOPIC_DIST_ANALYSIS/' + run_name + '_ENI.png'
    fig.savefig(filename)

    # Calculate KL divergence

    # replace 0 values with small value to stop KL values of infinity
    for j in range(1, number_topics + 1):
        column_name = 'topic_' + str(j)
        yearly_topic_dist_df[column_name] = yearly_topic_dist_df[column_name].replace(0, 10**(-9))

    missing_years = [x for x in range(min(years), max(years)) if x not in years]
    KL_over_multiple_years = [(x+1) for x in missing_years if (x+1) in years]

    kl_list = []
    # get just the topic dist
    prev_year_dist = yearly_topic_dist_df.iloc[0].tolist()[2:(number_topics+2)]
    first_entry = 0  # placeholder: will drop later
    kl_list.append(first_entry)

    for j in range(1, number_of_years):
        this_year_dist = yearly_topic_dist_df.iloc[j].tolist()[2:(number_topics+2)]
        # Checks that the data retrieved is the probability distribution
        # for the topics
        assert(abs(1-sum(this_year_dist)) < 0.001)
        kl_divergence = ss.entropy(this_year_dist, prev_year_dist)
        kl_list.append(kl_divergence)
        prev_year_dist = this_year_dist

    yearly_topic_dist_df['KL'] = kl_list

    yearly_topic_dist_df = yearly_topic_dist_df.drop([0])
    filepath = 'TOPIC_DIST_ANALYSIS/' + run_name + '.csv'
    yearly_topic_dist_df.to_csv(filepath)

    fig = yearly_topic_dist_df.plot(colormap='spring', x='year', y='KL', ylabel='Novelty (KL divergence)', xlabel='Year', title='Year to year novelty', figsize=(8, 8)).get_figure()
    filename = 'TOPIC_DIST_ANALYSIS/' + run_name + '_KL.png'
    fig.savefig(filename)

    # Plot again with breaks in the time series if KL was calculated over
    # more than 1 year

    kl_gaps_plot = []
    index_counter = 1
    for year in range(min(years) + 1, max(years) + 1):
        if year in years:
            # have KL data for this year
            if year in KL_over_multiple_years:
                kl_gaps_plot.append(None)
            else:
                kl_gaps_plot.append(kl_list[index_counter])
            index_counter += 1
        else:
            kl_gaps_plot.append(None)

    years_to_plot = [year for year in range(min(years) + 1, max(years) + 1)]
    fig = plt.figure(figsize=(12, 10), dpi=80)
    ax1 = fig.add_subplot(111)
    lines = ax1.plot(years_to_plot, kl_gaps_plot)
    plt.xlabel('Year', fontsize=13)
    plt.ylabel('Novelty (KL divergence)', fontsize=13)
    plt.title('Novelty compared to previous year', fontsize=15)
    filename = 'TOPIC_DIST_ANALYSIS/' + run_name + '_KL_w_gaps.png'
    fig.savefig(filename)

    # The all time topic dists
    all_time_topic_dist_file = 'TOPIC_DISTS/' + run_name + '_all_time_topic_dist_dict.pkl'
    with open(all_time_topic_dist_file, 'rb') as f:
        all_time_topic_dist = pickle.load(f)

    topic_labels = [str(i) for i in range(1, number_topics + 1)]
    values = list(all_time_topic_dist.values())[1:]

    plt.figure(figsize=(8,8))
    plt.bar(topic_labels, values, color='#6b03fc', width=0.3)
    plt.title('All time topic distribution', fontsize=13)
    plt.xlabel('Topic', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    filename = 'TOPIC_DIST_ANALYSIS/' + run_name + '_all_time.png'
    plt.savefig(filename)


analyse_yearly_topic_dists('tv_long_500_l0')
analyse_yearly_topic_dists('tv_long_500_l1')
analyse_yearly_topic_dists('tv_long_l0')
analyse_yearly_topic_dists('tv_long_l1')
analyse_yearly_topic_dists('tv_long_l2')
analyse_yearly_topic_dists('tv_original_500_l0')
analyse_yearly_topic_dists('tv_original_500_l1')
analyse_yearly_topic_dists('tv_original_500_l2')
analyse_yearly_topic_dists('tv_original_l0')
analyse_yearly_topic_dists('tv_original_l1')
analyse_yearly_topic_dists('tv_original_l2')
analyse_yearly_topic_dists('tv_related_500_l0')
analyse_yearly_topic_dists('tv_related_l0')
analyse_yearly_topic_dists('tv_short_500_l0')
analyse_yearly_topic_dists('tv_short_500_l1')
analyse_yearly_topic_dists('tv_short_l0')
analyse_yearly_topic_dists('tv_short_l1')
analyse_yearly_topic_dists('tv_short_l2')

analyse_yearly_topic_dists('vg_long_500_l0')
analyse_yearly_topic_dists('vg_long_500_l1')
analyse_yearly_topic_dists('vg_long_l0')
analyse_yearly_topic_dists('vg_long_l1')
analyse_yearly_topic_dists('vg_long_l2')
analyse_yearly_topic_dists('vg_original_500_l0')
analyse_yearly_topic_dists('vg_original_500_l1')
analyse_yearly_topic_dists('vg_original_l0')
analyse_yearly_topic_dists('vg_original_l1')
analyse_yearly_topic_dists('vg_original_l2')
analyse_yearly_topic_dists('vg_related_500_l0')
analyse_yearly_topic_dists('vg_related_l0')
analyse_yearly_topic_dists('vg_short_500_l0')
analyse_yearly_topic_dists('vg_short_500_l1')
analyse_yearly_topic_dists('vg_short_l0')
analyse_yearly_topic_dists('vg_short_l1')
analyse_yearly_topic_dists('vg_short_l2')
