# rawg
import requests
import pickle

API_KEY = '306161ea5c2542909ae10ebff329e43a'

for i in range(18):

    # Read the file
    filename = 'game_name_chunk_' + str(i) + '.pkl'

    print('Reading: ' + filename)

    with open(filename, 'rb') as f:
        games_titles = pickle.load(f)

    # Set up the data structures to save
    results = {}

    for title in games_titles:
        print('Downloading: ' + title)

        # Make the API request
        url = 'https://api.rawg.io/api/games/' + title + '?key=' + API_KEY
        response = requests.get(url)

        print(response)

        # Check success
        if str(response.status_code)[0] == '2':
            response = response.json()
            # Some games may be redirected to the right page
            if response['slug'] != title:
                new_title = response['slug']
                if new_title == 'google-play':
                    continue
                print('Redirected to: ' + new_title)
                url = 'https://api.rawg.io/api/games/' + new_title + '?key=' + API_KEY
                response = requests.get(url)
                if str(response.status_code)[0] == '2':
                    response = response.json()
                else:
                    continue

            current_results = {}

            current_results['metacritic'] = response['metacritic']
            current_results['release_date'] = response['released']
            current_results['number_ratings'] = response['ratings_count']
            current_results['developers'] = [developer['slug'] for developer in response['developers']]
            current_results['genres'] = [genre['slug'] for genre in response['genres']]

            results[title] = current_results

    # Saving the files each iteration

    print(results)

    filename = 'rawg_data_dict_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(results, f)
