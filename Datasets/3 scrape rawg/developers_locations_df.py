import pandas
import pickle
from fuzzywuzzy import fuzz
import inflection

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
                      'Singapore': 'SG', 'Egypt': 'EG', 'United Kingdom (England)': 'GB',
                      'United Kingdom': 'GB'}

locations_blacklist = ['Europe']

fuzzy_blacklist = ['neon', 'hand', 'pixelpigames', 'easygame', 'goods',
                       'andrew', 'nana', 'blam', 'amaranthgames', 'chime',
                       'ocean', 'goo', 'deck', 'pixelneststudio',
                       'pixeltrickery', 'small', 'amazumedia', 'sen',
                       'pixelpainterscorporation', 'smile', 'unknown',
                       'kingofthejungle', 'sol']


def match_developers(rawg_developer, developers_with_locations):
    rawg_developer = rawg_developer.replace('-', '')

    # Match with decreasing level of granularity
    if rawg_developer in developers_with_locations:
        location_developer = rawg_developer

    else:
        best_match_name = ''
        best_match_distance = 0

        for developer in developers_with_locations:
            fuzzy_distance = fuzz.partial_ratio(rawg_developer, developer)
            if fuzzy_distance > best_match_distance:
                best_match_distance = fuzzy_distance
                best_match_name = developer
            elif fuzzy_distance == 100 and (
             fuzz.ratio(rawg_developer, developer) >
             fuzz.ratio(rawg_developer, best_match_name)):
                best_match_name = developer

        if best_match_distance == 100 and (
         rawg_developer.startswith(best_match_name) or
         best_match_name.startswith(rawg_developer)) and (rawg_developer not
                                                          in fuzzy_blacklist):
            location_developer = best_match_name
            print('Fuzzy match: ' + rawg_developer + ' and ' + location_developer)
        else:
            location_developer = ''

    return location_developer


# 1: combine all the datasets and save
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
developer_locations['Company'] = developer_locations['Company'].str.replace('-','')

# make country format same as imdb
developer_locations['Country'].replace(COUNTRY_CODES_IMDB, inplace=True)

developer_locations = developer_locations.drop_duplicates()

print(developer_locations.head())
print(developer_locations.shape)

# SAVE IT
developer_locations.to_pickle('dev_locations_df.pkl')

# 2. FIND WHAT DEVS NOT included and match developers
with open('developers.txt', 'r') as f:
    rawg_developers = f.read().splitlines()

developers_with_locations = list(developer_locations['Company'])

for i in range(len(developers_with_locations)):
    developers_with_locations[i] = developers_with_locations[i].replace('-','')

with open('developers_w_locs.txt', 'w') as f:
    for developer in developers_with_locations:
        f.write(developer + '\n')

matched_developers = {}
for developer in rawg_developers:
    location_dev = match_developers(developer, developers_with_locations)
    if location_dev != '':
        matched_developers[developer] = location_dev

developers_included = len(matched_developers.items())
print('Number of rawg developers:')
print(len(rawg_developers))
developers_not_included = len(rawg_developers) - developers_included

print('Have data for xx of these: ')
print(developers_included)
print('Dont have data for xx of these: ')
print(developers_not_included)

print('have location data for xxx devs in total')
print(len(developers_with_locations))

# 3. find how many games have an associated country

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
        if developer in matched_developers.keys():
            at_least_1_location = True
    if at_least_1_location:
        at_least_1_dev_loc.append(game)
    else:
        no_loc.append(game)

print('Games with a location: ' + str(len(at_least_1_dev_loc)))
print('Games without location: ' + str(len(no_loc)))

# 4. construct the dataframe for game countries data

# for loc
developer_locations = developer_locations.set_index('Company')

with open('game_original_names_dict.pkl', 'rb') as f:
    original_names = pickle.load(f)

location_data_fordf = []
for game, data in games_data.items():
    game_camel = original_names[game]
    for developer in data['developers']:
        if developer in matched_developers.keys():
            query_developer = matched_developers[developer]
            dev_country = developer_locations.loc[query_developer, 'Country']
            if type(dev_country) == pandas.core.series.Series:
                # the developer has multiple countries
                dev_countries_list = dev_country.tolist()
                for country in dev_countries_list:
                    if country not in locations_blacklist:
                        location_data_fordf.append({'title': game_camel,
                                                    'developer': developer,
                                                    'country': country})
            else:
                if dev_country not in locations_blacklist:
                    location_data_fordf.append({'title': game_camel,
                                                'developer': developer,
                                                'country': dev_country})

print(location_data_fordf)
game_countries = pandas.DataFrame(location_data_fordf)
pandas.set_option('display.max_rows', 100)
print(game_countries.head(n=30))
game_countries.to_pickle('game_countries_df.pkl')
