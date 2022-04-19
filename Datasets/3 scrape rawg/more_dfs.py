import pandas
import pickle

with open('rawg_data_dict_combined.pkl', 'rb') as f:
    games_data = pickle.load(f)

with open('game_original_names_dict.pkl', 'rb') as f:
    original_names = pickle.load(f)

genre_data_fordf = []
other_data_fordf = []

for game, data in games_data.items():

    oname = original_names[game]

    other_data_fordf.append({'title': oname, 'metacritic': data['metacritic'],
                             'release_date': data['release_date'],
                             'number_ratings': data['number_ratings']})

    for genre in data['genres']:
        genre_data_fordf.append({'title': oname, 'genre': genre})

game_genres = pandas.DataFrame(genre_data_fordf)
print(game_genres.head())
game_genres.to_pickle('game_genres_df.pkl')

game_misc_data = pandas.DataFrame(other_data_fordf)
print(game_misc_data.head())
game_misc_data.to_pickle('game_misc_df.pkl')

print(game_misc_data.loc[game_misc_data['title'] == 'TheWitcher3WildHunt'])
