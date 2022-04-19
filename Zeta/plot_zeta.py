from scipy import stats as ss
import pickle
import pandas
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

# VG

# Plot yearly zeta on one graph with line colour varying
vg_years = [x for x in range(1990, 2022)]

n = len(vg_years)
colors = plt.cm.plasma(np.linspace(0,1,n))
plt.figure(figsize=(8,8))

for i, year in enumerate(vg_years):

    filename = '../../../ZETA_RESULTS/vg_zeta_' + str(year) + '.csv'
    year_df = pandas.read_csv(filename)

    plt.plot(year_df['order'], year_df['value'], color=colors[i], label=str(year))

sm = plt.cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=vg_years[0], vmax=vg_years[-1]))
plt.colorbar(sm)
plt.title('Yearly Zeta Diversity')
plt.xlabel('Order')
plt.ylabel('Zeta diversity')
plt.savefig('../../../ZETA_RESULTS/vg_zeta_fig.png')

# Plot all time zeta with standard deviation (like KL)

at_df = pandas.read_csv('../../../ZETA_RESULTS/vg_alltime_zeta.csv')
plt.figure(figsize=(8,8))
plt.plot(at_df['order'], at_df['value'])
y_low_error = [at_df['value'][i] - at_df['sd'][i] for i in range(len(at_df['order']))]
y_high_error = [at_df['value'][i] + at_df['sd'][i] for i in range(len(at_df['order']))]
plt.fill_between(at_df['order'], y_low_error, y_high_error, color='#bdfffd')
plt.title('All time Zeta diversity')
plt.xlabel('Order')
plt.ylabel('Zeta diversity')
plt.savefig('../../../ZETA_RESULTS/vg_alltime_fig.png')

# TV

# Plot yearly zeta on one graph with line colour varying
tv_years = [x for x in range(1980, 2022)]

n = len(tv_years)
colors = plt.cm.plasma(np.linspace(0,1,n))
plt.figure(figsize=(8,8))

for i, year in enumerate(tv_years):

    filename = '../../../ZETA_RESULTS/tv_zeta_' + str(year) + '.csv'
    year_df = pandas.read_csv(filename)

    plt.plot(year_df['order'], year_df['value'], color=colors[i], label=str(year))

sm = plt.cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=vg_years[0], vmax=vg_years[-1]))
plt.colorbar(sm)
plt.title('Yearly Zeta Diversity')
plt.xlabel('Order')
plt.ylabel('Zeta diversity')
plt.savefig('../../../ZETA_RESULTS/tv_zeta_fig.png')

# Plot all time zeta with standard deviation (like KL)

at_df = pandas.read_csv('../../../ZETA_RESULTS/tv_alltime_zeta.csv')
plt.figure(figsize=(8,8))
plt.plot(at_df['order'], at_df['value'])
y_low_error = [at_df['value'][i] - at_df['sd'][i] for i in range(len(at_df['order']))]
y_high_error = [at_df['value'][i] + at_df['sd'][i] for i in range(len(at_df['order']))]
plt.fill_between(at_df['order'], y_low_error, y_high_error, color='#bdfffd')
plt.title('All time Zeta diversity')
plt.xlabel('Order')
plt.ylabel('Zeta diversity')
plt.savefig('../../../ZETA_RESULTS/tv_alltime_fig.png')
