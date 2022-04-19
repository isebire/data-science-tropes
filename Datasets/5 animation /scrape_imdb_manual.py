# Scrape IMDB

from imdbpie import Imdb
import pickle

imdb = Imdb()

# Set up the data structures to save
chunk_results = {}
title_matches = {}

with open('replace_wa.txt', 'r') as f:
    replace_list = f.read().splitlines()

ADD_IMDB = {}
for item in replace_list:
    temp = item.split(' ')
    ADD_IMDB[temp[0]] = temp[1].strip()


for title, id in ADD_IMDB.items():

    print('Downloading: ' + title)

    if id == 'NONE':
        continue

    # Set up data structure
    current_results = {}

    general = imdb.get_title(id)

    print('Matched to: ' + general['base']['title'])
    title_matches[title] = general['base']['title']

    # Save its title in imdb so similar shows can be easily renamed
    # to fit the TVTropes dataset
    current_results['imdb_title'] = general['base']['title']

    # Note the try blocks are because not every data item is present for
    # every show

    try:
        current_results['number_episodes'] = general['base']['numberOfEpisodes']
    except KeyError:
        pass

    try:
        current_results['start_year'] = general['base']['seriesStartYear']
    except KeyError:
        pass

    try:  # end year doesn't exist if ongoing show
        current_results['end_year'] = general['base']['seriesEndYear']
    except KeyError:
        pass

    genres = imdb.get_title_genres(id)
    try:
        current_results['genres'] = genres['genres']
    except KeyError:
        pass

    ratings = imdb.get_title_ratings(id)
    try:
        current_results['rating'] = ratings['rating']
    except KeyError:
        pass

    try:
        current_results['rating_count'] = ratings['ratingCount']
    except KeyError:
        pass

    similar = imdb.get_title_similarities(id)
    similar_shows = []
    try:
        for item in similar['similarities']:
            if item['title'] != similar['base']['title']:
                # don't include self
                similar_shows.append(item['title'])
        current_results['similar_titles'] = similar_shows
    except KeyError:
        pass

    versions = imdb.get_title_versions(id)
    try:
        current_results['countries'] = versions['origins']
    except KeyError:
        pass

    # Save the data if the dict is non empty
    if bool(current_results):
        chunk_results[title] = current_results

filename = 'imdb_data_dict_westernani_manual.pkl'
with open(filename, 'wb') as f:
    pickle.dump(chunk_results, f)

# save title matches to check duplicates later
filename = 'title_matches_westernani_manual.pkl'
with open(filename, 'wb') as f:
    pickle.dump(title_matches, f)
