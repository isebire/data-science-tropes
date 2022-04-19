from imdbpie import Imdb
import pickle
import pandas

with open('remove_wa.txt', 'r') as f:
    remove_list = f.read().splitlines()

with open('replace_wa.txt', 'r') as f:
    replace_list = f.read().splitlines()

replace_dict = {}
for item in replace_list:
    temp = item.split(' ')
    replace_dict[temp[0]] = temp[1]



# remove the films etc from the dataframe
df = pandas.read_pickle('tv_tropes_westernani_removedknownfilms.pkl')

print(len(list(dict.fromkeys(df['title']))))
df = df[~df['title'].isin(remove_list)]
print(len(list(dict.fromkeys(df['title']))))

df.to_pickle('tv_tropes_westernani_removedknownfilms_c1.pkl')

# remove non tv and ones to replace from imdb_data_dict.pkl
with open('imdb_data_dict_westernani.pkl', 'rb') as f:
    imdb_data_dict = pickle.load(f)

data_new = {}

for key, value in imdb_data_dict.items():
    if key not in remove_list and key not in replace_dict.keys():
        data_new[key] = value

'''
with open('imdb_data_dict_manual.pkl', 'rb') as f:
    imdb_data_dict_manual = pickle.load(f)
    data_new.update(imdb_data_dict_manual)
'''

with open('imdb_data_dict_westernani_cleaned1.pkl', 'wb') as f:
    pickle.dump(data_new, f)

# remove non tv and ones to replace from title matches

with open('title_matches_westernani.pkl', 'rb') as f:
    title_matches = pickle.load(f)

data_new = {}

for key, value in title_matches.items():
    if key not in remove_list and key not in replace_dict.keys():
        data_new[key] = value

with open('title_matches_westernani_cleaned1.pkl', 'wb') as f:
    pickle.dump(data_new, f)
