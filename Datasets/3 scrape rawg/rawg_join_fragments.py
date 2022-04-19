# joins the fragments from downloading rawg
import pickle

rawg_data = {}

for i in range(18):
    filename = 'rawg_data_dict_' + str(i) + '.pkl'
    with open(filename, 'rb') as f:
        chunk_dict = pickle.load(f)
        rawg_data.update(chunk_dict)

with open('rawg_data_dict.pkl', 'wb') as f:
    pickle.dump(rawg_data, f)
