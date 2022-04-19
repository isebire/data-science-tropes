import pickle
import pandas
import numpy as np

TV_FILEPATH = '../data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/tv_tropes.pkl'
TV_COUNTRIES = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_countries.pkl'
TV_MISC = '../data_new/* PRIMARY DATASETS/WORKS_TV_SUPPLEMENTARY/tv_misc.pkl'

# Read dataframes
tv_df = pandas.read_pickle(TV_FILEPATH)
tv_countries_df = pandas.read_pickle(TV_COUNTRIES)
tv_times_df = pandas.read_pickle(TV_MISC).drop(['imdb_title', 'number_episodes', 'end_year', 'rating', 'rating_count'], axis=1)
tv_times_df = tv_times_df.dropna()

# Get a list of all titles
all_tv = tv_df['title'].unique().tolist()

# Make a binary matrix
print('Making the binary matrix....')
tv_binary = pandas.crosstab(tv_df.title, tv_df.trope)

# Make a dict of with countries as key, and list of works that year as value
# Note that a country can be part for multiple different countries
print('Getting works per country....')
df2 = tv_countries_df[tv_countries_df['title'].isin(all_tv)].groupby('country').apply(lambda x: list(x['title'].unique()))
works_per_country_sorted = dict(sorted(df2.to_dict().items(), key=lambda i: -len(i[1])))

# For countries which comprise more than 1% of the dataset
works_per_country = {}
for k, v in works_per_country_sorted.items():
    if len(v) > len(all_tv)/100:
        works_per_country[k] = v

print(works_per_country.keys())
countries_to_consider = works_per_country.keys()

countries_agg_matrix = []

for country, works in works_per_country.items():
    print('Calculating for ' + country)

    this_country = [0 for i in range(len(tv_binary.columns))]

    for title in works:
        current_row = tv_binary.loc[title].tolist()
        this_country = np.bitwise_or(current_row, this_country).tolist()

    countries_agg_matrix.append([country] + this_country)

print('Making the dataframe...')
columns = ['title']
for col in tv_binary.columns:
    columns.append(col)
zeta_df = pandas.DataFrame(countries_agg_matrix, columns=columns)
zeta_df.to_csv('zeta_data_alltime.csv')

# Yearly

print('Splitting into years...')
tv_times_df = tv_times_df.drop(tv_times_df[tv_times_df.start_year < 1980].index)
works_per_year = tv_times_df.groupby('start_year').apply(lambda x: list(x['title'].unique())).to_dict()

for year, year_works in works_per_year.items():
    print('#### Calculating for ' + str(year))

    # split just these year_works into the countries above
    print('Splitting into countries...')
    works_to_consider = list(set(year_works).intersection(set(all_tv)))
    df2 = tv_countries_df[tv_countries_df['title'].isin(works_to_consider)].groupby('country').apply(lambda x: list(x['title'].unique()))
    works_per_country_sorted_temp = dict(sorted(df2.to_dict().items(), key=lambda i: -len(i[1])))
    works_per_country = {}
    for k, v in works_per_country_sorted_temp.items():
        if k in countries_to_consider:
            works_per_country[k] = v

    # make the matrix
    countries_agg_matrix = []

    for country, works in works_per_country.items():
        print('Calculating for ' + country)

        this_country = [0 for i in range(len(tv_binary.columns))]

        for title in works:
            current_row = tv_binary.loc[title].tolist()
            this_country = np.bitwise_or(current_row, this_country).tolist()

        countries_agg_matrix.append([country] + this_country)

    # make and save the matrix
    print('Making the dataframe...')
    columns = ['country']
    for col in tv_binary.columns:
        columns.append(col)
    zeta_df = pandas.DataFrame(countries_agg_matrix, columns=columns)
    filepath = 'zeta_data_' + str(year) + '.csv'
    zeta_df.to_csv(filepath)
