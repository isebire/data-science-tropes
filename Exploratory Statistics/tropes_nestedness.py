import pickle
import pandas
from nestedness_calculator import NestednessCalculator
import numpy as np

VG_FILEPATH = '../data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/vg_tropes.pkl'
TV_FILEPATH = '../data_new/* PRIMARY DATASETS/TROPES_WORKS_MAPPING/tv_tropes.pkl'

# Read dataframes
tv_df = pandas.read_pickle(TV_FILEPATH)
vg_df = pandas.read_pickle(VG_FILEPATH)

# Get a list of all titles
all_vg = vg_df['title'].unique().tolist()
all_tv = tv_df['title'].unique().tolist()

# Get a list of the top 500 titles from main datasets for vg and tv
top_500_vg = vg_df.groupby(by='title').agg('count').sort_values(by='trope', ascending=False).head(n=500).reset_index()
top_500_vg = top_500_vg['title'].tolist()
top_500_tv = tv_df.groupby(by='title').agg('count').sort_values(by='trope', ascending=False).head(n=500).reset_index()
top_500_tv = top_500_tv['title'].tolist()

# Test
matrix_a = [[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,0],[1,0,1,1,0]]
matrix_a = np.array(matrix_a)
nestedness = NestednessCalculator(matrix_a).nodf(matrix_a)
print(nestedness)

# Tv
tv_binary = pandas.crosstab(tv_df.title, tv_df.trope)
tv_df_matrix = tv_binary.to_numpy()
# input(tv_df_matrix.shape)
nestedness = NestednessCalculator(tv_df_matrix).nodf(tv_df_matrix)
print(nestedness)

# Vg
vg_binary = pandas.crosstab(vg_df.title, vg_df.trope)
vg_df_matrix = vg_binary.to_numpy()
nestedness = NestednessCalculator(vg_df_matrix).nodf(vg_df_matrix)
print(nestedness)
