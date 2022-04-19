# Remove things from 2022-

import pickle
import pandas

pandas.set_option('display.max_rows', 100)

# TV

tv_misc_df = pandas.read_pickle('WORKS_TV_SUPPLEMENTARY/tv_misc_animation_and_normal.pkl')
tv_countries_df = pandas.read_pickle('WORKS_TV_SUPPLEMENTARY/tv_countries_animation_and_normal.pkl')
tv_genres_df = pandas.read_pickle('WORKS_TV_SUPPLEMENTARY/tv_genres_animation_and_normal.pkl')
tv_df = pandas.read_pickle('TROPES_WORKS_MAPPING/tv_tropes_animation_and_normal.pkl')
tv_similar_df = pandas.read_pickle('WORKS_TV_SUPPLEMENTARY/tv_similar_animation_and_normal.pkl')

# Sizes before
print('Misc data')
print(tv_misc_df['title'].nunique())
print('Countries data')
print(tv_countries_df['title'].nunique())
print('Genre data')
print(tv_genres_df['title'].nunique())
print('Tropes data')
print(tv_df['title'].nunique())
print('TV similar')
print(tv_similar_df['title'].nunique())

# Find ones to remove
future_ones_tv = tv_misc_df[tv_misc_df.start_year >= 2022]['title'].tolist()

# Remove from ALL DATAFRAMES
# checked number of unique titles decreased only by len(future_ones_tv)
tv_misc_df = tv_misc_df[~tv_misc_df.title.isin(future_ones_tv)]
tv_countries_df = tv_countries_df[~tv_countries_df.title.isin(future_ones_tv)]
tv_genres_df = tv_genres_df[~tv_genres_df.title.isin(future_ones_tv)]
tv_df = tv_df[~tv_df.title.isin(future_ones_tv)]
# Remove any rows containing a future one
tv_similar_df = tv_similar_df[~tv_similar_df.title.isin(future_ones_tv)]
tv_similar_df = tv_similar_df[~tv_similar_df.similar_title.isin(future_ones_tv)]

# Sizes after
print('Misc data')
print(tv_misc_df['title'].nunique())
print('Countries data')
print(tv_countries_df['title'].nunique())
print('Genre data')
print(tv_genres_df['title'].nunique())
print('Tropes data')
print(tv_df['title'].nunique())
print('TV similar')
print(tv_similar_df['title'].nunique())

# Save ALL DATAFRAMES
tv_misc_df.to_pickle('WORKS_TV_SUPPLEMENTARY/tv_misc_animation_and_normal_C.pkl')
tv_countries_df.to_pickle('WORKS_TV_SUPPLEMENTARY/tv_countries_animation_and_normal_C.pkl')
tv_genres_df.to_pickle('WORKS_TV_SUPPLEMENTARY/tv_genres_animation_and_normal_C.pkl')
tv_df.to_pickle('TROPES_WORKS_MAPPING/tv_tropes_animation_and_normal_C.pkl')
tv_similar_df.to_pickle('WORKS_TV_SUPPLEMENTARY/tv_similar_animation_and_normal_C.pkl')

# VG

vg_misc_df = pandas.read_pickle('WORKS_VG_SUPPLEMENTARY/game_misc_df.pkl')
vg_countries_df = pandas.read_pickle('WORKS_VG_SUPPLEMENTARY/game_countries_df.pkl')
vg_genres_df = pandas.read_pickle('WORKS_VG_SUPPLEMENTARY/game_genres_df.pkl')
vg_df = pandas.read_pickle('TROPES_WORKS_MAPPING/vg_tropes_no_duplicates.pkl')

# Sizes before
print('Misc data')
print(vg_misc_df['title'].nunique())
print('Countries data')
print(vg_countries_df['title'].nunique())
print('Genre data')
print(vg_genres_df['title'].nunique())
print('Tropes data')
print(vg_df['title'].nunique())

# Find ones to remove
vg_misc_df_y = vg_misc_df
vg_misc_df_y['release_date'] = pandas.DatetimeIndex(vg_misc_df['release_date']).year
vg_misc_df_y = vg_misc_df_y.rename(columns={'release_date': 'start_year'})
future_ones_vg = vg_misc_df[vg_misc_df_y.start_year >= 2022]['title'].tolist()
vg_misc_df = pandas.read_pickle('WORKS_VG_SUPPLEMENTARY/game_misc_df.pkl')

# Remove from ALL DATAFRAMES
vg_misc_df = vg_misc_df[~vg_misc_df.title.isin(future_ones_vg)]
vg_countries_df = vg_countries_df[~vg_countries_df.title.isin(future_ones_vg)]
vg_genres_df = vg_genres_df[~vg_genres_df.title.isin(future_ones_vg)]
vg_df = vg_df[~vg_df.title.isin(future_ones_vg)]

# Sizes after
print('Misc data')
print(vg_misc_df['title'].nunique())
print('Countries data')
print(vg_countries_df['title'].nunique())
print('Genre data')
print(vg_genres_df['title'].nunique())
print('Tropes data')
print(vg_df['title'].nunique())

# Save ALL DATAFRAMES
vg_misc_df.to_pickle('WORKS_VG_SUPPLEMENTARY/game_misc_df_C.pkl')
vg_countries_df.to_pickle('WORKS_VG_SUPPLEMENTARY/game_countries_df_C.pkl')
vg_genres_df.to_pickle('WORKS_VG_SUPPLEMENTARY/game_genres_df_C.pkl')
vg_df.to_pickle('TROPES_WORKS_MAPPING/vg_tropes_no_duplicates_C.pkl')
