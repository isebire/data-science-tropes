from scipy import stats as ss
import pickle
import pandas
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np


# Read data
yearly_topic_dist_file = 'TOPIC_DISTS/tv_original_l0_yearly_topic_dist_df.csv'
yearly_topic_dist_df_tv = pandas.read_csv(yearly_topic_dist_file, index_col=0)

number_topics = int(list(yearly_topic_dist_df_tv.columns)[-1].split('_')[1])
years = [int(x) for x in yearly_topic_dist_df_tv['year'].tolist()]

# Calculate effective number of issues for each year
number_of_years = yearly_topic_dist_df_tv.shape[0]
eni_list = []

for i in range(number_of_years):
    year_dist = yearly_topic_dist_df_tv.iloc[i].tolist()[2:]
    entropy = ss.entropy(year_dist)
    eni = 2**entropy
    eni_list.append(eni)

yearly_topic_dist_df_tv['ENI'] = eni_list

yearly_topic_dist_file = 'TOPIC_DISTS/vg_original_l0_yearly_topic_dist_df.csv'
yearly_topic_dist_df_vg = pandas.read_csv(yearly_topic_dist_file, index_col=0)

number_topics = int(list(yearly_topic_dist_df_vg.columns)[-1].split('_')[1])
years = [int(x) for x in yearly_topic_dist_df_vg['year'].tolist()]

# Calculate effective number of issues for each year
number_of_years = yearly_topic_dist_df_vg.shape[0]
eni_list = []

for i in range(number_of_years):
    year_dist = yearly_topic_dist_df_vg.iloc[i].tolist()[2:]
    entropy = ss.entropy(year_dist)
    eni = 2**entropy
    eni_list.append(eni)

yearly_topic_dist_df_vg['ENI'] = eni_list

plt.figure(figsize=(8,8))
plt.plot(yearly_topic_dist_df_tv['year'], yearly_topic_dist_df_tv['ENI'], label='TV Shows')
plt.plot(yearly_topic_dist_df_vg['year'], yearly_topic_dist_df_vg['ENI'], label='Video Games')
plt.title('Effective Number of Genres per Year')
plt.xlabel('Year')
plt.ylabel('Effective Number of Genres')
plt.legend()
plt.savefig('eni_combine_original_l0.png')


# Read data
yearly_topic_dist_file = 'TOPIC_DISTS/tv_original_l1_yearly_topic_dist_df.csv'
yearly_topic_dist_df_tv = pandas.read_csv(yearly_topic_dist_file, index_col=0)

number_topics = int(list(yearly_topic_dist_df_tv.columns)[-1].split('_')[1])
years = [int(x) for x in yearly_topic_dist_df_tv['year'].tolist()]

# Calculate effective number of issues for each year
number_of_years = yearly_topic_dist_df_tv.shape[0]
eni_list = []

for i in range(number_of_years):
    year_dist = yearly_topic_dist_df_tv.iloc[i].tolist()[2:]
    entropy = ss.entropy(year_dist)
    eni = 2**entropy
    eni_list.append(eni)

yearly_topic_dist_df_tv['ENI'] = eni_list

yearly_topic_dist_file = 'TOPIC_DISTS/vg_original_l1_yearly_topic_dist_df.csv'
yearly_topic_dist_df_vg = pandas.read_csv(yearly_topic_dist_file, index_col=0)

number_topics = int(list(yearly_topic_dist_df_vg.columns)[-1].split('_')[1])
years = [int(x) for x in yearly_topic_dist_df_vg['year'].tolist()]

# Calculate effective number of issues for each year
number_of_years = yearly_topic_dist_df_vg.shape[0]
eni_list = []

for i in range(number_of_years):
    year_dist = yearly_topic_dist_df_vg.iloc[i].tolist()[2:]
    entropy = ss.entropy(year_dist)
    eni = 2**entropy
    eni_list.append(eni)

yearly_topic_dist_df_vg['ENI'] = eni_list

plt.figure(figsize=(8,8))
plt.plot(yearly_topic_dist_df_tv['year'], yearly_topic_dist_df_tv['ENI'], label='TV Shows')
plt.plot(yearly_topic_dist_df_vg['year'], yearly_topic_dist_df_vg['ENI'], label='Video Games')
plt.title('Effective Number of Genres per Year')
plt.xlabel('Year')
plt.ylabel('Effective Number of Genres')
plt.legend()
plt.savefig('eni_combine_original_l1.png')
