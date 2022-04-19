# Some more cleaning

import pandas
import pickle

# Making videogame titles lowercase

def lowercase_title_df(df):
    number_titles_covered = len(list(dict.fromkeys(df['title'])))
    print('Have data for ' + str(number_titles_covered))
    df['title'] = df['title'].str.lower()
    df = df.drop_duplicates()
    number_titles_covered = len(list(dict.fromkeys(df['title'])))
    print('Have data for ' + str(number_titles_covered))
    return df

vg_df = pandas.read_pickle('TROPES_WORKS_MAPPING/vg_tropes_no_duplicates.pkl')
vg_df = lowercase_title_df(vg_df)
vg_df.to_pickle('TROPES_WORKS_MAPPING/vg_tropes_no_duplicates_2.pkl')

vg_genres_df = pandas.read_pickle('WORKS_VG_SUPPLEMENTARY/game_genres_df.pkl')
vg_genres_df = lowercase_title_df(vg_genres_df)
vg_genres_df.to_pickle('WORKS_VG_SUPPLEMENTARY/game_genres_df_2.pkl')

vg_misc_df = pandas.read_pickle('WORKS_VG_SUPPLEMENTARY/game_misc_df.pkl')
vg_misc_df = lowercase_title_df(vg_misc_df)
vg_misc_df.to_pickle('WORKS_VG_SUPPLEMENTARY/game_misc_df_2.pkl')

vg_countries_df = pandas.read_pickle('WORKS_VG_SUPPLEMENTARY/game_countries_df.pkl')
vg_countries_df = lowercase_title_df(vg_countries_df)
vg_countries_df.to_pickle('WORKS_VG_SUPPLEMENTARY/game_countries_df_2.pkl')
