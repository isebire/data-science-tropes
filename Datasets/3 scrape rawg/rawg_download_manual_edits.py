# rawg

import requests
import pickle

API_KEY = '306161ea5c2542909ae10ebff329e43a'

with open('not_included_manual.txt', 'r') as f:
    search_names = f.read().splitlines()

with open('not_included_onames.txt', 'r') as f:
    original_names = f.read().splitlines()

print(len(search_names))
print(len(original_names))
print(list(zip(original_names,search_names)))

# Set up the data structures to save
results = {}
missing_data_ones = []

for i in range(len(search_names)):
    print('Downloading: ' + original_names[i])

    # Make the API request
    url = 'https://api.rawg.io/api/games/' + search_names[i] + '?key=' + API_KEY
    response = requests.get(url)

    print(response)

    # Check success
    if str(response.status_code)[0] == '2':
        response = response.json()

        current_results = {}

        try:
            current_results['metacritic'] = response['metacritic']
            current_results['release_date'] = response['released']
            current_results['number_ratings'] = response['ratings_count']
            current_results['developers'] = [developer['slug'] for developer in response['developers']]
            current_results['genres'] = [genre['slug'] for genre in response['genres']]

            results[original_names[i]] = current_results

        except:
            print('missing data')
            missing_data_ones.append(original_names[i])
            continue

# Saving the files each iteration

print(results)
print(missing_data_ones)

filename = 'rawg_data_dict_manual_ones.pkl'
with open(filename, 'wb') as f:
    pickle.dump(results, f)
