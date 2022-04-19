from scipy import stats as ss
import pickle
import pandas
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

# VG

# Normalised by the number of tropes in the year
# Plot yearly zeta on one graph with line colour varying
vg_years = [x for x in range(1990, 2022)]

tropes_per_year = {}
for year in vg_years:
    print(year)
    filename = 'matrices/vg_zeta_data_' + str(year) + '.0.csv'
    year_mat_df = pandas.read_csv(filename).drop(['country'], axis=1)

    tropes = year_mat_df.iloc[0].tolist()
    for i in year_mat_df.index.tolist()[1:]:
        tropes = np.bitwise_or(tropes, year_mat_df.iloc[i].tolist()).tolist()

    tropes_per_year[year] = tropes.count(1)

'''
# Alt: drop 0 columns
for year in vg_years:
    print(year)
    filename = 'matrices/vg_zeta_data_' + str(year) + '.0.csv'
    year_mat_df = pandas.read_csv(filename).drop(['country'], axis=1)
    year_mat_df = year_mat_df.loc[:, (year_mat_df != 0).any(axis=0)]
    print(year_mat_df.shape[1])
'''


n = len(vg_years)
colors = plt.cm.plasma(np.linspace(0,1,n))
plt.figure(figsize=(8,8))

for i, year in enumerate(vg_years):

    filename = '../../../ZETA_RESULTS/vg_zeta_' + str(year) + '.csv'
    year_df = pandas.read_csv(filename)

    plt.plot(year_df['order'], [x / tropes_per_year[year] for x in year_df['value']], color=colors[i], label=str(year))

sm = plt.cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=vg_years[0], vmax=vg_years[-1]))
plt.colorbar(sm)
plt.title('Yearly Zeta Diversity')
plt.xlabel('Order')
plt.ylabel('Zeta diversity as proportion of yearly tropes')
plt.savefig('../../../ZETA_RESULTS/vg_zeta_fig_norm.png')

# TV

tv_years = [x for x in range(1980, 2022)]

tropes_per_year = {}
for year in tv_years:
    print(year)
    filename = 'matrices/zeta_data_' + str(year) + '.0.csv'
    year_mat_df = pandas.read_csv(filename).drop(['country'], axis=1)

    tropes = year_mat_df.iloc[0].tolist()
    for i in year_mat_df.index.tolist()[1:]:
        tropes = np.bitwise_or(tropes, year_mat_df.iloc[i].tolist()).tolist()

    tropes_per_year[year] = tropes.count(1)

n = len(tv_years)
colors = plt.cm.plasma(np.linspace(0,1,n))
plt.figure(figsize=(8,8))

for i, year in enumerate(tv_years):

    filename = '../../../ZETA_RESULTS/tv_zeta_' + str(year) + '.csv'
    year_df = pandas.read_csv(filename)

    plt.plot(year_df['order'], [x / tropes_per_year[year] for x in year_df['value']], color=colors[i], label=str(year))

sm = plt.cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=vg_years[0], vmax=vg_years[-1]))
plt.colorbar(sm)
plt.title('Yearly Zeta Diversity')
plt.xlabel('Order')
plt.ylabel('Zeta diversity as proportion of yearly tropes')
plt.savefig('../../../ZETA_RESULTS/tv_zeta_fig_norm.png')
