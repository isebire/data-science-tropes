# IMDB for animation

import pandas
import pickle
from imdbpie import Imdb
from fuzzywuzzy import fuzz
import inflection

# Get all the titles
df = pandas.read_pickle('tv_tropes_anime_wmanga_removedknownfilms.pkl')
titles = list(dict.fromkeys(df['title']))

imdb = Imdb()

# Set up the data structures to save
chunk_results = {}
check_manually = {}
title_matches = {}

for title in titles:

    print('Downloading: ' + inflection.titleize(title))

    # Get the id of the title to retrieve further data
    # it might not be the first search result so find the best match
    search_title = inflection.titleize(title).rstrip('0123456789')
    search_results = imdb.search_for_title(search_title)

    best_match_score = 0
    id = None
    title_lower = search_title.lower()
    best_title = None

    for result in search_results:
        # skip non TV entires
        if result['type'] is None:
            continue

        #elif result['type'] == 'feature':
        #    if fuzz.ratio(result['title'].lower(), title_lower) > 80:
        #        check_manually[title] = 'think it is a movie'
        #        print('This is probably a movie')
        #        best_title = 'MOVIE'
        #        break

        elif not result['type'].startswith('TV'):
            continue

        result_title = result['title'].lower()
        if fuzz.ratio(result_title, title_lower) > best_match_score:
            best_match_score = fuzz.ratio(result_title, title_lower)
            id = result['imdb_id']
            best_title = result_title
            if best_match_score == 100 or result_title.startswith(title_lower):
                break

    if best_match_score == 0:
        check_manually[title] = 'None'
        continue

    print(best_match_score)

    if best_title is not None:
        title_matches[title] = best_title

    if best_match_score < 80:  # from inspection, unsure ones
        check_manually[title] = best_title

    if title.rstrip('0123456789') != title:
        check_manually[title] = best_title

    # Set up data structure
    current_results = {}

    general = imdb.get_title(id)
    # if general['base']['titleType'] == 'tvSeries':  # remove as also tvMiniSeries, tvMovie - begins tv?

    print('Matched to: ' + general['base']['title'])

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
        if 'Animation' not in genres['genres']:
            check_manually[title] = best_title
            print('maybe not animated')
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


# Saving the files each iteration
print(chunk_results)
filename = 'imdb_data_dict_animem.pkl'
with open(filename, 'wb') as f:
    pickle.dump(chunk_results, f)

# save ones to check manually
filename = 'manual_checks_animem.pkl'
with open(filename, 'wb') as f:
    pickle.dump(check_manually, f)

# save title matches to check duplicates later
filename = 'title_matches_animem.pkl'
with open(filename, 'wb') as f:
    pickle.dump(title_matches, f)

# save suspected films
#filename = 'suspected_films_easterneur.pkl'
#with open(filename, 'wb') as f:
#    pickle.dump(films, f)
