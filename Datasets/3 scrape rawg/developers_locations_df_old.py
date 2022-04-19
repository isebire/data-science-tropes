import pandas
import pickle

# according to
# https://help.imdb.com/article/contribution/other-submission-guides/country-codes/G99K4LFRMSC37DCN#
COUNTRY_CODES_IMDB = {'Luxembourg': 'LU', 'Canada': 'CA', 'Mexico': 'MX', 'Czech Republic': 'CZ',
                      'Latvia': 'LV', 'England': 'GB', 'Jordan': 'JO', 'Lebanon': 'LB', 'Uruguay': 'UY',
                      'Wales': 'GB', 'Japan': 'JP', 'Estonia': 'EE', 'Malta': 'MT', 'Argentina': 'AR',
                      'Bulgaria': 'BG', 'Austria': 'AT', 'Syria': 'SY', 'India': 'IN', 'France': 'FR',
                      'South Korea': 'KR', 'Belarus': 'BY', 'Pakistan': 'PK', 'South Africa': 'ZA',
                      'Romania': 'RO', 'Lithuania': 'LT', 'Tunisia': 'TN', 'Netherlands': 'NL',
                      'Switzerland': 'CH', 'Liechtenstein': 'LI', 'Peru': 'PE', 'Sweden': 'SE',
                      'Nigeria': 'NG', 'Qatar': 'QA', 'Slovenia': 'SI', 'Saudi Arabia': 'SA',
                      'Thailand': 'TH', 'Vietnam': 'VN', 'Russia': 'RU', 'Brazil': 'BR', 'Greece': 'GR',
                      'Belgium': 'BE', 'United Arab Emirates': 'AE', 'Iceland': 'IS', 'Taiwan': 'TW',
                      'Scotland': 'GB', 'Ecuador': 'EC', 'Palestine': 'PS', 'Portugal': 'PT',
                      'Hungary': 'HU', 'Norway': 'NO', 'Ukraine': 'UA', 'Italy': 'IT', 'Macedonia': 'MK',
                      'Morocco': 'MA', 'Australia': 'AU', 'Ireland': 'IE', 'Bosnia and Herzegovina': 'BA',
                      'Malaysia': 'MY', 'Spain': 'ES', 'New Zealand': 'NZ', 'Finland': 'FI',
                      'Guatemala': 'GT', 'Bahrain': 'BH', 'Iran': 'IR', 'Sri Lanka': 'LK', 'Chile': 'CL',
                      'Denmark': 'DK', 'Israel': 'IL', 'Cyprus': 'CY', 'Germany': 'DE', 'Poland': 'PL',
                      'Turkey': 'TR', 'United States': 'US', 'Croatia': 'HR', 'Costa Rica': 'CR',
                      'Philippines': 'PH', 'Slovakia': 'SK', 'Serbia': 'RS', 'Kuwait': 'KW',
                      'Ghana': 'GH', 'Indonesia': 'ID', 'Colombia': 'CO', 'China': 'CN',
                      'Singapore': 'SG', 'Egypt': 'EG'}

# combine all the datasets
developer_locations = pandas.read_csv('1kaggle_locations.csv')

data_2 = pandas.read_csv('2indie-games-developers.csv')
developer_locations = developer_locations.append(data_2, ignore_index=True)

data_3 = pandas.read_csv('3video-games-developers.csv')
developer_locations = developer_locations.append(data_3, ignore_index=True)

developer_locations = developer_locations.dropna()
developer_locations = developer_locations.drop_duplicates()

# make developer format same as from rawg
developer_locations['Company'] = developer_locations['Company'].str.lower()
developer_locations['Company'] = developer_locations['Company'].str.replace(' ','')

# make country format same as imdb
developer_locations['Country'].replace(COUNTRY_CODES_IMDB, inplace=True)

developer_locations = developer_locations.drop_duplicates()

print(developer_locations.head())

# SAVE IT
developer_locations.to_pickle('dev_locations_df.pkl')

# FIND WHAT DEVS NOT included
with open('developers.txt', 'r') as f:
    rawg_developers = f.read().splitlines()

developers_with_locations = list(developer_locations['Company'])
for i in range(len(developers_with_locations)):
    developers_with_locations[i] = developers_with_locations[i].replace('-','').replace('co','').replace('ltd','')

with open('developers_w_locs.txt', 'w') as f:
    for developer in developers_with_locations:
        f.write(developer + '\n')

for i in range(len(rawg_developers)):
    if rawg_developers[i].endswith('-2'):
        rawg_developers[i] = rawg_developers[i][:-2]
    rawg_developers[i] = rawg_developers[i].replace('-','').replace('co','').replace('ltd','')

developers_included = [developer for developer in rawg_developers if developer in developers_with_locations]
developers_not_included = [developer for developer in rawg_developers if developer not in developers_with_locations]

print(len(developers_included))
print(len(developers_not_included))

print(len(developers_with_locations))

with open('rawg_data_dict_combined.pkl', 'rb') as f:
    games_data = pickle.load(f)

at_least_1_dev_loc = []
no_loc = []

print('There are ' + str(len(games_data)) + ' games with  rawg data')

games_with_devs = []
for game, data in games_data.items():
    if data['developers'] != []:
        games_with_devs.append(game)

print('There are ' + str(len(games_with_devs)) + ' games with DEVELOPER rawg data')

for game, data in games_data.items():
    at_least_1_location = False
    for developer in data['developers']:
        if developer.endswith('-2'):
            developer = developer[:-2]
        if developer.replace('-','').replace('co','').replace('ltd','') in developers_with_locations:
            at_least_1_location = True
    if at_least_1_location:
        at_least_1_dev_loc.append(game)
    else:
        no_loc.append(game)

print('Games with a location: ' + str(len(at_least_1_dev_loc)))
print('Games without location: ' + str(len(no_loc)))

print('Not included games')
print(no_loc)
