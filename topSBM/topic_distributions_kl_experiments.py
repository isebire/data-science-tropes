from scipy import stats as ss
import pickle
import pandas
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

vg_short_500_l0 = 'TOPIC_DISTS/vg_short_500_l0_yearly_topic_dist_df.csv'


def kl_experiments(yearly_topic_dist_file, run_name):
    print('Running for: ' + run_name)

    # Read data
    yearly_topic_dist_df = pandas.read_csv(yearly_topic_dist_file, index_col=0)

    number_topics = int(list(yearly_topic_dist_df.columns)[-1].split('_')[1])
    years = [int(x) for x in yearly_topic_dist_df['year'].tolist()]
    number_of_years = yearly_topic_dist_df.shape[0]


    # replace 0 values with small value to stop KL values of infinity
    small_values = [0, 10**(-3), 10**(-4), 10**(-5), 10**(-6), 10**(-7),
                    10**(-8), 10**(-9), 10**(-10)]

    for i, small_value in enumerate(small_values):

        experiement_df = yearly_topic_dist_df.copy()

        for j in range(1, number_topics + 1):
            column_name = 'topic_' + str(j)
            experiement_df[column_name] = experiement_df[column_name].replace(0, small_value)

        missing_years = [x for x in range(min(years), max(years)) if x not in years]
        KL_over_multiple_years = [(x+1) for x in missing_years if (x+1) in years]

        kl_list = []
        # get just the topic dist
        prev_year_dist = experiement_df.iloc[0].tolist()[2:(number_topics+2)]
        first_entry = 0  # placeholder: will drop later
        kl_list.append(first_entry)

        kl_gaps_plot = []

        for j in range(1, number_of_years):
            this_year_dist = experiement_df.iloc[j].tolist()[2:(number_topics+2)]
            # Checks that the data retrieved is the probability distribution
            # for the topics
            assert(abs(1-sum(this_year_dist)) < 0.001)
            kl_divergence = ss.entropy(this_year_dist, prev_year_dist)
            kl_list.append(kl_divergence)
            year = experiement_df.iloc[j].tolist()[0]
            if year in missing_years or year in KL_over_multiple_years:
                kl_gaps_plot.append(None)
            else:
                kl_gaps_plot.append(kl_divergence)
            prev_year_dist = this_year_dist

        col = 'KL_' + str(i)
        yearly_topic_dist_df[col] = kl_list

    yearly_topic_dist_df = yearly_topic_dist_df.drop([0])
    print(yearly_topic_dist_df)
    yearly_topic_dist_df.to_csv('kl_test.csv')


kl_experiments(vg_short_500_l0, 'vg_short_500_l0')
