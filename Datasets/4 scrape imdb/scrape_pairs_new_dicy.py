import pickle

with open('scrape_title_pairs.pkl', 'rb') as f:
    pairs = pickle.load(f)

with open('imdb_data_dict.pkl', 'rb') as f:
    imdb_data = pickle.load(f)

with open('replacements.txt', 'r') as f:
    more_replacements = f.read().splitlines()

for item in more_replacements:
    title, id = item.split(' ')
    pairs[title] = id
    try:
        imdb_data.pop(title)
    except:
        pass


print(pairs)

with open('scrape_title_pairs.pkl', 'wb') as f:
    pickle.dump(pairs, f)

with open('imdb_data_dict.pkl', 'wb') as f:
    pickle.dump(imdb_data, f)
