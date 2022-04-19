import pickle

# Compile the main data

imdb_data_dict = {}

for i in range(12):
    filename = 'imdb_data_dict_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_dict = pickle.load(f)
        imdb_data_dict.update(chunk_dict)

print(len(imdb_data_dict))

# Load the ones to remove

removal_total = []

for i in range(12):
    filename = 'remove_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_list = pickle.load(f)
        removal_total = removal_total + chunk_list

print(len(removal_total))

# Remove them

for title in removal_total:
    try:
        imdb_data_dict.pop(title)
    except:
        pass

print(len(imdb_data_dict))

# Save

with open('imdb_data_dict.pkl', 'wb') as f:
    pickle.dump(imdb_data_dict, f)

# Compile dict of ones still to scrape

scrape_pairs = {}

for i in range(12):
    filename = 'replacements_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_dict = pickle.load(f)
        scrape_pairs.update(chunk_dict)

print(len(scrape_pairs))

with open('scrape_title_pairs.pkl', 'wb') as f:
    pickle.dump(scrape_pairs, f)
