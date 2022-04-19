# imdbpie test

from imdbpie import Imdb
from fuzzywuzzy import fuzz
import inflection

imdb = Imdb()
title = 'Test'
title = inflection.titleize(title).rstrip('0123456789')
print(title)
results = imdb.search_for_title(title)
print(results)

# it might not be the first one so pick the best match

best_match_score_partial = 0
best_match_score = 0
id = None
title_lower = title.lower()
title_lower = title_lower.rstrip('0123456789')  # ADDED

print(title_lower)

for result in results:
    # skip non TV entires
    if not result['type'].startswith('TV'):
        continue
    result_title = result['title'].lower()
    # result_title = filter(lambda x: x.isalpha(), result_title)
    print('Checking ' + result_title)
    # print(fuzz.partial_ratio(result_title, title_lower))
    print(fuzz.ratio(result_title, title_lower))

    '''
    if (fuzz.partial_ratio(result_title, title_lower) >
        best_match_score_partial) or (best_match_score == 100 and
                                      fuzz.ratio(result_title, title_lower)
                                      > best_match_score):
    '''
    if fuzz.ratio(result_title, title_lower) > best_match_score:
        best_match_score_partial = fuzz.partial_ratio(result_title,
                                                      title_lower)
        best_match_score = fuzz.ratio(result_title, title_lower)
        id = result['imdb_id']
        print(result_title)
        if best_match_score == 100 or title_lower in result_title:
            break

print(id)

print('\n GET TITLE')
general = imdb.get_title(id)
print(general['base']['titleType'])  # check it is tvSeries
print(general['base']['title'])
input('fish')

print(general['base']['numberOfEpisodes'])
print(general['base']['seriesStartYear'])
try:
    # may be ongoing
    print(general['base']['seriesEndYear'])
except KeyError:
    print('Ongoing')

print('\n GET GENRES')
genres = imdb.get_title_genres(id)
print(genres['genres'])

print('\n GET RATINGS')  # -> name year type, RATING AND COUNT, + DEMOGRAPHIC INFO
ratings = imdb.get_title_ratings(id)
print(ratings['rating'])  # add also normalised ver in dataset: x10 and round
print(ratings['ratingCount'])

print('\n GET SIMILARITIES')
similar = imdb.get_title_similarities(id)
for item in similar['similarities']:
    if item['title'] != similar['base']['title']: #don't include self
        print(item['title'])

print('\n GET VERSIONS')
versions = imdb.get_title_versions(id)
print(versions)
print(versions['origins'])
