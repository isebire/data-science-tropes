# vg test
import pandas
import pickle
import inflection

vg_df = pandas.read_pickle('vg_tropes_no_duplicates.pkl')
print(vg_df.head())
# this line puts the titles into the right format for rawg
originals = list(dict.fromkeys(vg_df['title']))
games = [inflection.dasherize(inflection.underscore(title)).lower() for title in originals]
names_dict = {}
for i in range(len(originals)):
    names_dict[games[i]] = originals[i]

with open('game_original_names_dict.pkl', 'wb') as f:
    pickle.dump(names_dict, f)


# gets all the games names in a list
print(len(games))
with open('games_names.pkl', 'wb') as f:
    pickle.dump(games, f)
