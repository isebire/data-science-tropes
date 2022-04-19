# compile manual and auto, formats

import pickle
import pandas

# Compile the data dictionary

with open('imdb_data_dict_westernani_cleaned1.pkl', 'rb') as f:
    imdb_data_dict = pickle.load(f)

with open('imdb_data_dict_westernani_manual.pkl', 'rb') as f:
    imdb_data_dict_manual = pickle.load(f)
    imdb_data_dict.update(imdb_data_dict_manual)

with open('imdb_data_dict_westernani_compiled.pkl', 'wb') as f:
    pickle.dump(imdb_data_dict, f)

# Compile the title matches

with open('title_matches_westernani_cleaned1.pkl', 'rb') as f:
    title_matches = pickle.load(f)

with open('title_matches_westernani_manual.pkl', 'rb') as f:
    title_matches_manual = pickle.load(f)
    title_matches.update(title_matches_manual)

with open('title_matches_westernani_compiled.pkl.pkl', 'wb') as f:
    pickle.dump(title_matches, f)
