import pandas

tv_df = pandas.read_pickle('tv_tropes_animation_no_duplicates.pkl')

print(tv_df.head())

number_titles_covered = len(list(dict.fromkeys(tv_df['title'])))
print('Have data for ' + str(number_titles_covered))

tv_df['title'] = tv_df['title'].str.lower()
tv_df = tv_df.drop_duplicates()

number_titles_covered = len(list(dict.fromkeys(tv_df['title'])))
print('Have data for ' + str(number_titles_covered))

tv_df.to_pickle('tv_tropes_animation_no_duplicates2.pkl')
