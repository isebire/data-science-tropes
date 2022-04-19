# TV Titles List and Chunks

import pandas
import pickle

# Get all the titles
tv_df = vg_df = pandas.read_pickle('tv_tropes_no_duplicates.pkl')
series_titles = list(dict.fromkeys(tv_df['title']))

with open('tv_series_titles.pkl', 'wb') as f:
    pickle.dump(series_titles, f)

# Make the chunks
data_chunks = [series_titles[i:i+500] for i in range(0, len(series_titles), 500)]
print(len(data_chunks))

for i in range(len(data_chunks)):
    filename = 'tv_series_name_chunk_' + str(i) + '.pkl'
    with open(filename, 'wb') as f:
        pickle.dump(data_chunks[i], f)


# Later: to join the fragments
'''
rawg_data = {}

for i in range(18):
    filename = 'rawg_data_dict_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_dict = pickle.load(f)
        rawg_data.update(chunk_dict)

with open('rawg_data_dict.pkl', 'wb') as f:
    pickle.dump(rawg_data, f)
'''
