# sort through the stuff from ugh.py

import pickle
import pandas

# append all the info for the descriptions

print('Saving the trope descriptions')

descriptions = {}

for i in range(74):
    filename = 'trope_descriptions_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_dict = pickle.load(f)
        descriptions.update(chunk_dict)

with open('trope_description_dict.pkl', 'wb') as f:
    pickle.dump(descriptions, f)

short_descriptions = {}

print('Saving the trope short descriptions')

for i in range(74):
    filename = 'trope_descriptions_laconic_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_dict = pickle.load(f)
        short_descriptions.update(chunk_dict)

with open('trope_description_laconic_dict.pkl', 'wb') as f:
    pickle.dump(short_descriptions, f)


related_tropes = {}

print('Saving the related tropes')

for i in range(74):
    filename = 'related_tropes_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_dict = pickle.load(f)
        related_tropes.update(chunk_dict)

with open('related_tropes_dict.pkl', 'wb') as f:
    pickle.dump(related_tropes, f)

# deal with alternative titles

print('Loading the alternative titles')

alt_titles = {}

for i in range(74):
    filename = 'alt_trope_titles_dict_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_dict = pickle.load(f)
        alt_titles.update(chunk_dict)

print(alt_titles['conlang'])

alt_titles = {k: v for k, v in alt_titles.items() if v}

with open('alt_trope_titles_dict_cleaned.pkl', 'wb') as f:
    pickle.dump(alt_titles, f)

# remove alternatives from tv and vg datasets

print('Finding replacement titles')

replacements = {}

for key, value in alt_titles.items():
    for alt in value:
        replacements[alt] = key

with open('alt_trope_title_replacements.pkl', 'wb') as f:
    pickle.dump(replacements, f)

vg_df = pandas.read_pickle('vg_tropes.pkl')
tv_df = pandas.read_pickle('tv_tropes.pkl')

print('Replacing alternate titles in the dataframes')

# replace alternative titles with the original
vg_df['trope'].replace(replacements, inplace=True)
tv_df['trope'].replace(replacements, inplace=True)

print('Removing duplicates in the dataframes')

# remove any duplicates
vg_df = vg_df.drop_duplicates()
tv_df = tv_df.drop_duplicates()

# remove the not tropes

print('Loading non-tropes')

not_tropes = []

for i in range(74):
    filename = 'non_tropes_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_dict = pickle.load(f)
        not_tropes.extend(chunk_dict)

with open('not_tropes.pkl', 'wb') as f:
    pickle.dump(not_tropes, f)

print('Removing non-tropes')

vg_df = vg_df[~vg_df['trope'].isin(not_tropes)]
tv_df = tv_df[~tv_df['trope'].isin(not_tropes)]

# save

number_tropes_games = vg_df['trope'].nunique()
print('Games total number of tropes: ' + str(number_tropes_games))

print('Saving the datasets')

vg_df.to_pickle('vg_tropes_no_duplicates.pkl')
tv_df.to_pickle('tv_tropes_no_duplicates.pkl')
