import pickle
import pandas

DATA_FILE = 'data_new/* PRIMARY DATASETS/TROPES_DATA/related_tropes_dict.pkl'
ALT_NAMES = 'alt_trope_title_replacements.pkl'

with open(DATA_FILE, 'rb') as f:
    related_tropes_dict = pickle.load(f)

with open(ALT_NAMES, 'rb') as f:
    replacements = pickle.load(f)

with open('trope_names_list.pkl', 'rb') as f:
    trope_names = pickle.load(f)

no_alt_titles_dict = {}
for key_trope, related_tropes in related_tropes_dict.items():
    print(key_trope)

    if key_trope in replacements.keys():
        new_key = replacements[key_trope]

    else:
        new_key = key_trope

    if new_key not in no_alt_titles_dict.keys():
        no_alt_titles_dict[new_key] = []

    for related_trope in related_tropes:
        if related_trope not in trope_names:
            continue

        if related_trope in replacements.keys():
            no_alt_titles_dict[new_key].append(replacements[related_trope])
        else:
            no_alt_titles_dict[new_key].append(related_trope)

    no_alt_titles_dict[new_key] = list(set(no_alt_titles_dict[new_key]))

print(len(no_alt_titles_dict))

with open('data_new/* PRIMARY DATASETS/TROPES_DATA/related_tropes_dict_2.pkl', 'wb') as f:
    pickle.dump(no_alt_titles_dict, f)
