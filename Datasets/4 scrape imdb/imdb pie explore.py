# imdbpie test

from imdbpie import Imdb
imdb = Imdb()
results = imdb.search_for_title("test")
id = (results[0]['imdb_id'])
print(results[0]['type'])

print('\n GET GENRES')  # -> ID, TITLE, TYPE (TVSERIES), YEAR, GENRES
print(imdb.get_title_genres(id))
input('next: ')
# dict has 'year' and 'genres' (list)

print('\n GET CREDITS')
print(imdb.get_title_credits(id))
input('next: ')
# has 'base' then within this 'numberOfEpisodes', 'seriesEndYear', 'seriesStartYear'

print('\n GET QUOTES')
print(imdb.get_title_quotes(id))
input('next: ')

print('\n GET RATINGS')  # -> name year type, RATING AND COUNT, + DEMOGRAPHIC INFO
print(imdb.get_title_ratings(id))
input('next: ')
# 'rating', 'ratingCount'

print('\n GET CONNECTIONS')
print(imdb.get_title_connections(id))
input('next: ')

print('\n GET SIMILARITIES')
print(imdb.get_title_similarities(id))
input('next: ')
# in 'similarities': 'title'

print('\n GET VIDEOS')
print(imdb.get_title_videos(id))
input('next: ')

print('\n GET NEWS')
print(imdb.get_title_news(id))
input('next: ')

print('\n GET TRIVIA')
print(imdb.get_title_trivia(id))
input('next: ')

print('\n GET SOUNDTRACKS')
print(imdb.get_title_soundtracks(id))
input('next: ')

print('\n GET GOOFS')
print(imdb.get_title_goofs(id))
input('next: ')

print('\n GET TECHNICAL')
print(imdb.get_title_technical(id))
input('next: ')

print('\n GET COMPANIES')  # -> REGIONS PROVIDED FOR THE COMPANIES (PRODUCTION IN TYPES)
print(imdb.get_title_companies(id))
input('next: ')

print('\n GET EPSIODES')
print(imdb.get_title_episodes(id))
input('next: ')

print('\n GET EPISODES DETAIL')
print(imdb.get_title_episodes_detailed(id, season=1))
input('next: ')

print('\n GET TOP CREW')
print(imdb.get_title_top_crew(id))
input('next: ')

print('\n GET PLOT')
print(imdb.get_title_plot(id))
input('next: ')

print('\n GET PLOT SYN.')
print(imdb.get_title_plot_synopsis(id))
input('next: ')

print('\n GET AWARDS')
print(imdb.get_title_awards(id))
input('next: ')

print('\n GET RELEASES')
print(imdb.get_title_releases(id))
input('next: ')

print('\n GET VERSIONS')
versions = imdb.get_title_versions(id)
print(versions)
print(versions['origins'])
input('next: ')

print('\n GET USER REVIEWS')
print(imdb.get_title_user_reviews(id))
input('next: ')

print('\n GET METACRITIC REVIEWS')
print(imdb.get_title_metacritic_reviews(id))
input('next: ')

print('\n GET AUX INFO')
imdb.get_title_auxiliary(id)
input('next: ')

print('\n GET TITLE')   # -> number of episodes, start and end year,
# also contains rating, count, and demographic info
print(imdb.get_title(id))
input('next: ')
# 'numberOfEpisodes' 'seriesStartYear' 'seriesEndYear'
