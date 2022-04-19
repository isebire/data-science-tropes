from scipy import stats as ss
import pickle
import pandas
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np
import seaborn as sns

sns.set('talk') # alternatively, poster <- presets for font size
sns.set_style('ticks')

def analyse_yearly_topic_dists(run_name):
    print('Running for: ' + run_name)

    # Read data
    yearly_topic_dist_file = 'TOPIC_DISTS/' + run_name + '_yearly_topic_dist_df.csv'
    yearly_topic_dist_df = pandas.read_csv(yearly_topic_dist_file, index_col=0)

    number_topics = int(list(yearly_topic_dist_df.columns)[-1].split('_')[1])
    years = [int(x) for x in yearly_topic_dist_df['year'].tolist()]

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
    cmap.set_over(color='#ffccf2') ##56fc03
    plt.imshow(heatmap_data, origin='lower', aspect='auto',
               interpolation='none', cmap=cmap)
               # ,norm=colours.LogNorm())
    plt.ylim(-0.5, number_topics - 0.5)
    plt.title('Topic distribution per year', fontsize=30)
    plt.xlabel('Year', fontsize=30)
    plt.ylabel('Topics', fontsize=30)
    plt.clim(0, 0.2)
    plt.colorbar()
    plt.xticks(np.arange(len(range(min(years), max(years) + 1))), labels=[x for x in range(min(years), max(years) + 1)])
    ax = plt.gca()
    ax.set_xticks(ax.get_xticks()[::10])
    if run_name == 'tv_original_l1':
        labels = ['1: Crime', '2: Romance', '3: General devices', '4: Sitcom', '5: N/A',
                  '6: Storytelling devices', '7: Scifi, superpowers', '8: Anime and animation',
                  '9: Anime', '10: Action and intrigue', '11: Exaggerated supernatural',
                  '12: Dark themes', '13: Temporal and geographical', '14: Adaptions and spinoffs',
                  '15: Protagonists and antagonists', '16: Comedy', '17: Character archetypes',
                  '18: Reality TV and gameshows', '19: Western animation', '20: Historical fantasy']
    elif run_name == 'vg_original_l1':
        labels = ['1: Traditional themed level design', '2: Exaggerated fantasy, temporal',
                  '3: Gameplay features', '4: Gameplay and narrative features',
                  '5: N/A', '6: Gameplay features', '7: Impactful narrative',
                  '8: Dark action, shooting, post-apocalyptic', '9: Platform games',
                  '10: Romance', '11: Medieval fantasy', '12: Real life or history inspired',
                  '13: Horror', '14: Traditional RPGs', '15: Classic exploration',
                  '16: Character archetypes', '17: Science fiction']
    else:
        labels = [i for i in range(1, number_topics + 1)]
    plt.yticks(np.arange(number_topics), labels=labels, fontsize=20)
    filename = run_name + '_topics_heatmap_label.png'
    plt.savefig(filename, bbox_inches='tight')



analyse_yearly_topic_dists('tv_original_l1')
analyse_yearly_topic_dists('vg_original_l1')
