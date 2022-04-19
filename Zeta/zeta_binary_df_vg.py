import pickle
import pandas
import numpy as np

VG_FILEPATH = '../data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/vg_tropes.pkl'
VG_COUNTRIES = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_countries.pkl'
VG_MISC = '../data_new/* PRIMARY DATASETS/WORKS_VG_SUPPLEMENTARY/game_misc.pkl'


# Read dataframes
vg_df = pandas.read_pickle(VG_FILEPATH)
vg_countries_df = pandas.read_pickle(VG_COUNTRIES)
vg_times_df = pandas.read_pickle(VG_MISC).drop(['metacritic', 'number_ratings'], axis=1)
vg_times_df['release_date'] = pandas.DatetimeIndex(vg_times_df['release_date']).year
vg_times_df = vg_times_df.rename(columns={'release_date': 'start_year'})
vg_times_df = vg_times_df.dropna()

# Get a list of all titles
all_vg = vg_df['title'].unique().tolist()

# Make a binary matrix
print('Making the binary matrix....')
vg_binary = pandas.crosstab(vg_df.title, vg_df.trope)

# Make a dict of with countries as key, and list of works that year as value
# Note that a country can be part for multiple different countries
print('Getting works per country....')
df2 = vg_countries_df[vg_countries_df['title'].isin(all_vg)].groupby('country').apply(lambda x: list(x['title'].unique()))
works_per_country_sorted = dict(sorted(df2.to_dict().items(), key=lambda i: -len(i[1])))

# For countries which comprise more than 1% of the dataset
works_per_country = {}
for k, v in works_per_country_sorted.items():
    if len(v) > len(all_vg)/100:
        works_per_country[k] = v

print(works_per_country.keys())
countries_to_consider = works_per_country.keys()

countries_agg_matrix = []

for country, works in works_per_country.items():
    print('Calculating for ' + country)

    this_country = [0 for i in range(len(vg_binary.columns))]

    for title in works:
        current_row = vg_binary.loc[title].tolist()
        this_country = np.bitwise_or(current_row, this_country).tolist()

    countries_agg_matrix.append([country] + this_country)

print('Making the dataframe...')
columns = ['title']
for col in vg_binary.columns:
    columns.append(col)
zeta_df = pandas.DataFrame(countries_agg_matrix, columns=columns)
zeta_df.to_csv('vg_zeta_data_alltime.csv')

# Yearly

print('Splitting into years...')
vg_times_df = vg_times_df.drop(vg_times_df[vg_times_df.start_year < 1990].index)
works_per_year = vg_times_df.groupby('start_year').apply(lambda x: list(x['title'].unique())).to_dict()

for year, year_works in works_per_year.items():
    print('#### Calculating for ' + str(year))

    # split just these year_works into the countries above
    print('Splitting into countries...')
    works_to_consider = list(set(year_works).intersection(set(all_vg)))
    df2 = vg_countries_df[vg_countries_df['title'].isin(works_to_consider)].groupby('country').apply(lambda x: list(x['title'].unique()))
    works_per_country_sorted_temp = dict(sorted(df2.to_dict().items(), key=lambda i: -len(i[1])))
    works_per_country = {}
    for k, v in works_per_country_sorted_temp.items():
        if k in countries_to_consider:
            works_per_country[k] = v

    # make the matrix
    countries_agg_matrix = []

    for country, works in works_per_country.items():
        print('Calculating for ' + country)

        this_country = [0 for i in range(len(vg_binary.columns))]

        for title in works:
            current_row = vg_binary.loc[title].tolist()
            this_country = np.bitwise_or(current_row, this_country).tolist()

        countries_agg_matrix.append([country] + this_country)

    # make and save the matrix
    print('Making the dataframe...')
    columns = ['country']
    for col in vg_binary.columns:
        columns.append(col)
    zeta_df = pandas.DataFrame(countries_agg_matrix, columns=columns)
    filepath = 'vg_zeta_data_' + str(year) + '.csv'
    zeta_df.to_csv(filepath)
