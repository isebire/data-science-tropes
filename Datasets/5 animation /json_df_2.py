import pandas
import json
import pickle
import matplotlib.pyplot as plt


with open('tvtropes.json') as json_file:
    data = json.load(json_file)  # this gives a dict
df = pandas.DataFrame.from_dict(data, orient="index").sort_index().stack().reset_index(level=1, drop=True).reset_index()
df.columns = ['title', 'trope']
df['trope'] = df['trope'].str.lower()
# df['title'] = df['title'].str.lower()
df = df.drop_duplicates()
print(df.head())

print(list(dict.fromkeys(df['title'])))
print(len(list(dict.fromkeys(df['title']))))

df.to_pickle('tv_tropes_anime_wmanga.pkl')
