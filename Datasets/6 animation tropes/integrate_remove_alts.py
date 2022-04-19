# sort through the stuff from ugh.py

import pickle
import pandas

# Combining data

print('combining the trope descriptions')

with open('trope_description_dict.pkl', 'rb') as f:
    descriptions = pickle.load(f)

with open('trope_descriptions_2.pkl', 'rb') as f:
    descriptions.update(pickle.load(f))

with open('trope_description_dict_COMBINED.pkl', 'wb') as f:
    pickle.dump(descriptions, f)

print('combining the trope short descriptions')

with open('trope_description_laconic_dict.pkl', 'rb') as f:
    short_descriptions = pickle.load(f)

with open('trope_descriptions_laconic_2.pkl', 'rb') as f:
    short_descriptions.update(pickle.load(f))

with open('trope_description_laconic_COMBINED.pkl', 'wb') as f:
    pickle.dump(short_descriptions, f)

print('combining the related tropes')

with open('related_tropes_dict.pkl', 'rb') as f:
    related_tropes = pickle.load(f)

with open('related_tropes_2.pkl', 'rb') as f:
    related_tropes.update(pickle.load(f))

with open('related_tropes_COMBINED.pkl', 'wb') as f:
    pickle.dump(related_tropes, f)

# deal with alternative titles

print('Loading the alternative titles')

with open('alt_trope_titles_dict_cleaned.pkl', 'rb') as f:
    alt_titles = pickle.load(f)

with open('alt_trope_titles_dict_2.pkl', 'rb') as f:
    alt_titles.update(pickle.load(f))

alt_titles = {k: v for k, v in alt_titles.items() if v}

with open('alt_trope_titles_dict_cleaned_COMBINED.pkl', 'wb') as f:
    pickle.dump(alt_titles, f)

# remove alternatives from tv and vg datasets

print('Finding replacement titles')

replacements = {}

for key, value in alt_titles.items():
    for alt in value:
        replacements[alt] = key

with open('alt_trope_title_replacements.pkl', 'wb') as f:
    pickle.dump(replacements, f)

ani_df = pandas.read_pickle('tv_tropes_animation.pkl')

print('Replacing alternate titles in the dataframes')

# replace alternative titles with the original
ani_df['trope'].replace(replacements, inplace=True)

print('Removing duplicates in the dataframes')

# remove any duplicates
ani_df = ani_df.drop_duplicates()

# remove the not tropes

print('Loading non-tropes')

with open('not_tropes.pkl', 'rb') as f:
    not_tropes = pickle.load(f)

with open('non_tropes_2.pkl', 'rb') as f:
    not_tropes.extend(pickle.load(f))

with open('non_tropes_COMBINED.pkl', 'wb') as f:
    pickle.dump(not_tropes, f)

print('Removing non-tropes')

ani_df = ani_df[~ani_df['trope'].isin(not_tropes)]

# save

number_tropes_ani = ani_df['trope'].nunique()
print('Animation total number of tropes: ' + str(number_tropes_ani))

print('Saving the datasets')

ani_df.to_pickle('tv_tropes_animation_no_duplicates.pkl')
