# combines tv and animated tv

import pickle
import pandas

# Note: all the titles are disjoint!! so no issues there :)

# Combine main dataframes

df_ani = pandas.read_pickle('tv_tropes_animation_no_duplicates2.pkl')
df_tv = pandas.read_pickle('tv_tropes_no_duplicates.pkl')

df_all_tv = pandas.concat([df_ani, df_tv])
df_all_tv = df_all_tv.drop_duplicates()
print(df_all_tv.head())
print(len(list(dict.fromkeys(df_all_tv['title']))))
df_all_tv.to_pickle('tv_tropes_animation_and_normal.pkl')

# Combine countries

df_ani = pandas.read_pickle('animation_countries_df.pkl')
df_tv = pandas.read_pickle('tv_countries_df.pkl')

df_all_tv = pandas.concat([df_ani, df_tv])
df_all_tv = df_all_tv.drop_duplicates()
print(df_all_tv.head())
print(len(list(dict.fromkeys(df_all_tv['title']))))
df_all_tv.to_pickle('tv_countries_animation_and_normal.pkl')

# Combine genres

df_ani = pandas.read_pickle('animation_genres_df.pkl')
df_tv = pandas.read_pickle('tv_genres_df.pkl')

df_all_tv = pandas.concat([df_ani, df_tv])
df_all_tv = df_all_tv.drop_duplicates()
print(df_all_tv.head())
print(len(list(dict.fromkeys(df_all_tv['title']))))
df_all_tv.to_pickle('tv_genres_animation_and_normal.pkl')

# Combine misc imdb

df_ani = pandas.read_pickle('animation_misc_df.pkl')
df_tv = pandas.read_pickle('tv_misc_df.pkl')

df_all_tv = pandas.concat([df_ani, df_tv])
df_all_tv = df_all_tv.drop_duplicates()
print(df_all_tv.head())
print(len(list(dict.fromkeys(df_all_tv['title']))))
df_all_tv.to_pickle('tv_misc_animation_and_normal.pkl')

# Combine similar works

df_ani = pandas.read_pickle('animation_similar_df.pkl')
df_tv = pandas.read_pickle('tv_similar_df.pkl')

df_all_tv = pandas.concat([df_ani, df_tv])
df_all_tv = df_all_tv.drop_duplicates()
print(df_all_tv.head())
print(len(list(dict.fromkeys(df_all_tv['title']))))
df_all_tv.to_pickle('tv_similar_animation_and_normal.pkl')
