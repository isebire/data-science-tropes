import pickle
import pandas

with open('manual_checks_westernani.pkl', 'rb') as f:
    check = pickle.load(f)

print(len(check))

for item in check.items():
    input(item)


#df = pandas.read_pickle('tv_tropes_anime.pkl')

#print(list(dict.fromkeys(df['title'])))
